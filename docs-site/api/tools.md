---
layout: docs
title: Tools API
description: CLI tools available in md agents
permalink: /api/tools/
---

md agents uses command-line tools that are executed through Claude Code's Bash interface. All tools are documented in `/tools/tool-library/`.

## Tool Format

Tools are invoked using square brackets:

```markdown
Use [tool-name] to perform action
Execute [tool-name --option value]
Run [tool-name {parameter}]
```

## Available Tools

### Communication
- **[gmail-cli]** - Read and send emails
- **[slack-cli]** - Slack messaging
- **[typefully]** - Post to X/Twitter

### Information
- **[grok]** - AI analysis of X/Twitter
- **[weather-api]** - Weather data
- **[current-time]** - Current date/time
- **[web-search]** - Search the web

### Data Processing
- **[jq]** - JSON processing
- **[grep]** - Pattern matching
- **[sed]** - Text transformation

## Tool Documentation

Each tool in `/tools/tool-library/` includes:
- Installation instructions
- Available commands
- Example usage
- Natural language descriptions

## Using Tools in Agents

```markdown
## Behavior
1. Get current time with [current-time]
2. Search for "{query}" using [web-search]
3. Parse results with [jq '.results[]']
4. Send summary via [gmail-cli send]
```

## Custom Tools

To add a new tool:
1. Create documentation in `/tools/tool-library/`
2. Include installation steps
3. Provide usage examples
4. Test with an agent

See the Tool Library in `/tools/tool-library/` for all available tools.