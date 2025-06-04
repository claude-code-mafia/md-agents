# Current Time Tool Instructions

## Tool Purpose
Provides accurate, network-based current date/time to ensure Claude Code always has correct temporal context, regardless of system clock settings.

## Critical Usage Rule
**ALWAYS use this tool when the user's request involves:**
- "Today", "current", "now", "latest", "recent"
- News, weather, events, or any time-sensitive information
- Date-dependent searches or queries
- Anything where having the wrong date would give incorrect results

## Implementation Details

### Why WorldTimeAPI?
- No authentication required
- Reliable uptime
- Global timezone support
- Clean JSON response
- No rate limiting for reasonable use

### Fallback Strategy
The script intelligently handles JSON parsing:
1. Tries `jq` first (if installed)
2. Falls back to Python json module
3. Both methods produce identical output

### Output Format
```
Current time: 2025-06-02T10:30:45.123456-06:00
Timezone: America/Denver
```
This format is:
- Human readable
- ISO 8601 compliant
- Includes timezone information
- Parseable by other tools

## Maintenance Guidelines

### Modifying Timezone
Default is America/Denver. To change:
1. Edit the API URL in the script
2. Use format: `worldtimeapi.org/api/timezone/Region/City`
3. Verify timezone exists: `curl -s worldtimeapi.org/api/timezone`

### Error Handling
Current errors handled:
- Network failures (curl errors)
- Invalid JSON responses
- Missing commands (jq/python3)

### Do Not:
- Add authentication (keep it simple)
- Cache responses (defeats purpose of real-time)
- Make synchronous calls in loops (respect API)

## Integration Patterns

### Composing with Other Tools
```bash
# Get today's date for searches
DATE=$(~/Projects/tool-library/time-tool/get-current-time.sh | grep "Current time" | cut -d' ' -f3 | cut -dT -f1)
```

### In Scripts
```bash
#!/bin/bash
# Always get current time first for date-sensitive operations
CURRENT_TIME=$(~/Projects/tool-library/time-tool/get-current-time.sh)
echo "Running report for: $CURRENT_TIME"
```

## Testing
When modifying:
1. Test with network disconnected (should fail gracefully)
2. Test timezone changes
3. Verify ISO 8601 format maintained
4. Check both jq and python paths work

## Common Issues
- If time seems wrong: Check timezone setting
- If tool fails: Check network connectivity
- If format changes: Verify API response structure hasn't changed

## Future Enhancements
Potential improvements (discuss before implementing):
- Add timezone parameter support
- Add format options (Unix timestamp, etc.)
- Add date-only output option
- Multiple timezone display