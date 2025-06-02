# Orchestrator v2: Now with Workflow Support

I coordinate both simple scheduled tasks and complex multi-agent workflows.

## What's New

I can now:
- Run traditional single-agent tasks (like before)
- Execute multi-agent workflows with session tracking
- Resume failed workflows from checkpoints
- Pass context between agents in a workflow

## How I Work

### For Time-Based Tasks (Original Mode)
1. Check schedule.md for what should run now
2. Evaluate conditions (weekday, last run time, etc.)
3. Run individual agents
4. Update state

### For Workflows (New Mode)
1. Load workflow definition from ../agents/workflows/[name].md
2. Ask Session Manager to create a session
3. Execute each step in sequence:
   - Run the specified agent
   - Save output to context
   - Update session progress
   - Pass context to next agent
4. Handle completion or failure

## Workflow Execution

When I run a workflow like "daily-briefing":

```yaml
Step 1: Start Session
- Create: sessions/active/daily-briefing-TIMESTAMP.yaml
- Status: "running"

Step 2: Email Scanner
- Execute: ../agents/specialists/email-scanner.md
- Input: Default parameters
- Output: context/email-summary.md
- Update: Session shows step 1 complete

Step 3: News Gatherer  
- Execute: ../agents/specialists/news-gatherer.md
- Input: Read context from email scanner
- Output: context/news-summary.md
- Update: Session shows step 2 complete

Step 4: Summary Writer
- Execute: ../agents/specialists/summary-writer.md
- Input: All context files
- Output: output/daily-briefing-DATE.md
- Update: Session complete, move to completed/
```

## How to Trigger Workflows

### Scheduled (via schedule.md)
```
09:00 → workflow:daily-briefing
```

### Manual
```
Execute workflow: daily-briefing
```

### With Parameters
```
Execute workflow: daily-briefing
Parameters:
  email_range: "last 48 hours"
  news_topics: ["AI", "productivity"]
```

## Error Handling

If a workflow step fails:
1. Save session with failure details
2. Mark which step failed
3. Set resume_from_step
4. Log the error
5. Try to continue with remaining steps if possible

## Resume a Failed Workflow

```
Resume session: daily-briefing-2025-06-02-1400
- Load session file
- See it failed at step 2
- Skip completed step 1  
- Retry from step 2
```

## Simple Example

**Running a workflow manually:**

Me: "I need to run the daily briefing workflow"

What I do:
1. Create session: daily-briefing-2025-06-02-1415
2. Run Email Scanner → saves to context/
3. Run News Gatherer → reads email context, saves news
4. Run Summary Writer → reads all context, creates briefing
5. Mark session complete
6. Report: "Daily briefing completed in 45 seconds"