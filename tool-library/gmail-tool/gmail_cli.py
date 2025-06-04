#!/Users/pete/Projects/tool-library/gmail-tool/venv/bin/python
"""
Gmail CLI Tool - Fixed version using requests instead of httplib2
"""

import os
import sys
import json
import pickle
import base64
import argparse
import socket
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Force IPv4 to avoid network issues
original_getaddrinfo = socket.getaddrinfo
def forced_ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = forced_ipv4_getaddrinfo

# Set httplib2 timeout for OAuth flow
os.environ['HTTPLIB2_TIMEOUT'] = '30'

from google.auth.transport.requests import Request, AuthorizedSession
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels',
    'https://www.googleapis.com/auth/gmail.settings.basic',
    'https://www.googleapis.com/auth/gmail.settings.sharing'
]

# Configuration
CONFIG_DIR = Path.home() / '.gmail-cli'
TOKEN_FILE = CONFIG_DIR / 'token.pickle'
CREDENTIALS_FILE = CONFIG_DIR / 'credentials.json'

# Base URL for Gmail API
BASE_URL = 'https://www.googleapis.com/gmail/v1'


class GmailCLI:
    def __init__(self):
        self.session = None
        self.user_email = None
        self._service = None
    
    @property
    def service(self):
        """Compatibility property for gmail_advanced"""
        return self._service
        
    def authenticate(self):
        """Authenticate and create authorized session"""
        creds = None
        
        # Token file stores the user's access and refresh tokens
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired token...")
                creds.refresh(Request())
            else:
                if not CREDENTIALS_FILE.exists():
                    print(f"Error: credentials.json not found at {CREDENTIALS_FILE}")
                    print("\nTo set up Gmail CLI:")
                    print("1. Go to https://console.cloud.google.com/")
                    print("2. Create a new project or select existing")
                    print("3. Enable Gmail API")
                    print("4. Create OAuth 2.0 credentials (Desktop application)")
                    print(f"5. Download credentials.json to {CREDENTIALS_FILE}")
                    sys.exit(1)
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES)
                
                # Run with fixed port and timeout
                print("Starting OAuth flow...")
                creds = flow.run_local_server(
                    port=8080,
                    authorization_prompt_message='Please visit this URL to authorize: {url}',
                    success_message='Authorization complete! You can close this window.',
                    open_browser=True
                )
            
            # Save the credentials for the next run
            CONFIG_DIR.mkdir(exist_ok=True)
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
            print("Authentication successful!")
        
        # Create authorized session
        self.session = AuthorizedSession(creds)
        self.session.headers.update({'Accept': 'application/json'})
        
        # Create compatibility service wrapper for gmail_advanced
        from gmail_service_compat import ServiceWrapper
        self._service = ServiceWrapper(self.session, BASE_URL)
        
        # Get user's email address
        try:
            response = self.session.get(f'{BASE_URL}/users/me/profile', timeout=30)
            if response.status_code == 200:
                profile = response.json()
                self.user_email = profile['emailAddress']
            else:
                print(f"Error getting profile: {response.status_code} - {response.text}")
                sys.exit(1)
        except Exception as error:
            print(f"An error occurred: {error}")
            sys.exit(1)
    
    def list_messages(self, query: str = '', max_results: int = 10, 
                     include_spam_trash: bool = False) -> List[Dict]:
        """List messages matching query"""
        try:
            params = {
                'maxResults': max_results,
                'includeSpamTrash': include_spam_trash
            }
            
            if query:
                params['q'] = query
            
            response = self.session.get(
                f'{BASE_URL}/users/me/messages',
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Error listing messages: {response.status_code} - {response.text}")
                return []
            
            results = response.json()
            messages = results.get('messages', [])
            
            # Get message details
            detailed_messages = []
            for msg in messages:
                try:
                    detail_response = self.session.get(
                        f'{BASE_URL}/users/me/messages/{msg["id"]}',
                        params={
                            'format': 'metadata',
                            'metadataHeaders': ['From', 'To', 'Subject', 'Date']
                        },
                        timeout=30
                    )
                    if detail_response.status_code == 200:
                        detailed_messages.append(detail_response.json())
                except Exception as error:
                    print(f"Error getting message {msg['id']}: {error}")
            
            return detailed_messages
            
        except Exception as error:
            print(f"An error occurred: {error}")
            return []
    
    def get_message(self, msg_id: str, format: str = 'full') -> Optional[Dict]:
        """Get a specific message"""
        try:
            response = self.session.get(
                f'{BASE_URL}/users/me/messages/{msg_id}',
                params={'format': format},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting message: {response.status_code} - {response.text}")
                return None
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def send_message(self, to: str, subject: str, body: str, 
                    attachments: Optional[List[str]] = None) -> Optional[Dict]:
        """Send an email message"""
        try:
            message = MIMEMultipart() if attachments else MIMEText(body, 'plain')
            message['to'] = to
            message['from'] = self.user_email
            message['subject'] = subject
            
            if attachments:
                message.attach(MIMEText(body, 'plain'))
                
                for file_path in attachments:
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename={os.path.basename(file_path)}'
                            )
                            message.attach(part)
            
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()).decode('utf-8')
            
            response = self.session.post(
                f'{BASE_URL}/users/me/messages/send',
                json={'raw': raw_message},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error sending message: {response.status_code} - {response.text}")
                return None
            
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def list_labels(self) -> List[Dict]:
        """List all labels"""
        try:
            response = self.session.get(
                f'{BASE_URL}/users/me/labels',
                timeout=30
            )
            if response.status_code == 200:
                results = response.json()
                return results.get('labels', [])
            else:
                print(f"Error listing labels: {response.status_code} - {response.text}")
                return []
        except Exception as error:
            print(f"An error occurred: {error}")
            return []
    
    def create_label(self, name: str, label_list_visibility: str = 'labelShow',
                    message_list_visibility: str = 'show') -> Optional[Dict]:
        """Create a new label"""
        try:
            label_object = {
                'name': name,
                'labelListVisibility': label_list_visibility,
                'messageListVisibility': message_list_visibility
            }
            
            response = self.session.post(
                f'{BASE_URL}/users/me/labels',
                json=label_object,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error creating label: {response.status_code} - {response.text}")
                return None
            
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def modify_message(self, msg_id: str, add_labels: Optional[List[str]] = None,
                      remove_labels: Optional[List[str]] = None) -> Optional[Dict]:
        """Modify message labels"""
        try:
            body = {}
            if add_labels:
                body['addLabelIds'] = add_labels
            if remove_labels:
                body['removeLabelIds'] = remove_labels
            
            response = self.session.post(
                f'{BASE_URL}/users/me/messages/{msg_id}/modify',
                json=body,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error modifying message: {response.status_code} - {response.text}")
                return None
            
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def trash_message(self, msg_id: str) -> bool:
        """Move message to trash"""
        try:
            response = self.session.post(
                f'{BASE_URL}/users/me/messages/{msg_id}/trash',
                timeout=30
            )
            return response.status_code == 200
        except Exception as error:
            print(f"An error occurred: {error}")
            return False
    
    def delete_message(self, msg_id: str) -> bool:
        """Permanently delete a message"""
        try:
            response = self.session.delete(
                f'{BASE_URL}/users/me/messages/{msg_id}',
                timeout=30
            )
            return response.status_code == 204
        except Exception as error:
            print(f"An error occurred: {error}")
            return False
    
    def batch_delete(self, msg_ids: List[str]) -> bool:
        """Batch delete messages"""
        try:
            response = self.session.post(
                f'{BASE_URL}/users/me/messages/batchDelete',
                json={'ids': msg_ids},
                timeout=30
            )
            return response.status_code == 204
        except Exception as error:
            print(f"An error occurred: {error}")
            return False
    
    def create_filter(self, criteria: Dict, action: Dict) -> Optional[Dict]:
        """Create a filter"""
        try:
            filter_object = {
                'criteria': criteria,
                'action': action
            }
            
            response = self.session.post(
                f'{BASE_URL}/users/me/settings/filters',
                json=filter_object,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error creating filter: {response.status_code} - {response.text}")
                return None
            
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def list_filters(self) -> List[Dict]:
        """List all filters"""
        try:
            response = self.session.get(
                f'{BASE_URL}/users/me/settings/filters',
                timeout=30
            )
            if response.status_code == 200:
                results = response.json()
                return results.get('filter', [])
            else:
                print(f"Error listing filters: {response.status_code} - {response.text}")
                return []
        except Exception as error:
            print(f"An error occurred: {error}")
            return []
    
    def watch_mailbox(self, topic_name: str, label_ids: Optional[List[str]] = None) -> Optional[Dict]:
        """Set up push notifications for mailbox changes"""
        try:
            request = {
                'topicName': topic_name,
                'labelIds': label_ids or ['INBOX']
            }
            
            response = self.session.post(
                f'{BASE_URL}/users/me/watch',
                json=request,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error setting up watch: {response.status_code} - {response.text}")
                return None
            
        except Exception as error:
            print(f"An error occurred: {error}")
            return None


def format_message_display(message: Dict) -> str:
    """Format message for display"""
    headers = {h['name']: h['value'] for h in message['payload']['headers']}
    
    output = []
    output.append(f"ID: {message['id']}")
    output.append(f"From: {headers.get('From', 'Unknown')}")
    output.append(f"To: {headers.get('To', 'Unknown')}")
    output.append(f"Subject: {headers.get('Subject', 'No Subject')}")
    output.append(f"Date: {headers.get('Date', 'Unknown')}")
    
    if 'labelIds' in message:
        output.append(f"Labels: {', '.join(message['labelIds'])}")
    
    output.append("-" * 50)
    
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(description='Gmail CLI - Command line interface for Gmail')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List messages
    list_parser = subparsers.add_parser('list', help='List messages')
    list_parser.add_argument('-q', '--query', default='', help='Search query')
    list_parser.add_argument('-n', '--number', type=int, default=10, help='Number of messages')
    list_parser.add_argument('--include-spam-trash', action='store_true', help='Include spam and trash')
    
    # Read message
    read_parser = subparsers.add_parser('read', help='Read a message')
    read_parser.add_argument('message_id', help='Message ID')
    read_parser.add_argument('--format', choices=['minimal', 'full', 'raw', 'metadata'], 
                           default='full', help='Message format')
    
    # Send message
    send_parser = subparsers.add_parser('send', help='Send a message')
    send_parser.add_argument('to', help='Recipient email')
    send_parser.add_argument('subject', help='Email subject')
    send_parser.add_argument('body', help='Email body')
    send_parser.add_argument('-a', '--attach', action='append', help='Attachment file path')
    
    # Labels
    labels_parser = subparsers.add_parser('labels', help='Manage labels')
    labels_subparsers = labels_parser.add_subparsers(dest='labels_command')
    
    labels_list_parser = labels_subparsers.add_parser('list', help='List labels')
    
    labels_create_parser = labels_subparsers.add_parser('create', help='Create label')
    labels_create_parser.add_argument('name', help='Label name')
    
    labels_apply_parser = labels_subparsers.add_parser('apply', help='Apply label to message')
    labels_apply_parser.add_argument('message_id', help='Message ID')
    labels_apply_parser.add_argument('label', help='Label to apply')
    
    # Trash/Delete
    trash_parser = subparsers.add_parser('trash', help='Move message to trash')
    trash_parser.add_argument('message_id', help='Message ID')
    
    delete_parser = subparsers.add_parser('delete', help='Permanently delete message')
    delete_parser.add_argument('message_id', help='Message ID')
    
    # Batch delete
    batch_delete_parser = subparsers.add_parser('batch-delete', help='Delete multiple messages')
    batch_delete_parser.add_argument('message_ids', nargs='+', help='Message IDs to delete')
    
    # Filters
    filters_parser = subparsers.add_parser('filters', help='Manage filters')
    filters_subparsers = filters_parser.add_subparsers(dest='filters_command')
    
    filters_list_parser = filters_subparsers.add_parser('list', help='List filters')
    
    # Watch
    watch_parser = subparsers.add_parser('watch', help='Set up push notifications')
    watch_parser.add_argument('topic', help='Pub/Sub topic name')
    watch_parser.add_argument('-l', '--labels', nargs='+', help='Label IDs to watch')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize Gmail CLI
    gmail = GmailCLI()
    gmail.authenticate()
    
    # Execute commands
    if args.command == 'list':
        messages = gmail.list_messages(
            query=args.query,
            max_results=args.number,
            include_spam_trash=args.include_spam_trash
        )
        
        if messages:
            for msg in messages:
                print(format_message_display(msg))
        else:
            print("No messages found.")
    
    elif args.command == 'read':
        message = gmail.get_message(args.message_id, format=args.format)
        if message:
            if args.format == 'metadata':
                print(format_message_display(message))
            else:
                print(json.dumps(message, indent=2))
        else:
            print("Message not found.")
    
    elif args.command == 'send':
        result = gmail.send_message(
            to=args.to,
            subject=args.subject,
            body=args.body,
            attachments=args.attach
        )
        if result:
            print(f"Message sent successfully. ID: {result['id']}")
        else:
            print("Failed to send message.")
    
    elif args.command == 'labels':
        if args.labels_command == 'list':
            labels = gmail.list_labels()
            for label in labels:
                print(f"{label['name']} (ID: {label['id']})")
        
        elif args.labels_command == 'create':
            label = gmail.create_label(args.name)
            if label:
                print(f"Label created: {label['name']} (ID: {label['id']})")
            else:
                print("Failed to create label.")
        
        elif args.labels_command == 'apply':
            # Get label ID from name
            labels = gmail.list_labels()
            label_id = None
            for label in labels:
                if label['name'] == args.label:
                    label_id = label['id']
                    break
            
            if label_id:
                result = gmail.modify_message(args.message_id, add_labels=[label_id])
                if result:
                    print(f"Label '{args.label}' applied to message.")
                else:
                    print("Failed to apply label.")
            else:
                print(f"Label '{args.label}' not found.")
    
    elif args.command == 'trash':
        if gmail.trash_message(args.message_id):
            print("Message moved to trash.")
        else:
            print("Failed to trash message.")
    
    elif args.command == 'delete':
        response = input("Are you sure you want to permanently delete this message? (y/N): ")
        if response.lower() == 'y':
            if gmail.delete_message(args.message_id):
                print("Message permanently deleted.")
            else:
                print("Failed to delete message.")
        else:
            print("Deletion cancelled.")
    
    elif args.command == 'batch-delete':
        response = input(f"Are you sure you want to permanently delete {len(args.message_ids)} messages? (y/N): ")
        if response.lower() == 'y':
            if gmail.batch_delete(args.message_ids):
                print(f"Successfully deleted {len(args.message_ids)} messages.")
            else:
                print("Failed to delete messages.")
        else:
            print("Deletion cancelled.")
    
    elif args.command == 'filters':
        if args.filters_command == 'list':
            filters = gmail.list_filters()
            for f in filters:
                print(f"Filter ID: {f['id']}")
                if 'criteria' in f:
                    print(f"  Criteria: {json.dumps(f['criteria'], indent=4)}")
                if 'action' in f:
                    print(f"  Action: {json.dumps(f['action'], indent=4)}")
                print("-" * 50)
    
    elif args.command == 'watch':
        result = gmail.watch_mailbox(args.topic, args.labels)
        if result:
            print(f"Watch set up successfully.")
            print(f"History ID: {result['historyId']}")
            print(f"Expiration: {result['expiration']}")
        else:
            print("Failed to set up watch.")


if __name__ == '__main__':
    main()