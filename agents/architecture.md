# System Architecture: Natural Language Agents

Visual overview of how everything connects.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                          │
│                  (Claude Code / Terminal)                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       Orchestrator                           │
│                                                              │
│  • Reads schedule.md for time-based tasks                   │
│  • Executes workflows from workflows/                       │
│  • Manages sessions and state                               │
│  • Handles errors and recovery                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        ▼                                     ▼
┌───────────────────┐              ┌───────────────────┐
│    Workflows      │              │   Specialists     │
│                   │              │                   │
│ • daily-briefing  │              │ • email-scanner   │
│ • x-poster        │              │ • news-gatherer   │
│ • resilient-brief │              │ • summary-writer  │
│ • parallel-demo   │              │ • weather-agent   │
└───────┬───────────┘              └─────────┬─────────┘
        │                                     │
        └──────────────┬──────────────────────┘
                       ▼
        ┌──────────────────────────┐
        │   Context & Sessions     │
        │                          │
        │ • YAML state files       │
        │ • Shared context/        │
        │ • Session tracking       │
        └──────────────────────────┘
```

## Workflow Execution Flow

```
Start Workflow
     │
     ▼
┌─────────────┐     ┌──────────────┐
│Create       │────▶│ sessions/    │
│Session      │     │ [id].yaml    │
└─────────────┘     └──────────────┘
     │
     ▼
┌─────────────┐
│Load Workflow│────▶ workflows/daily-briefing.md
│Definition   │
└─────────────┘
     │
     ▼
┌─────────────┐     ┌──────────────┐
│Execute      │────▶│ specialists/ │
│Step 1       │     │ email-scan.md│
└─────────────┘     └──────┬───────┘
     │                      │
     │                      ▼
     │              ┌──────────────┐
     │              │context/      │
     │              │email-sum.md  │
     │              └──────────────┘
     ▼
┌─────────────┐
│Update       │
│Session      │
└─────────────┘
     │
     ▼
[Repeat for each step]
     │
     ▼
┌─────────────┐     ┌──────────────┐
│Complete     │────▶│ output/      │
│Workflow     │     │ result.md    │
└─────────────┘     └──────────────┘
```

## Parallel Execution

```
         Orchestrator
              │
    ┌─────────┴─────────┬─────────────┐
    ▼                   ▼             ▼
Email Scanner      News Gatherer   Weather Agent
    │                   │             │
    ▼                   ▼             ▼
context/email      context/news    context/weather
    │                   │             │
    └─────────┬─────────┘             │
              ▼                       │
        Summary Writer ◀──────────────┘
              │
              ▼
        output/briefing.md
```

## Session State Management

```
Session Lifecycle:

[Created] ──▶ [Running] ──▶ [Completed]
                  │              │
                  ▼              ▼
              [Failed] ──▶ [Resumed]
                  │
                  ▼
             [Archived]

Session File Structure:
┌────────────────────────────┐
│ session.yaml               │
├────────────────────────────┤
│ workflow: daily-briefing   │
│ status: running            │
│ current_step: 2            │
│ steps:                     │
│   - email: completed       │
│   - news: running          │
│   - summary: pending       │
│ context:                   │
│   email_count: 23          │
│   urgent_items: 3          │
│ errors: []                 │
└────────────────────────────┘
```

## Context Flow

```
Agent A Output          Context Directory         Agent B Input
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│email-scanner│───────▶│context/     │◀───────│news-gatherer│
│             │ write  │             │ read   │             │
│Found topics:│        │email-sum.md │        │Reads topics │
│- AI meeting │        │news-sum.md  │        │to search    │
│- Budget rev │        │weather.md   │        │relevant news│
└─────────────┘        └─────────────┘        └─────────────┘
```

## Directory Structure

```
agents/
│
├── orchestrator.md          # Main controller
├── schedule.md             # Time-based triggers
│
├── specialists/            # Individual agents
│   ├── agent-template.md
│   ├── email-scanner.md
│   ├── news-gatherer.md
│   └── summary-writer.md
│
├── workflows/              # Multi-agent workflows
│   ├── workflow-template.md
│   ├── daily-briefing.md
│   └── x-poster-workflow.md
│
├── sessions/               # Execution tracking
│   ├── active/            # Currently running
│   ├── completed/         # Finished sessions
│   └── session-template.yaml
│
├── utils/                  # Helper agents
│   ├── error-handler.md
│   └── workflow-runner.md
│
├── context/               # Temporary shared data
│   └── [cleaned after each workflow]
│
└── output/                # Final results
    └── [workflow outputs with timestamps]
```

## Error Handling Flow

```
                Error Occurs
                     │
    ┌────────────────┴────────────────┐
    ▼                                 ▼
Recoverable?                    Non-Recoverable
    │                                 │
    ▼                                 ▼
┌─────────┐                    ┌─────────────┐
│Retry    │                    │Log Error    │
│Logic    │                    │Save State   │
└────┬────┘                    │Mark Failed  │
     │                         └──────┬──────┘
     ▼                                │
Success? ──No──▶ Fallback             ▼
     │           Strategy        Notify User
     ▼              │
Continue         Use Cache/
Workflow         Partial Data
```

## Tool Integration

```
   Specialist Agent
         │
         ▼
"I need to check email"
         │
         ▼
┌─────────────────────┐
│  Natural Language   │
│  Tool Description   │
└─────────────────────┘
         │
         ▼
    gmail_cli.py ◀────── External Tool
         │
         ▼
    Email Results
         │
         ▼
   Context Output
```

## Performance Characteristics

```
Sequential Execution:
Step1 ──▶ Step2 ──▶ Step3 ──▶ Done
10s       15s       5s       = 30s total

Parallel Execution:
Step1 ──┐
Step2 ──┼──▶ Step4 ──▶ Done
Step3 ──┘
  15s         5s     = 20s total (33% faster)
```

## Security Model

```
┌─────────────────────────────────────────┐
│           User Space                     │
│  • Agent definitions (safe markdown)     │
│  • Workflows (declarative)               │
│  • Read-only context access              │
└──────────────┬──────────────────────────┘
               │ Controlled Interface
┌──────────────▼──────────────────────────┐
│          Tool Space                      │
│  • Gmail CLI (OAuth secured)            │
│  • File system (scoped access)          │
│  • APIs (credential managed)            │
└─────────────────────────────────────────┘
```

## Key Design Principles

1. **Everything is a file**: Agents, workflows, state - all markdown/YAML
2. **Natural language first**: No code required to create agents
3. **Composable**: Small agents combine into powerful workflows
4. **Observable**: Every step is logged and trackable
5. **Resilient**: Graceful degradation and recovery
6. **Simple**: Complexity hidden, simplicity exposed

This architecture enables anyone to build, understand, and maintain intelligent agent systems using only natural language.