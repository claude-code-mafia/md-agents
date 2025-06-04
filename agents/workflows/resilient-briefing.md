# Workflow: Resilient Briefing

This workflow creates a daily briefing that handles failures gracefully.

## Triggers
- **Schedule**: 0 8 * * 1-5  # 8am weekdays
- **Command**: "resilient briefing"

## Input
- email_range: str = "24 hours"
- continue_on_error: bool = true

## Steps

### Step 0: Get Current Timestamp
- **Execute**: [current-time]
- **Purpose**: Get timestamp for file naming
- **Get**: {timestamp}

### Step 1: Try Email Scan
- **Execute**: %email-scanner%
- **With**: time_range = {email_range}
- **Get**: {emails}
- **On Error**: Set {emails} = null, continue

### Step 2: Try News
- **Execute**: %news-gatherer%
- **With**: topics = extract from {emails} or ["general"]
- **Get**: {news}
- **On Error**: Set {news} = null, continue

### Step 3: Try Weather
- **Execute**: %weather-agent%
- **With**: location = ~global.user_location~
- **Get**: {weather}
- **On Error**: Set {weather} = null, continue

### Step 4: Create Briefing
- **Execute**: %summary-writer%
- **With**: 
  - sources = [{emails}, {news}, {weather}] excluding nulls
  - format = "brief"
  - note_failures = true
- **Save**: output/resilient-briefing-{timestamp}.md

## Success
- [ ] At least one data source worked
- [ ] Summary created with available data

## If Things Go Wrong
- Individual failures don't stop workflow
- Summary notes what was unavailable
- Always produces some output