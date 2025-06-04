# Claude Agents Development

You are working on a markdown-based agent system where agents are defined purely in markdown files.

## Project Overview
- Agents are markdown specifications, not code
- Each agent defines its purpose, behavior, and tools
- Agents can compose and invoke other agents
- Everything runs through natural language instructions

## Working with Agents
- To "build an agent": create/edit markdown files in `/agents/`
- Test agents by running them with the execution scripts
- Follow existing agent patterns for consistency
- Agent behavior is defined in plain English, not programming logic

## Key Conventions
- Agents organized in `/agents/specialists/`, `/agents/workflows/`, and `/agents/coordinators/`
- Tool documentation in `/tool-library/`
- Outputs saved to `/runtime/output/`
- Logs saved to `/logs/`

## Agent Structure
Each agent markdown file should contain:
- **Metadata**: Version, type, dependencies
- **Purpose**: Clear description of what the agent does
- **Behavior**: Step-by-step instructions in natural language
- **Error Handling**: What to do when things go wrong
- **Output Format**: How results should be formatted

## Testing Agents
```bash
# Run all agents via coordinator
./scripts/run-agents.sh

# Check logs
tail -f logs/activity.log

# View outputs
ls -la runtime/output/
```

## Philosophy
- **Simplicity**: Agents are just markdown files with instructions
- **Composability**: Agents work together through orchestration
- **Flexibility**: Natural language allows easy customization
- **Transparency**: Everything is human-readable