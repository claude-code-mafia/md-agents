---
layout: docs
title: Agent Types
description: Understanding Specialists, Workflows, and Coordinators
permalink: /docs/agent-types/
---

md agents provides three distinct agent types, each designed for different use cases. Understanding when to use each type is key to building effective systems.

## Overview

| Type | Purpose | Execution | Best For |
|------|---------|-----------|----------|
| **Specialists** | Single task | Standalone | Focused operations |
| **Workflows** | Sequential pipeline | Step-by-step | Predictable processes |
| **Coordinators** | Dynamic routing | Adaptive | Complex decisions |

## Specialists

Specialists are single-purpose agents that excel at one specific task.

### Characteristics

- **Focused**: Does one thing well
- **Reusable**: Can be called by any workflow or coordinator
- **Stateless**: By default, doesn't maintain state between calls
- **Tool-oriented**: Often wraps external tools

### Structure

```markdown
# Specialist: [Name]

<<System prompt defining the agent's expertise>>

## Triggers
- **Event**: When called by other agents
- **Schedule**: Optional scheduled execution

## Input
- param1: type = default
- param2: type

## Behavior
1. Specific step-by-step instructions
2. Usually involves tool usage
3. Returns structured output

## Output
- result: type
- metadata: type?
```

### Example: Email Scanner

```markdown
# Specialist: Email Scanner

<<You scan Gmail for important emails and categorize them.>>

## Input
- time_range: str = "24 hours"
- categories: list[str] = ["urgent", "important", "fyi"]

## Behavior
1. Use [gmail-cli] to fetch emails from {time_range}
2. Analyze each email for urgency indicators
3. Categorize based on sender, subject, keywords
4. Return structured summary

## Output
- emails: list[EmailSummary]
- stats: dict[str, int]
```

### When to Use Specialists

- **Tool Wrapping**: Encapsulate external tool usage
- **Data Processing**: Transform or analyze specific data
- **Single Operations**: One clear input → output transformation
- **Reusable Components**: Shared functionality across workflows

## Workflows

Workflows are sequential pipelines that orchestrate multiple agents in a fixed order.

### Characteristics

- **Sequential**: Steps execute in order
- **Deterministic**: Same inputs produce same outputs
- **Composable**: Can include other workflows
- **Data Flow**: Passes data between steps

### Structure

```markdown
# Workflow: [Name]

Description of the workflow's purpose

## Triggers
- **Schedule**: 0 8 * * *
- **Command**: "run workflow"

## Input
- param: type = default

## Steps

### Step 1: [Description]
- **Execute**: %agent-name%
- **With**: parameters
- **Get**: {output_variable}

### Step 2: [Description]
- **Execute**: %another-agent%
- **With**: input = {output_variable}
- **Save**: path/to/output
```

### Example: Daily Briefing

```markdown
# Workflow: Daily Briefing

Creates a comprehensive morning briefing

## Triggers
- **Schedule**: 0 7 * * *  # 7am daily

## Steps

### Step 1: Gather Email
- **Execute**: %email-scanner%
- **With**: time_range = "12 hours"
- **Get**: {emails}

### Step 2: Check Calendar
- **Execute**: %calendar-checker%
- **Get**: {events}

### Step 3: Get Weather
- **Execute**: %weather-reporter%
- **With**: location = ~global.home_city~
- **Get**: {weather}

### Step 4: Create Briefing
- **Execute**: %briefing-writer%
- **With**:
    - emails = {emails}
    - events = {events}
    - weather = {weather}
- **Save**: output/daily-briefing-{date}.md
```

### Advanced Workflow Features

**Conditional Execution**
```markdown
### Step 3: Check If Needed
- **If**: {emails.urgent_count} > 0
  - **Execute**: %urgent-handler%
- **Else**:
  - **Continue**: to next step
```

**Parallel Execution**
```markdown
### Step 2: Gather Data
- **Parallel**:
  - %news-gatherer% → {news}
  - %stock-checker% → {stocks}
  - %weather-agent% → {weather}
```

**Error Handling**
```markdown
### Step 4: Process Data
- **Execute**: %processor%
- **On Error**:
  - **Log**: error to ~memory.errors~
  - **Execute**: %error-notifier%
  - **Stop**: workflow
```

### When to Use Workflows

