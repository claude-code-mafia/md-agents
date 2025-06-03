# MD Agents

Build intelligent agent systems with markdown. No code required.

**📖 Documentation**: https://peteknowsai.github.io/md-agents/  
**📁 Project Structure**: See [STRUCTURE.md](STRUCTURE.md)

## What is MD Agents?

MD Agents is a framework where AI agents are defined entirely in markdown files. Instead of writing code, you describe agent behaviors in plain English, and the framework handles the execution.

```markdown
# Specialist: Weather Agent

<<You check weather conditions and provide forecasts.>>

## Behavior
1. Use [weather-api] to get current conditions
2. Format temperature in both F and C
3. Include forecast for next 3 days

## Output
- current_temp: int
- conditions: str
- forecast: list[str]
```

## Key Features

✨ **Zero Code**: Define agents in markdown with natural language  
🧩 **Composable**: Agents can invoke other agents to handle complex tasks  
📝 **Human-Readable**: All configurations are transparent markdown files  
⚡ **Instant Changes**: Edit markdown, see results immediately  
🛠️ **CLI Tools**: Rich library of command-line tools optimized for Claude Code

## Quick Start

```bash
# Clone the repository
git clone https://github.com/peteknowsai/md-agents.git
cd md-agents

# Create your first agent
cat > agents/specialists/hello.md << 'EOF'
# Specialist: Hello Agent

<<You greet users warmly.>>

## Behavior
1. Greet the user by name
2. Ask how you can help today
3. Be enthusiastic but professional
EOF

# Run the agent
./scripts/run-agents.sh hello
```

## Agent Types

### 🎯 **Specialists**
Single-purpose agents that excel at one task
```markdown
%email-scanner%   # Scans for important emails
%news-gatherer%   # Collects news on topics
%fact-checker%    # Verifies claims
```

### 🔄 **Workflows**  
Sequential pipelines that orchestrate multiple agents
```markdown
@daily-briefing@  # Morning news + email summary
@research-flow@   # Multi-step research process
```

### 🧠 **Coordinators**
Dynamic orchestrators that make intelligent routing decisions
```markdown
%research-director%  # Routes research to appropriate specialists
%smart-assistant%    # Handles any user request intelligently
```

## Example: Daily Briefing Workflow

```markdown
# Workflow: Daily Briefing

## Triggers
- **Schedule**: 0 8 * * *  # 8am daily

## Steps

### Step 1: Check Email
- **Execute**: %email-scanner%
- **Get**: {important_emails}

### Step 2: Get News  
- **Execute**: %news-gatherer%
- **With**: topics = ["AI", "technology"]
- **Get**: {news}

### Step 3: Create Summary
- **Execute**: %summary-writer%
- **With**: 
    - emails = {important_emails}
    - news = {news}
- **Save**: output/daily-briefing-{date}.md
```

## Tool Library

MD Agents uses CLI tools optimized for Claude Code:

- **[gmail-cli]**: Read and send emails
- **[weather-api]**: Get weather data
- **[web-search]**: Search the web
- **[grok]**: Analyze X/Twitter content
- **[typefully]**: Post to social media
- And many more in `/tools/tool-library/`

Tools are executed as commands through Claude Code's Bash interface.

## Directory Structure

```
/agents/
  /specialists/     # Single-purpose agents
  /workflows/       # Multi-step pipelines  
  /coordinators/    # Dynamic orchestrators
  /utils/          # Helper agents

/tools/
  /tool-library/   # CLI tool documentation

/runtime/          # Execution environment
  /output/         # Agent outputs
  /state/          # Persistent storage
  /sessions/       # Execution history

/docs-site/        # GitHub Pages documentation
/scripts/          # Run and schedule agents
```

## Creating New Agents

1. Create a markdown file in `/agents/`
2. Define the agent's purpose and behavior
3. Specify inputs, outputs, and error handling
4. Test with `./scripts/run-agents.sh`

See our [Quickstart Guide](https://peteknowsai.github.io/md-agents/quickstart/) for detailed instructions.

## Philosophy

- **Natural Language First**: Describe what you want, not how to code it
- **Composition Over Configuration**: Build complex systems from simple parts
- **Transparency**: Every decision and action is readable
- **AI-Native**: Designed for how AI understands instructions

## Documentation

Full documentation available at https://peteknowsai.github.io/md-agents/

- [Quickstart Tutorial](https://peteknowsai.github.io/md-agents/quickstart/)
- [Core Concepts](https://peteknowsai.github.io/md-agents/docs/concepts/)
- [Example Gallery](https://peteknowsai.github.io/md-agents/examples/)
- [API Reference](https://peteknowsai.github.io/md-agents/api/)

## Contributing

MD Agents is open source. Contributions welcome!

1. Fork the repository
2. Create your agent or enhancement
3. Test thoroughly
4. Submit a pull request

## License

MIT License - see LICENSE file for details