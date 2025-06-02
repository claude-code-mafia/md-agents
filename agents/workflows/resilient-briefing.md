# Workflow: Resilient Daily Briefing

This workflow creates a daily briefing with robust error handling and recovery.

## When to Run

Run this workflow when:
- Every morning at 8:00 AM
- When you need a briefing despite potential failures
- Testing error recovery mechanisms

## The Team

This workflow uses agents with fallback options:
- **Email Scanner**: Check emails (with fallback)
- **News Gatherer**: Get news (with cache fallback)  
- **Weather Agent**: Get weather (with retry)
- **Summary Writer**: Always runs with available data

## The Process

### Step 1: Email Scan with Fallback
- **Who**: Email Scanner
- **What**: Check Gmail for important emails
- **Error Handling**:
  ```yaml
  on_error:
    - type: "auth_failure"
      action: "Skip emails, note in summary"
    - type: "timeout"
      action: "Retry once, then use cached if available"
    - type: "rate_limit"
      action: "Use basic email count only"
  ```
- **Produces**: `context/emails.md` or `context/email-error.md`

### Step 2: News with Cache Fallback
- **Who**: News Gatherer
- **What**: Get today's news
- **Error Handling**:
  ```yaml
  on_error:
    - type: "api_down"
      action: "Use cached news if < 6 hours old"
    - type: "no_cache"
      action: "Try alternate news source"
    - type: "all_failed"
      action: "Continue without news"
  ```
- **Produces**: `context/news.md` or cached version

### Step 3: Weather with Retry
- **Who**: Weather Agent
- **What**: Get weather forecast
- **Error Handling**:
  ```yaml
  retry_policy:
    attempts: 3
    backoff: [5s, 15s, 30s]
  on_final_failure:
    action: "Use yesterday's forecast with warning"
  ```
- **Produces**: `context/weather.md`

### Step 4: Resilient Summary
- **Who**: Summary Writer
- **What**: Create briefing with all available data
- **Handles**:
  - Missing sections gracefully
  - Includes error notifications
  - Prioritizes successful data
- **Always Produces**: `output/briefing-YYYY-MM-DD.md`

## Error Recovery Examples

### Scenario 1: Email Auth Fails
```
[08:00:05] Email Scanner: Gmail auth failed
[08:00:06] Error Handler: Skipping email section
[08:00:07] Continue with news...
[08:00:20] Summary includes: "⚠️ Email unavailable - please check manually"
```

### Scenario 2: Multiple Failures
```
[08:00:05] Email Scanner: ✓ Found 12 important emails
[08:00:15] News Gatherer: ✗ API timeout
[08:00:16] Error Handler: Checking cache... found 4-hour old news ✓
[08:00:25] Weather Agent: ✗ Service unavailable
[08:00:30] Weather Agent: Retry 1... ✗
[08:00:45] Weather Agent: Retry 2... ✓ Success!
[08:00:50] Summary: Includes all sections
```

### Scenario 3: Graceful Degradation
```
Emails: ✓ Full data
News: ⚠️ Using 4-hour cache  
Weather: ✗ Unavailable
Summary: Created with 2/3 sources
```

## Success Criteria

The workflow succeeded when:
- [ ] At least one data source provided information
- [ ] Summary was created (even if degraded)
- [ ] All errors were logged with recovery attempts
- [ ] User was informed of any limitations

## Session Error Log Example

```yaml
session_id: resilient-briefing-2025-06-03-0800
completed: true
errors_encountered: 2
errors:
  - agent: "news-gatherer"
    error: "API timeout"
    recovery: "Used 4-hour old cache"
    impact: "minor"
    
  - agent: "weather-agent"  
    error: "Service unavailable"
    recovery: "Succeeded on retry 2"
    impact: "none"
    
summary_quality: "good"
sections_included: ["emails", "news", "weather"]
```

## Final Output Example

Even with errors, produces useful output:
```markdown
# Daily Briefing - June 3, 2025

⚠️ Note: Using cached news from 4:00 AM

## 📧 Emails (12 important)
[Full email summary]

## 📰 News (cached)
[4-hour old news, still relevant]

## ☀️ Weather
[Current weather after retry]

---
Generated with some limitations. All critical info included.
```