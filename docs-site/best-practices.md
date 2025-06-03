---
layout: docs
title: Best Practices
description: Guidelines for building effective md agents
permalink: /best-practices/
---

Follow these best practices to create reliable, maintainable agent systems.

## Agent Design

### Single Responsibility
Each agent should do one thing well:

✅ **Good**: 
- `email-scanner` - Scans emails
- `weather-checker` - Checks weather
- `summary-writer` - Writes summaries

❌ **Avoid**:
- `email-scanner-and-summarizer-and-sender`
- `do-everything-agent`

### Clear Interfaces

Define explicit inputs and outputs:

```markdown
## Input
- email_id: str          # The email to analyze
- include_history: bool = false  # Include conversation history

## Output
- urgency: float         # 0-1 urgency score
- summary: str           # Brief summary
- action_required: bool  # Needs response?
```

### Error Handling

Always plan for failures:

```markdown
## Error Handling
- If email not found: Return empty summary
- If API timeout: Retry 3 times with backoff
- If parse error: Log and return partial data
- Always: Update error count in ~memory.errors~
```

## Workflow Patterns

### Test Steps Individually
Before combining agents, verify each works:

```bash
# Test each specialist
./scripts/run-agents.sh email-scanner
./scripts/run-agents.sh summarizer

# Then test workflow
./scripts/run-agents.sh email-summary-workflow
```

### Use Meaningful Variables

✅ **Good**: 
```markdown
- **Get**: {email_summary}
- **Get**: {weather_report}
- **Get**: {analyzed_data}
```

❌ **Avoid**:
```markdown
- **Get**: {data}
- **Get**: {result}
- **Get**: {x}
```

### Add Checkpoints

Save intermediate results:

```markdown
### Step 2: Process Data
- **Execute**: %processor%
- **Get**: {processed}
- **Save**: temp/checkpoint-{timestamp}.json  # Checkpoint
```

## State Management

### Choose Appropriate Scope

- **Memory** (`~memory~`): Agent-specific persistence
- **Cache** (`~cache~`): Temporary session data
- **Global** (`~global~`): Shared configuration
- **Session** (`~session~`): Current execution

### Name Keys Clearly

✅ **Good**: 
```markdown
~memory.email_scanner.last_scan_time~
~cache.weather_data.new_york.2024_01_20~
~global.api_keys.openai~
```

❌ **Avoid**:
```markdown
~memory.data~
~cache.temp~
~global.key~
```

### Clean Up State

Remove old cache entries:

```markdown
## Behavior
1. Check age of ~cache.old_data~
2. If older than 24 hours, delete
3. Create new cache entry
```

## Performance

### Parallel When Possible

```markdown
### Step 1: Gather Data
- **Parallel**:
  - %weather-agent% → {weather}
  - %news-agent% → {news}
  - %email-agent% → {emails}
```

### Cache Expensive Operations

```markdown
1. Check ~cache.expensive_result~
2. If exists and fresh, use cached
3. Else, compute and cache for 1 hour
```

### Fail Fast

```markdown
## Behavior
1. Validate inputs immediately
2. If invalid, return error without processing
3. Only proceed with valid data
```

## Security

### Never Hardcode Secrets

✅ **Good**: 
```markdown
Get API key from ~global.api_keys.service_name~
```

❌ **Avoid**:
```markdown
Use API key "sk-1234567890abcdef"
```

### Validate External Input

```markdown
## Behavior
1. Sanitize {user_input}
2. Check against allowed patterns
3. Reject suspicious content
4. Process validated input only
```

### Limit Permissions

Only request necessary access:

```markdown
## Required Permissions
- Read: Email metadata only
- Write: Output directory only
- No delete permissions needed
```

## Documentation

### Document State Usage

```markdown
## State Used
- ~memory.last_scan~ - Track scan progress
- ~memory.vip_list~ - Important contacts
- ~cache.email_*~ - Temporary email data
```

### Include Examples

```markdown
## Example
Input:
  time_range: "24 hours"
  categories: ["urgent", "important"]

Output:
  total_emails: 47
  urgent_count: 3
  summary: "3 urgent emails require attention..."
```

### Explain Complex Logic

```markdown
## Behavior
1. Calculate urgency score:
   - Keywords (+0.3): URGENT, ASAP, deadline
   - Sender VIP (+0.2): Check ~memory.vip_list~
   - Time sensitive (+0.2): Due within 24h
   - Cap at 1.0
```

## Testing

### Create Test Agents

```markdown
# Specialist: Test Email Scanner

<<Test version with mock data.>>

## Behavior
1. Return mock email data
2. Simulate various scenarios
3. Test error conditions
```

### Use Dry Run Mode

```bash
# Test without side effects
./scripts/run-agents.sh workflow --dry-run
```

### Monitor Success Metrics

Track in state:
- Success rate
- Average execution time
- Error frequency
- Resource usage

## Maintenance

### Version Your Agents

```markdown
## Metadata
- version: 1.2.0
- last_updated: 2024-01-20
- author: Your Name
```

### Log Deprecations

```markdown
## Deprecated
- Old parameter 'limit' → Use 'max_results'
- Will be removed in v2.0
```

### Review Regularly

- Check error logs monthly
- Update deprecated patterns
- Optimize slow agents
- Remove unused agents

## Summary

1. **Keep It Simple**: Start basic, add complexity gradually
2. **Be Explicit**: Clear inputs, outputs, and behavior
3. **Handle Errors**: Plan for every failure mode
4. **Test Thoroughly**: Verify each component works
5. **Document Well**: Future you will thank present you