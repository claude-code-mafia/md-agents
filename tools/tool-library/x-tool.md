# X (Twitter) CLI Tools

## Overview

This document describes the command-line tools available for interacting with X/Twitter in the MD Agents project. These tools are executed through Claude Code's Bash tool and don't require complex server setups.

## Available X/Twitter CLI Tools

### 1. Typefully CLI (Recommended for Posting)

Typefully is a professional tool for creating and scheduling X posts. It's already installed in Claude Code environments.

```bash
# Authentication (one-time setup)
typefully auth

# Create and post immediately
typefully create "Your tweet content"

# Create a thread (use 4 newlines or --threadify)
typefully create "First tweet


Second tweet


Third tweet"

# Schedule a post
typefully create "Scheduled tweet" --schedule "2025-01-07 10:00"
typefully create "Tweet" --schedule next --share

# View your content
typefully list scheduled
typefully list published --json
```

### 2. Grok CLI (For Analysis & Trends)

Grok provides X/Twitter analysis and real-time trending data.

```bash
# Get trending topics
grok trending --category tech
grok trending --json  # For structured output

# Analyze specific posts
grok analyze "https://x.com/user/status/123"

# Sentiment analysis
grok sentiment "Claude Code" --posts 50
```

### 3. Web-Based Search (No API Needed)

For basic searching without authentication:

```bash
# Search X using web scraping
curl -s "https://x.com/search?q=Claude%20Code" | \
  grep -E 'data-testid="tweet"' | \
  head -10

# Or use WebFetch tool in Claude Code
# WebFetch can handle JavaScript-rendered content better
```

## Setting Up Authentication

### For Typefully:
1. Get API key from https://typefully.com (Settings > API & Integrations)
2. Run `typefully auth` and enter your API key
3. Key is stored in `~/.typefully/config.json`

### For Grok:
1. Get xAI API key from https://x.ai
2. Set environment variable: `export GROK_API_KEY=your-key`
3. Or add to `~/.bashrc` for persistence

## Usage Examples

### Finding Claude Code Tips
```bash
# Using Grok to find trending Claude Code content
grok trending --query "Claude Code" --json

# Using web search for recent posts
curl -s "https://x.com/search?q=%22Claude%20Code%22%20tip&src=typed_query&f=live"
```

### Posting a Daily Tip
```bash
# Create and post immediately
typefully create "💡 Claude Code Tip: Did you know you can use 'cc' as a shortcut for 'claude'? Save keystrokes on every command! #ClaudeCode #DevProductivity"

# Schedule for optimal engagement time
typefully create "Your tip here" --schedule "10:00"
```

### Creating a Thread
```bash
typefully create "🧵 5 Claude Code features you might have missed:


1️⃣ Image reading: Claude Code can view images! Just use the Read tool on any PNG/JPG file.


2️⃣ Web search: Get current information with the WebSearch tool - no need to leave your terminal.


3️⃣ Parallel execution: Run multiple tools simultaneously for faster results.


4️⃣ Session management: Your work persists between Claude Code sessions.


5️⃣ Custom aliases: Set up 'cc' as an alias for 'claude' to save typing!"
```

## Best Practices

1. **Rate Limiting**: Add delays between requests to avoid hitting limits
2. **Error Handling**: Always check command exit codes
3. **Content Validation**: Verify tweet length (280 chars) before posting
4. **Scheduling**: Post during peak engagement hours (typically 9-10 AM and 7-9 PM in your audience's timezone)
5. **Threading**: Use 4 newlines to separate tweets in a thread

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify API keys are correctly set
   - Check if keys have proper permissions

2. **Rate Limits**
   - Implement exponential backoff
   - Cache results when possible

3. **Content Formatting**
   - Escape special characters in bash
   - Use quotes around content with spaces

## Example Agent Integration

```markdown
# In your agent markdown file:

## Tools I Use

### X/Twitter Access
I use these CLI tools to interact with X:
- `typefully create` - Post new content
- `grok trending` - Find trending topics
- `curl` with X search - Find specific content

## How I Post

When I need to post to X, I:
1. Format the content (check length, add hashtags)
2. Use `typefully create "content"` to post
3. Save the URL from the response for tracking
```

## Security Notes

- API keys are stored locally in config files
- Never commit API keys to version control
- Use environment variables for sensitive data
- Consider using a dedicated X account for automation