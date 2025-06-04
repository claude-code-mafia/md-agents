#!/bin/bash
# Simple script to get accurate current time from worldtimeapi

if ! command -v jq &> /dev/null; then
    # Fallback to python if jq not installed
    curl -s worldtimeapi.org/api/timezone/America/Denver | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Current time: {data['datetime']}\"); print(f\"Timezone: {data['timezone']}\")"
else
    # Use jq if available
    curl -s worldtimeapi.org/api/timezone/America/Denver | jq -r '"Current time: \(.datetime)\nTimezone: \(.timezone)"'
fi