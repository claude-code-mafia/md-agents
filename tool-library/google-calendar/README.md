# Google Calendar CLI

A unified command-line interface for Google Calendar with comprehensive event management, scheduling, and analysis features.

## Installation

```bash
./install-tool.sh google-calendar
```

## Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google Calendar API
3. Create OAuth 2.0 credentials (Desktop application)
4. Download `credentials.json` to `~/.gcal-cli/credentials.json`

The tool will guide you through authentication on first use.

## Commands

### Basic Event Management

```bash
# List events
gcal list                                    # Next 10 events
gcal list -n 20 --from "2025-06-01" --to "2025-06-30"
gcal list -s "meeting" --show-id             # Search with IDs

# Create events
gcal create "Team Meeting" "2025-06-15 14:00"
gcal create "All Day Event" "2025-06-20" --all-day
gcal create "Meeting" "tomorrow 2pm" -e "tomorrow 3pm" \
  -l "Room 101" -d "Quarterly review" \
  -a john@example.com jane@example.com \
  -r 10m 1h --color 5

# Quick add (natural language)
gcal quick "Coffee with Sarah tomorrow at 3pm"
gcal quick "Team lunch every Friday at noon"

# Update events
gcal update EVENT_ID -s "New Title" --color 11
gcal update EVENT_ID --start "2025-06-20 15:00" -l "New Location"

# Delete events
gcal delete EVENT_ID
gcal delete EVENT_ID --no-notify
```

### Calendar Operations

```bash
# List calendars
gcal calendars
gcal calendars --json

# Check availability
gcal busy "2025-06-15" "2025-06-16"
gcal busy "tomorrow 9am" "tomorrow 5pm" -c primary work@example.com
```

### Advanced Features

```bash
# Analyze calendar patterns
gcal analyze                    # Last 30 days
gcal analyze -d 90 --json       # 90 days in JSON

# Find meeting times
gcal find-times 60 -a person1@email.com person2@email.com
gcal find-times 30 -a team@email.com -d 14  # Next 14 days

# Export to CSV
gcal export                     # Export with timestamp
gcal export -o calendar.csv --from "2025-01-01" --to "2025-12-31"
```

### Event Management

```bash
# Move/Copy events between calendars
gcal move EVENT_ID --to work@group.calendar.google.com
gcal copy EVENT_ID --from primary --to team@group.calendar.google.com

# Respond to invitations
gcal respond EVENT_ID --status accepted
gcal respond EVENT_ID --status declined
gcal respond EVENT_ID --status tentative

# List event attendees with status
gcal attendees EVENT_ID
gcal attendees EVENT_ID --json
```

### Calendar Management

```bash
# Create new calendar
gcal calendar create "Project Calendar" -d "For project tracking"
gcal calendar create "Team Events" -t "America/New_York"

# Update calendar properties
gcal calendar update CALENDAR_ID -s "New Name" -d "New description"
gcal calendar update CALENDAR_ID -t "Europe/London"

# Get calendar details
gcal calendar get CALENDAR_ID

# Delete calendar (with confirmation)
gcal calendar delete CALENDAR_ID
gcal calendar delete CALENDAR_ID --yes  # Skip confirmation
```

### Google Meet Integration

```bash
# Create event with Google Meet
gcal create-meet "Team Standup" "tomorrow 10am" -e "tomorrow 10:30am"
gcal create-meet "Client Call" "2pm" -a client@example.com -d "Quarterly review"
```

### Attachments

```bash
# Add attachment to event
gcal attach EVENT_ID "https://docs.google.com/document/d/..." --title "Meeting Notes"
gcal attach EVENT_ID "https://drive.google.com/file/..." --title "Presentation" \
  --mime-type "application/pdf"

# List event attachments
gcal attachments EVENT_ID
gcal attachments EVENT_ID --json
```

### Special Event Types

```bash
# Create out of office event
gcal out-of-office "2025-07-01" "2025-07-07" -m "On vacation, will respond when I return"

# Create focus time blocks
gcal focus-time "Deep Work" "9am" "11am"
gcal focus-time "Writing Time" "2pm" "4pm" --recurrence "FREQ=DAILY;BYDAY=MO,WE,FR"
```

## Features

### Event Options
- **Colors**: 11 color options (1-11)
- **Reminders**: Use format like `10m`, `1h`, `1d`
- **Recurrence**: RRULE format (e.g., `FREQ=WEEKLY;BYDAY=MO,WE,FR`)
- **Attendees**: Multiple emails with automatic invitations
- **All-day events**: Use `--all-day` flag
- **Google Meet**: Automatic conference room creation
- **Attachments**: Link documents from Google Drive or URLs
- **Event Types**: Regular, Out of Office, Focus Time

### Time Formats
- Specific: `"2025-06-15 14:00"`
- Natural: `"tomorrow 2pm"`, `"next Monday"`
- Relative: `"in 2 hours"`

### Output Formats
- Human-readable (default)
- JSON with `--json` flag for automation
- CSV export for spreadsheet analysis

## Examples

### Daily Workflow
```bash
# Morning: Check today's schedule
gcal list --from "today" --to "today"

# Schedule a meeting
gcal find-times 30 -a colleague@example.com
gcal create "Quick Sync" "2025-06-15 10:00" -a colleague@example.com

# End of day: Analyze time spent
gcal analyze -d 7
```

### Automation
```bash
# Get events as JSON
gcal list --json | jq '.[] | {summary, start}'

# Count meetings
gcal list -n 100 --json | jq '[.[] | select(.attendees)] | length'

# Export for reporting
gcal export -o monthly_report.csv --from "2025-06-01" --to "2025-06-30"
```

## Tips

- Use `--show-id` to see event IDs for updates/deletes
- Colors: 1=Lavender, 5=Banana, 9=Blueberry, 11=Tomato
- Timezone is automatically detected from your calendar
- All times without timezone are treated as local time
- Calendar IDs can be email addresses or Google Calendar IDs
- Focus time blocks automatically decline conflicting meetings
- Out of office events show you as busy and can include auto-response messages

## Troubleshooting

- **Auth issues**: Delete `~/.gcal-cli/token.pickle` and re-authenticate
- **Timeouts**: Check network connection and Google Calendar API status
- **Permissions**: Ensure calendar has appropriate access rights