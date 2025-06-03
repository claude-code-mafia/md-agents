---
layout: docs
title: State Management
description: Managing persistent state and memory in md agents
permalink: /docs/state/
---

md agents provides a flexible state management system that allows agents to maintain memory, share data, and track execution context.

## State Types

### 1. Memory (`~memory~`)
Agent-specific persistent storage that survives between executions.

```markdown
Store in ~memory.vip_senders~
Check ~memory.last_processed_id~
Update ~memory.statistics.total_processed~
```

### 2. Cache (`~cache~`)
Temporary storage for the current session, cleared after execution.

```markdown
Cache expensive API call in ~cache.api_response~
Reuse ~cache.calculated_values~
```

### 3. Global (`~global~`)
System-wide configuration shared across all agents.

```markdown
Read from ~global.user_preferences~
Access ~global.api_keys.openai~
```

### 4. Session (`~session~`)
Current execution context, useful for tracking workflow progress.

```markdown
Track ~session.steps_completed~
Log to ~session.error_log~
```

## State Operations

### Reading State
```markdown
Load user list from ~memory.users~
Get preference from ~global.settings.theme~
Check if exists in ~cache.processed_items~
```

### Writing State
```markdown
Store result in ~memory.last_result~
Save to ~cache.temporary_data~
Update ~global.last_run_time~
```

### Complex Operations
```markdown
Append to ~memory.history~
Increment ~memory.counters.emails_processed~
Merge with existing ~cache.aggregated_data~
```

## Best Practices

1. **Use appropriate scope**: Memory for persistence, cache for temporary data
2. **Clear naming**: Use descriptive keys like `~memory.email_scanner.last_id~`
3. **Handle missing keys**: Always have defaults when reading state
4. **Clean up**: Remove unnecessary cached data
5. **Document state**: List what state your agent uses

## Example: Stateful Email Scanner

```markdown
# Specialist: Email Scanner

## Behavior
1. Load ~memory.last_scan_time~ or default to "24 hours ago"
2. Fetch emails since {last_scan_time}
3. For each email:
   - Check if sender in ~memory.vip_list~
   - Cache email data in ~cache.emails.{email_id}~
4. Update ~memory.last_scan_time~ = {current_time}
5. Increment ~memory.stats.total_scanned~ by {email_count}

## State Used
- ~memory.last_scan_time~ - Track scanning progress
- ~memory.vip_list~ - Important senders
- ~memory.stats~ - Running statistics
- ~cache.emails.*~ - Temporary email storage
```

For more state management patterns and examples, see the [Best Practices]({{ '/best-practices/' | relative_url }}) guide.