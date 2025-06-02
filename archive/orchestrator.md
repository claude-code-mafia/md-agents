# Intelligent Orchestrator

Makes smart decisions about which workflows to run based on schedule, conditions, and state.

## Execution Flow

1. **Get Current Time**: Use time tool to get current date/time
2. **Read Schedule**: Check schedule.md for time matches
3. **Load State**: Read orchestrator-state.json for tracking data
4. **Evaluate Conditions**: For each scheduled workflow, check if it should run
5. **Execute Workflows**: Run approved workflows only
6. **Update State**: Record execution times and results

## Workflow Conditions

### morning-report
- **Schedule**: Daily at 09:00
- **Conditions**:
  - Has NOT run successfully today
  - Current day is Monday-Friday
  - Gmail CLI tool is available
- **Action**: Generate email summary and action items

### x-poster
- **Schedule**: Daily at 10:00  
- **Conditions**:
  - Last successful post was > 20 hours ago
  - Twitter API MCP is configured
  - Not a major holiday
- **Action**: Execute /agents/x-poster/main-orchestrator.md

### evening-summary
- **Schedule**: Daily at 18:00
- **Conditions**:
  - Always runs (no skip conditions)
- **Actions**:
  - Check for Knicks game (Oct-June only)
  - Generate daily activity summary
  - Compile agent execution report

### daily-cleanup
- **Schedule**: Daily at 23:00
- **Conditions**:
  - Output folder has > 30 files
- **Action**: Archive old outputs by month

### health-check
- **Schedule**: Every hour at :00
- **Conditions**:
  - Only between 08:00-22:00
  - If previous health check failed
- **Action**: Quick system status check

## Decision Examples

```
Current time: Monday 09:05
Schedule match: morning-report (09:00)
Evaluation:
  - Last run: Sunday 09:00 ✓ (not today)
  - Is weekday: Monday ✓
  - Gmail configured: Yes ✓
Decision: RUN morning-report

Current time: Saturday 10:00  
Schedule match: x-poster (10:00)
Evaluation:
  - Last post: 3 hours ago ✗ (too recent)
Decision: SKIP x-poster
```

## State Management

Track in `output/orchestrator-state.json`:
- Last successful run timestamp for each workflow
- Consecutive failure count
- Total execution count
- Custom workflow data (e.g., last_post_time)

## Error Handling

- If workflow fails, increment failure count
- After 3 consecutive failures, skip workflow for 24 hours
- Log all decisions and reasons
- Continue with remaining workflows

## Time Matching Logic

- **Daily times**: Within 10 minutes of scheduled time
- **Hourly (*:00)**: Within 5 minutes of any hour
- **Weekly**: Exact day + within 10 minutes of time

## Special Instructions

1. Always save detailed decision log to output/orchestrator-decisions-YYYY-MM-DD.md
2. If state file doesn't exist, create it with empty history
3. Never run same workflow twice in same hour (safeguard)
4. Include summary at end showing what ran and what was skipped