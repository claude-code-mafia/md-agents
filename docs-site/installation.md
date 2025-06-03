---
layout: docs
title: Installation
description: Get md agents up and running on your system
permalink: /installation/
---

md agents is designed to work with Claude Code and requires minimal setup.

## Prerequisites

- **Operating System**: macOS, Linux, or Windows with WSL
- **Claude Code**: The official Claude desktop app
- **Git**: For cloning the repository
- **Bash**: For running scripts (included on Unix systems)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/peteknowsai/md-agents.git
cd md-agents
```

### 2. Make Scripts Executable

```bash
chmod +x scripts/*.sh
```

### 3. Verify Installation

```bash
# Test the execution script
./scripts/run-agents.sh --help

# List available agents
ls agents/specialists/
ls agents/workflows/
```

## Directory Permissions

Ensure Claude Code has access to:
- Read all markdown files in `/agents/`
- Write to `/runtime/output/`
- Write to `/logs/`
- Read/write to `/runtime/state/`

## Optional: Install Additional Tools

md agents can use various CLI tools. See [Tool Library](/api/tools/) for available tools and installation instructions.

### Common Tools

```bash
# Gmail CLI (for email agents)
pip install gmail-cli

# Weather CLI
npm install -g weather-cli

# Other tools as needed...
```

## Configuration

### Global Settings

Create or edit `/runtime/state/global.json`:

```json
{
  "user_name": "Your Name",
  "home_city": "New York",
  "timezone": "America/New_York"
}
```

### Agent-Specific Settings

Each agent can have its own configuration in `/runtime/state/`.

## Testing Your Installation

### Run a Simple Agent

```bash
# Create a test agent
cat > agents/specialists/test.md << 'EOF'
# Specialist: Test Agent

<<You verify the system is working.>>

## Behavior
1. Say "System is working!"
2. Report current time
3. List available tools
EOF

# Run it
./scripts/run-agents.sh test
```

### Run a Workflow

```bash
# Use an existing workflow
./scripts/run-agents.sh daily-briefing --dry-run
```

## Troubleshooting

### Permission Denied

```bash
# Fix script permissions
chmod +x scripts/*.sh
```

### Agent Not Found

- Check file exists in `/agents/`
- Ensure filename matches agent name
- Verify `.md` extension

### No Output

- Check `/logs/activity.log` for errors
- Ensure `/runtime/output/` is writable
- Verify agent syntax is correct

## Next Steps

✅ Installation complete! Now you can:

1. Follow the [Quickstart Guide](/quickstart/)
2. Browse [Examples](/examples/)
3. Read about [Core Concepts](/docs/concepts/)
4. Create your first agent

## Updating md agents

```bash
# Pull latest changes
git pull origin main

# Check for new tools or agents
git log --oneline -5
```