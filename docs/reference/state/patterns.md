# State Management

How agents remember things and share context.

## State Types

```markdown
~memory.key~        # Agent's own memory
~cache.key~         # Temporary storage
~global.key~        # Shared between all agents
~session.key~       # Current workflow/session only
```

## Using State

### Reading
```markdown
Check ~memory.last_run~
Use ~global.user_timezone~
```

### Writing  
```markdown
Update ~memory.last_run~ = {timestamp}
Store ~cache.results~ = {data}
```

### Common Patterns
```markdown
# Remember things
~memory.patterns.common_queries~
~memory.stats.total_processed~

# Cache expensive operations
~cache.api_results~ (expires after 1 hour)

# Share between agents
~global.current_project~
~global.urgent_topics~
```

## Examples

### In a Specialist
```markdown
Check ~memory.vip_senders~ for important people
Update ~memory.stats.emails_processed~ += {count}
```

### In a Workflow  
```markdown
Step 1: Store {results} in ~session.step1_data~
Step 2: Read ~session.step1_data~ and process
```

### In a Coordinator
```markdown
Check ~memory.successful_strategies~ for what worked before
Update ~cache.recent_analysis~ with results
```

That's it. Agents can remember and share.