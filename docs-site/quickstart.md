---
layout: docs
title: Quickstart
description: Get up and running with md agents in 5 minutes
permalink: /quickstart/
---

This guide will walk you through creating your first agent system. By the end, you'll have a working multi-agent workflow that gathers information and creates summaries.

## Prerequisites

- A Unix-like system (macOS, Linux, WSL)
- Basic command line knowledge
- A text editor

## Installation

```bash
# Clone the repository
git clone https://github.com/peteknowsai/md-agents.git
cd md-agents

# Make scripts executable
chmod +x scripts/*.sh

# Verify installation
./scripts/run-agents.sh --help
```

## Your First Specialist

Let's create a simple weather agent. Create `agents/specialists/weather-checker.md`:

```markdown
# Specialist: Weather Checker

<<You check the weather and provide current conditions.>>

## Triggers
- **Event**: When user asks about weather

## Input
- location: str = "New York"

## Behavior
1. Use [weather-api] to get current conditions
2. Format the response clearly
3. Include temperature, conditions, and forecast

## Output
- temperature: int
- conditions: str
- forecast: str
```

Run your agent:

```bash
./scripts/run-agents.sh weather-checker --location "San Francisco"
```

## Creating a Workflow

Now let's create a morning briefing workflow. Create `agents/workflows/morning-briefing.md`:

```markdown
# Workflow: Morning Briefing

This workflow creates your personalized morning update.

## Triggers
- **Schedule**: 0 8 * * *  # 8am daily
- **Command**: "morning briefing"

## Steps

### Step 1: Check Weather
- **Execute**: %weather-checker%
- **With**: location = ~global.user_location~
- **Get**: {weather}

### Step 2: Scan Emails
- **Execute**: %email-scanner%
- **With**: time_range = "8 hours"
- **Get**: {emails}

### Step 3: Get News
- **Execute**: %news-gatherer%
- **With**: topics = ~memory.interests~
- **Get**: {news}

### Step 4: Create Summary
- **Execute**: %summary-writer%
- **With**: 
    - weather = {weather}
    - emails = {emails}
    - news = {news}
- **Save**: output/morning-briefing-{date}.md
```

## Adding a Coordinator

For dynamic behavior, create `agents/coordinators/smart-assistant.md`:

```markdown
# Coordinator: Smart Assistant

<<You intelligently route requests to appropriate agents.>>

## Behavior

Analyze each request and decide:
- Weather questions → %weather-checker%
- Email queries → %email-scanner%
- Research needs → %research-director%
- Simple facts → %fact-finder%

If multiple agents needed, coordinate their execution.

## Example Routing

"What's the weather and any urgent emails?"
1. Execute %weather-checker%
2. Execute %email-scanner% with urgency filter
3. Combine results

"Research climate change impacts"
1. Delegate to %research-director%
2. Let it orchestrate specialist agents
```

## Running Your System

### Execute a specific workflow:
```bash
./scripts/run-agents.sh "morning briefing"
```

### Let the coordinator handle requests:
```bash
./scripts/run-agents.sh coordinator "What's the weather and news today?"
```

### Set up scheduled execution:
```bash
# Add to crontab
crontab -e

# Add this line for daily morning briefings
0 8 * * * cd /path/to/md-agents && ./scripts/run-agents.sh "morning briefing"
```

## Understanding the Output

Agents save their output to `runtime/output/`:

```bash
ls -la runtime/output/
# morning-briefing-2024-01-20.md
# weather-check-1705750800.json
# research-climate-change.md
```

View logs for debugging:

```bash
tail -f logs/activity.log
```

## Next Steps

Now that you have a working system:

1. **Explore Examples**: Check `/examples/` for more complex agents
2. **Learn Notation**: Read the [Notation Guide](/docs/notation/) 
3. **Add Tools**: See [Available Tools](/api/tools/)
4. **Build Custom Agents**: Follow patterns in `/agents/specialists/`

### Quick Tips

- Keep agents focused on one task
- Use workflows for sequential operations
- Use coordinators for dynamic routing
- Save important state with `~memory~`
- Test agents individually before combining

## Troubleshooting

<div class="alert alert-info">
<strong>Agent not found?</strong> Check the file exists in `/agents/` and filename matches agent name.
</div>

<div class="alert alert-info">
<strong>Tool errors?</strong> Ensure tools are configured in `/tools/tool-library/`.
</div>

<div class="alert alert-info">
<strong>No output?</strong> Check logs in `/logs/activity.log` for error messages.
</div>

Ready to build something more complex? Check out our [examples](/examples/) or dive into the [documentation](/docs/).