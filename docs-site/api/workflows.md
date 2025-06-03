---
layout: docs
title: Workflows API
description: Complete reference for workflow agents
permalink: /api/workflows/
---

Workflows are sequential pipelines that orchestrate multiple agents in a fixed order.

## Structure

```markdown
# Workflow: [Name]

Description of the workflow purpose

## Triggers
- **Schedule**: cron_expression
- **Command**: command_string

## Input
- param: type = default

## Steps

### Step 1: [Description]
- **Execute**: %agent-name%
- **With**: parameters
- **Get**: {variable}

### Step 2: [Description]
- **Execute**: %another-agent%
- **With**: input = {variable}
- **Save**: output/path
```

## Step Directives

- **Execute**: Run an agent
- **With**: Pass parameters
- **Get**: Capture output
- **Save**: Write to file
- **If/Else**: Conditional
- **Parallel**: Concurrent
- **For each**: Iteration

## Examples

See [Workflow Examples]({{ '/examples/workflows/' | relative_url }}) for complete implementations.