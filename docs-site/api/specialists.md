---
layout: docs
title: Specialists API
description: Complete reference for specialist agents
permalink: /api/specialists/
---

Specialists are single-purpose agents that excel at one specific task.

## Structure

```markdown
# Specialist: [Name]

<<System prompt defining expertise>>

## Metadata
- version: str
- author: str
- tags: list[str]

## Triggers
- **Schedule**: cron_expression
- **Event**: event_description
- **Command**: command_string

## Input
- param_name: type = default_value
- required_param: type
- optional_param: type?

## Behavior
Step-by-step instructions in natural language

## Output
- field_name: type
- optional_field: type?

## Error Handling
Error scenarios and recovery strategies

## State Used
- ~memory.key~ - Description
- ~cache.key~ - Description
```

## Required Fields

- **Title**: Must start with "Specialist:"
- **System Prompt**: Enclosed in `<<>>`
- **Behavior**: Natural language instructions

## Optional Fields

- **Metadata**: Version, author, tags
- **Triggers**: How the agent is activated
- **Input/Output**: Typed parameters
- **Error Handling**: Failure scenarios
- **State Used**: Memory and cache usage

## Examples

### Minimal Specialist

```markdown
# Specialist: Greeter

<<You greet users warmly.>>

## Behavior
1. Say hello
2. Be friendly
```

### Full-Featured Specialist

```markdown
# Specialist: Email Analyzer

<<You analyze emails for urgency, sentiment, and required actions.>>

## Metadata
- version: 1.0.0
- author: md agents Team
- tags: [email, analysis, nlp]

## Triggers
- **Event**: When email scanner completes
- **Command**: "analyze email"

## Input
- email_id: str
- include_sentiment: bool = true
- urgency_threshold: float = 0.7

## Behavior
1. Load email content using [gmail-cli read {email_id}]
2. Analyze for urgency indicators:
   - Keywords: URGENT, ASAP, deadline
   - Sender importance from ~memory.vip_senders~
   - Time-sensitive language
3. If {include_sentiment}:
   - Determine emotional tone
   - Identify potential concerns
4. Extract action items
5. Calculate urgency score

## Output
- urgency_score: float
- sentiment: "positive" | "neutral" | "negative"?
- action_items: list[str]
- summary: str

## Error Handling
- If email not found: Return error ::EmailNotFound::
- If analysis fails: Return partial results
- Always: Log errors to ~session.errors~

## State Used
- ~memory.vip_senders~ - List of important senders
- ~cache.email_{email_id}~ - Cached email content
```

## Input Types

### Basic Types
- `str` - String
- `int` - Integer
- `float` - Decimal
- `bool` - Boolean

### Complex Types
- `list[T]` - List of type T
- `dict[K,V]` - Dictionary
- Custom types: `::TypeName::`

### Optional Types
- `type?` - Optional (may be null)
- `type = default` - With default value

## Common Patterns

### Tool Wrapper
```markdown
# Specialist: Weather Checker

<<You check weather conditions.>>

## Input
- location: str
- units: "metric" | "imperial" = "imperial"

## Behavior
1. Use [weather-api --location {location} --units {units}]
2. Parse JSON response
3. Format for readability

## Output
- temperature: float
- conditions: str
- forecast: list[str]
```

### Data Processor
```markdown
# Specialist: Data Cleaner

<<You clean and validate data.>>

## Input
- data: list[dict]
- rules: ::CleaningRules::

## Behavior
1. For each item in {data}:
   - Apply validation rules
   - Fix common issues
   - Mark invalid entries
2. Remove duplicates
3. Sort by relevance

## Output
- cleaned_data: list[dict]
- removed_count: int
- issues_found: list[str]
```

### Stateful Specialist
```markdown
# Specialist: Incremental Processor

<<You process new items since last run.>>

## Behavior
1. Load ~memory.last_processed_id~
2. Fetch items > {last_id}
3. Process each item
4. Update ~memory.last_processed_id~

## State Used
- ~memory.last_processed_id~ - Track progress
- ~memory.processed_count~ - Statistics
```

## Best Practices

1. **Single Responsibility**: One task, done well
2. **Clear Interface**: Explicit inputs/outputs  
3. **Error Resilience**: Handle failures gracefully
4. **State Documentation**: List all state usage
5. **Tool Abstraction**: Hide tool complexity

## See Also

- [Agent Types]({{ '/docs/agent-types/' | relative_url }})
- [Notation Guide]({{ '/docs/notation/' | relative_url }})
- [Example Specialists]({{ '/examples/basic/' | relative_url }})