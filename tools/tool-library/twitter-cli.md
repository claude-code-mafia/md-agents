# Tool: Twitter/X CLI Tools

## Purpose
Provides command-line access to X (Twitter) for searching content, reading timelines, and publishing posts. Multiple CLI tools are available depending on your needs.

## Available CLI Tools

### 1. Typefully CLI (Recommended)
A professional tool for creating and scheduling X posts.

```bash
# Installation (if not already installed)
npm install -g typefully-cli

# Authentication (first time)
typefully auth

# Basic usage
typefully create "Your tweet content"
typefully create "Long content..." --threadify
typefully create "Tweet" --schedule "2025-01-07 10:00"
typefully list scheduled
```

### 2. Grok CLI
For X/Twitter analysis and trending topics (requires xAI API key).

```bash
# Basic usage
grok trending --category tech
grok analyze "https://x.com/user/status/123"
grok sentiment "Apple Vision Pro" --posts 100

# For JSON output (better for agents)
grok trending --json
```

### 3. Custom X Search (via web scraping)
For searching without API access:

```bash
# Using curl and web parsing
curl -s "https://x.com/search?q=Claude%20Code&src=typed_query" | \
  grep -oP '(?<=<span>)[^<]+(?=</span>)' | \
  head -20
```

## Usage in Agents

When agents use these tools, they express intentions like:
- "Search for recent posts about Claude Code"
- "Post this tip to X/Twitter"
- "Get trending topics in tech"
- "Find posts with #ClaudeCode from the last 24 hours"

## Authentication

Each tool has its own authentication method:
- **Typefully**: API key from Settings > API & Integrations
- **Grok**: xAI API key as environment variable
- **Web scraping**: No auth needed (but limited functionality)

## Rate Limits
- Typefully: Depends on your plan
- Grok: Based on xAI API limits
- Web scraping: Be respectful, add delays between requests

## Best Practices
1. Use Typefully for posting (most reliable)
2. Use Grok for analysis and trends
3. Cache search results to avoid rate limits
4. Always validate post length before sending
5. Store post IDs/URLs for tracking

## Example Agent Usage
```markdown
## Tools
### twitter-cli
- Description: Access X/Twitter for searching and posting
- Commands: typefully create, grok trending
- Usage: Search for Claude Code tips and post curated content
```