#!/Users/pete/Projects/tool-library/gmail-tool/venv/bin/python
"""
Gmail CLI Advanced Features - Extended functionality for power users
"""

import os
import json
import csv
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import re

from gmail_cli import GmailCLI
from gmail_service_compat import HttpError


class GmailAdvanced(GmailCLI):
    """Extended Gmail functionality"""
    
    def __init__(self):
        super().__init__()
        self.rate_limit_delay = 0.1  # 100ms between requests
    
    def search_and_export(self, query: str, output_format: str = 'json', 
                         output_file: str = None, include_body: bool = False) -> int:
        """Search and export messages to various formats"""
        try:
            all_messages = []
            page_token = None
            
            while True:
                results = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    pageToken=page_token,
                    maxResults=500
                ).execute()
                
                if 'messages' in results:
                    # Get full details for each message
                    for msg in results['messages']:
                        time.sleep(self.rate_limit_delay)
                        
                        format_type = 'full' if include_body else 'metadata'
                        message = self.service.users().messages().get(
                            userId='me',
                            id=msg['id'],
                            format=format_type
                        ).execute()
                        all_messages.append(message)
                        
                        print(f"\rProcessed {len(all_messages)} messages...", end='', flush=True)
                
                page_token = results.get('nextPageToken')
                if not page_token:
                    break
            
            print(f"\nTotal messages found: {len(all_messages)}")
            
            # Export based on format
            if output_format == 'json':
                output_data = json.dumps(all_messages, indent=2)
            elif output_format == 'csv':
                output_data = self._messages_to_csv(all_messages)
            elif output_format == 'mbox':
                output_data = self._messages_to_mbox(all_messages)
            else:
                raise ValueError(f"Unsupported format: {output_format}")
            
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(output_data)
                print(f"Exported to {output_file}")
            else:
                print(output_data)
            
            return len(all_messages)
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return 0
    
    def _messages_to_csv(self, messages: List[Dict]) -> str:
        """Convert messages to CSV format"""
        output = []
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['ID', 'Date', 'From', 'To', 'Subject', 'Labels', 'Snippet'])
        
        for msg in messages:
            headers = {h['name']: h['value'] for h in msg['payload'].get('headers', [])}
            
            writer.writerow([
                msg['id'],
                headers.get('Date', ''),
                headers.get('From', ''),
                headers.get('To', ''),
                headers.get('Subject', ''),
                ','.join(msg.get('labelIds', [])),
                msg.get('snippet', '')
            ])
        
        return '\n'.join(output)
    
    def _messages_to_mbox(self, messages: List[Dict]) -> str:
        """Convert messages to mbox format"""
        mbox_content = []
        
        for msg in messages:
            # Get raw message
            try:
                raw_msg = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='raw'
                ).execute()
                
                # mbox format requires 'From ' line
                timestamp = datetime.now().strftime('%a %b %d %H:%M:%S %Y')
                mbox_content.append(f"From MAILER-DAEMON {timestamp}")
                
                # Decode raw message
                import base64
                raw_data = base64.urlsafe_b64decode(raw_msg['raw'])
                mbox_content.append(raw_data.decode('utf-8', errors='ignore'))
                mbox_content.append('')  # Empty line between messages
                
            except Exception as e:
                print(f"Error processing message {msg['id']}: {e}")
        
        return '\n'.join(mbox_content)
    
    def bulk_label_operations(self, query: str, add_labels: List[str] = None,
                            remove_labels: List[str] = None) -> int:
        """Apply label changes to all messages matching query"""
        try:
            # Get all message IDs matching query
            message_ids = []
            page_token = None
            
            while True:
                results = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    pageToken=page_token,
                    maxResults=500
                ).execute()
                
                if 'messages' in results:
                    message_ids.extend([msg['id'] for msg in results['messages']])
                
                page_token = results.get('nextPageToken')
                if not page_token:
                    break
            
            print(f"Found {len(message_ids)} messages to update")
            
            # Get label IDs
            label_map = self._get_label_map()
            add_label_ids = [label_map.get(l, l) for l in (add_labels or [])]
            remove_label_ids = [label_map.get(l, l) for l in (remove_labels or [])]
            
            # Batch modify (max 1000 per request)
            modified_count = 0
            for i in range(0, len(message_ids), 1000):
                batch_ids = message_ids[i:i+1000]
                
                body = {
                    'ids': batch_ids,
                    'addLabelIds': add_label_ids,
                    'removeLabelIds': remove_label_ids
                }
                
                self.service.users().messages().batchModify(
                    userId='me',
                    body=body
                ).execute()
                
                modified_count += len(batch_ids)
                print(f"Modified {modified_count}/{len(message_ids)} messages...")
                time.sleep(self.rate_limit_delay)
            
            return modified_count
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return 0
    
    def _get_label_map(self) -> Dict[str, str]:
        """Get mapping of label names to IDs"""
        labels = self.list_labels()
        return {label['name']: label['id'] for label in labels}
    
    def analyze_inbox(self, days: int = 30) -> Dict:
        """Analyze inbox patterns and statistics"""
        try:
            # Calculate date range
            start_date = datetime.now() - timedelta(days=days)
            query = f"after:{start_date.strftime('%Y/%m/%d')}"
            
            messages = []
            page_token = None
            
            print(f"Analyzing messages from last {days} days...")
            
            while True:
                results = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    pageToken=page_token,
                    maxResults=500
                ).execute()
                
                if 'messages' in results:
                    for msg in results['messages']:
                        # Get metadata
                        message = self.service.users().messages().get(
                            userId='me',
                            id=msg['id'],
                            format='metadata',
                            metadataHeaders=['From', 'Date', 'Subject']
                        ).execute()
                        messages.append(message)
                        
                        if len(messages) % 100 == 0:
                            print(f"\rProcessed {len(messages)} messages...", end='', flush=True)
                
                page_token = results.get('nextPageToken')
                if not page_token:
                    break
            
            print(f"\nAnalyzing {len(messages)} messages...")
            
            # Analyze patterns
            analysis = {
                'total_messages': len(messages),
                'date_range': f"{days} days",
                'senders': defaultdict(int),
                'domains': defaultdict(int),
                'labels': defaultdict(int),
                'hourly_distribution': defaultdict(int),
                'daily_distribution': defaultdict(int),
                'thread_sizes': defaultdict(int)
            }
            
            for msg in messages:
                headers = {h['name']: h['value'] for h in msg['payload'].get('headers', [])}
                
                # Sender analysis
                from_header = headers.get('From', '')
                email_match = re.search(r'<(.+?)>', from_header)
                if email_match:
                    email = email_match.group(1)
                    analysis['senders'][email] += 1
                    domain = email.split('@')[-1]
                    analysis['domains'][domain] += 1
                
                # Label analysis
                for label in msg.get('labelIds', []):
                    analysis['labels'][label] += 1
                
                # Time analysis
                date_header = headers.get('Date', '')
                try:
                    # Parse various date formats
                    from email.utils import parsedate_to_datetime
                    msg_date = parsedate_to_datetime(date_header)
                    analysis['hourly_distribution'][msg_date.hour] += 1
                    analysis['daily_distribution'][msg_date.strftime('%A')] += 1
                except:
                    pass
            
            # Sort and limit results
            analysis['top_senders'] = sorted(
                analysis['senders'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:20]
            
            analysis['top_domains'] = sorted(
                analysis['domains'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:20]
            
            # Clean up raw data
            del analysis['senders']
            del analysis['domains']
            
            return analysis
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return {}
    
    def create_filters_from_analysis(self, analysis: Dict, auto_archive_threshold: int = 50):
        """Create filters based on inbox analysis"""
        suggestions = []
        
        # Suggest filters for high-volume senders
        for sender, count in analysis.get('top_senders', []):
            if count >= auto_archive_threshold:
                suggestions.append({
                    'criteria': {'from': sender},
                    'action': {'removeLabelIds': ['INBOX'], 'addLabelIds': ['ARCHIVE']},
                    'reason': f"Sender {sender} sent {count} emails"
                })
        
        # Suggest filters for domains
        for domain, count in analysis.get('top_domains', []):
            if count >= auto_archive_threshold * 2:  # Higher threshold for domains
                suggestions.append({
                    'criteria': {'from': f"@{domain}"},
                    'action': {'addLabelIds': [f"Domain/{domain}"]},
                    'reason': f"Domain {domain} sent {count} emails"
                })
        
        return suggestions
    
    def smart_cleanup(self, older_than_days: int = 180, 
                     skip_labels: List[str] = None) -> int:
        """Smart cleanup of old messages"""
        skip_labels = skip_labels or ['IMPORTANT', 'STARRED']
        
        # Build query
        date = datetime.now() - timedelta(days=older_than_days)
        query_parts = [f"before:{date.strftime('%Y/%m/%d')}"]
        
        for label in skip_labels:
            query_parts.append(f"-label:{label}")
        
        query = ' '.join(query_parts)
        
        print(f"Searching for messages to clean up: {query}")
        
        # Get message IDs
        message_ids = []
        page_token = None
        
        while True:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                pageToken=page_token,
                maxResults=500
            ).execute()
            
            if 'messages' in results:
                message_ids.extend([msg['id'] for msg in results['messages']])
            
            page_token = results.get('nextPageToken')
            if not page_token:
                break
        
        print(f"Found {len(message_ids)} messages older than {older_than_days} days")
        
        if message_ids:
            response = input("Do you want to move these to trash? (y/N): ")
            if response.lower() == 'y':
                # Batch trash
                for i in range(0, len(message_ids), 1000):
                    batch_ids = message_ids[i:i+1000]
                    
                    self.service.users().messages().batchModify(
                        userId='me',
                        body={
                            'ids': batch_ids,
                            'addLabelIds': ['TRASH']
                        }
                    ).execute()
                    
                    print(f"Trashed {min(i+1000, len(message_ids))}/{len(message_ids)} messages...")
                
                return len(message_ids)
        
        return 0


def main():
    """Advanced features CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gmail CLI Advanced Features')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export messages')
    export_parser.add_argument('query', help='Search query')
    export_parser.add_argument('-f', '--format', choices=['json', 'csv', 'mbox'], 
                             default='json', help='Export format')
    export_parser.add_argument('-o', '--output', help='Output file')
    export_parser.add_argument('--include-body', action='store_true', 
                             help='Include message body')
    
    # Bulk label command
    bulk_parser = subparsers.add_parser('bulk-label', help='Bulk label operations')
    bulk_parser.add_argument('query', help='Search query')
    bulk_parser.add_argument('--add', nargs='+', help='Labels to add')
    bulk_parser.add_argument('--remove', nargs='+', help='Labels to remove')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze inbox patterns')
    analyze_parser.add_argument('-d', '--days', type=int, default=30, 
                              help='Number of days to analyze')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Smart cleanup old messages')
    cleanup_parser.add_argument('-d', '--days', type=int, default=180,
                              help='Delete messages older than X days')
    cleanup_parser.add_argument('--skip-labels', nargs='+', 
                              help='Labels to skip during cleanup')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize
    gmail = GmailAdvanced()
    gmail.authenticate()
    
    # Execute commands
    if args.command == 'export':
        count = gmail.search_and_export(
            args.query,
            output_format=args.format,
            output_file=args.output,
            include_body=args.include_body
        )
        print(f"Exported {count} messages")
    
    elif args.command == 'bulk-label':
        count = gmail.bulk_label_operations(
            args.query,
            add_labels=args.add,
            remove_labels=args.remove
        )
        print(f"Modified {count} messages")
    
    elif args.command == 'analyze':
        analysis = gmail.analyze_inbox(days=args.days)
        
        print("\n=== Inbox Analysis ===")
        print(f"Total messages: {analysis['total_messages']}")
        print(f"Date range: {analysis['date_range']}")
        
        print("\nTop 10 Senders:")
        for sender, count in analysis['top_senders'][:10]:
            print(f"  {sender}: {count} messages")
        
        print("\nTop 10 Domains:")
        for domain, count in analysis['top_domains'][:10]:
            print(f"  {domain}: {count} messages")
        
        print("\nLabel Distribution:")
        for label, count in sorted(analysis['labels'].items(), 
                                  key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {label}: {count} messages")
        
        # Save full analysis
        with open('inbox_analysis.json', 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        print("\nFull analysis saved to inbox_analysis.json")
    
    elif args.command == 'cleanup':
        count = gmail.smart_cleanup(
            older_than_days=args.days,
            skip_labels=args.skip_labels
        )
        print(f"Cleaned up {count} messages")


if __name__ == '__main__':
    main()