# Cal.com CLI Tool

Command-line interface for managing Cal.com bookings, events, and availability.

## Installation

```bash
./install-tool.sh cal-com
```

## Configuration

First, authenticate with your Cal.com API key:

```bash
cal-com auth
```

You can find your API key in Cal.com at Settings > Security > API Keys.

## Usage

### Authentication
```bash
# Interactive setup
cal-com auth

# With API key
cal-com auth --key cal_live_xxxxxx
```

### Bookings Management
```bash
# List all bookings
cal-com bookings list

# List upcoming bookings only
cal-com bookings list --status upcoming

# Get booking details
cal-com bookings get BOOKING_ID

# Cancel a booking
cal-com bookings cancel BOOKING_ID
cal-com bookings cancel BOOKING_ID --reason "Meeting rescheduled"

# JSON output
cal-com bookings list --json
```

### Event Types
```bash
# List all event types
cal-com events list

# Create a new event type
cal-com events create "30 Minute Call" 30-min-call 30
cal-com events create "Consultation" consultation 60 --description "Initial consultation"

# Update an event type
cal-com events update EVENT_ID --title "New Title"
cal-com events update EVENT_ID --length 45
cal-com events update EVENT_ID --hidden true

# Delete an event type
cal-com events delete EVENT_ID
```

### Availability
```bash
# List availabilities
cal-com availability list
```

### Schedules
```bash
# List schedules
cal-com schedules list
```

### User Information
```bash
# Get current user info
cal-com users me
```

## Examples

### Common Workflows

1. **Set up a new event type for consultations**:
```bash
cal-com events create "Free Consultation" free-consultation 30 \
  --description "30-minute free consultation call"
```

2. **View today's bookings**:
```bash
cal-com bookings list --status upcoming --json | \
  jq '.[] | select(.startTime | startswith("2024-01-07"))'
```

3. **Cancel all bookings for a specific event**:
```bash
# First list bookings for the event
cal-com bookings list --json | \
  jq '.[] | select(.eventTypeId == 12345) | .id' | \
  xargs -I {} cal-com bookings cancel {}
```

## Configuration

The CLI stores configuration in `~/.cal-com/config.json`:
- `api_key`: Your Cal.com API key

## Output Formats

- **Human-readable**: Default format with formatted output
- **JSON**: Use `--json` flag for machine-readable output

## Error Handling

The CLI provides clear error messages:
- Authentication errors when API key is invalid
- Network errors when Cal.com is unreachable
- Validation errors for invalid inputs
- API errors with detailed messages

## API Documentation

For more details about the Cal.com API:
- [Cal.com API v1 Documentation](https://cal.com/docs/api-reference/v1/introduction)
- [Authentication Guide](https://cal.com/docs/api-reference/v1/authentication)