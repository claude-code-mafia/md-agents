---
layout: docs
title: Core Concepts
description: Understand the fundamental concepts of md agents
permalink: /docs/concepts/
---

md agents introduces a new paradigm: **agents as markdown specifications**. This guide covers the core concepts that make the framework powerful yet simple.

## Philosophy

### Natural Language First

Instead of writing code, you describe what agents should do in plain English:

```markdown
## Behavior
1. Search for recent news on the topic
2. Verify facts from multiple sources
3. Summarize key findings
4. Flag any contradictions
```

The framework interprets these instructions and executes them intelligently.

### Composition Over Configuration

Agents can invoke other agents using simple notation:

```markdown
- **Execute**: %fact-checker%
- **With**: claims = {news.claims}
```

This creates powerful multi-agent systems without complex orchestration code.

## Agent Types

md agents has three fundamental agent types:

### 1. Specialists
Single-purpose agents that excel at one specific task.

```markdown
# Specialist: Email Scanner
<<You scan emails and identify important messages.>>
```

**Characteristics:**
- Focused on one domain
- Reusable across workflows
- Stateless by default
- Tool-oriented

### 2. Workflows
Sequential pipelines that orchestrate multiple agents.

```markdown
# Workflow: Daily Report
Step-by-step execution of multiple agents
```

**Characteristics:**
- Deterministic execution
- Fixed sequence of steps
- Pass data between agents
- Schedule-friendly

### 3. Coordinators
Dynamic orchestrators that make decisions.

```markdown
# Coordinator: Research Director
Intelligently route and coordinate based on context
```

**Characteristics:**
- Adaptive behavior
- Conditional routing
- Parallel execution
- Context-aware

## The Notation System

md agents uses intuitive symbols to represent different elements:

### Core Symbols

| Symbol | Meaning | Usage |
|--------|---------|-------|
| `[tool]` | External tool | `[gmail-cli]` invokes the Gmail CLI |
| `%agent%` | Agent reference | `%summarizer%` calls the summarizer agent |
| `@workflow@` | Workflow reference | `@daily-briefing@` runs a workflow |
| `{variable}` | Dynamic value | `{user.name}` accesses variables |
| `~state~` | State/memory | `~memory.last_run~` retrieves state |
| `<<prompt>>` | System prompt | `<<You are a helpful assistant>>` |
| `::Type::` | Type reference | `::Summary::` references a type |

### Practical Example

```markdown
## Behavior
1. Fetch emails with [gmail-cli] from {time_range}
2. Analyze with %email-analyzer%
3. Store important senders in ~memory.vip_list~
4. Return ::EmailSummary::
```

## State Management

Agents can maintain state across executions:

### State Types

1. **Memory** (`~memory~`): Agent-specific persistent storage
   ```markdown
   Store in ~memory.processed_items~
   ```

2. **Cache** (`~cache~`): Temporary execution storage
   ```markdown
   Cache results in ~cache.api_response~
   ```

3. **Global** (`~global~`): Shared across all agents
   ```markdown
   Read user preferences from ~global.settings~
   ```

4. **Session** (`~session~`): Current execution context
   ```markdown
   Track progress in ~session.steps_completed~
   ```

## Triggers

Agents can be activated in three ways:

### Schedule Triggers
Cron-style scheduling:
```markdown
## Triggers
- **Schedule**: 0 */4 * * *  # Every 4 hours
```

### Event Triggers
Respond to system events:
```markdown
## Triggers
- **Event**: When email received
- **Event**: When user asks question
```

### Command Triggers
Direct invocation:
```markdown
## Triggers
- **Command**: "check weather"
- **Command**: "daily summary"
```

## Input/Output Contracts

Agents define clear interfaces using Pydantic-style schemas:

### Input Schema
```markdown
## Input
- query: str
- max_results: int = 10
- include_metadata: bool = false
```

### Output Schema
```markdown
## Output
- results: list[str]
- confidence: float
- metadata: dict?
```

### Type References
Common types can be defined and reused:
```markdown
## Output
- summary: ::Summary::
- errors: list[::Error::]
```

## Error Handling

Agents handle errors gracefully:

```markdown
## Error Handling
- If API fails → Retry 3 times with backoff
- If no results → Return empty summary
- If invalid input → Log and skip
- Always → Update ~memory.error_log~
```

## Best Practices

### 1. Single Responsibility
Each specialist should do one thing well:
```markdown
# Good: Specialist: Email Scanner
# Bad: Specialist: Email Scanner and Analyzer and Responder
```

### 2. Clear Contracts
Define explicit inputs and outputs:
```markdown
## Input
- emails: list[str]  # List of email IDs to process
- urgency_threshold: int = 3  # 1-5 scale
```

### 3. Graceful Degradation
Always have fallback behavior:
```markdown
If weather API fails:
- Try alternate service
- Return last known good data
- Note data staleness
```

### 4. Meaningful State
Only store what's necessary:
```markdown
# Good: ~memory.vip_senders~
# Bad: ~memory.all_emails_ever_seen~
```

## Execution Model

Understanding how md agents executes your specifications:

1. **Parse**: Markdown is parsed into structured instructions
2. **Resolve**: Agent references and tools are resolved
3. **Execute**: Instructions are executed with AI interpretation
4. **Persist**: State changes are saved
5. **Output**: Results are formatted and returned

## Debugging

md agents provides visibility into execution:

### Activity Logs
```bash
tail -f logs/activity.log
```

### Session Traces
```bash
cat runtime/sessions/session-{id}.json
```

### State Inspection
```bash
cat runtime/state/coordinator-state.json
```

## Next Steps

- Explore [Agent Types](/docs/agent-types/) in detail
- Learn the complete [Notation Guide](/docs/notation/)
- See [State Management](/docs/state/) patterns
- Browse [Examples](/examples/) for inspiration