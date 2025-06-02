# X (Twitter) MCP Tool - mcp-twikit

## Overview

This document describes how to set up and use mcp-twikit as an MCP server within the claude-agents project. Unlike the typical Claude Desktop configuration, we're running this as a project-based MCP server that can be used by Claude Code.

## What is mcp-twikit?

mcp-twikit is a Model Context Protocol (MCP) server that enables AI assistants to interact with X/Twitter without requiring expensive API keys. It uses the Twikit library for authentication and interaction.

### Key Features
- **No API Key Required**: Uses username/password authentication
- **Free to Use**: Avoids Twitter's expensive API pricing ($200+/month minimum)
- **Search Functionality**: Search tweets with advanced query operators
- **Timeline Access**: Retrieve home timeline tweets
- **Project-Based**: Runs within your project, not globally

## Setup Instructions

### 1. Project Structure

Create the following structure in the project:

```
claude-agents/
├── mcp-servers/
│   ├── twitter/
│   │   ├── server.py
│   │   └── requirements.txt
│   └── .env
└── .claude.json (or claude_config.json)
```

### 2. Install Dependencies

First, create a Python virtual environment:

```bash
cd mcp-servers/twitter
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install mcp-twikit:

```bash
pip install git+https://github.com/adhikasp/mcp-twikit
```

### 3. Create Wrapper Script

Create `mcp-servers/twitter/server.py`:

```python
#!/usr/bin/env python
import os
import sys
import subprocess

# Set environment variables from .env file if needed
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

if __name__ == "__main__":
    load_env()
    
    # Run mcp-twikit
    subprocess.run([
        sys.executable, 
        "-m", 
        "mcp_twikit"
    ])
```

### 4. Configure Credentials

Create `mcp-servers/.env`:

```env
TWITTER_USERNAME=@your_username
TWITTER_EMAIL=your_email@example.com
TWITTER_PASSWORD=your_password
```

**Security Note**: Add `.env` to `.gitignore` to prevent committing credentials.

### 5. Configure Claude Code

Update your Claude Code configuration to include the MCP server. For project-specific configuration:

```json
{
  "projects": {
    "/Users/pete/Projects/claude-agents": {
      "mcpServers": {
        "twitter": {
          "command": "python",
          "args": ["./mcp-servers/twitter/server.py"],
          "env": {
            "PYTHONPATH": "./mcp-servers/twitter"
          }
        }
      }
    }
  }
}
```

Alternatively, create a `.mcp.json` in the project root:

```json
{
  "mcpServers": {
    "twitter": {
      "command": "python",
      "args": ["./mcp-servers/twitter/server.py"]
    }
  }
}
```

## Usage

Once configured, Claude Code will have access to the following tools:

### 1. search_twitter

Search for tweets using Twitter's search syntax:

```
Parameters:
- query: Search query (supports operators like "to:username", "from:username")
- count: Number of tweets to retrieve
- sort_by: Sorting method (e.g., "Latest")

Example queries:
- "to:@IndiHomeCare" - Tweets directed at a specific account
- "from:@elonmusk tesla" - Tweets from a user containing "tesla"
- "#AI lang:en" - English tweets with #AI hashtag
```

### 2. get_timeline

Retrieve tweets from the authenticated user's home timeline:

```
Parameters: None
Returns: Recent tweets from accounts the user follows
```

## Example Use Cases

### Customer Sentiment Analysis
```
Search for recent tweets directed at competitor accounts to analyze customer feedback:
- query: "to:@CompetitorA OR to:@CompetitorB"
- count: 50
- sort_by: "Latest"
```

### Industry Monitoring
```
Track discussions about specific topics:
- query: "#AI #MachineLearning -filter:retweets"
- count: 100
- sort_by: "Latest"
```

### Personal Timeline Summary
```
Get a summary of what's happening on your timeline without opening Twitter
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify credentials in `.env` file
   - Check if account requires 2FA (may not work with mcp-twikit)

2. **Server Not Starting**
   - Ensure Python path is correct
   - Check if virtual environment is activated
   - Verify mcp-twikit is installed

3. **MCP Connection Issues**
   - Run Claude Code with `--mcp-debug` flag
   - Check server.py has execute permissions
   - Verify paths in configuration are correct

### Debug Mode

To see MCP communication:
```bash
claude --mcp-debug
```

## Alternatives

If mcp-twikit doesn't meet your needs:

1. **x-mcp**: Another Twikit-based server with FastMCP
2. **twitter-mcp**: Requires API keys but offers more features
3. **Custom Implementation**: Build your own MCP server using the Twitter API

## Security Considerations

- Store credentials securely (use environment variables or secret management)
- Never commit `.env` files to version control
- Consider using a dedicated Twitter account for automation
- Be aware of Twitter's rate limits and terms of service

## Resources

- [mcp-twikit GitHub](https://github.com/adhikasp/mcp-twikit)
- [Model Context Protocol Docs](https://modelcontextprotocol.io)
- [Twikit Library](https://github.com/d60/twikit)
- [Twitter Search Operators](https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators)