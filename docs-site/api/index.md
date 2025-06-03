---
layout: docs
title: API Reference
description: Complete reference for all md agents components
---

The md agents API is expressed entirely through markdown specifications. This reference documents all available fields, patterns, and options.

## Agent Specification

All agents follow this structure:

```markdown
# [Type]: [Name]

<<System prompt defining agent's role>>

## Metadata
  version: str
  author: str  
  tags: list[str]

## Triggers
  **Schedule**: cron expression
  **Event**: event description
  **Command**: command string

## Input
  param_name: type = default_value
  required_param: type
  optional_param: type?

## Behavior
Natural language instructions

## Output  
  field_name: type
  optional_field: type?

## Error Handling
Error scenarios and recovery
```

## Component Types

### [Specialists](/api/specialists/)
Single-purpose agents with focused behavior.

**Required Fields:**
- Title with "Specialist:" prefix
- System prompt in `<<>>`
- Behavior section

**Optional Fields:**
- Triggers
- Input/Output schemas
- Error handling
- State management

### [Workflows](/api/workflows/)
Sequential execution pipelines.

**Required Fields:**
- Title with "Workflow:" prefix  
- Steps section with numbered steps

**Optional Fields:**
- Triggers
- Input parameters
- Conditional logic
- Parallel execution

### [Coordinators](/api/coordinators/)
Dynamic orchestration agents.

**Required Fields:**
- Title with "Coordinator:" prefix
- System prompt
- Behavior with routing logic

**Optional Fields:**
- Decision criteria
- State tracking
- Fallback behavior

## Notation Reference

### Symbol Quick Reference

```markdown
[tool]       # External tool invocation
%agent%      # Agent reference (any type)
@workflow@   # Workflow reference  
{variable}   # Variable interpolation
~state~      # State/memory access
<<prompt>>   # System prompt
::Type::     # Type definition reference
```

### Extended Notation

#### Conditional Execution
```markdown
- **If**: {condition}
  - **Execute**: %agent%
- **Else**:
  - **Execute**: %other-agent%
```

#### Parallel Execution  
```markdown
- **Parallel**:
  - %agent-1% → {result1}
  - %agent-2% → {result2}
```

#### Loop Execution
```markdown
- **For each**: item in {list}
  - **Execute**: %processor%
  - **With**: data = {item}
```

## Type System

### Built-in Types

- `str` - String
- `int` - Integer  
- `float` - Floating point
- `bool` - Boolean
- `list[T]` - List of type T
- `dict[K,V]` - Dictionary
- `object` - Any object
- `?` suffix - Optional

### Custom Types

Define in `/docs/reference/types/`:

```markdown
### ::EmailMessage::
- id: str
- sender: str
- subject: str
- body: str
- timestamp: int
- attachments: list[str]?
```

## State Management

### State Scopes

| Scope | Symbol | Persistence | Use Case |
|-------|--------|------------|----------|
| Memory | `~memory~` | Per agent | Agent-specific data |
| Cache | `~cache~` | Per session | Temporary storage |
| Global | `~global~` | System-wide | Shared configuration |
| Session | `~session~` | Current run | Execution context |

### State Operations

```markdown
# Read
Load from ~memory.key~

# Write  
Store in ~memory.key~

# Update
Increment ~memory.counter~

# Delete
Clear ~cache.temp_data~
```

## Tool Integration

### Tool Declaration

Tools are defined in `/tools/tool-library/`:

```markdown
# Tool: [gmail-cli]

## Description
Command-line interface for Gmail

## Commands
  list: List emails
  read: Read specific email  
  send: Send new email

## Usage
[gmail-cli] list --unread --limit 10
```

### Tool Invocation

```markdown
## Behavior
1. Use [gmail-cli] to list emails
2. Parse results with [json-parser]
3. Filter with custom logic
```

## Execution Directives

### Step Directives

- **Execute**: Run an agent
- **With**: Pass parameters
- **Get**: Capture output
- **Save**: Write to file
- **If/Else**: Conditional logic
- **Parallel**: Concurrent execution
- **For each**: Iteration

### Example Step

```markdown
### Step 2: Process Data
  **Execute**: %data-processor%
  **With**: 
    data = {raw_data}
    format = "json"
  **Get**: {processed}
  **Save**: output/processed-{timestamp}.json
```

## Error Handling

### Error Specification

```markdown
## Error Handling
  **On API timeout**: 
    Retry 3 times with exponential backoff
    Use cached data if available
    Log failure to ~memory.errors~
  
  **On invalid input**:
    Return error: ::InvalidInputError::
    Suggest corrections
  
  **Always**:
    Update ~session.last_error~
    Maintain partial results
```

### Error Types

```markdown
### ::Error::
  code: str
  message: str  
  retryable: bool
  details: object?
```

## Scheduling

### Cron Expressions

```markdown
## Triggers
- **Schedule**: 0 8 * * *     # Daily at 8am
- **Schedule**: */15 * * * *  # Every 15 minutes
- **Schedule**: 0 0 * * MON   # Weekly on Monday
```

### Schedule Patterns

| Pattern | Meaning |
|---------|---------|
| `* * * * *` | Every minute |
| `0 * * * *` | Every hour |
| `0 0 * * *` | Daily at midnight |
| `0 0 * * 0` | Weekly on Sunday |
| `0 0 1 * *` | Monthly on the 1st |

## Best Practices

### Agent Design

1. **Single Responsibility**: One agent, one purpose
2. **Clear Contracts**: Explicit inputs/outputs
3. **Graceful Failure**: Always handle errors
4. **Stateless Default**: Only use state when necessary

### Performance

1. **Parallel When Possible**: Use parallel execution
2. **Cache Expensive Operations**: Use `~cache~`
3. **Batch Operations**: Process multiple items together
4. **Early Termination**: Fail fast on errors

### Security

1. **Never Hardcode Secrets**: Use `~global.secrets~`
2. **Validate Inputs**: Check before processing
3. **Limit Permissions**: Principle of least privilege
4. **Audit Trail**: Log sensitive operations

## Complete Example

```markdown
# Specialist: Smart Email Processor

<<You intelligently process emails with advanced filtering.>>

## Metadata
  version: 1.0.0
  author: md agents Team
  tags: [email, automation, productivity]

## Triggers
  **Schedule**: */30 * * * *  # Every 30 minutes
  **Event**: When email received
  **Command**: "process emails"

## Input
  time_range: str = "30 minutes"
  categories: list[str] = ["urgent", "important", "fyi"]
  auto_respond: bool = false

## Behavior

1. Fetch emails from {time_range} using [gmail-cli]
2. For each email:
   Extract sender, subject, and key phrases
   Check against ~memory.vip_senders~
   Classify into {categories}
   
3. Process by priority:
   Urgent: Notify immediately
   Important: Add to task list
   FYI: Archive after summary

4. If {auto_respond} is true:
   Generate contextual response
   Queue for sending with delay

5. Update statistics in ~memory.stats~

## Output
  processed_count: int
  urgent_items: list[::EmailSummary::]
  actions_taken: dict[str, int]

## Error Handling
  **On Gmail API error**: 
    Retry with backoff
    Use cached email list
    Alert user after 3 failures
  
  **On classification error**:
    Default to "important" category
    Log for manual review
  
  **Always**:
    Save partial progress
    Report what was completed
```

For detailed examples of each component type, see:

- [Specialist Reference](/api/specialists/)
- [Workflow Reference](/api/workflows/)
- [Coordinator Reference](/api/coordinators/)
- [Tools Reference](/api/tools/)