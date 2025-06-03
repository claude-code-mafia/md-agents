---
layout: docs
title: Extensions
description: Extending MD Agents with custom capabilities
---

MD Agents is designed to be extensible. Add new capabilities by creating custom agents, tools, and patterns.

## Creating Custom Tools

To add a new CLI tool:

1. **Document the tool** in `/tools/tool-library/[tool-name].md`
2. **Include**:
   - Installation instructions
   - Available commands
   - Usage examples
   - Natural language descriptions

Example tool documentation:
```markdown
# Tool: [my-tool]

## Description
Brief description of what the tool does

## Installation
```bash
pip install my-tool
# or
npm install -g my-tool
```

## Commands
- `my-tool list` - List items
- `my-tool get <id>` - Get specific item
- `my-tool create` - Create new item

## Usage in Agents
Use [my-tool list] to get all items
Execute [my-tool get {item_id}] for details
```

## Custom Agent Types

While MD Agents provides three core types, you can create variations:

### Domain-Specific Specialists
```markdown
# Specialist: Legal Document Analyzer
# Specialist: Medical Record Scanner
# Specialist: Financial Report Parser
```

### Industry Workflows
```markdown
# Workflow: Compliance Check
# Workflow: Patient Onboarding
# Workflow: Investment Analysis
```

### Specialized Coordinators
```markdown
# Coordinator: Security Operations Center
# Coordinator: Healthcare Triage
# Coordinator: Trading Desk
```

## Integration Patterns

### Webhooks
Create agents that respond to external webhooks:
```markdown
## Triggers
- **Event**: Webhook received at /api/agents/notify
```

### API Integration
Wrap any API as a tool:
```markdown
Use [api-wrapper --endpoint /users --method GET]
```

### Database Connections
Access databases through CLI tools:
```markdown
Query with [db-cli "SELECT * FROM users"]
```

## Contributing

Share your extensions with the community:

1. Fork the repository
2. Add your extension
3. Include documentation
4. Submit a pull request

See our [Contributing Guide](https://github.com/peteknowsai/md-agents/blob/main/CONTRIBUTING.md) for details.