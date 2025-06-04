# Google Calendar CLI - AI Instructions

## When to Use This Tool

### Automatic Usage Triggers
- User mentions "calendar", "schedule", "meeting", "event", "appointment"
- Requests about availability, free time, busy times
- Planning or scheduling tasks
- Time management queries
- Recurring events or routines

### Primary Use Cases
1. **Scheduling**: Creating and managing events
2. **Availability**: Checking free/busy times
3. **Planning**: Finding meeting slots with multiple people
4. **Organization**: Managing multiple calendars
5. **Analysis**: Understanding time usage patterns

## Integration Patterns

### Quick Scheduling Workflow
```bash
# Check availability first
gcal busy "tomorrow" "tomorrow"

# Then create event
gcal create "Meeting" "tomorrow 14:00" -a attendee@example.com
```

### Meeting Coordination
```bash
# Find available time for multiple people
gcal-advanced find-times 60 -a person1@example.com person2@example.com

# Create event at chosen time
gcal create "Team Sync" "2025-01-15 10:00" -a person1@example.com person2@example.com
```

### Time Analysis
```bash
# Get calendar statistics
gcal-advanced analyze --json

# Export for detailed analysis
gcal-advanced export-csv
```

## Command Selection Guide

### Basic Operations
- **list**: View upcoming events, search calendar
- **create**: Add new events with various options
- **quick**: Natural language event creation
- **update**: Modify existing events
- **delete**: Remove events

### Advanced Operations
- **analyze**: Get insights about calendar usage
- **find-times**: Coordinate meetings with multiple people
- **batch-create**: Import multiple events
- **sync**: Mirror events between calendars
- **export-csv**: Extract data for analysis

## Natural Language Processing

The `quick` command understands phrases like:
- "Meeting tomorrow at 3pm"
- "Lunch with John next Friday"
- "Weekly standup every Monday at 9am"
- "Dentist appointment June 15th 2-3pm"

## Output Handling

### Human-Readable (Default)
- Formatted event displays with times, locations, attendees
- Clear success/error messages
- Interactive confirmations for deletions

### JSON Output (--json flag)
- Structured data for parsing
- Suitable for automation and integration
- Can be piped to jq for filtering

## Error Handling Patterns

### Authentication Errors
- First-time setup requires manual OAuth flow
- Token refresh happens automatically
- If auth fails, suggest deleting token.pickle

### Permission Errors
- Check calendar access rights
- Verify calendar ID is correct
- Ensure API is enabled in Google Cloud

### Quota Errors
- Implement delays between bulk operations
- Use batch commands when available
- Respect Google Calendar API limits

## Best Practices

### Event Creation
1. Always include time zones for clarity
2. Use descriptive summaries
3. Add reminders for important events
4. Include location for in-person meetings
5. Add attendees for collaborative events

### Calendar Management
1. Use calendar IDs consistently
2. Implement prefixes for synced events
3. Regular cleanup of old events
4. Export backups periodically

### Time Coordination
1. Check free/busy before scheduling
2. Consider working hours constraints
3. Allow buffer time between meetings
4. Respect attendee time zones

## Integration Examples

### With Current Time Tool
```bash
# Get current time
current-time

# Schedule event 1 hour from now
gcal create "Quick Call" "2025-01-06 15:00" -e "2025-01-06 15:30"
```

### With Task Management
```bash
# After completing a task, schedule follow-up
gcal create "Review Project Results" "next Monday 10am"
```

### With Email (Gmail CLI)
```bash
# Check email for meeting requests
gmail list -q "meeting invitation"

# Create calendar event based on email
gcal quick "Strategy meeting Friday 2pm with Sarah"
```

## Common Automation Patterns

### Daily Schedule Email
```bash
# Get tomorrow's schedule
gcal list --from "tomorrow" --to "tomorrow" --json > schedule.json

# Process and email (integrate with gmail tool)
```

### Meeting Prep Automation
```bash
# Find all meetings for the day
gcal list --from "today" --to "today" --json | \
  jq '.[] | select(.attendees) | {summary, start, attendees}'
```

### Calendar Cleanup
```bash
# Regular cleanup of old events
gcal-advanced cleanup -d 365  # Remove events older than 1 year
```

## Security Considerations

### Credentials
- OAuth tokens stored in ~/.gcal-cli/token.pickle
- Never share credentials.json or token files
- Tokens can be revoked via Google Account settings

### Privacy
- Be cautious with calendar data in scripts
- Use calendar-specific access when possible
- Consider privacy when syncing calendars

### Permissions
- Tool requests full calendar access
- Review permissions in Google Account settings
- Use read-only access where appropriate

## Debugging Tips

### Verbose Output
Add error handling in scripts:
```bash
if ! gcal create "Meeting" "tomorrow 2pm"; then
    echo "Failed to create event"
    exit 1
fi
```

### Check Authentication
```bash
# Verify authentication is working
gcal list -n 1 || echo "Authentication failed"
```

### Calendar Access
```bash
# List all accessible calendars
gcal calendars list
```

## Performance Optimization

### Batch Operations
- Use batch-create for multiple events
- Minimize API calls with appropriate filters
- Cache calendar IDs and frequently used data

### Query Optimization
- Use specific date ranges
- Limit results with -n flag
- Filter server-side with search queries

### Rate Limiting
- Default delay between operations
- Increase delay for bulk operations
- Monitor quota usage in Google Cloud Console