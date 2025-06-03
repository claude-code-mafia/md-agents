---
layout: docs
title: Triggers
description: How agents are activated in MD Agents
---

Triggers define when and how agents are activated. MD Agents supports three types of triggers.

## Trigger Types

### Schedule Triggers

Use cron expressions for time-based activation:

```markdown
## Triggers
- **Schedule**: 0 8 * * *     # Daily at 8am
- **Schedule**: */15 * * * *  # Every 15 minutes
- **Schedule**: 0 0 * * MON   # Weekly on Monday
```

### Event Triggers

Respond to system or user events:

```markdown
## Triggers
- **Event**: When email received
- **Event**: When user asks question
- **Event**: When file uploaded
```

### Command Triggers

Direct invocation by command:

```markdown
## Triggers
- **Command**: "check weather"
- **Command**: "run analysis"
- **Command**: "generate report"
```

## Multiple Triggers

Agents can have multiple triggers:

```markdown
## Triggers
- **Schedule**: 0 9 * * *        # Run at 9am
- **Schedule**: 0 17 * * *       # Also at 5pm
- **Event**: When requested      # And on demand
- **Command**: "status update"   # Via command
```

## Conditional Triggers

Add conditions to triggers:

```markdown
## Triggers
- **Schedule**: 0 8 * * MON-FRI  # Weekdays only
- **Event**: When email received AND sender in ~memory.vip_list~
```

For cron expression help, see [crontab.guru](https://crontab.guru).