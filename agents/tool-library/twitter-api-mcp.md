# Tool: Twitter API MCP

## Metadata
- Version: 1.0
- Type: external-api
- Category: social-media
- MCP-Server: twitter-api-mcp

## Purpose
Provides access to X (Twitter) API v2 for reading posts, searching content, and publishing tweets. This tool enables agents to interact with the X platform programmatically.

## Installation
```bash
# Install the MCP server
npm install -g @mcp/twitter-api

# Or add to project
npm install @mcp/twitter-api
```

## Configuration
Requires X API credentials:
```json
{
  "twitter-api-mcp": {
    "api_key": "YOUR_API_KEY",
    "api_secret": "YOUR_API_SECRET",
    "access_token": "YOUR_ACCESS_TOKEN",
    "access_token_secret": "YOUR_ACCESS_TOKEN_SECRET"
  }
}
```

## Available Operations

### search_posts
Search for posts matching specific criteria.
```yaml
input:
  query: string (required) - Search query
  max_results: number (optional, default: 10, max: 100)
  start_time: string (optional) - ISO 8601 date
  end_time: string (optional) - ISO 8601 date
  
output:
  posts: array of post objects
  meta: result metadata
```

### get_post
Retrieve a specific post by ID.
```yaml
input:
  post_id: string (required)
  
output:
  post: post object with full details
```

### create_post
Publish a new post to X.
```yaml
input:
  text: string (required, max: 280 chars)
  reply_to: string (optional) - Post ID to reply to
  
output:
  post: created post object
  url: direct link to the post
```

### get_user_posts
Get recent posts from a specific user.
```yaml
input:
  username: string (required)
  max_results: number (optional, default: 10)
  exclude_replies: boolean (optional, default: false)
  
output:
  posts: array of post objects
```

## Rate Limits
- Search: 180 requests per 15 minutes
- Post creation: 300 per 3 hours
- User timeline: 900 per 15 minutes

## Natural Language Usage

When agents use this tool, they can express intentions like:
- "Search for recent posts about Claude Code"
- "Post this tip to my timeline"
- "Get the last 20 posts from @anthropic"
- "Find posts with #ClaudeCode from the last 24 hours"

## Error Handling
Common errors:
- `401`: Invalid credentials
- `429`: Rate limit exceeded
- `403`: Forbidden (check permissions)
- `400`: Invalid request (check parameters)

## Best Practices
1. Cache search results to avoid rate limits
2. Include error handling for all operations
3. Respect rate limits with backoff strategies
4. Always validate post length before sending
5. Store post IDs for tracking and threading

## Example Agent Usage
```markdown
## Tools
### twitter-api-mcp
- Description: Access X/Twitter for searching and posting
- Operations: search_posts, create_post
- Usage: Search for Claude Code tips and post curated content
```