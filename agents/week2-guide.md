# Week 2 Guide: Making Workflows Work

## What We Built

We made the agent system actually functional by adding:

1. **Session Management**: Track workflow execution from start to finish
2. **Enhanced Orchestrator**: Can now run multi-agent workflows
3. **Context Passing**: Agents share information seamlessly
4. **Error Recovery**: Workflows can resume if something fails

## Key Components

### 1. Sessions
Each workflow run gets a session that tracks:
- Which steps have completed
- What each agent produced  
- Current status and progress
- Recovery information if needed

### 2. Orchestrator v2
Now handles two modes:
- **Classic**: Time-based single agent tasks
- **Workflows**: Multi-agent coordinated tasks

### 3. Context Flow
```
Email Scanner → context/email-summary.md
                                        ↓
                            News Gatherer (reads email context)
                                        ↓
                            context/news-summary.md
                                        ↓
                            Summary Writer (reads all context)
                                        ↓
                            output/daily-briefing.md
```

## How It Works

### Starting a Workflow
```
User: "Run daily briefing"
Orchestrator: "Starting workflow with new session"
Session Manager: "Created session: daily-briefing-2025-06-03-0900"
```

### During Execution
```
Step 1: Email Scanner runs → saves to context/
Session: Updates to show step 1 complete

Step 2: News Gatherer runs → reads context, saves output  
Session: Updates to show step 2 complete

Step 3: Summary Writer runs → reads all context
Session: Marks workflow complete
```

### On Completion
```
Orchestrator: "Workflow complete in 28 seconds"
Session Manager: "Archived session to completed/"
User: Gets unified briefing in output/
```

## What's Different from Week 1

### Week 1: Static Definitions
- Agents existed but didn't run
- Workflows were just documentation
- No execution mechanism

### Week 2: Living System  
- Orchestrator executes workflows
- Sessions track everything
- Context flows between agents
- Real outputs are produced

## Simple but Powerful

The beauty is in the simplicity:
- No complex state machines
- No proprietary formats
- Just markdown, YAML, and clear instructions
- Everything is readable and debuggable

## Next Week Preview

Week 3 will:
- Migrate existing agents to the new structure
- Add parallel execution
- Implement more sophisticated error handling

But the core remains simple - natural language agents working together!