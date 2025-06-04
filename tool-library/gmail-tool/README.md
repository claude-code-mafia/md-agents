# Gmail CLI Tool

A comprehensive command-line interface for Gmail that leverages the full capabilities of the Gmail API.

## Purpose

This tool provides complete Gmail functionality from the command line with an intuitive interface:
- Reading, searching, and sending emails
- Thread management and replies
- Draft creation and management
- Attachment handling
- Label and filter management
- Settings configuration
- Inbox analysis and export
- Smart features like unsubscribe detection

## Setup

### 1. Google Cloud Console Setup
1. Go to https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as application type
   - Download the credentials JSON file

### 2. Install Tool
```bash
# Clone the repository
cd ~/Projects/tool-library/gmail-tool

# Install dependencies (handled by setup.sh)
./setup.sh

# Move credentials file
mkdir -p ~/.gmail-cli
mv ~/Downloads/credentials.json ~/.gmail-cli/credentials.json
```

### 3. First Run
```bash
gmail list
# This will open a browser for OAuth authentication
# Grant permissions and the tool will save tokens for future use
```

## Command Structure

All commands follow the pattern: `gmail <command> [subcommand] [options]`

## Core Commands

### List and Search Messages
```bash
# List recent messages
gmail list
gmail list -n 20  # List 20 messages

# Search messages
gmail search "is:unread"
gmail search "from:example@gmail.com" -n 50
gmail search "has:attachment after:2024/12/1"
gmail search "subject:invoice label:important"
```

### Read Messages
```bash
# Read a message
gmail read MESSAGE_ID

# Different formats
gmail read MESSAGE_ID --format metadata  # Headers only
gmail read MESSAGE_ID --format raw       # Raw email
gmail read MESSAGE_ID --format full      # Full message (default)
```

### Send Messages
```bash
# Simple message
gmail send "user@example.com" "Subject" "Message body"

# With attachments
gmail send "user@example.com" "Report" "Please find attached" -a report.pdf -a data.csv

# Reply to a thread
gmail reply THREAD_ID "user@example.com" "Reply body"

# Forward a message
gmail forward MESSAGE_ID "forward@example.com" -c "FYI, please review"
```

## Draft Management
```bash
# List drafts
gmail draft list

# Create a draft
gmail draft create "to@example.com" "Subject" "Message body"

# Send a draft
gmail draft send DRAFT_ID

# Delete a draft
gmail draft delete DRAFT_ID
```

## Thread Management
```bash
# View entire conversation thread
gmail thread view THREAD_ID

# Reply to a thread
gmail thread reply THREAD_ID "to@example.com" "Reply body"
```

## Attachment Operations
```bash
# List attachments in a message
gmail attachment list MESSAGE_ID

# Download all attachments
gmail attachment download MESSAGE_ID -o ./downloads/

# Search by attachment
gmail attachment search --filename "*.pdf"
gmail attachment search --larger 5000000   # Files > 5MB
gmail attachment search --smaller 100000   # Files < 100KB
```

## Label Management
```bash
# List all labels
gmail label list

# Create a new label
gmail label create "Projects/ClientA"

# Apply label to message
gmail label apply MESSAGE_ID "Projects/ClientA"

# Remove label from message
gmail label remove MESSAGE_ID "Projects/ClientA"
```

## Filter Management
```bash
# List filters
gmail filter list

# Create a filter
gmail filter create --from "newsletter@example.com" --add-label "Newsletters"
gmail filter create --subject "invoice" --add-label "Billing" --remove-label "INBOX"

# Delete a filter
gmail filter delete FILTER_ID
```

## Settings
```bash
# Vacation responder
gmail settings vacation get
gmail settings vacation enable --subject "Out of Office" --body "I'll be back Monday"
gmail settings vacation disable

# List send-as aliases
gmail settings sendas

# List forwarding addresses
gmail settings forwarding
```

## Smart Features
```bash
# Mark messages as important
gmail important mark MESSAGE_ID1 MESSAGE_ID2
gmail important unmark MESSAGE_ID

# Find unsubscribe link
gmail unsubscribe MESSAGE_ID

# Delete/Trash messages
gmail trash MESSAGE_ID              # Move to trash
gmail delete MESSAGE_ID             # Permanent delete (with confirmation)
gmail batch-delete ID1 ID2 ID3      # Delete multiple
```

## Analysis and Export
```bash
# Analyze inbox patterns
gmail analyze                    # Last 30 days
gmail analyze --days 7          # Last 7 days
gmail analyze --json            # Output as JSON

# Export messages
gmail export "is:important" -f json -o important.json
gmail export "from:client@example.com" -f csv -o client_emails.csv
gmail export "label:archive" -f mbox -o archive.mbox --include-body
```

