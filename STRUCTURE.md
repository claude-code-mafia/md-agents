# Project Structure

## Overview

The Claude Agents project is organized with clear separation of concerns:

```
/claude-agents/                    # Project root
├── README.md                      # Project overview
├── CLAUDE.md                      # Development instructions
├── STRUCTURE.md                   # This file
├── .gitignore
│
├── /agents/                       # Agent definitions only
│   ├── /specialists/              # Individual specialist agents
│   ├── /workflows/                # Sequential multi-agent pipelines
│   ├── /coordinators/             # Dynamic orchestration agents
│   └── /utils/                    # Utility/helper agents
│
├── /runtime/                      # Execution environment
│   ├── CLAUDE.md                  # Runtime instructions
│   ├── coordinator.md             # Main execution coordinator
│   ├── schedule.md                # Time-based scheduling
│   ├── /state/                    # Persistent state
│   ├── /sessions/                 # Active and completed sessions
│   ├── /context/                  # Temporary context between agents
│   └── /output/                   # Generated outputs
│
├── /scripts/                      # Shell scripts
│   ├── run-agents.sh              # Execute agents/workflows
│   └── scheduler.sh               # Schedule recurring tasks
│
├── /docs/                         # All documentation
│   ├── /guides/                   # How-to guides
│   ├── /reference/                # Templates and architecture
│   └── /journey/                  # Weekly development guides
│
├── /examples/                     # Example agents for learning
│   ├── /fun/                      # Fun examples (jokes, facts)
│   ├── /practical/                # Practical examples
│   └── /tests/                    # Test scenarios
│
├── /tools/                        # External tool integrations
│   └── /tool-library/             # Tool documentation
│
├── /logs/                         # Execution logs
│
├── /mcp-servers/                  # MCP server implementations
│
└── /archive/                      # Old/deprecated files
```

## Directory Purposes

### `/agents/`
**Purpose**: Contains ONLY agent and workflow definitions  
**What goes here**: Real agents that do work  
**What doesn't**: Documentation, templates, examples, runtime files

### `/runtime/`
**Purpose**: Everything needed to execute agents  
**Key files**:
- `CLAUDE.md` - Instructions for runtime execution
- `coordinator.md` - Manages execution of agents, workflows, and coordinators
- `schedule.md` - Defines when workflows run
- Session tracking, context passing, outputs

### `/docs/`
**Purpose**: All documentation and guides  
**Includes**: 
- How-to guides (quick-start, testing, best practices)
- Reference docs (templates, architecture)
- Development journey (weekly guides)

### `/examples/`
**Purpose**: Example agents for learning  
**Not for**: Production agents (those go in `/agents/`)

### `/scripts/`
**Purpose**: Shell scripts at root level for easy access  
**Usage**: `./scripts/run-agents.sh`

## Key Files

### Two CLAUDE.md Files
1. **Root `/CLAUDE.md`** - For development (how to build agents)
2. **Runtime `/runtime/CLAUDE.md`** - For execution (how to run agents)

This separation ensures the right context is loaded for each activity.

### Important Paths
- Agent definitions: `/agents/specialists/`, `/agents/workflows/`, `/agents/coordinators/`
- Runtime state: `/runtime/state/`
- Execution logs: `/logs/activity.log`
- Generated outputs: `/runtime/output/`

## Quick Navigation

- **Want to create an agent?** → Start with `/docs/guides/quick-start.md`
- **Want to run agents?** → Use `/scripts/run-agents.sh`
- **Want to see examples?** → Check `/examples/`
- **Want to understand the system?** → Read `/docs/reference/architecture.md`