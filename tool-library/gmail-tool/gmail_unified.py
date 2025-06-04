#!/Users/pete/Projects/tool-library/gmail-tool/venv/bin/python
"""
Unified Gmail CLI - All Gmail functionality in one intuitive interface
"""

import os
import sys
import json
import base64
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Import all functionality from existing modules
from gmail_cli import GmailCLI, format_message_display
from gmail_advanced import GmailAdvanced
from gmail_enhanced import GmailEnhanced, format_thread_display, format_draft_display


def main():
    parser = argparse.ArgumentParser(
        description='Gmail CLI - Unified command-line interface for Gmail',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gmail list                      # List recent emails
  gmail search "is:unread"        # Search emails
  gmail read MESSAGE_ID           # Read an email
  gmail send to@email.com "Subject" "Body"
  gmail draft create to@email.com "Subject" "Body"
  gmail thread view THREAD_ID     # View conversation
  gmail attachment list MSG_ID    # List attachments
  gmail analyze                   # Analyze inbox patterns
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # LIST - List messages
    list_parser = subparsers.add_parser('list', help='List messages')
    list_parser.add_argument('-n', '--number', type=int, default=10, help='Number of messages')
    list_parser.add_argument('-q', '--query', default='', help='Search query')
    list_parser.add_argument('--include-spam-trash', action='store_true', help='Include spam and trash')
    
    # SEARCH - Search messages (alias for list with query)
    search_parser = subparsers.add_parser('search', help='Search messages')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('-n', '--number', type=int, default=10, help='Number of results')
    search_parser.add_argument('--include-spam-trash', action='store_true', help='Include spam and trash')
    
    # READ - Read a message
    read_parser = subparsers.add_parser('read', help='Read a message')
    read_parser.add_argument('message_id', help='Message ID')
    read_parser.add_argument('--format', choices=['minimal', 'full', 'raw', 'metadata'], 
                           default='full', help='Message format')
    
    # SEND - Send a message
    send_parser = subparsers.add_parser('send', help='Send a message')
    send_parser.add_argument('to', help='Recipient email')
    send_parser.add_argument('subject', help='Email subject')
    send_parser.add_argument('body', help='Email body')
    send_parser.add_argument('-a', '--attach', action='append', help='Attachment file path')
    
    # REPLY - Reply to a message
    reply_parser = subparsers.add_parser('reply', help='Reply to a message')
    reply_parser.add_argument('thread_id', help='Thread ID to reply to')
    reply_parser.add_argument('to', help='Recipient')
    reply_parser.add_argument('body', help='Reply body')
    
    # FORWARD - Forward a message
    forward_parser = subparsers.add_parser('forward', help='Forward a message')
    forward_parser.add_argument('message_id', help='Message ID')
    forward_parser.add_argument('to', help='Recipient')
    forward_parser.add_argument('-c', '--comment', default='', help='Comment to add')
    
    # DRAFT - Draft operations
    draft_parser = subparsers.add_parser('draft', help='Draft operations')
    draft_sub = draft_parser.add_subparsers(dest='draft_command')
    
    draft_list = draft_sub.add_parser('list', help='List drafts')
    draft_list.add_argument('-n', '--number', type=int, default=10)
    
    draft_create = draft_sub.add_parser('create', help='Create draft')
    draft_create.add_argument('to', help='Recipient')
    draft_create.add_argument('subject', help='Subject')
    draft_create.add_argument('body', help='Body')
    
    draft_send = draft_sub.add_parser('send', help='Send draft')
    draft_send.add_argument('draft_id', help='Draft ID')
    
    draft_delete = draft_sub.add_parser('delete', help='Delete draft')
    draft_delete.add_argument('draft_id', help='Draft ID')
    
    # THREAD - Thread operations
    thread_parser = subparsers.add_parser('thread', help='Thread operations')
    thread_sub = thread_parser.add_subparsers(dest='thread_command')
    
    thread_view = thread_sub.add_parser('view', help='View thread')
    thread_view.add_argument('thread_id', help='Thread ID')
    
    thread_reply = thread_sub.add_parser('reply', help='Reply to thread')
    thread_reply.add_argument('thread_id', help='Thread ID')
    thread_reply.add_argument('to', help='Recipient')
    thread_reply.add_argument('body', help='Reply body')
    
    # ATTACHMENT - Attachment operations
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
    
    # LABEL - Label operations
    label_parser = subparsers.add_parser('label', help='Label operations')
    label_sub = label_parser.add_subparsers(dest='label_command')
    
    label_list = label_sub.add_parser('list', help='List labels')
    
    label_create = label_sub.add_parser('create', help='Create label')
    label_create.add_argument('name', help='Label name')
    
    label_apply = label_sub.add_parser('apply', help='Apply label')
    label_apply.add_argument('message_id', help='Message ID')
    label_apply.add_argument('label', help='Label to apply')
    
    label_remove = label_sub.add_parser('remove', help='Remove label')
    label_remove.add_argument('message_id', help='Message ID')
    label_remove.add_argument('label', help='Label to remove')
    
    # FILTER - Filter operations
    filter_parser = subparsers.add_parser('filter', help='Filter operations')
    filter_sub = filter_parser.add_subparsers(dest='filter_command')
    
    filter_list = filter_sub.add_parser('list', help='List filters')
    
    filter_create = filter_sub.add_parser('create', help='Create filter')
    filter_create.add_argument('--from', dest='from_addr', help='From address')
    filter_create.add_argument('--to', help='To address')
    filter_create.add_argument('--subject', help='Subject contains')
    filter_create.add_argument('--add-label', help='Add label')
    filter_create.add_argument('--remove-label', help='Remove label')
    
    filter_delete = filter_sub.add_parser('delete', help='Delete filter')
    filter_delete.add_argument('filter_id', help='Filter ID')
    
    # TRASH/DELETE - Message deletion
    trash_parser = subparsers.add_parser('trash', help='Move to trash')
    trash_parser.add_argument('message_id', help='Message ID')
    
    delete_parser = subparsers.add_parser('delete', help='Permanently delete')
    delete_parser.add_argument('message_id', help='Message ID')
    
    batch_delete_parser = subparsers.add_parser('batch-delete', help='Delete multiple')
    batch_delete_parser.add_argument('message_ids', nargs='+', help='Message IDs')
    
    # SETTINGS - Settings management
    settings_parser = subparsers.add_parser('settings', help='Settings operations')
    settings_sub = settings_parser.add_subparsers(dest='settings_command')
    
    # Vacation settings
    vacation_parser = settings_sub.add_parser('vacation', help='Vacation responder')
    vacation_sub = vacation_parser.add_subparsers(dest='vacation_command')
    
    vacation_get = vacation_sub.add_parser('get', help='Get settings')
    vacation_enable = vacation_sub.add_parser('enable', help='Enable responder')
    vacation_enable.add_argument('--subject', required=True, help='Response subject')
    vacation_enable.add_argument('--body', required=True, help='Response body')
    vacation_disable = vacation_sub.add_parser('disable', help='Disable responder')
    
    settings_sendas = settings_sub.add_parser('sendas', help='List send-as aliases')
    settings_forward = settings_sub.add_parser('forwarding', help='List forwarding addresses')
    
    # ANALYZE - Analyze inbox
    analyze_parser = subparsers.add_parser('analyze', help='Analyze inbox patterns')
    analyze_parser.add_argument('--days', type=int, default=30, help='Days to analyze')
    analyze_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # EXPORT - Export messages
    export_parser = subparsers.add_parser('export', help='Export messages')
    export_parser.add_argument('query', help='Search query')
    export_parser.add_argument('-f', '--format', choices=['json', 'csv', 'mbox'], 
                             default='json', help='Export format')
    export_parser.add_argument('-o', '--output', help='Output file')
    export_parser.add_argument('--include-body', action='store_true', help='Include message body')
    
    # IMPORTANT - Mark as important
    important_parser = subparsers.add_parser('important', help='Mark as important')
    important_sub = important_parser.add_subparsers(dest='important_command')
    
    important_mark = important_sub.add_parser('mark', help='Mark as important')
    important_mark.add_argument('message_ids', nargs='+', help='Message IDs')
    
    important_unmark = important_sub.add_parser('unmark', help='Remove important')
    important_unmark.add_argument('message_ids', nargs='+', help='Message IDs')
    
    # UNSUBSCRIBE - Find unsubscribe link
    unsub_parser = subparsers.add_parser('unsubscribe', help='Find unsubscribe link')
    unsub_parser.add_argument('message_id', help='Message ID')
    
    # WATCH - Set up push notifications
    watch_parser = subparsers.add_parser('watch', help='Set up push notifications')
    watch_parser.add_argument('topic', help='Pub/Sub topic name')
    watch_parser.add_argument('-l', '--labels', nargs='+', help='Label IDs to watch')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize appropriate Gmail client based on command
    if args.command in ['analyze', 'export']:
        gmail = GmailAdvanced()
    elif args.command in ['draft', 'thread', 'attachment', 'forward', 'settings', 'important', 'unsubscribe']:
        gmail = GmailEnhanced()
    else:
        gmail = GmailCLI()
    
    gmail.authenticate()
    
    # Execute commands
    try:
        # LIST/SEARCH
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
        
        elif args.command == 'search':
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
        
        # READ
        elif args.command == 'read':
            message = gmail.get_message(args.message_id, format=args.format)
            if message:
                if args.format == 'metadata':
                    print(format_message_display(message))
                else:
                    print(json.dumps(message, indent=2))
            else:
                print("Message not found.")
        
        # SEND
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
        
        # REPLY
        elif args.command == 'reply':
            result = gmail.reply_to_thread(args.thread_id, args.to, args.body)
            if result:
                print(f"Reply sent successfully! Message ID: {result['id']}")
        
        # FORWARD
        elif args.command == 'forward':
            result = gmail.forward_message(args.message_id, args.to, args.comment)
            if result:
                print(f"Message forwarded! ID: {result['id']}")
        
        # DRAFT
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
        
        # THREAD
        elif args.command == 'thread':
            if args.thread_command == 'view':
                thread = gmail.get_thread(args.thread_id)
                if thread:
                    print(format_thread_display(thread))
            
            elif args.thread_command == 'reply':
                result = gmail.reply_to_thread(args.thread_id, args.to, args.body)
                if result:
                    print(f"Reply sent successfully! Message ID: {result['id']}")
        
        # ATTACHMENT
        elif args.command == 'attachment':
            if args.att_command == 'list':
                attachments = gmail.list_attachments(args.message_id)
                for att in attachments:
                    print(f"Filename: {att['filename']}")
                    print(f"  Type: {att['mimeType']}")
                    print(f"  Size: {att['size']} bytes")
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
                    print(format_message_display(msg))
        
        # LABEL
        elif args.command == 'label':
            if args.label_command == 'list':
                labels = gmail.list_labels()
                for label in labels:
                    print(f"{label['name']} (ID: {label['id']})")
            
            elif args.label_command == 'create':
                label = gmail.create_label(args.name)
                if label:
                    print(f"Label created: {label['name']} (ID: {label['id']})")
            
            elif args.label_command in ['apply', 'remove']:
                # Get label ID from name
                labels = gmail.list_labels()
                label_id = None
                for label in labels:
                    if label['name'] == args.label:
                        label_id = label['id']
                        break
                
                if label_id:
                    if args.label_command == 'apply':
                        result = gmail.modify_message(args.message_id, add_labels=[label_id])
                    else:
                        result = gmail.modify_message(args.message_id, remove_labels=[label_id])
                    
                    if result:
                        action = "applied to" if args.label_command == 'apply' else "removed from"
                        print(f"Label '{args.label}' {action} message.")
                else:
                    print(f"Label '{args.label}' not found.")
        
        # FILTER
        elif args.command == 'filter':
            if args.filter_command == 'list':
                filters = gmail.list_filters()
                for f in filters:
                    print(f"Filter ID: {f['id']}")
                    if 'criteria' in f:
                        print(f"  Criteria: {json.dumps(f['criteria'], indent=4)}")
                    if 'action' in f:
                        print(f"  Action: {json.dumps(f['action'], indent=4)}")
                    print("-" * 50)
            
            elif args.filter_command == 'create':
                criteria = {}
                if args.from_addr:
                    criteria['from'] = args.from_addr
                if args.to:
                    criteria['to'] = args.to
                if args.subject:
                    criteria['subject'] = args.subject
                
                action = {}
                if args.add_label:
                    # Get label ID
                    labels = gmail.list_labels()
                    for label in labels:
                        if label['name'] == args.add_label:
                            action['addLabelIds'] = [label['id']]
                            break
                
                if args.remove_label:
                    # Get label ID
                    labels = gmail.list_labels()
                    for label in labels:
                        if label['name'] == args.remove_label:
                            action['removeLabelIds'] = [label['id']]
                            break
                
                if criteria and action:
                    result = gmail.create_filter(criteria, action)
                    if result:
                        print(f"Filter created! ID: {result['id']}")
                else:
                    print("Error: Must specify at least one criteria and one action")
            
            elif args.filter_command == 'delete':
                if gmail.delete_filter(args.filter_id):
                    print("Filter deleted successfully!")
        
        # TRASH/DELETE
        elif args.command == 'trash':
            if gmail.trash_message(args.message_id):
                print("Message moved to trash.")
        
        elif args.command == 'delete':
            response = input("Are you sure you want to permanently delete this message? (y/N): ")
            if response.lower() == 'y':
                if gmail.delete_message(args.message_id):
                    print("Message permanently deleted.")
                else:
                    print("Failed to delete message.")
        
        elif args.command == 'batch-delete':
            response = input(f"Are you sure you want to permanently delete {len(args.message_ids)} messages? (y/N): ")
            if response.lower() == 'y':
                if gmail.batch_delete(args.message_ids):
                    print(f"Successfully deleted {len(args.message_ids)} messages.")
        
        # SETTINGS
        elif args.command == 'settings':
            if args.settings_command == 'vacation':
                if args.vacation_command == 'get':
                    settings = gmail.get_vacation_settings()
                    if settings:
                        print(json.dumps(settings, indent=2))
                
                elif args.vacation_command == 'enable':
                    result = gmail.update_vacation_settings(
                        True, args.subject, args.body
                    )
                    if result:
                        print("Vacation responder enabled!")
                
                elif args.vacation_command == 'disable':
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
        
        # ANALYZE
        elif args.command == 'analyze':
            analysis = gmail.analyze_inbox(days=args.days)
            if args.json:
                print(json.dumps(analysis, indent=2))
            else:
                print(f"\n=== Inbox Analysis ===")
                print(f"Total messages: {analysis['total_messages']}")
                print(f"Date range: {args.days} days")
                
                print("\nTop 10 Senders:")
                for sender, count in analysis['top_senders'][:10]:
                    print(f"  {sender}: {count} messages")
                
                print("\nTop 10 Domains:")
                for domain, count in analysis['top_domains'][:10]:
                    print(f"  {domain}: {count} messages")
                
                print("\nLabel Distribution:")
                for label, count in sorted(analysis['labels'].items(), 
                                          key=lambda x: x[1], reverse=True):
                    print(f"  {label}: {count} messages")
                
                print("\nFull analysis saved to inbox_analysis.json")
        
        # EXPORT
        elif args.command == 'export':
            count = gmail.search_and_export(
                query=args.query,
                output_format=args.format,
                output_file=args.output,
                include_body=args.include_body
            )
            print(f"Exported {count} messages")
        
        # IMPORTANT
        elif args.command == 'important':
            if args.important_command == 'mark':
                success = gmail.mark_important(args.message_ids, True)
                if success:
                    print("Messages marked as important")
            
            elif args.important_command == 'unmark':
                success = gmail.mark_important(args.message_ids, False)
                if success:
                    print("Important label removed from messages")
        
        # UNSUBSCRIBE
        elif args.command == 'unsubscribe':
            link = gmail.find_unsubscribe_link(args.message_id)
            if link:
                print(f"Unsubscribe link found: {link}")
            else:
                print("No unsubscribe link found")
        
        # WATCH
        elif args.command == 'watch':
            result = gmail.watch_mailbox(args.topic, args.labels)
            if result:
                print(f"Watch set up successfully.")
                print(f"History ID: {result['historyId']}")
                print(f"Expiration: {result['expiration']}")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()