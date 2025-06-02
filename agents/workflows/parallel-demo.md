# Workflow: Parallel Demo

This workflow demonstrates parallel execution of independent agents.

## When to Run

Run this workflow when:
- You need multiple types of information quickly
- Agents don't depend on each other's output
- Speed is more important than sequence

## The Team

This workflow uses these specialist agents in parallel groups:
- **Group 1 (Parallel)**:
  - Email Scanner: Check recent emails
  - News Gatherer: Get today's news
  - Weather Agent: Get weather forecast
- **Group 2 (Sequential)**:
  - Summary Writer: Combine all outputs

## The Process

### Parallel Step Group 1: Gather Information
Run these three agents at the same time:

#### Branch A: Email Check
- **Who**: Email Scanner
- **What**: Scan inbox for important messages
- **Produces**: `context/emails.md`

#### Branch B: News Check  
- **Who**: News Gatherer
- **What**: Find relevant news
- **Produces**: `context/news.md`

#### Branch C: Weather Check
- **Who**: Weather Agent (new)
- **What**: Get today's weather
- **Produces**: `context/weather.md`

**Wait for**: All three branches to complete

### Step 2: Combine Results
- **Who**: Summary Writer
- **What**: Read all three context files and create unified summary
- **Needs**: All outputs from Step 1
- **Produces**: `output/parallel-demo-YYYY-MM-DD.md`

## Parallel Execution Rules

When agents run in parallel:
- Each gets its own context namespace
- No shared state during parallel execution
- All must complete before next step
- If one fails, others continue
- Session tracks each branch separately

## Session Tracking Example

```yaml
session_id: parallel-demo-2025-06-03-1000
status: running
steps:
  - name: "Parallel Group 1"
    status: "running"
    branches:
      - name: "Email Scanner"
        status: "completed"
        duration: "5 seconds"
      - name: "News Gatherer"
        status: "running"
        started: "10:00:01"
      - name: "Weather Agent"
        status: "completed"
        duration: "3 seconds"
  - name: "Summary Writer"
    status: "waiting"
    waiting_for: ["News Gatherer"]
```

## Success Looks Like

The workflow succeeded when:
- [ ] All parallel agents completed (even if some failed)
- [ ] At least 2 of 3 information sources succeeded
- [ ] Summary Writer created unified output
- [ ] Total time < sequential time

## Error Handling

- If Email Scanner fails: Continue with news and weather
- If 2+ agents fail: Abort workflow
- If Summary Writer fails: Keep individual outputs
- Always: Log which parallel branches succeeded

## Performance Example

**Sequential Timing:**
- Email Scanner: 10 seconds
- News Gatherer: 15 seconds  
- Weather Agent: 5 seconds
- Summary Writer: 5 seconds
- **Total: 35 seconds**

**Parallel Timing:**
- Parallel Group: 15 seconds (slowest agent)
- Summary Writer: 5 seconds
- **Total: 20 seconds (43% faster!)**