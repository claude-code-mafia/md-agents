---
layout: docs
title: Documentation
description: Learn how to build with md agents
permalink: /docs/
---

Welcome to the md agents documentation. This guide will help you understand and master the framework.

## Getting Started

<div class="alert alert-info">
<strong>New to md agents?</strong> Start with our <a href="{{ '/quickstart/' | relative_url }}">Quickstart Guide</a> to build your first agent in 5 minutes.
</div>

## Documentation Overview

### 📚 [Core Concepts]({{ '/docs/concepts/' | relative_url }})
Understand the fundamental principles behind md agents:
- Natural language specifications
- Agent composition
- The notation system
- Execution model

### 🎯 [Agent Types]({{ '/docs/agent-types/' | relative_url }})
Learn about the three types of agents:
- **Specialists**: Single-purpose agents
- **Workflows**: Sequential pipelines
- **Coordinators**: Dynamic orchestrators

### 🔤 [Notation Guide]({{ '/docs/notation/' | relative_url }})
Master the simple notation system:
- Tool invocation with `[tool]`
- Agent references with `%agent%`
- Variable interpolation with `{variable}`
- State management with `~state~`

### 💾 [State Management]({{ '/docs/state/' | relative_url }})
Learn how agents maintain and share state:
- Memory persistence
- Session context
- Global configuration
- Cache strategies

### ⚡ [Triggers]({{ '/docs/triggers/' | relative_url }})
Understand how agents are activated:
- Schedule triggers (cron)
- Event triggers
- Command triggers
- Trigger composition

## Quick Reference

### Basic Agent Structure

```markdown
# [Type]: [Name]

<<System prompt>>

## Triggers
- **Schedule**: cron expression
- **Event**: event description

## Input
- param: type = default

## Behavior
Natural language instructions

## Output
- field: type
```

### Common Patterns

**Sequential Execution**
```markdown
1. Execute %agent-1%
2. Use output in %agent-2%
3. Save final result
```

**Conditional Logic**
```markdown
If condition:
  Execute %agent-a%
Else:
  Execute %agent-b%
```

**State Access**
```markdown
Load from ~memory.key~
Store in ~cache.temp~
Update ~global.config~
```

## Learning Path

1. **Beginners**
   - Read [Core Concepts]({{ '/docs/concepts/' | relative_url }})
   - Follow [Quickstart]({{ '/quickstart/' | relative_url }})
   - Try [Basic Examples]({{ '/examples/basic/' | relative_url }})

2. **Intermediate**
   - Study [Agent Types]({{ '/docs/agent-types/' | relative_url }})
   - Build custom workflows
   - Implement error handling

3. **Advanced**
   - Create coordinators
   - Design complex state management
   - Build reusable components

## Best Practices

- **Start Simple**: Begin with specialists before workflows
- **Test Incrementally**: Verify each agent works alone
- **Use Clear Names**: Agent names should describe their purpose
- **Document Behavior**: Be explicit about what agents do
- **Handle Errors**: Always plan for failure cases

## Need Help?

- Browse our [Examples]({{ '/examples/' | relative_url }})
- Check the [API Reference]({{ '/api/' | relative_url }})
- Read [Troubleshooting]({{ '/debugging/' | relative_url }})
- Review [Best Practices]({{ '/best-practices/' | relative_url }})