## Advanced Features

### Push Notifications
```bash
# Set up push notifications (requires Pub/Sub topic)
gmail watch "projects/myproject/topics/gmail-push"
gmail watch "projects/myproject/topics/gmail-push" -l INBOX IMPORTANT
```

### Complex Searches
Common search operators:
- `is:unread` - Unread messages
- `from:user@example.com` - From specific sender
- `to:me` - Sent directly to you
- `subject:invoice` - Subject contains word
- `has:attachment` - Messages with attachments
- `filename:pdf` - Specific attachment types
- `after:2024/12/1 before:2024/12/31` - Date range
- `label:work -label:done` - Label combinations
- `larger:10M` - Size filters
- `in:anywhere` - Search all folders

## Output Examples

### Message Display
```
ID: 18d5a2b3c4d5e6f7
From: John Doe <john@example.com>
To: you@gmail.com
Subject: Meeting Tomorrow
Date: Mon, 1 Jan 2025 10:30:00 -0800
Labels: UNREAD, INBOX, IMPORTANT
--------------------------------------------------
```

### Thread Display
```
Thread ID: 18d5a2b3c4d5e6f7
Messages: 3
--------------------------------------------------

Message 1:
  From: John Doe <john@example.com>
  Date: Mon, 1 Jan 2025 10:30:00 -0800
  Subject: Meeting Tomorrow
  Preview: Can we meet tomorrow at 2pm to discuss...

Message 2:
  From: you@gmail.com
  Date: Mon, 1 Jan 2025 11:00:00 -0800
  Subject: Re: Meeting Tomorrow
  Preview: Sure, 2pm works for me. See you then...
```

### Inbox Analysis Output
```
=== Inbox Analysis ===
Total messages: 636
Date range: 30 days

Top 10 Senders:
  john@example.com: 45 messages
  newsletter@company.com: 23 messages
  ...

Top 10 Domains:
  gmail.com: 120 messages
  company.com: 89 messages
  ...

Label Distribution:
  INBOX: 245 messages
  IMPORTANT: 89 messages
  UNREAD: 34 messages
  ...
```

## Configuration

- **Config Directory**: `~/.gmail-cli/`
- **Credentials**: `~/.gmail-cli/credentials.json` (OAuth client config)
- **Token Storage**: `~/.gmail-cli/token.pickle` (saved authentication)

## Error Handling

The tool provides clear error messages for common issues:
- Missing credentials file
- Invalid OAuth tokens
- API quota exceeded
- Network connectivity issues
- Invalid message IDs

## Tips and Tricks

1. **Batch Operations**: Many commands support multiple IDs for efficiency
2. **JSON Output**: Add `--json` to many commands for scripting
3. **Pipe Commands**: Output can be piped to other tools
4. **Search First**: Use search to find messages before operating on them

## Examples

### Daily Email Workflow
```bash
# Check unread messages
gmail search "is:unread" -n 20

# Read specific message
gmail read MESSAGE_ID

# Reply to thread
gmail reply THREAD_ID "sender@example.com" "Thanks for the update"

# Archive by applying label and removing from inbox
gmail label apply MESSAGE_ID "Archive"
gmail label remove MESSAGE_ID "INBOX"
```

### Bulk Operations
```bash
# Find and export client emails
gmail export "from:client@company.com" -f csv -o client_communications.csv

# Clean up old newsletters
gmail search "from:newsletter@* older_than:30d" -n 100
# Review the list, then batch delete if desired

# Find large attachments
gmail attachment search --larger 10000000  # > 10MB
```

### Automation Examples
```bash
# Check for urgent emails
urgent=$(gmail search "is:unread subject:urgent" -n 10)

# Auto-label emails
gmail filter create --from "boss@company.com" --add-label "Priority"

# Export today's emails for backup
gmail export "after:$(date +%Y/%m/%d)" -f mbox -o "backup_$(date +%Y%m%d).mbox"
```

## Security Notes

- OAuth tokens are stored locally with appropriate permissions
- No passwords are ever stored
- Tokens can be revoked through Google Account settings
- Each scope is explicitly requested during authentication

## Rate Limits

- 250 quota units per user per second
- 1 billion quota units per day
- Batch operations help reduce quota usage

## Troubleshooting

1. **Authentication Issues**: Delete `~/.gmail-cli/token.pickle` and re-authenticate
2. **Permission Errors**: Ensure all Gmail API scopes are enabled
3. **Timeout Errors**: The tool uses requests library with proper timeouts
4. **Network Issues**: Check internet connectivity and firewall settings