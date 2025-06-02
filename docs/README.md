# Natural Language Agent System

A revolutionary approach to AI agents that prioritizes human readability and natural language over code.

## What Makes This Different

Traditional agent systems require programming. Ours uses natural language:

**Traditional Agent:**
```python
class EmailAgent:
    def process(self, timeRange):
        emails = self.api.fetch(timeRange)
        return self.categorize(emails)
```

**Our Natural Language Agent:**
```markdown
I am a specialist agent that quickly scans your inbox for important emails.

When I work, I check your Gmail for messages from the last 24 hours,
identify which ones need attention, and create a summary highlighting
what's urgent.
```

## Core Concepts

### 1. Agents Are Specialists
Each agent has one clear job and explains it in first person:
- "I search X for Claude Code tips"
- "I check your email for urgent messages"
- "I combine information into clear summaries"

### 2. Workflows Coordinate Agents
Workflows read like recipes, coordinating multiple agents:
```markdown
Step 1: Email Scanner checks inbox
Step 2: News Gatherer finds relevant news
Step 3: Summary Writer combines everything
```

### 3. Everything Is Readable
- No code to debug
- No complex configurations
- Just markdown files with clear instructions

## Directory Structure

```
agents/
├── specialists/          # Individual agents
│   ├── email-scanner.md
│   ├── news-gatherer.md
│   └── summary-writer.md
├── workflows/            # Multi-agent workflows  
│   ├── daily-briefing.md
│   └── x-poster-workflow.md
├── sessions/            # Workflow execution tracking
├── utils/               # Helper agents
└── orchestrator.md      # Runs everything
```

## Key Features

### Natural Language First
Agents describe what they do, not how:
- ✅ "I search for news related to your interests"
- ❌ `def search_news(interests: List[str]) -> NewsItems:`

### Simple Context Passing
Agents share information through readable files:
```yaml
email_summary:
  urgent: 3
  important: 8
  topics: ["project deadline", "team meeting"]
```

### Parallel Execution
Run multiple agents simultaneously:
```markdown
Run these agents at the same time:
- Email Scanner
- News Gatherer
- Weather Agent
```

### Resilient Error Handling
Graceful degradation in plain English:
```markdown
If email scanning fails:
- Try using cached data
- If no cache, continue without emails
- Note the limitation in the summary
```

## Getting Started

### 1. Create Your First Agent

Create `agents/specialists/my-agent.md`:
```markdown
# Agent: My Helper

I am a specialist agent that [what you do].

## What I Do
[2-3 sentences explaining your purpose]

## How I Work
1. First, I [step 1]
2. Then, I [step 2]
3. Finally, I [step 3]

## What I Produce
After I'm done, you'll have:
- [Output 1]
- [Output 2]
```

### 2. Create a Simple Workflow

Create `agents/workflows/my-workflow.md`:
```markdown
# Workflow: My Task

This workflow [what it accomplishes].

## The Process

### Step 1: [Name]
- **Who**: My Helper agent
- **What**: [What they do]
- **Produces**: [Output location]
```

### 3. Run Your Workflow

```bash
# From agents directory
Execute workflow: my-workflow
```

## Real Examples

### Daily Briefing Workflow
Combines emails, news, and weather into a morning summary:
- Runs three agents in parallel
- Handles failures gracefully
- Always produces useful output

### X Poster Workflow  
Finds and posts Claude Code tips:
- Searches X for tips
- Filters for uniqueness
- Crafts engaging posts
- Updates posting history

## Advanced Features

### Session Management
Every workflow run creates a session:
```yaml
session_id: daily-briefing-2025-06-03-0900
status: running
current_step: 2 of 3
errors: []
```

### Error Recovery
Multiple strategies for resilience:
- Retry with exponential backoff
- Cache fallbacks
- Graceful degradation
- Partial result handling

### Performance Optimization
- Parallel agent execution
- Smart caching
- Minimal state overhead

## Why Natural Language?

1. **Accessibility**: Anyone can read and modify agents
2. **Maintainability**: No code rot or dependency issues
3. **Debuggability**: See exactly what agents are doing
4. **Flexibility**: Easy to adjust behavior
5. **Collaboration**: Non-programmers can contribute

## Best Practices

1. **Keep Agents Focused**: One job per agent
2. **Use Clear Examples**: Show, don't just tell
3. **Handle Errors Gracefully**: Plan for failures
4. **Write Like You're Explaining**: To a helpful assistant
5. **Test with Real Scenarios**: Ensure agents work together

## Contributing

To add new agents:
1. Follow the templates in `specialists/agent-template.md`
2. Use first person "I" statements
3. Focus on what, not how
4. Include examples
5. Test in a workflow

## Future Enhancements

- Visual workflow designer
- Agent marketplace
- Performance analytics
- Version control for agents
- Natural language debugging

## License

This project demonstrates the future of AI agent development - where natural language is the programming language.

---

Built with ❤️ using Claude Code and the power of readable AI.