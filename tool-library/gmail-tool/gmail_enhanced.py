#!/Users/pete/Projects/tool-library/gmail-tool/venv/bin/python
"""
Gmail Enhanced CLI - Additional features for Gmail
"""

import os
import sys
import json
import base64
import mimetypes
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta

from gmail_cli import GmailCLI, BASE_URL
from gmail_service_compat import HttpError


class GmailEnhanced(GmailCLI):
    """Extended Gmail functionality with thread, draft, and attachment support"""
    
    def __init__(self):
        super().__init__()
    
    # Thread Management
    def get_thread(self, thread_id: str, format: str = 'full') -> Optional[Dict]:
        """Get a full conversation thread"""
        try:
            response = self.session.get(
                f'{BASE_URL}/users/me/threads/{thread_id}',
                params={'format': format},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting thread: {response.status_code} - {response.text}")
                return None
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def reply_to_thread(self, thread_id: str, to: str, body: str, 
                       message_id: str = None, references: str = None) -> Optional[Dict]:
        """Reply to a specific thread"""
        try:
            # Get the original message to extract headers
            if not message_id and thread_id:
                thread = self.get_thread(thread_id)
                if thread and thread.get('messages'):
                    # Get the last message in thread
                    last_msg = thread['messages'][-1]
                    message_id = last_msg.get('id')
                    
                    # Extract In-Reply-To and References headers
                    headers = {h['name']: h['value'] 
                              for h in last_msg['payload'].get('headers', [])}
                    in_reply_to = headers.get('Message-ID', f'<{message_id}@mail.gmail.com>')
                    references = headers.get('References', '') + ' ' + in_reply_to
            
            # Create reply
            from email.mime.text import MIMEText
            message = MIMEText(body, 'plain')
            message['to'] = to
            message['from'] = self.user_email
            message['subject'] = f"Re: {thread_id}"  # This should be extracted from thread
            
            # Add threading headers
            if message_id:
                message['In-Reply-To'] = in_reply_to if 'in_reply_to' in locals() else f'<{message_id}@mail.gmail.com>'
            if references:
                message['References'] = references
            
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()).decode('utf-8')
            
            response = self.session.post(
                f'{BASE_URL}/users/me/messages/send',
                json={'raw': raw_message, 'threadId': thread_id},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error sending reply: {response.status_code} - {response.text}")
                return None
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def forward_message(self, msg_id: str, to: str, comment: str = "") -> Optional[Dict]:
        """Forward a message"""
        try:
            # Get original message
            original = self.get_message(msg_id, format='full')
            if not original:
                return None
            
            # Extract original content
            headers = {h['name']: h['value'] 
                      for h in original['payload'].get('headers', [])}
            
            # Build forward body
            forward_body = comment + "\n\n---------- Forwarded message ---------\n"
            forward_body += f"From: {headers.get('From', 'Unknown')}\n"
            forward_body += f"Date: {headers.get('Date', 'Unknown')}\n"
            forward_body += f"Subject: {headers.get('Subject', 'No Subject')}\n"
            forward_body += f"To: {headers.get('To', 'Unknown')}\n\n"
            
            # Get message body
            body_text = self._extract_body(original['payload'])
            forward_body += body_text
            
            # Create forward message
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            message = MIMEMultipart() if self._has_attachments(original) else MIMEText(forward_body, 'plain')
            message['to'] = to
            message['from'] = self.user_email
            message['subject'] = f"Fwd: {headers.get('Subject', 'No Subject')}"
            
            if isinstance(message, MIMEMultipart):
                message.attach(MIMEText(forward_body, 'plain'))
                # TODO: Forward attachments
            
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
                print(f"Error forwarding message: {response.status_code} - {response.text}")
                return None
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    # Draft Management
    def create_draft(self, to: str, subject: str, body: str, 
                    thread_id: Optional[str] = None) -> Optional[Dict]:
        """Create a draft"""
        try:
            from email.mime.text import MIMEText
            message = MIMEText(body, 'plain')
            message['to'] = to
            message['from'] = self.user_email
            message['subject'] = subject
            
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()).decode('utf-8')
            
            draft = {'message': {'raw': raw_message}}
            if thread_id:
                draft['message']['threadId'] = thread_id
            
            response = self.session.post(
                f'{BASE_URL}/users/me/drafts',
                json=draft,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error creating draft: {response.status_code} - {response.text}")
                return None
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def list_drafts(self, max_results: int = 10) -> List[Dict]:
        """List drafts"""
        try:
            response = self.session.get(
                f'{BASE_URL}/users/me/drafts',
                params={'maxResults': max_results},
                timeout=30
            )
            
            if response.status_code == 200:
                results = response.json()
                drafts = results.get('drafts', [])
                
                # Get full draft details
                detailed_drafts = []
                for draft in drafts:
                    detail_response = self.session.get(
                        f'{BASE_URL}/users/me/drafts/{draft["id"]}',
                        timeout=30
                    )
                    if detail_response.status_code == 200:
                        detailed_drafts.append(detail_response.json())
                
                return detailed_drafts
            else:
                print(f"Error listing drafts: {response.status_code} - {response.text}")
                return []
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return []
    
    def update_draft(self, draft_id: str, to: str = None, subject: str = None, 
                    body: str = None) -> Optional[Dict]:
        """Update a draft"""
        try:
            # Get current draft
            response = self.session.get(
                f'{BASE_URL}/users/me/drafts/{draft_id}',
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Error getting draft: {response.status_code}")
                return None
            
            draft = response.json()
            current_msg = draft['message']
            
            # Decode current message
            if 'raw' in current_msg:
                import email
                decoded = base64.urlsafe_b64decode(current_msg['raw'])
                msg = email.message_from_bytes(decoded)
                
                # Update fields
                if to:
                    msg['To'] = to
                if subject:
                    msg['Subject'] = subject
                if body:
                    # This is simplified - proper implementation would handle multipart
                    msg.set_payload(body)
            else:
                # Create new message if no raw content
                from email.mime.text import MIMEText
                msg = MIMEText(body or '', 'plain')
                msg['to'] = to or ''
                msg['from'] = self.user_email
                msg['subject'] = subject or ''
            
            # Encode updated message
            raw_message = base64.urlsafe_b64encode(
                msg.as_bytes()).decode('utf-8')
            
            # Update draft
            update_response = self.session.put(
                f'{BASE_URL}/users/me/drafts/{draft_id}',
                json={'message': {'raw': raw_message}},
                timeout=30
            )
            
            if update_response.status_code == 200:
                return update_response.json()
            else:
                print(f"Error updating draft: {update_response.status_code}")
                return None
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def send_draft(self, draft_id: str) -> Optional[Dict]:
        """Send a draft"""
        try:
            response = self.session.post(
                f'{BASE_URL}/users/me/drafts/send',
                json={'id': draft_id},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error sending draft: {response.status_code} - {response.text}")
                return None
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def delete_draft(self, draft_id: str) -> bool:
        """Delete a draft"""
        try:
            response = self.session.delete(
                f'{BASE_URL}/users/me/drafts/{draft_id}',
                timeout=30
            )
            return response.status_code == 204
        except Exception as error:
            print(f"An error occurred: {error}")
            return False
    
    # Attachment Handling
    def get_attachment(self, msg_id: str, attachment_id: str) -> Optional[bytes]:
        """Download an attachment"""
        try:
            response = self.session.get(
                f'{BASE_URL}/users/me/messages/{msg_id}/attachments/{attachment_id}',
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                # Decode base64url encoded data
                attachment_data = base64.urlsafe_b64decode(data['data'])
                return attachment_data
            else:
                print(f"Error getting attachment: {response.status_code}")
                return None
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def list_attachments(self, msg_id: str) -> List[Dict]:
        """List all attachments in a message"""
        try:
            message = self.get_message(msg_id, format='full')
            if not message:
                return []
            
            attachments = []
            self._extract_attachments(message['payload'], attachments)
            return attachments
            
        except Exception as error:
            print(f"An error occurred: {error}")
            return []
    
    def download_attachments(self, msg_id: str, output_dir: str = ".") -> List[str]:
        """Download all attachments from a message"""
        try:
            Path(output_dir).mkdir(exist_ok=True)
            attachments = self.list_attachments(msg_id)
            downloaded = []
            
            for att in attachments:
                if att.get('attachmentId'):
                    data = self.get_attachment(msg_id, att['attachmentId'])
                    if data:
                        filename = att.get('filename', f'attachment_{att["attachmentId"]}')
                        filepath = Path(output_dir) / filename
                        
                        with open(filepath, 'wb') as f:
                            f.write(data)
                        
                        downloaded.append(str(filepath))
                        print(f"Downloaded: {filename} ({att.get('size', 0)} bytes)")
            
            return downloaded
            
        except Exception as error:
            print(f"An error occurred: {error}")
            return []
    
    def search_by_attachment(self, has_attachment: bool = True, 
                           filename: Optional[str] = None,
                           larger_than: Optional[int] = None,
                           smaller_than: Optional[int] = None) -> List[Dict]:
        """Search messages by attachment criteria"""
        query_parts = []
        
        if has_attachment:
            query_parts.append("has:attachment")
        
        if filename:
            query_parts.append(f'filename:"{filename}"')
        
        if larger_than:
            query_parts.append(f"larger:{larger_than}")
        
        if smaller_than:
            query_parts.append(f"smaller:{smaller_than}")
        
        query = " ".join(query_parts)
        return self.list_messages(query=query, max_results=50)
    
    # Settings Management
    def get_vacation_settings(self) -> Optional[Dict]:
        """Get vacation responder settings"""
        try:
            response = self.session.get(
                f'{BASE_URL}/users/me/settings/vacation',
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting vacation settings: {response.status_code}")
                return None
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def update_vacation_settings(self, enable: bool, response_subject: str = None,
                               response_body: str = None, start_time: int = None,
                               end_time: int = None) -> Optional[Dict]:
        """Update vacation responder settings"""
        try:
            settings = {
                'enableAutoReply': enable
            }
            
            if enable:
                if response_subject:
                    settings['responseSubject'] = response_subject
                if response_body:
                    settings['responseBodyPlainText'] = response_body
                if start_time:
                    settings['startTime'] = start_time
                if end_time:
                    settings['endTime'] = end_time
            
            response = self.session.put(
                f'{BASE_URL}/users/me/settings/vacation',
                json=settings,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error updating vacation settings: {response.status_code}")
                return None
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def list_send_as(self) -> List[Dict]:
        """List send-as aliases"""
        try:
            response = self.session.get(
                f'{BASE_URL}/users/me/settings/sendAs',
                timeout=30
            )
            
            if response.status_code == 200:
                results = response.json()
                return results.get('sendAs', [])
            else:
                print(f"Error listing send-as: {response.status_code}")
                return []
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return []
    
    def list_forwarding_addresses(self) -> List[Dict]:
        """List forwarding addresses"""
        try:
            response = self.session.get(
                f'{BASE_URL}/users/me/settings/forwardingAddresses',
                timeout=30
            )
            
            if response.status_code == 200:
                results = response.json()
                return results.get('forwardingAddresses', [])
            else:
                print(f"Error listing forwarding addresses: {response.status_code}")
                return []
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return []
    
    # Filter Management
    def get_filter(self, filter_id: str) -> Optional[Dict]:
        """Get a specific filter"""
        try:
            response = self.session.get(
                f'{BASE_URL}/users/me/settings/filters/{filter_id}',
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting filter: {response.status_code}")
                return None
                
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def delete_filter(self, filter_id: str) -> bool:
        """Delete a filter"""
        try:
            response = self.session.delete(
                f'{BASE_URL}/users/me/settings/filters/{filter_id}',
                timeout=30
            )
            return response.status_code == 204
        except Exception as error:
            print(f"An error occurred: {error}")
            return False
    
    # Smart Features
    def mark_important(self, msg_ids: List[str], important: bool = True) -> bool:
        """Mark messages as important/not important"""
        try:
            for msg_id in msg_ids:
                if important:
                    result = self.modify_message(msg_id, add_labels=['IMPORTANT'])
                else:
                    result = self.modify_message(msg_id, remove_labels=['IMPORTANT'])
                
                if not result:
                    return False
            return True
        except Exception as error:
            print(f"An error occurred: {error}")
            return False
    
    def find_unsubscribe_link(self, msg_id: str) -> Optional[str]:
        """Find unsubscribe link in a message"""
        try:
            message = self.get_message(msg_id, format='full')
            if not message:
                return None
            
            # Check List-Unsubscribe header
            headers = {h['name']: h['value'] 
                      for h in message['payload'].get('headers', [])}
            
            list_unsub = headers.get('List-Unsubscribe', '')
            if list_unsub:
                # Extract URL from header
                import re
                urls = re.findall(r'<(https?://[^>]+)>', list_unsub)
                if urls:
                    return urls[0]
            
            # Search in message body
            body = self._extract_body(message['payload'])
            
            # Common unsubscribe patterns
            import re
            patterns = [
                r'(https?://[^\s]+unsubscribe[^\s]*)',
                r'(https?://[^\s]+/unsub[^\s]*)',
                r'(https?://[^\s]+\?.*unsub[^\s]*)',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, body, re.IGNORECASE)
                if matches:
                    return matches[0]
            
            return None
            
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    # Helper methods
    def _extract_body(self, payload: Dict) -> str:
        """Extract text body from message payload"""
        body = ""
        
        if payload.get('parts'):
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        body += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                elif part['mimeType'].startswith('multipart'):
                    body += self._extract_body(part)
        elif payload['body'].get('data'):
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        
        return body
    
    def _extract_attachments(self, payload: Dict, attachments: List[Dict], level: int = 0):
        """Recursively extract attachment information"""
        if payload.get('parts'):
            for part in payload['parts']:
                if part.get('filename'):
                    att_info = {
                        'filename': part['filename'],
                        'mimeType': part.get('mimeType', 'application/octet-stream'),
                        'size': part['body'].get('size', 0),
                        'attachmentId': part['body'].get('attachmentId')
                    }
                    attachments.append(att_info)
                elif part.get('mimeType', '').startswith('multipart'):
                    self._extract_attachments(part, attachments, level + 1)
    
    def _has_attachments(self, message: Dict) -> bool:
        """Check if message has attachments"""
        attachments = []
        self._extract_attachments(message.get('payload', {}), attachments)
        return len(attachments) > 0


def format_thread_display(thread: Dict) -> str:
    """Format thread for display"""
    lines = []
    messages = thread.get('messages', [])
    
    lines.append(f"Thread ID: {thread['id']}")
    lines.append(f"Messages: {len(messages)}")
    lines.append("-" * 50)
    
    for i, msg in enumerate(messages):
        headers = {h['name']: h['value'] 
                  for h in msg['payload'].get('headers', [])}
        
        lines.append(f"\nMessage {i+1}:")
        lines.append(f"  From: {headers.get('From', 'Unknown')}")
        lines.append(f"  Date: {headers.get('Date', 'Unknown')}")
        lines.append(f"  Subject: {headers.get('Subject', 'No Subject')}")
        
        # Show snippet
        if msg.get('snippet'):
            snippet = msg['snippet'][:100] + '...' if len(msg['snippet']) > 100 else msg['snippet']
            lines.append(f"  Preview: {snippet}")
    
    return '\n'.join(lines)


def format_draft_display(draft: Dict) -> str:
    """Format draft for display"""
    lines = []
    message = draft.get('message', {})
    
    lines.append(f"Draft ID: {draft['id']}")
    
    if 'payload' in message:
        headers = {h['name']: h['value'] 
                  for h in message['payload'].get('headers', [])}
        
        lines.append(f"To: {headers.get('To', 'Not set')}")
        lines.append(f"Subject: {headers.get('Subject', 'No Subject')}")
        
        if message.get('snippet'):
            lines.append(f"Preview: {message['snippet'][:100]}...")
    
    lines.append("-" * 50)
    return '\n'.join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Gmail Enhanced CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Thread commands
    thread_parser = subparsers.add_parser('thread', help='Thread operations')
    thread_sub = thread_parser.add_subparsers(dest='thread_command')
    
    thread_view = thread_sub.add_parser('view', help='View full thread')
    thread_view.add_argument('thread_id', help='Thread ID')
    
    thread_reply = thread_sub.add_parser('reply', help='Reply to thread')
    thread_reply.add_argument('thread_id', help='Thread ID')
    thread_reply.add_argument('to', help='Recipient')
    thread_reply.add_argument('body', help='Reply body')
    
    # Draft commands
    draft_parser = subparsers.add_parser('draft', help='Draft operations')
    draft_sub = draft_parser.add_subparsers(dest='draft_command')
    
    draft_list = draft_sub.add_parser('list', help='List drafts')
    draft_list.add_argument('-n', '--number', type=int, default=10, help='Number of drafts')
    
    draft_create = draft_sub.add_parser('create', help='Create draft')
    draft_create.add_argument('to', help='Recipient')
    draft_create.add_argument('subject', help='Subject')
    draft_create.add_argument('body', help='Body')
    
    draft_send = draft_sub.add_parser('send', help='Send draft')
    draft_send.add_argument('draft_id', help='Draft ID')
    
    draft_delete = draft_sub.add_parser('delete', help='Delete draft')
    draft_delete.add_argument('draft_id', help='Draft ID')
    
    # Attachment commands
    att_parser = subparsers.add_parser('attachment', help='Attachment operations')
    att_sub = att_parser.add_subparsers(dest='att_command')
    
    att_list = att_sub.add_parser('list', help='List attachments')
    att_list.add_argument('message_id', help='Message ID')
    
    att_download = att_sub.add_parser('download', help='Download attachments')
    att_download.add_argument('message_id', help='Message ID')
    att_download.add_argument('-o', '--output', default='.', help='Output directory')
    
    att_search = att_sub.add_parser('search', help='Search by attachment')
    att_search.add_argument('-f', '--filename', help='Filename pattern')
    att_search.add_argument('--larger', type=int, help='Larger than (bytes)')
    att_search.add_argument('--smaller', type=int, help='Smaller than (bytes)')
    
    # Settings commands
    settings_parser = subparsers.add_parser('settings', help='Settings operations')
    settings_sub = settings_parser.add_subparsers(dest='settings_command')
    
    vacation_parser = settings_sub.add_parser('vacation', help='Vacation responder')
    vacation_sub = vacation_parser.add_subparsers(dest='vacation_command')
    
    vacation_get = vacation_sub.add_parser('get', help='Get vacation settings')
    
    vacation_set = vacation_sub.add_parser('set', help='Set vacation responder')
    vacation_set.add_argument('--enable', action='store_true', help='Enable responder')
    vacation_set.add_argument('--disable', action='store_true', help='Disable responder')
    vacation_set.add_argument('--subject', help='Response subject')
    vacation_set.add_argument('--body', help='Response body')
    
    sendas_list = settings_sub.add_parser('sendas', help='List send-as aliases')
    forward_list = settings_sub.add_parser('forwarding', help='List forwarding addresses')
    
    # Smart features
    smart_parser = subparsers.add_parser('smart', help='Smart features')
    smart_sub = smart_parser.add_subparsers(dest='smart_command')
    
    important_parser = smart_sub.add_parser('important', help='Mark as important')
    important_parser.add_argument('message_ids', nargs='+', help='Message IDs')
    important_parser.add_argument('--remove', action='store_true', help='Remove important label')
    
    unsub_parser = smart_sub.add_parser('unsubscribe', help='Find unsubscribe link')
    unsub_parser.add_argument('message_id', help='Message ID')
    
    # Forward command
    forward_parser = subparsers.add_parser('forward', help='Forward message')
    forward_parser.add_argument('message_id', help='Message ID')
    forward_parser.add_argument('to', help='Recipient')
    forward_parser.add_argument('-c', '--comment', default='', help='Comment to add')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize Gmail Enhanced
    gmail = GmailEnhanced()
    gmail.authenticate()
    
    # Execute commands
    if args.command == 'thread':
        if args.thread_command == 'view':
            thread = gmail.get_thread(args.thread_id)
            if thread:
                print(format_thread_display(thread))
        
        elif args.thread_command == 'reply':
            result = gmail.reply_to_thread(args.thread_id, args.to, args.body)
            if result:
                print(f"Reply sent successfully! Message ID: {result['id']}")
    
    elif args.command == 'draft':
        if args.draft_command == 'list':
            drafts = gmail.list_drafts(args.number)
            for draft in drafts:
                print(format_draft_display(draft))
        
        elif args.draft_command == 'create':
            draft = gmail.create_draft(args.to, args.subject, args.body)
            if draft:
                print(f"Draft created! ID: {draft['id']}")
        
        elif args.draft_command == 'send':
            result = gmail.send_draft(args.draft_id)
            if result:
                print(f"Draft sent! Message ID: {result['id']}")
        
        elif args.draft_command == 'delete':
            if gmail.delete_draft(args.draft_id):
                print("Draft deleted successfully!")
    
    elif args.command == 'attachment':
        if args.att_command == 'list':
            attachments = gmail.list_attachments(args.message_id)
            for att in attachments:
                print(f"Filename: {att['filename']}")
                print(f"  Type: {att['mimeType']}")
                print(f"  Size: {att['size']} bytes")
                print(f"  ID: {att.get('attachmentId', 'N/A')}")
                print()
        
        elif args.att_command == 'download':
            files = gmail.download_attachments(args.message_id, args.output)
            print(f"Downloaded {len(files)} attachments")
        
        elif args.att_command == 'search':
            messages = gmail.search_by_attachment(
                filename=args.filename,
                larger_than=args.larger,
                smaller_than=args.smaller
            )
            print(f"Found {len(messages)} messages with attachments")
            for msg in messages[:10]:
                headers = {h['name']: h['value'] 
                          for h in msg['payload']['headers']}
                print(f"ID: {msg['id']}")
                print(f"  From: {headers.get('From', 'Unknown')}")
                print(f"  Subject: {headers.get('Subject', 'No Subject')}")
                print()
    
    elif args.command == 'settings':
        if args.settings_command == 'vacation':
            if hasattr(args, 'vacation_command') and args.vacation_command == 'get':
                settings = gmail.get_vacation_settings()
                if settings:
                    print(json.dumps(settings, indent=2))
            elif hasattr(args, 'vacation_command') and args.vacation_command == 'set':
                if args.enable:
                    result = gmail.update_vacation_settings(
                        True, args.subject, args.body
                    )
                    if result:
                        print("Vacation responder enabled!")
                elif args.disable:
                    result = gmail.update_vacation_settings(False)
                    if result:
                        print("Vacation responder disabled!")
        
        elif args.settings_command == 'sendas':
            aliases = gmail.list_send_as()
            for alias in aliases:
                print(f"Email: {alias['sendAsEmail']}")
                print(f"  Name: {alias.get('displayName', 'Not set')}")
                print(f"  Default: {alias.get('isDefault', False)}")
                print()
        
        elif args.settings_command == 'forwarding':
            addresses = gmail.list_forwarding_addresses()
            for addr in addresses:
                print(f"Email: {addr['forwardingEmail']}")
                print(f"  Verification: {addr.get('verificationStatus', 'Unknown')}")
                print()
    
    elif args.command == 'smart':
        if args.smart_command == 'important':
            success = gmail.mark_important(args.message_ids, not args.remove)
            if success:
                action = "removed from" if args.remove else "marked as"
                print(f"Messages {action} important")
        
        elif args.smart_command == 'unsubscribe':
            link = gmail.find_unsubscribe_link(args.message_id)
            if link:
                print(f"Unsubscribe link found: {link}")
            else:
                print("No unsubscribe link found")
    
    elif args.command == 'forward':
        result = gmail.forward_message(args.message_id, args.to, args.comment)
        if result:
            print(f"Message forwarded! ID: {result['id']}")


if __name__ == '__main__':
    main()