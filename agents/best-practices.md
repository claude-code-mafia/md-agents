# Best Practices: Building Great Natural Language Agents

Lessons learned from building real agent systems.

## 1. Agent Design Principles

### Keep Agents Focused
✅ **Good**: "I scan emails for urgent messages"
❌ **Bad**: "I manage all email operations including sending, organizing, and filtering"

One agent, one clear purpose.

### Use First Person
✅ **Good**: "I search X for Claude Code tips"
❌ **Bad**: "This agent searches X for Claude Code tips"

Agents should feel like helpful team members.

### Be Specific About Needs
✅ **Good**: 
```markdown
To do my job, I need:
- Gmail access via CLI tool
- Time range (default: 24 hours)
- Minimum importance threshold
```

❌ **Bad**: "I need email access and some parameters"

## 2. Writing Clear Instructions

### Show, Don't Just Tell
✅ **Good**:
```markdown
## Example
**Input**: "Check emails from last week"
**What I Do**: I scan 147 emails, finding 12 urgent ones
**Output**: Categorized summary with urgent items first
```

❌ **Bad**: "I process emails and return results"

### Include Tool Examples
✅ **Good**:
```bash
# How I check emails
~/Projects/tool-library/gmail-tool/gmail_cli.py list -q "is:unread"
```

❌ **Bad**: "I use the gmail tool"

## 3. Workflow Best Practices

### Clear Step Definition
✅ **Good**:
```markdown
### Step 2: Analyze Emails
- **Who**: Email Analyzer
- **What**: Extract action items from urgent emails
- **Needs**: Email list from Step 1
- **Produces**: `context/action-items.md`
- **Estimated Time**: 10-15 seconds
```

### Explicit Dependencies
Always clarify what each step needs:
```markdown
**Needs**: 
- Email summary from Step 1
- User calendar from context
- Previous action items for deduplication
```

### Plan for Failure
Every workflow should handle errors:
```markdown
**If Email Scanner fails**:
- Log error with timestamp
- Try cached email data if < 2 hours old
- Continue workflow with warning
- Note limitation in final output
```

## 4. Context and State Management

### Use Simple Formats
✅ **Good**: YAML or Markdown for context
```yaml
email_analysis:
  total_scanned: 47
  urgent: 3
  categories:
    - project_updates: 12
    - meetings: 8
```

❌ **Bad**: Complex nested JSON structures

### Meaningful Context Keys
✅ **Good**: `email_urgency_scores`
❌ **Bad**: `data1`, `temp_results`

### Version Your Context
Include metadata:
```yaml
context_version: "1.0"
created_by: "email-scanner"
timestamp: "2025-06-03T10:30:00"
```

## 5. Error Handling Patterns

### Graceful Degradation
```markdown
1. Try primary method
2. Fall back to simpler approach
3. Use cached data if available
4. Provide partial results
5. Always communicate limitations
```

### User-Friendly Errors
✅ **Good**: 
```
"I couldn't access your email (authentication expired). 
I'll continue with other information sources."
```

❌ **Bad**: 
```
"Error: OAuth2 token refresh failed with status 401"
```

### Log Everything
```yaml
error_log:
  - time: "10:30:15"
    agent: "news-gatherer"
    error: "API rate limit"
    action: "Using 1-hour cache"
    impact: "minor"
```

## 6. Performance Optimization

### Identify Parallel Opportunities
Tasks that can run simultaneously:
- Different data sources (email, news, weather)
- Independent analyses
- Multiple file processing

### Cache Strategically
```markdown
## Caching Policy
- News: Valid for 6 hours
- Weather: Valid for 1 hour
- Email counts: Valid for 30 minutes
- Never cache: Personal data, passwords
```

### Set Reasonable Timeouts
```markdown
## Timeouts
- API calls: 30 seconds
- File operations: 10 seconds
- Total workflow: 5 minutes
- Always have a cutoff
```

## 7. Testing and Validation

### Test the Edges
Always test:
- Empty inputs
- Maximum scale
- Missing dependencies
- Network failures
- Concurrent execution

### Document Test Scenarios
```markdown
## Test: Large Email Volume
**Given**: 1000+ emails in inbox
**Expected**: Process in batches, summarize top 50
**Actual**: Completed in 45 seconds
```

## 8. Documentation Standards

### Every Agent Needs
1. Clear purpose statement
2. Input/output examples
3. Error scenarios
4. Integration points
5. Performance expectations

### Keep Examples Real
Use actual scenarios:
```markdown
**Real Example from Production**:
On May 15, processed 234 emails, found urgent contract 
deadline, alerted user 3 hours before cutoff.
```

## 9. Common Pitfalls to Avoid

### Over-Engineering
❌ Complex state machines
✅ Simple status tracking

### Under-Specifying
❌ "Handle errors appropriately"
✅ "On timeout: retry once, then use cache"

### Mixing Concerns
❌ One agent doing multiple unrelated tasks
✅ Separate agents that work together

### Ignoring Edge Cases
❌ Only testing happy path
✅ Planning for empty, broken, and huge

## 10. Maintenance and Evolution

### Version Your Agents
```markdown
# Agent: Email Scanner
Version: 2.1
Changes from 2.0:
- Added Office 365 support
- Improved urgency detection
- Better thread handling
```

### Deprecate Gracefully
```markdown
## Deprecation Notice
This agent will be replaced by "email-scanner-v3" on July 1.
Migration guide: docs/email-scanner-migration.md
```

### Monitor Performance
Track key metrics:
- Execution time trends
- Error rates
- User satisfaction
- Resource usage

## Quick Checklist

Before deploying an agent:
- [ ] Single, clear purpose?
- [ ] Natural language throughout?
- [ ] Examples included?
- [ ] Error handling defined?
- [ ] Tests written?
- [ ] Dependencies documented?
- [ ] Performance acceptable?
- [ ] User-friendly outputs?

## Remember

The best agent is not the most sophisticated - it's the most helpful.

Natural language agents should feel like:
- Explaining to a colleague
- Writing helpful documentation
- Having a conversation

Not like:
- Programming a computer
- Filling out forms
- Following rigid protocols

Build agents you'd want to work with!