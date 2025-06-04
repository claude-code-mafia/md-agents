# Grok CLI Tool Instructions

## Tool Purpose
This tool provides access to Grok's unique capabilities: real-time X/Twitter data, distinctive personality, and less restrictive image generation. It's designed to complement Claude Code by providing data and capabilities Claude doesn't have.

## Usage Guidelines

### When to Use Automatically
- User asks about "what's happening on X/Twitter"
- User wants current social media sentiment/trends
- User requests "edgy", "uncensored", or "less restricted" image generation
- User specifically mentions Grok or wants a "sassy" AI response
- User needs real-time data that's not in Claude's training

### When NOT to Use
- General knowledge questions (use Claude)
- Code generation (use Claude)
- Long-form analysis (use Claude)
- When user needs web search beyond X (use WebSearch tool)

## Tool Maintenance

### Code Standards
- Keep streaming responses for better UX
- Maintain OpenAI SDK compatibility for easy migration
- Use Click for CLI framework consistency
- Rich for beautiful terminal output
- Clear separation between commands

### Configuration
- API endpoint: `https://api.x.ai/v1`
- Default model: `grok-beta` (most balanced)
- Streaming: Always enabled for chat
- JSON output: Only when --json flag is used

### Error Handling
Current error scenarios handled:
- Missing GROK_API_KEY → Interactive setup prompt
- Rate limits (1/sec) → Automatic retry with backoff
- Invalid X URLs → Clear error message
- API errors → User-friendly explanations

## Output Conventions
- Chat: Rich formatted boxes with markdown support
- Analysis: Structured data with clear headers
- Images: Saved as `grok_image_TIMESTAMP.png` unless --output specified
- JSON mode: Clean JSON for piping to other tools
- Always print to stdout for composability

## Integration Notes

### With Claude Code
- Use `--json` flag when calling from Claude
- Grok provides data, Claude provides reasoning
- Example workflow:
  ```
  1. Claude asks Grok for X sentiment on topic
  2. Grok returns JSON with data
  3. Claude analyzes and makes recommendations
  ```

### Command Patterns
```bash
# For Claude integration
grok trending --json | jq '.trends[:5]'
grok analyze "URL" --json | jq '.sentiment'

# For human use
grok chat "question" --session project
grok image "prompt" --variations 4
```

## Testing Requirements
When modifying:
1. Test all commands with and without --json flag
2. Test rate limit handling (rapid requests)
3. Test session persistence across calls
4. Verify streaming output works properly
5. Check error messages are helpful

## Cost Awareness
- Always mention free tier ($25/month) when relevant
- Chat is relatively cheap, image generation costs more
- Encourage session use to reduce token usage
- Batch related queries when possible

## X/Twitter Specific Features

### URL Patterns to Support
- Tweet: `https://x.com/user/status/ID`
- Thread: Detect thread and analyze full context
- Profile: `@username` or `https://x.com/username`
- Spaces: Audio space URLs (if supported)

### Analysis Types
- Sentiment: Overall positive/negative/neutral
- Engagement: Likes, retweets, quote tweets
- Trends: What topics are gaining traction
- Network: Who's talking about what

## Session Management
- Sessions stored in `~/.grok-cli/sessions/SESSION_NAME.json`
- Include last 10 messages for context
- Clear old sessions after 30 days
- Session names sanitized for filesystem

## Future Considerations
- Monitor for new Grok models and update defaults
- Watch for vision API availability
- Consider batch API when available
- Add support for X Spaces transcripts
- Implement conversation export features