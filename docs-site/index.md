---
layout: home
title: 🧩 md agents framework
---

# Build intelligent agents with markdown

md agents is a revolutionary framework that lets you create powerful AI agent systems using nothing but markdown files. No code required.

```markdown
# Specialist: Research Agent

<<You research topics and provide comprehensive summaries.>>

## Triggers
- **Event**: When user asks for research

## Behavior
1. Search for relevant information
2. Analyze and synthesize findings
3. Create structured summary

## Output
- summary: str
- sources: list[str]
```

## Why md agents?

### 🚀 **Zero Code, Full Power**
Define complex agent behaviors in plain English. The framework handles all the implementation details.

### 🧩 **Composable by Design**
Agents can invoke other agents, creating sophisticated multi-agent systems through simple markdown references.

### 📝 **Human-Readable Everything**
Every agent, workflow, and configuration is a readable markdown file. No black boxes.

### ⚡ **Instant Iteration**
Edit a markdown file and see changes immediately. No compilation, no deployment.

## Get Started in 2 Minutes

```bash
# Clone the repository
git clone https://github.com/peteknowsai/md-agents.git
cd md-agents

# Create your first agent
echo '# Specialist: Hello Agent

<<You greet users warmly.>>

## Behavior
1. Say hello
2. Ask how you can help' > agents/specialists/hello.md

# Run it
./scripts/run-agents.sh hello
```

## Core Concepts

### Three Agent Types

<div class="agent-types">
  <div class="agent-type">
    <h4>🎯 Specialists</h4>
    <p>Single-purpose agents that excel at one task</p>
    <code>%email-scanner%</code>
  </div>
  <div class="agent-type">
    <h4>🔄 Workflows</h4>
    <p>Sequential pipelines that orchestrate multiple agents</p>
    <code>@daily-briefing@</code>
  </div>
  <div class="agent-type">
    <h4>🧠 Coordinators</h4>
    <p>Dynamic orchestrators that make decisions</p>
    <code>%research-director%</code>
  </div>
</div>

### Simple Notation System

| Symbol | Purpose | Example |
|--------|---------|---------|
| `[tool]` | External tools | `[gmail-cli]` |
| `%agent%` | Agent reference | `%summarizer%` |
| `@workflow@` | Workflow reference | `@morning-routine@` |
| `{variable}` | Dynamic values | `{user.name}` |
| `~state~` | State access | `~memory.last_run~` |

## Real-World Examples

### Daily Briefing Workflow
```markdown
# Workflow: Daily Briefing

## Steps
1. **Execute**: %email-scanner%
2. **Execute**: %news-gatherer%
3. **Execute**: %summary-writer%
   **With**: sources = [{emails}, {news}]
4. **Save**: output/briefing-{date}.md
```

### Smart Research Coordinator
```markdown
# Coordinator: Research Director

## Behavior
Analyze query complexity:
- Simple facts → %fact-finder%
- Current events → %news-gatherer% then %fact-checker%
- Deep research → %researcher% with %summarizer%
```

## Ready to Build?

<div class="cta-buttons">
  <a href="{{ '/quickstart/' | relative_url }}" class="btn btn-primary">Start Tutorial</a>
  <a href="{{ '/examples/' | relative_url }}" class="btn btn-secondary">Browse Examples</a>
  <a href="https://github.com/peteknowsai/md-agents" class="btn btn-outline">View on GitHub</a>
</div>