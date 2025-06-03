---
layout: docs
title: Coordinators API
description: Complete reference for coordinator agents
---

Coordinators are dynamic orchestrators that make intelligent routing decisions based on context.

## Structure

```markdown
# Coordinator: [Name]

<<System prompt defining coordination strategy>>

## Input
- request: str
- context: dict?

## Behavior

Analyze and route based on patterns:

### Pattern: [Description]
If [condition]:
- Execute %specialist%
- Monitor results
- Adapt as needed

## State Management
- Track decisions
- Learn from outcomes
```

## Key Features

- **Adaptive**: Changes approach based on results
- **Intelligent**: Makes routing decisions
- **Scalable**: Manages agent networks
- **Contextual**: Considers history

## Examples

See [Coordinator Examples](/examples/coordinators/) for implementations.