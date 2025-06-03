---
layout: docs
title: Notation Guide
description: Complete reference for MD Agents notation system
---

MD Agents uses a simple, intuitive notation system to represent tools, agents, variables, and state. This guide covers all notation symbols and their usage.

## Quick Reference

| Symbol | Purpose | Example |
|--------|---------|---------|
| `[tool]` | External tool invocation | `[gmail-cli]` |
| `%agent%` | Agent reference | `%email-scanner%` |
| `@workflow@` | Workflow reference | `@daily-briefing@` |
| `{variable}` | Variable interpolation | `{user.name}` |
| `~state~` | State/memory access | `~memory.last_run~` |
| `<<prompt>>` | System prompt | `<<You are helpful>>` |
| `::Type::` | Type definition | `::EmailSummary::` |

## Detailed Symbol Guide

### `[tool]` - External Tools

Square brackets indicate external CLI tools that agents can use.

**Usage:**
```markdown
## Behavior
1. Use [gmail-cli] to fetch emails
2. Parse with [jq] for JSON extraction
3. Send notification with [slack-cli]
```

**Tool Arguments:**
```markdown
Use [gmail-cli --unread --limit 10] to get recent unread emails
Execute [weather-api --location "New York" --units metric]
```

**Common Tools:**
- `[gmail-cli]` - Gmail operations
- `[grok]` - AI analysis of X/Twitter
- `[typefully]` - Social media posting
- `[web-search]` - Web searching
- `[current-time]` - Get current date/time

### `%agent%` - Agent References

Percent signs wrap agent names for both specialists and coordinators.

**Basic Usage:**
```markdown
## Steps
1. Execute %email-scanner%
2. Pass results to %summarizer%
3. Let %coordinator% decide next steps
```

**With Parameters:**
```markdown
- **Execute**: %weather-checker%
- **With**: 
    - location = "Boston"
    - units = "fahrenheit"
```

**Getting Output:**
```markdown
- **Execute**: %analyzer%
- **Get**: {analysis_results}
```

### `@workflow@` - Workflow References

At-signs wrap workflow names for sequential pipelines.

**Usage:**
```markdown
## Behavior
For daily updates, run @morning-briefing@
For research, execute @research-pipeline@
```

**In Coordinators:**
```markdown
If user needs comprehensive research:
  - Execute @deep-research-workflow@
Else:
  - Execute @quick-search-workflow@
```

### `{variable}` - Variable Interpolation

Curly braces for dynamic values and data passing.

**Simple Variables:**
```markdown
Greet the user with "Hello, {name}!"
Search for articles about {topic}
Process files from {input_directory}
```

**Nested Access:**
```markdown
Email {user.email} with subject {email.subject}
Temperature is {weather.current.temp_f}°F
Found {results.count} matches
```

**From Previous Steps:**
```markdown
### Step 1: Get Data
- **Execute**: %data-fetcher%
- **Get**: {raw_data}

### Step 2: Process
- **Execute**: %processor%
- **With**: input = {raw_data}
```

### `~state~` - State Management

Tilde notation for accessing persistent state and memory.

**State Types:**

1. **Memory** (`~memory~`) - Agent-specific persistence
   ```markdown
   Store VIP senders in ~memory.vip_list~
   Check ~memory.last_processed_date~
   ```

2. **Cache** (`~cache~`) - Temporary session storage
   ```markdown
   Cache API response in ~cache.weather_data~
   Reuse ~cache.expensive_calculation~
   ```

3. **Global** (`~global~`) - System-wide configuration
   ```markdown
   Read user preferences from ~global.settings~
   Get API key from ~global.api_keys.openai~
   ```

4. **Session** (`~session~`) - Current execution context
   ```markdown
   Track progress in ~session.completed_steps~
   Store errors in ~session.error_log~
   ```

**Operations:**
```markdown
# Read
Load from ~memory.key~

# Write
Store value in ~memory.key~

# Update
Append to ~memory.list~
Increment ~memory.counter~

# Delete
Clear ~cache.temporary~
```

### `<<prompt>>` - System Prompts

Double angle brackets define the agent's core identity and capabilities.

**Usage:**
```markdown
# Specialist: Email Expert

<<You are an email management specialist. You excel at 
scanning, categorizing, and summarizing emails. You 
understand urgency, importance, and can identify 
action items.>>
```

**Guidelines:**
- Keep concise but comprehensive
- Define expertise clearly
- Set behavioral boundaries
- Establish tone and approach

