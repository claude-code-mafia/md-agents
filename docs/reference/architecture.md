# System Architecture

How the agent system works.

## Components

```
┌─────────────────────────────────────────────┐
│              Coordinator                     │
│                                              │
│  • Executes specialists, workflows,          │
│    and other coordinators                    │
│  • Manages sessions and state                │
└──────────────────┬───────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│Specialists│ │Workflows │ │Coordinators  │
│           │ │          │ │              │
│ %agent%   │ │@workflow@│ │ %coordinator%│
└───────────┘ └──────────┘ └──────────────┘
```

## Execution Flow

1. **Trigger** (schedule, event, or command)
2. **Coordinator** receives request
3. **Execution** of appropriate component
4. **State** updates and output saved

## State Management

```
~memory~    - Agent-specific memory
~cache~     - Temporary storage
~global~    - Shared state
~session~   - Current execution context
```

## Directory Structure

```
/agents/
  /specialists/     # Single-purpose agents
  /workflows/       # Sequential pipelines
  /coordinators/    # Dynamic orchestrators
  /utils/          # Helper agents

/runtime/
  coordinator.md    # Main executor
  schedule.md      # Time triggers
  /state/          # Persistent storage
  /output/         # Results
```