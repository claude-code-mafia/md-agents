# Week 1 Guide: Natural Language Agents

## What We Built

We created a simple, natural language system for agents that work together:

1. **Specialist Agents**: Each agent has one job and does it well
2. **Workflows**: Coordinate multiple agents to accomplish bigger tasks
3. **Context Sharing**: Simple YAML files let agents pass information

## Key Principles

### 1. Natural Language First
Agents read like instructions to a helpful assistant, not code:
```markdown
I am a specialist agent that quickly scans your inbox for important emails.
```

### 2. Simple Context Passing
Agents share information through readable context files:
```yaml
agent_outputs:
  email_scanner:
    summary: "Found 3 urgent emails"
    key_topics: ["AI project", "deadline change"]
```

### 3. Clear Workflows
Workflows are like recipes - easy to follow steps:
```markdown
Step 1: Email Scanner checks inbox
Step 2: News Gatherer finds relevant news
Step 3: Summary Writer combines everything
```

## How to Use

### Running a Specialist Agent
Each agent works independently:
```
Execute agent: email-scanner
Input: Check last 24 hours
Output: Saves summary to context/email-summary.md
```

### Running a Workflow
Workflows coordinate multiple agents:
```
Execute workflow: daily-briefing
- Automatically runs email scanner
- Passes results to news gatherer
- Summary writer creates final briefing
```

### Understanding Context
The context file shows workflow progress:
- Which agents have completed
- What each agent produced
- Current status

## What's Different

### Before (Traditional Approach)
```python
class EmailAgent:
    def __init__(self, config):
        self.gmail_api = GmailAPI(config)
    
    def process(self, time_range):
        emails = self.gmail_api.fetch(time_range)
        return self.categorize(emails)
```

### Now (Natural Language)
```markdown
I check your Gmail inbox for messages from the last 24 hours.
When I need to check emails, I use:
~/Projects/tool-library/gmail-tool/gmail_cli.py list -q "newer_than:1d"
```

## Next Week Preview

Week 2 will add:
- Automatic session management
- Orchestrator updates to run these workflows
- Error recovery and resumability

But the core stays simple - agents are just markdown files with instructions!