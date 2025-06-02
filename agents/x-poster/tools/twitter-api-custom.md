# Tool: Twitter API (X Poster Team Configuration)

## Metadata
- Based-On: twitter-api-mcp
- Team: x-poster
- Customized: 2025-01-30

## Team-Specific Configuration

This is the X Poster team's customized configuration of the twitter-api-mcp tool.

## Search Queries

Our team uses these specific search patterns:
```
"Claude Code" tip OR trick OR hack
"@anthropic" "Claude Code"
"#ClaudeCode" -filter:replies
"cc command" workflow
"claude-code" "did you know"
from:anthropic "Claude Code"
```

## Posting Rules

1. **Character Limits**:
   - Leave 30 char buffer for X's link expansion
   - Max 250 chars to ensure space for edits

2. **Required Elements**:
   - One of our hook phrases
   - The actual tip
   - Attribution to original author
   - At least #ClaudeCode hashtag

3. **Forbidden Content**:
   - No posting about bugs/issues
   - No unverified claims
   - No promotional content
   - No personal opinions

## Rate Limit Strategy

For our daily posting:
- Search: Max 5 queries per run
- Post: 1 tweet per day max
- User lookups: Only if needed for attribution

## Error Recovery

If posting fails:
1. Log the attempt with timestamp
2. DO NOT retry automatically
3. Save formatted tweet to `failed-posts.md`
4. Alert user to review and manually post

## Search Filtering

When TipFinder uses search_posts:
```yaml
query: "Claude Code" tip OR trick
max_results: 50  # Cast wide net
start_time: 48 hours ago
exclude:
  - Low engagement (<5 likes)
  - Replies to threads
  - Quote tweets without context
```

## Post Formatting

When TweetPoster uses create_post:
```yaml
text: |
  {hook_phrase} {tip_text}
  
  {attribution} {hashtags}
  
validate:
  - Total length < 250
  - Has attribution
  - Has #ClaudeCode
```

## Monitoring

Track in log.md:
- Search queries used
- Number of results found
- Post selected and why
- Final character count
- Engagement (check manually later)