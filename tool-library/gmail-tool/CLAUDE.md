# Gmail CLI Tool Instructions

## Tool Maintenance

### Authentication Flow
- The tool uses OAuth 2.0 with local token storage
- Tokens are stored in `~/.gmail-cli/token.pickle`
- If token refresh fails, delete the token file and re-authenticate
- Credentials.json must be an "installed" (desktop) type, not "web"

### Error Handling Guidelines
- Always check for HttpError exceptions from the Gmail API
- Handle 401 (auth), 403 (permission), 429 (rate limit) specifically
- Implement exponential backoff for rate limit errors
- Log API errors with full context for debugging

### Testing Requirements
- Test with different Gmail account types (personal, Workspace)
- Verify attachment handling with various file types
- Test search queries with complex filters
- Ensure batch operations handle partial failures

### Version Compatibility
- Requires Python 3.6+ (uses f-strings)
- Gmail API v1 (check for deprecations)
- OAuth 2.0 scopes may change - monitor Gmail API announcements

## Usage Patterns

### When to Use Automatically
- When user asks about "email", "gmail", "messages" - suggest using this tool
- For bulk operations (delete old emails, apply labels)
- Setting up automated email workflows
- Searching through email history programmatically

### Parameter Conventions
- Message IDs are case-sensitive strings
- Labels can be user-created or system (INBOX, SENT, TRASH)
- Search queries follow Gmail search syntax exactly
- Dates in queries use YYYY/MM/DD format

### Output Handling
- Metadata format is best for listing/viewing
- Full format needed for parsing message body
- Raw format for email migration/backup
- JSON output can be piped to jq for processing

## Integration

### With Other Tools
- Can pipe message IDs to other commands
- Export raw messages for processing
- Use with cron for scheduled email tasks
- Combine with notification systems for alerts

### Data Flow
```
Credentials.json → OAuth Flow → Token.pickle → API Calls → JSON Response
```

### Common Integrations
```bash
# Archive old messages
./gmail_cli.py list -q "before:2024/1/1" -n 100 | grep "ID:" | cut -d' ' -f2 | xargs ./gmail_cli.py batch-delete

# Export emails to files
for id in $(./gmail_cli.py list -q "from:important@example.com" | grep "ID:" | cut -d' ' -f2); do
    ./gmail_cli.py read $id --format raw > "email_$id.eml"
done

# Monitor for new messages
watch -n 60 './gmail_cli.py list -q "is:unread" -n 5'
```

## Advanced Features

### Batch Operations
- Use batch endpoints when modifying multiple messages
- Batch delete is more efficient than individual deletes
- Group label operations to reduce API calls

### Push Notifications Setup
1. Create a Pub/Sub topic in Google Cloud Console
2. Grant gmail-api-push@system.gserviceaccount.com Pub/Sub Publisher role
3. Use the watch command with topic name
4. Renew watch before expiration (7 days)

### Filter Creation (Future)
```python
# Example filter structure
{
    "criteria": {
        "from": "notifications@example.com",
        "hasAttachment": true
    },
    "action": {
        "addLabelIds": ["Label_123"],
        "removeLabelIds": ["INBOX"],
        "forward": "archive@example.com"
    }
}
```

## Security Considerations

### Token Storage
- Token file contains refresh token - protect it
- Consider encrypting token.pickle at rest
- Implement token rotation if compromised

### Scope Minimization
- Tool requests all scopes for full functionality
- For production, consider minimal scope sets
- Different commands could use different scopes

### Audit Logging
- Consider logging all delete operations
- Track authentication events
- Monitor for unusual access patterns

## Performance Optimization

### Caching Strategy
- Cache label list (changes infrequently)
- Store message metadata locally for offline access
- Implement ETag support for conditional requests

### Quota Management
- Batch operations use less quota
- Metadata requests are cheaper than full
- Implement backoff for 429 errors
- Monitor daily quota usage

### Parallel Processing
- Can parallelize message fetching
- Use thread pool for attachment downloads
- Batch API supports up to 1000 operations

## Troubleshooting

### Common Issues
1. **"Credentials not found"**: Ensure credentials.json is in ~/.gmail-cli/
2. **"Invalid grant"**: Token expired, delete token.pickle
3. **"Quota exceeded"**: Implement exponential backoff
4. **"Label not found"**: Labels are case-sensitive

### Debug Mode
Add verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### API Explorer
Test queries at: https://developers.google.com/gmail/api/reference

## Future Development

### Planned Enhancements
- Interactive TUI with message threading
- Smart reply suggestions
- Email templates with variables
- Scheduled sending
- Undo send functionality
- S/MIME support

### Architecture Considerations
- Consider moving to async for better performance
- Implement connection pooling
- Add Redis cache for frequently accessed data
- Create plugin system for extensions