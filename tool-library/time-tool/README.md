# Current Time Tool

A simple, accurate network-based time retrieval tool that uses WorldTimeAPI.

## Purpose
Provides accurate current date and time from a reliable network source, ensuring Claude Code always has the correct date/time regardless of system clock settings.

## Usage
```bash
~/Projects/tool-library/time-tool/get-current-time.sh
```

## Output Example
```
Current time: 2025-06-02T10:30:45.123456-06:00
Timezone: America/Denver
```

## Features
- Network-based time (always accurate)
- No dependencies (uses curl and python3, both pre-installed on macOS)
- No sudo required
- Returns timezone-aware ISO 8601 formatted datetime
- Fallback between jq and python for JSON parsing

## When to Use
- Getting current date/time for any task
- News searches ("today's news")
- Time-sensitive queries
- Any task requiring accurate temporal context

## Configuration
Edit the script to change timezone by modifying the API endpoint:
```bash
# Default: America/Denver
curl -s worldtimeapi.org/api/timezone/America/Denver

# Change to any valid timezone:
curl -s worldtimeapi.org/api/timezone/America/New_York
curl -s worldtimeapi.org/api/timezone/Europe/London
curl -s worldtimeapi.org/api/timezone/Asia/Tokyo
```

## Available Timezones
Get full list: `curl -s worldtimeapi.org/api/timezone`

## Technical Details
- API: WorldTimeAPI (http://worldtimeapi.org)
- Protocol: HTTP/HTTPS
- Format: JSON response
- Rate limits: Reasonable use (no authentication required)