### `::Type::` - Type References

Double colons reference shared type definitions.

**Using Types:**
```markdown
## Output
- summary: ::EmailSummary::
- errors: list[::Error::]
- metadata: ::Metadata::?
```

**Common Types:**
```markdown
::Summary::
  - total: int
  - key_points: list[str]
  - confidence: float

::Error::
  - code: str
  - message: str
  - retryable: bool
```

## Advanced Notation Patterns

### Combining Notations

```markdown
## Behavior
1. Check if {user} exists in ~memory.users~
2. If not, fetch with [user-api --id {user.id}]
3. Process with %user-analyzer%
4. Store result in ~cache.user_{user.id}~
5. Return ::UserProfile::
```

### Conditional Notation

```markdown
- **If**: {score} > ~global.threshold~
  - **Execute**: %advanced-processor%
  - **With**: data = {input}
- **Else**:
  - **Execute**: %simple-processor%
```

### Dynamic Tool Selection

```markdown
Use [{tool_name} --option {option_value}] where:
- tool_name = ~memory.preferred_tool~ or "default-tool"
- option_value = {user.preference} or "standard"
```

### Nested Variable Access

```markdown
Process email from {email.sender.address}
Subject contains {search.terms[0]}
Priority is {config.rules.email.priority}
```

## Special Notations

### Timestamps and Dates

```markdown
Save to output/report-{timestamp}.md
Check emails since {date:yesterday}
Schedule for {time:now+1h}
```

### File Paths

```markdown
Read from input/{filename}
Save to ~/Documents/{project_name}/output.md
Use template from ./templates/{template_type}.md
```

### Environment Variables

```markdown
API key from {env:OPENAI_API_KEY}
Home directory is {env:HOME}
Custom setting from {env:MD_AGENTS_CONFIG}
```

## Best Practices

### 1. Clarity Over Brevity

Good:
```markdown
- **Execute**: %email-scanner%
- **With**: time_range = "24 hours"
- **Get**: {scanned_emails}
```

Avoid:
```markdown
Run %es% → {e}
```

### 2. Consistent Naming

- Agents: `%noun-verb%` (e.g., `%email-scanner%`, `%fact-checker%`)
- Workflows: `@adjective-noun@` (e.g., `@daily-briefing@`, `@quick-search@`)
- Variables: `snake_case` (e.g., `{user_email}`, `{search_results}`)

### 3. Meaningful State Keys

Good:
```markdown
~memory.processed_email_ids~
~cache.weather_boston_2024_01_20~
~global.user_preferences.theme~
```

Avoid:
```markdown
~memory.data~
~cache.temp~
~global.x~
```

### 4. Type Safety

Always specify types for inputs/outputs:
```markdown
## Input
- email_id: str
- include_attachments: bool = false

## Output
- result: ::ProcessedEmail::
- status: "success" | "partial" | "failed"
```

## Common Patterns

### Data Pipeline
```markdown
{raw_data} → %cleaner% → {clean_data} → %analyzer% → {insights}
```

### Tool with Fallback
```markdown
Try [primary-tool] or fallback to [backup-tool]
```

### Stateful Processing
```markdown
Last run: ~memory.last_run~
Process new items since then
Update ~memory.last_run~ = {timestamp}
```

### Error Context
```markdown
On error:
- Log to ~session.errors~
- Include {context} in ::Error::
- Notify %error-handler%
```

## Notation Errors to Avoid

❌ **Mixing notation types:**
```markdown
Execute [email-scanner]  # Wrong - agents use %
Use %gmail-cli%         # Wrong - tools use []
```

❌ **Forgetting quotes in values:**
```markdown
With: location = New York  # Wrong
With: location = "New York"  # Correct
```

❌ **Invalid state paths:**
```markdown
~memory~.key           # Wrong
~memory.key~           # Correct
```

❌ **Undefined variables:**
```markdown
Use {undefined_var}    # Will cause error
Use {defined_var}      # Must be defined earlier
```

## Summary

The MD Agents notation system is designed to be:
- **Intuitive**: Symbols match their purpose
- **Consistent**: Same pattern everywhere
- **Readable**: Clear at a glance
- **Powerful**: Express complex flows simply

Master these seven symbols and you can build any agent system:
- `[tool]` for external tools
- `%agent%` for agents
- `@workflow@` for workflows
- `{variable}` for data
- `~state~` for persistence
- `<<prompt>>` for identity
- `::Type::` for structure