# Typefully CLI Tool

A command-line interface for Typefully's API to create, schedule, and manage Twitter/X content.

## Purpose

This tool allows you to:
- Create and schedule tweets/threads from the command line
- View scheduled and published drafts
- Manage notifications
- Integrate Typefully into automated workflows

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up authentication:
   ```bash
   ./typefully_cli.py auth
   ```

## Usage

### Authentication
```bash
# Set up API key (interactive)
./typefully_cli.py auth

# Or set environment variable
export TYPEFULLY_API_KEY="your-api-key"
```

### Creating Content
```bash
# Create a simple tweet
./typefully_cli.py create "Hello from the CLI!"

# Create a thread (use 4 newlines to split)
./typefully_cli.py create "First tweet


Second tweet in thread"

# Schedule for specific time
./typefully_cli.py create "Scheduled tweet" --schedule "2025-01-07 10:00"

# Schedule to next available slot
./typefully_cli.py create "Auto-scheduled tweet" --schedule next

# Create with auto-retweet enabled
./typefully_cli.py create "Important announcement" --auto-retweet

# Generate share URL
./typefully_cli.py create "Check this out" --share
```

### Viewing Drafts
```bash
# List scheduled drafts
./typefully_cli.py list scheduled

# List published drafts
./typefully_cli.py list published

# Filter by content type
./typefully_cli.py list scheduled --filter threads
./typefully_cli.py list scheduled --filter tweets
```

### Managing Notifications
```bash
# View all notifications
./typefully_cli.py notifications

# View inbox notifications only
./typefully_cli.py notifications --kind inbox

# View activity notifications
./typefully_cli.py notifications --kind activity

# Mark all as read
./typefully_cli.py notifications mark-read
```

### Output Formats
```bash
# Default human-readable output
./typefully_cli.py list scheduled

# JSON output for scripting
./typefully_cli.py list scheduled --json
```

## Configuration

The tool stores configuration in `~/.typefully/`:
- `config.json` - API key and settings
- `cache/` - Temporary data

## API Key

Get your API key from Typefully:
1. Log in to [Typefully](https://typefully.com)
2. Go to Settings > API & Integrations
3. Generate or copy your API key

## Technical Details

- **API Base URL**: https://api.typefully.com/v1
- **Rate Limits**: Follow Twitter/X automation rules
- **Supported Platforms**: Twitter/X (primary), LinkedIn (limited)
- **Dependencies**: Python 3.8+, requests, click

## Examples

### Schedule a daily tweet
```bash
# Create and schedule to next slot
./typefully_cli.py create "Daily wisdom: Stay curious! 🌟" --schedule next
```

### Create a thread from a file
```bash
# Thread with proper formatting
echo -e "🧵 Let's talk about CLI tools\n\n\n\n1/ They save time\n\n\n\n2/ They enable automation" | ./typefully_cli.py create --stdin
```

### Check what's scheduled
```bash
# See upcoming tweets
./typefully_cli.py list scheduled --limit 10
```

## Error Handling

The tool provides clear error messages:
- Invalid API key: Prompts to run `auth` command
- Network errors: Suggests checking connection
- API errors: Shows Typefully's error message

## Security

- API keys are stored in `~/.typefully/config.json` with restricted permissions
- Never commit API keys to version control
- Use environment variables for CI/CD: `TYPEFULLY_API_KEY`