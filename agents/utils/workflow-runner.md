# Workflow Runner Utility

I'm a helper that shows how to execute workflows step by step.

## How to Run a Workflow

### 1. Load the Workflow
Read the workflow definition to understand:
- What agents are involved
- What order to run them
- How to pass context

### 2. Create a Session
```yaml
# Create new session file
session_id: daily-briefing-2025-06-02-1430
workflow: daily-briefing
status: running
current_step: 0
total_steps: 3
```

### 3. Execute Each Step

For each step in the workflow:

#### Step Execution Pattern
```
1. Read step definition
2. Load the agent markdown
3. Execute agent with inputs
4. Save output to context/
5. Update session progress
6. Check for errors
```

#### Context Passing
Each agent can read from context/:
- Previous agent outputs
- Shared workflow data
- Original inputs

### 4. Complete the Workflow
- Mark session as completed
- Move session to completed/
- Report final output location

## Example Execution Trace

```
[14:30:00] Starting workflow: daily-briefing
[14:30:01] Created session: daily-briefing-2025-06-02-1430
[14:30:02] Step 1/3: Running Email Scanner
[14:30:15] Email Scanner complete → context/email-summary.md
[14:30:16] Step 2/3: Running News Gatherer
[14:30:35] News Gatherer complete → context/news-summary.md
[14:30:36] Step 3/3: Running Summary Writer
[14:30:42] Summary Writer complete → output/daily-briefing-2025-06-02.md
[14:30:43] Workflow completed successfully
[14:30:43] Session archived to completed/
```

## Pseudo-code (Natural Language)

```
To run a workflow:
1. "I'll run the daily-briefing workflow"
2. "Creating session to track progress"
3. "Running Email Scanner... found 23 emails"
4. "Running News Gatherer... found 5 relevant stories"
5. "Running Summary Writer... combining everything"
6. "Workflow complete! Briefing saved to output/"
```

## Error Recovery

If step 2 fails:
```
[14:30:16] Step 2/3: Running News Gatherer
[14:30:25] ERROR: News Gatherer failed - API timeout
[14:30:25] Saving checkpoint at step 2
[14:30:25] Workflow paused - can resume later
[14:30:25] Partial results available from step 1
```

To resume:
```
[15:00:00] Resuming workflow: daily-briefing-2025-06-02-1430
[15:00:01] Skipping completed step 1
[15:00:02] Retrying step 2: News Gatherer
[15:00:15] News Gatherer complete
[15:00:16] Continuing with step 3...
```