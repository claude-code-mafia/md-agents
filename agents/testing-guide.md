# Testing Guide: Natural Language Agent Testing

How to test agents and workflows without writing code.

## Testing Philosophy

Since our agents use natural language, our tests do too:
- Describe scenarios in plain English
- Check outputs make sense
- Verify agents work together
- Ensure errors are handled gracefully

## 1. Agent Testing

### Test Template

Create `tests/test-[agent-name].md`:

```markdown
# Test: Email Scanner

## Test 1: Normal Operation
**Given**: 25 emails in inbox (3 urgent, 10 important, 12 FYI)
**When**: Email Scanner runs
**Then**: 
- Summary shows all three categories
- Urgent emails listed first
- Count matches reality

## Test 2: Empty Inbox  
**Given**: No new emails
**When**: Email Scanner runs
**Then**: Reports "No new emails"

## Test 3: API Failure
**Given**: Gmail API is down
**When**: Email Scanner runs  
**Then**: 
- Logs error appropriately
- Returns graceful failure message
- Doesn't crash workflow
```

### Running Agent Tests

```bash
# Test individual agent
Test agent: email-scanner
Scenario: "25 emails with 3 urgent"

# What happens:
1. Test framework sets up scenario
2. Runs agent with test input
3. Checks output matches expectations
4. Reports pass/fail
```

## 2. Workflow Testing

### Integration Test Example

Create `tests/test-daily-briefing-workflow.md`:

```markdown
# Test: Daily Briefing Workflow

## Scenario 1: All Systems Go
**Setup**:
- Email Scanner: Will find 5 urgent emails
- News Gatherer: Will find 3 relevant stories
- Weather Agent: Will report sunny, 72°F

**Execute**: Run daily-briefing workflow

**Verify**:
- Session completes successfully
- All three sections present in output
- No errors in session log
- Output saved to correct location

## Scenario 2: Email Scanner Fails
**Setup**:
- Email Scanner: Will fail with auth error
- News Gatherer: Will succeed
- Weather Agent: Will succeed

**Execute**: Run daily-briefing workflow

**Verify**:
- Workflow continues despite email failure
- Output includes news and weather
- Notes email unavailable
- Error logged properly
```

## 3. Test Utilities

### Test Data Generator

`tests/utils/test-data-generator.md`:
```markdown
# Agent: Test Data Generator

I create realistic test scenarios for agents.

## What I Can Generate
- Email lists with various urgency levels
- News articles on specific topics
- Weather conditions
- Error scenarios
- Edge cases

## Example Usage
Generate: "Email test data"
Parameters:
  - Total emails: 30
  - Urgent: 5
  - Important: 10
  - FYI: 15
  - Include: "boss email about deadline"
```

### Test Runner

`tests/utils/test-runner.md`:
```markdown
# Agent: Test Runner

I execute test scenarios and report results.

## How I Run Tests
1. Load test scenario
2. Set up test data
3. Execute agent/workflow
4. Compare actual vs expected
5. Generate test report

## Test Report Format
```
Test Suite: Email Scanner
Tests Run: 5
Passed: 4
Failed: 1

FAILED: Test 3 - API Failure
Expected: Graceful error message
Actual: No output produced
```
```

## 4. Testing Patterns

### Happy Path Testing
Test normal operation:
```markdown
Given: Normal inputs
When: Agent runs
Then: Expected outputs produced
```

### Edge Case Testing
Test boundaries:
```markdown
- Empty inputs
- Maximum inputs
- Unusual formats
- Special characters
```

### Error Testing
Test failure handling:
```markdown
- API failures
- Missing tools
- Invalid inputs
- Timeout scenarios
```

### Performance Testing
Test efficiency:
```markdown
Measure:
- Execution time
- Parallel vs sequential
- Resource usage
```

## 5. Continuous Testing

### Pre-Commit Tests
Before committing changes:
```bash
# Quick smoke tests
Test suite: smoke
- Basic agent responses
- Workflow starts correctly
- No syntax errors
```

### Daily Test Suite
Comprehensive testing:
```bash
# Full regression
Test suite: daily
- All agent scenarios
- All workflow paths
- Error conditions
- Performance benchmarks
```

## 6. Test Examples

### Testing Context Passing
```markdown
## Test: Context Flow
**Step 1**: Email Scanner produces:
```yaml
topics: ["AI meeting", "budget review"]
```

**Step 2**: News Gatherer reads topics
**Verify**: Searches for "AI" and "budget" news

**Step 3**: Summary Writer combines all
**Verify**: Links AI news to meeting
```

### Testing Parallel Execution
```markdown
## Test: Parallel Performance
**Setup**: Three agents that each take 10 seconds

**Sequential Test**:
- Total time: ~30 seconds

**Parallel Test**:
- Total time: ~10 seconds
- All outputs still correct
```

## 7. Debugging Failed Tests

When a test fails:

1. **Check the session log**:
   ```yaml
   errors:
     - agent: "news-gatherer"
       error: "API key missing"
   ```

2. **Verify test data**:
   - Is test data realistic?
   - Are mocks working?

3. **Run in isolation**:
   - Test just the failing agent
   - Simplify inputs

4. **Check dependencies**:
   - Required tools available?
   - Context files present?

## Best Practices

1. **Test One Thing**: Each test has single purpose
2. **Use Realistic Data**: Test with production-like inputs
3. **Test the Edges**: Empty, full, broken
4. **Document Why**: Explain what you're testing
5. **Keep Tests Simple**: Natural language, not code

## Example Test Run

```
$ run-tests agents/daily-briefing

Testing Daily Briefing Workflow
==============================
✓ Test 1: Normal operation - PASSED (15s)
✓ Test 2: Email failure handling - PASSED (12s)
✓ Test 3: Parallel execution - PASSED (8s)
✗ Test 4: Cache fallback - FAILED
  Expected: Use 6-hour old cache
  Actual: No cache found

Tests: 4 | Passed: 3 | Failed: 1
```

## Creating Your Own Tests

1. Copy test template
2. Describe scenario naturally
3. Define clear expectations
4. Run and verify
5. Add to test suite

Remember: If you can describe it, you can test it!