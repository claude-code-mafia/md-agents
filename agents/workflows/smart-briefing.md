# Workflow: Smart Briefing

This workflow creates an intelligent briefing by using dynamic research.

## Triggers
- **Schedule**: 0 7 * * 1-5  # 7am weekdays
- **Command**: "smart briefing"

## Input
- depth: "quick" | "standard" | "deep" = "standard"
- focus_areas: list[str]? = null

## Steps

### Step 1: Scan Communications
- **Execute**: %email-scanner%
- **With**: time_range = "48 hours"
- **Get**: {emails}

### Step 2: Dynamic Research
- **Execute**: %research-director%
- **With**: 
  - query = "Research topics from: " + {emails.key_points}
  - depth = {depth}
- **Get**: {research}

### Step 3: Weather Check
- **Execute**: %weather-agent%
- **With**: location = ~global.user_location~
- **Get**: {weather}

### Step 4: Compile Briefing
- **Execute**: %summary-writer%
- **With**:
  - sources = [{emails}, {research}, {weather}]
  - format = "detailed"
  - sections = ["urgent", "research_insights", "weather", "actions"]
- **Save**: output/smart-briefing-{timestamp}.md

## Success
- [ ] Emails scanned
- [ ] Research completed dynamically
- [ ] Weather included
- [ ] Intelligent briefing created

## If Things Go Wrong
- Research takes too long: Use quick mode
- No email topics: Use {focus_areas} instead