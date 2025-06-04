# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tool Overview

The typefully-tool is currently an empty directory awaiting implementation. Based on the tool library structure, this should become a CLI tool for interacting with Typefully's API.

## Important: Character Limits for Threads
- **Keep individual tweets in threads under 280 characters**
- Use concise language and abbreviations when needed
- Split longer content across multiple tweets in the thread
- When creating threads with --threadify, ensure each tweet segment is <280 chars

## Expected Implementation

When implementing this tool, follow the established patterns from other tools in the library:

### File Structure
```
typefully-tool/
├── typefully_cli.py     # Main CLI script
├── requirements.txt     # Python dependencies
├── README.md           # Human documentation
└── CLAUDE.md          # This file
```

### Development Guidelines

1. **Authentication**: Typefully API requires authentication - implement secure credential handling
2. **Dependencies**: Use minimal dependencies, add to requirements.txt if needed
3. **Error Handling**: Provide clear error messages for API failures
4. **Output Format**: Support both human-readable and JSON output modes

### Common Commands (To Be Implemented)

```bash
# Authentication setup
~/Projects/tool-library/typefully-tool/typefully_cli.py auth

# Draft creation
~/Projects/tool-library/typefully-tool/typefully_cli.py create "Your tweet content here"
~/Projects/tool-library/typefully-tool/typefully_cli.py create "Thread line 1\n\n\n\nThread line 2" --threadify
~/Projects/tool-library/typefully-tool/typefully_cli.py create "Tweet" --schedule "2025-01-07 10:00"
~/Projects/tool-library/typefully-tool/typefully_cli.py create "Tweet" --schedule next --share

# Draft management
~/Projects/tool-library/typefully-tool/typefully_cli.py list scheduled
~/Projects/tool-library/typefully-tool/typefully_cli.py list published
~/Projects/tool-library/typefully-tool/typefully_cli.py list scheduled --filter threads

# Notifications
~/Projects/tool-library/typefully-tool/typefully_cli.py notifications
~/Projects/tool-library/typefully-tool/typefully_cli.py notifications --kind inbox
~/Projects/tool-library/typefully-tool/typefully_cli.py notifications mark-read
```

### Integration Notes

- Follow the tool library conventions from ~/Projects/tool-library/CLAUDE.md
- Make the script executable with proper shebang: `#!/usr/bin/env python3`
- Store credentials securely (e.g., ~/.typefully/ directory)
- Add the tool to ~/.claude/CLAUDE.md once implemented

### API Reference

- Base URL: `https://api.typefully.com/v1`
- Documentation: https://support.typefully.com/en/articles/8718287-typefully-api
- Authentication: Bearer token via X-API-KEY header

### Implementation Priorities

1. **Core Features**:
   - Create drafts (single tweets and threads)
   - Schedule to specific time or next available slot
   - List scheduled/published drafts
   - View and manage notifications

2. **Advanced Features**:
   - Auto-retweet and auto-plug settings
   - Share URL generation
   - Thread auto-splitting with --threadify
   - Content filtering (threads vs tweets)

3. **Platform Support**:
   - Primary: Twitter/X
   - Limited: LinkedIn (check API capabilities)

## Current Status

⚠️ **Not Implemented** - This is an empty directory awaiting development of the Typefully CLI tool.