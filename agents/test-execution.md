# Test Execution: Daily Briefing Workflow

This shows a complete execution of the daily briefing workflow.

## Setup

Let's run through a complete workflow execution to test our system.

### Initial State
- Time: Monday, 9:00 AM
- Trigger: Scheduled via orchestrator
- Workflow: daily-briefing

## Execution Transcript

### 1. Orchestrator Starts
```
[09:00:00] Orchestrator: "Time matches schedule - running workflow: daily-briefing"
[09:00:01] Orchestrator: "Asking Session Manager to create session"
```

### 2. Session Creation
```yaml
# sessions/active/daily-briefing-2025-06-03-0900.yaml
workflow: daily-briefing
session_id: daily-briefing-2025-06-03-0900
started_at: 2025-06-03T09:00:01
status: running
current_step: 1
total_steps: 3
```

### 3. Step 1: Email Scanner
```
[09:00:02] Running: Email Scanner
[09:00:03] Email Scanner: "Checking Gmail for last 24 hours"
[09:00:08] Email Scanner: "Found 32 emails - 4 urgent, 10 important"
[09:00:09] Email Scanner: "Saving summary to context/email-summary.md"
```

**Context Output**:
```markdown
# Email Summary - 2025-06-03 09:00

## Urgent (4)
1. Boss: "Budget meeting moved to 10 AM today"
2. Client ABC: "Contract needs signature by noon"
3. IT: "Mandatory security update required"
4. Finance: "Expense report overdue"

## Important (10)
- Team meeting notes from Friday
- Project X status update needed
- 3 calendar invites for this week
[...]
```

### 4. Step 2: News Gatherer
```
[09:00:10] Running: News Gatherer
[09:00:11] News Gatherer: "Reading email context for relevant topics"
[09:00:12] News Gatherer: "Found topics: budget, contracts, security"
[09:00:13] News Gatherer: "Searching for related news"
[09:00:20] News Gatherer: "Found 5 relevant stories"
[09:00:21] News Gatherer: "Saving to context/news-summary.md"
```

**Context Output**:
```markdown
# News Summary - 2025-06-03 09:00

## Business News (Related to your budget meeting)
1. "Tech Companies Tighten Budgets in 2025" - WSJ
   - Industry trend toward efficiency
   - May be relevant for your 10 AM meeting

## Security News (Related to IT update)
2. "New Zero-Day Vulnerability Discovered" - TechCrunch
   - Affects systems like yours
   - Explains urgency of IT's request
[...]
```

### 5. Step 3: Summary Writer
```
[09:00:22] Running: Summary Writer
[09:00:23] Summary Writer: "Reading all context files"
[09:00:24] Summary Writer: "Combining email and news summaries"
[09:00:25] Summary Writer: "Creating unified briefing"
[09:00:26] Summary Writer: "Saving to output/daily-briefing-2025-06-03.md"
```

**Final Output**:
```markdown
# Daily Briefing - Monday, June 3, 2025

## ⚡ Immediate Actions Required
1. **Budget Meeting** - Moved to 10 AM TODAY (was 2 PM)
   - Related: WSJ reports tech budget tightening trend
   - Prepare efficiency proposals

2. **Contract Signature** - Due by noon
   - Client ABC awaiting
   - Check legal review status

## 🔒 Security Alert
- IT mandating security update (zero-day vulnerability reported)
- Complete before end of day

## 📅 Your Day
- 10:00 AM - Budget meeting (UPDATED TIME)
- 11:30 AM - Team standup
- 2:00 PM - Free (was budget meeting)

## 📰 Relevant News
[5 stories related to your work today]

---
Generated at 9:00 AM | Next update at 2:00 PM
```

### 6. Workflow Completion
```
[09:00:27] Orchestrator: "All steps completed successfully"
[09:00:28] Session Manager: "Moving session to completed/"
[09:00:29] Orchestrator: "Daily briefing ready at output/daily-briefing-2025-06-03.md"
```

**Final Session State**:
```yaml
status: completed
completed_at: 2025-06-03T09:00:29
total_time: 28 seconds
steps:
  - name: "Email Scanner"
    status: "completed"
    time: 7 seconds
  - name: "News Gatherer"
    status: "completed"
    time: 11 seconds
  - name: "Summary Writer"
    status: "completed"
    time: 4 seconds
outputs:
  final: "output/daily-briefing-2025-06-03.md"
  intermediate:
    - "context/email-summary.md"
    - "context/news-summary.md"
```

## Success! 

The workflow:
1. ✅ Created and tracked session
2. ✅ Ran agents in sequence
3. ✅ Passed context between agents
4. ✅ Produced unified output
5. ✅ Archived session when complete

Total time: 28 seconds for complete morning briefing!