- **Scheduled Tasks**: Daily reports, regular maintenance
- **Multi-Step Processes**: Data gathering → processing → output
- **Predictable Flows**: When steps are always the same
- **Batch Operations**: Processing multiple items similarly

## Coordinators

Coordinators are dynamic orchestrators that make intelligent routing decisions.

### Characteristics

- **Adaptive**: Chooses agents based on context
- **Intelligent**: Makes decisions about execution
- **Scalable**: Can manage complex agent networks
- **Contextual**: Considers state and history

### Structure

```markdown
# Coordinator: [Name]

<<System prompt defining coordination strategy>>

## Input
- request: str
- context: dict?

## Behavior

Analyze the request and route accordingly:

### Pattern 1: [Description]
If [condition]:
- Execute %specialist-a%
- Then %specialist-b% if needed

### Pattern 2: [Description]
For [scenario]:
- Delegate to %sub-coordinator%
- Monitor progress
- Aggregate results

## State Management
- Track in ~session.routing_history~
- Update ~memory.patterns~
```

### Example: Research Director

```markdown
# Coordinator: Research Director

<<You orchestrate comprehensive research by routing to appropriate specialists.>>

## Input
- query: str
- depth: int = 2
- time_limit: int = 300

## Behavior

### Query Analysis
Determine research needs:
- Current events? → Prioritize %news-gatherer%
- Technical topic? → Start with %academic-searcher%
- Controversial? → Include %fact-checker%
- Opinion needed? → Add %sentiment-analyzer%

### Execution Strategy

For depth = 1 (quick):
- Single pass with most relevant agent
- Basic fact checking

For depth = 2 (standard):
- Initial research with 2-3 agents
- Fact checking on key claims
- Synthesis of findings

For depth = 3 (comprehensive):
- Full agent network activation
- Cross-validation of sources
- Deep fact checking
- Multiple synthesis passes

### Adaptive Routing

Monitor results and adapt:
- If insufficient data → expand search
- If contradictions → deep fact check
- If time running out → quick synthesis
- If high confidence → early completion

## Output
- research_report: str
- confidence: float
- sources: list[Source]
- fact_check_results: dict?
```

### Coordinator Patterns

**Hub and Spoke**
```markdown
Central coordinator manages all specialists:
- Receive request
- Analyze and decompose
- Distribute to specialists
- Aggregate results
```

**Hierarchical**
```markdown
Layer of coordinators:
- Top coordinator routes to domain coordinators
- Domain coordinators manage specialists
- Results bubble up through hierarchy
```

**Peer-to-Peer**
```markdown
Coordinators collaborate:
- Research coordinator ↔ Analysis coordinator
- Share findings and adjust strategies
- Collaborative result building
```

### When to Use Coordinators

- **Complex Requests**: Multi-faceted user queries
- **Dynamic Scenarios**: When approach depends on results
- **Intelligent Routing**: Choosing best agents for the task
- **Adaptive Systems**: Learning from outcomes

## Choosing the Right Type

### Decision Tree

```
Is it a single, focused task?
  → Yes: Use a Specialist

Is it a fixed sequence of steps?
  → Yes: Use a Workflow

Does it require dynamic decisions?
  → Yes: Use a Coordinator
```

### Composition Examples

**Workflow calling Specialists**
```markdown
@daily-briefing@ 
  → %email-scanner%
  → %news-gatherer%
  → %summary-writer%
```

**Coordinator managing Workflows**
```markdown
%project-manager%
  → @research-workflow@
  → @analysis-workflow@
  → @report-workflow@
```

**Mixed composition**
```markdown
%smart-assistant%
  → @quick-search@ (workflow)
  → %fact-checker% (specialist)
  → %research-director% (coordinator)
```

## Best Practices

### Specialists
- Keep focused on one domain
- Make inputs/outputs explicit
- Handle errors gracefully
- Document tool dependencies

### Workflows
- Design for clarity over cleverness
- Test each step independently
- Use meaningful variable names
- Plan for partial failures

### Coordinators
- Start with simple routing rules
- Add complexity gradually
- Monitor and log decisions
- Build in fallback strategies

## Examples

See our [Examples]({{ '/examples/' | relative_url }}) section for complete implementations:
- [Basic Specialists]({{ '/examples/basic/' | relative_url }})
- [Common Workflows]({{ '/examples/workflows/' | relative_url }})
- [Advanced Coordinators]({{ '/examples/coordinators/' | relative_url }})