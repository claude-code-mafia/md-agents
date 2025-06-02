# Error Handler Utility

I help workflows handle errors gracefully and recover when possible.

## Error Categories

### 1. Recoverable Errors
These we can retry or work around:
- **API Timeout**: Wait and retry with backoff
- **Rate Limit**: Pause and retry later
- **Missing Input**: Use defaults or skip
- **Partial Failure**: Use what succeeded

### 2. Non-Recoverable Errors
These stop the workflow:
- **Invalid Credentials**: Can't proceed without access
- **Critical Tool Missing**: Required functionality unavailable
- **Data Corruption**: Unsafe to continue

## Error Handling Patterns

### Pattern 1: Retry with Backoff
```yaml
error: "API timeout"
attempts: 3
backoff: [5s, 15s, 60s]
action: 
  - Log attempt number
  - Wait backoff[attempt]
  - Retry operation
  - If all fail: Mark as failed
```

### Pattern 2: Graceful Degradation
```yaml
error: "News API unavailable"
action:
  - Log error with timestamp
  - Skip news gathering
  - Note in output: "News unavailable"
  - Continue with other agents
```

### Pattern 3: Fallback Options
```yaml
error: "Primary email tool failed"
fallback_chain:
  1. Try alternate email tool
  2. Try basic email check
  3. Skip email entirely
  4. Note limitation in output
```

### Pattern 4: Circuit Breaker
```yaml
error_threshold: 3 failures in 10 minutes
status: "open" | "closed" | "half-open"
action:
  - If closed: Normal operation
  - If open: Skip this agent for 30 minutes
  - If half-open: Try once, reset if success
```

## Session Error Tracking

Errors are tracked in session:
```yaml
errors:
  - agent: "news-gatherer"
    timestamp: "2025-06-03T10:15:23"
    type: "timeout"
    message: "API request timed out after 30s"
    recovery: "Will retry in next run"
    
  - agent: "email-scanner"
    timestamp: "2025-06-03T10:16:45"
    type: "auth_failed"
    message: "Gmail authentication expired"
    recovery: "Skipped email scanning"
```

## Recovery Strategies

### 1. Checkpoint Recovery
After each successful step:
- Save state to checkpoint
- On failure: Resume from last checkpoint
- Skip completed work

### 2. Partial Results
If workflow partially completes:
- Save what succeeded
- Mark incomplete sections
- Allow manual completion

### 3. Alternative Paths
If primary path fails:
- Check for alternate agents
- Use simplified workflow
- Provide degraded output

## Error Messages for Users

### Good Error Message
```
❌ Weather data temporarily unavailable (API timeout)
→ Tried 3 times over 80 seconds
→ Other parts of your briefing are ready
→ Weather will be included in next run
```

### Bad Error Message
```
Error: Connection refused: ETIMEDOUT
```

## Implementation Example

In a workflow:
```markdown
### Step 2: Gather News
- **Who**: News Gatherer
- **What**: Get today's news
- **Error Handling**:
  - On timeout: Retry up to 3 times
  - On API limit: Use cached news if < 6 hours old
  - On failure: Continue without news
  - Always: Log error details
```

## Best Practices

1. **Log Everything**: Timestamp, agent, error type, attempted recovery
2. **Fail Fast**: Don't retry known permanent failures
3. **Communicate Clearly**: Tell user what failed and what still worked
4. **Preserve Progress**: Never lose successful work
5. **Learn from Patterns**: Track common failures for improvement