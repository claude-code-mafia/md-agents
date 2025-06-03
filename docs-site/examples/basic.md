---
layout: docs
title: Basic Agent Examples
description: Simple specialist agents to get started
permalink: /examples/basic/
---

These examples demonstrate basic specialist agents that perform single tasks.

## Hello World Agent

The simplest possible agent:

```markdown
# Specialist: Hello World

<<You greet the world enthusiastically.>>

## Behavior
1. Say "Hello, World!"
2. Add current time
3. Be cheerful
```

## Weather Reporter

Using external tools:

```markdown
# Specialist: Weather Reporter

<<You provide weather updates for any location.>>

## Input
- location: str = "New York"
- units: "metric" | "imperial" = "imperial"

## Behavior
1. Use [weather-api] to get current weather for {location}
2. Convert temperature to {units} if needed
3. Format report with:
   - Current temperature
   - Conditions (sunny, cloudy, etc.)
   - "Feels like" temperature
   - Wind speed and direction
4. Add clothing recommendation based on temperature

## Output
- temperature: float
- feels_like: float
- conditions: str
- wind: str
- recommendation: str
```

## Email Counter

Working with email:

```markdown
# Specialist: Email Counter

<<You count unread emails and categorize by sender.>>

## Input
- include_spam: bool = false

## Behavior
1. Use [gmail-cli list --unread] to get unread emails
2. Count total unread
3. Group by sender domain
4. If not {include_spam}, filter spam folder
5. Create summary statistics

## Output
- total_unread: int
- by_domain: dict[str, int]
- top_senders: list[str]
```

## File Organizer

Local file operations:

```markdown
# Specialist: File Organizer

<<You organize files in a directory by type.>>

## Input
- directory: str = "./downloads"
- dry_run: bool = true

## Behavior
1. List all files in {directory}
2. Group by extension:
   - Documents: pdf, doc, docx, txt
   - Images: jpg, png, gif, svg
   - Videos: mp4, mov, avi
   - Other: everything else
3. If not {dry_run}:
   - Create subdirectories
   - Move files to appropriate folders
4. Report what was (or would be) moved

## Output
- files_processed: int
- organization: dict[str, list[str]]
- errors: list[str]?
```

## JSON Formatter

Data transformation:

```markdown
# Specialist: JSON Formatter

<<You format JSON data for readability.>>

## Input
- json_string: str
- indent: int = 2
- sort_keys: bool = false

## Behavior
1. Parse {json_string} as JSON
2. If invalid, try to fix common issues:
   - Missing quotes
   - Trailing commas
   - Single quotes → double quotes
3. Format with {indent} spaces
4. If {sort_keys}, sort object keys
5. Return formatted JSON

## Output
- formatted: str
- was_valid: bool
- fixes_applied: list[str]?
```

## Running These Examples

Save any example to `agents/specialists/[name].md` and run:

```bash
./scripts/run-agents.sh [name]
```

For example:
```bash
./scripts/run-agents.sh weather-reporter --location "San Francisco"
```

## Next Steps

- Try modifying these examples
- Combine them in workflows
- Add error handling
- Implement state management

See [Workflow Examples](/examples/workflows/) for multi-agent pipelines.