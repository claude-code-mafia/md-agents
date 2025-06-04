# Cal.com CLI - AI Instructions

## When to Use This Tool

Use the Cal.com CLI when:
- User mentions "Cal.com", "cal.com", or "scheduling"
- Managing bookings, appointments, or calendar events
- Creating or updating event types
- Checking availability or schedules
- Cancelling or rescheduling meetings
- Setting up scheduling links

## Key Triggers
- "Check my Cal.com bookings"
- "Create a new event type on Cal.com"
- "Cancel my meeting"
- "What's on my Cal.com calendar"
- "Set up a scheduling link"

## Usage Patterns

### For Automation/Integration
```bash
# Always use --json for parsing
cal-com bookings list --json
cal-com events list --json
cal-com users me --json
```

### Authentication Required
The tool requires authentication before use:
```bash
cal-com auth
```

User must provide API key from Cal.com Settings > Security > API Keys.

## Common Workflows

### 1. List Today's Bookings
```bash
cal-com bookings list --status upcoming --json | jq '.[] | select(.startTime | startswith("YYYY-MM-DD"))'
```

### 2. Create Standard Event Types
```bash
# 30-minute call
cal-com events create "Quick Call" quick-call 30

# 1-hour meeting
cal-com events create "Strategy Session" strategy-session 60
```

### 3. Bulk Operations
```bash
# Cancel all bookings for an event type
cal-com bookings list --json | jq '.[] | select(.eventTypeId == ID) | .id' | xargs -I {} cal-com bookings cancel {}
```

## Integration Notes

### Output Parsing
- All commands support `--json` flag for structured output
- Booking objects include: id, title, startTime, endTime, status, attendees
- Event type objects include: id, title, slug, length, description, hidden
- Use `jq` for filtering and transforming JSON output

### Error Handling
- Check for authentication errors (no API key configured)
- API errors include detailed messages in stderr
- Network failures will show connection errors

### Time Zones
- All times are returned in ISO 8601 format
- User's default timezone is shown in `cal-com users me`
- Consider timezone when filtering by date

## Best Practices

1. **Always check authentication first** - Run `cal-com users me` to verify setup
2. **Use JSON output for scripts** - Add `--json` for reliable parsing
3. **Handle pagination** - Use `--limit` parameter for large result sets
4. **Respect rate limits** - Cal.com API has rate limiting; batch operations carefully

## Chaining with Other Tools

```bash
# Send email about upcoming bookings
cal-com bookings list --status upcoming --json | \
  jq -r '.[] | "Meeting: \(.title) at \(.startTime)"' | \
  gmail send "me@example.com" "Today's Schedule" -

# Create social media post about availability
cal-com events list --json | \
  jq -r '.[] | select(.hidden == false) | "Book a \(.title): https://cal.com/username/\(.slug)"' | \
  head -1 | \
  typefully create -
```

## Security Considerations

- API key is stored in `~/.cal-com/config.json`
- Never share or expose the API key
- Use read-only operations when possible
- Be cautious with delete operations