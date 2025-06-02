# Workflow: Daily Briefing

This workflow creates a comprehensive morning briefing by coordinating multiple specialist agents.

## When to Run

Run this workflow when:
- Every weekday at 8:00 AM
- When you say "prepare my daily briefing"
- Before starting your workday

## The Team

This workflow uses these specialist agents:
- **Email Scanner**: Checks your inbox for important messages
- **News Gatherer**: Finds relevant news based on your interests
- **Summary Writer**: Combines everything into one clear briefing

## The Process

### Step 1: Scan Emails
- **Who**: Email Scanner
- **What**: Check Gmail for messages from the last 24 hours
- **Needs**: Gmail access
- **Produces**: Categorized email summary saved to `context/email-summary.md`

### Step 2: Gather News
- **Who**: News Gatherer  
- **What**: Find relevant news, using email context for topics
- **Needs**: Email summary (to identify relevant topics)
- **Produces**: News digest saved to `context/news-summary.md`

### Step 3: Create Briefing
- **Who**: Summary Writer
- **What**: Combine email and news summaries into unified briefing
- **Needs**: Both summaries from steps 1 and 2
- **Produces**: Complete briefing at `output/daily-briefing-YYYY-MM-DD.md`

## Success Looks Like

The workflow succeeded when:
- [ ] Email Scanner found and categorized emails
- [ ] News Gatherer found relevant stories
- [ ] Summary Writer created unified briefing
- [ ] Final output saved to output folder

## If Something Goes Wrong

- If Email Scanner fails: Continue with news only, note email unavailable
- If News Gatherer fails: Create briefing with just emails
- If Summary Writer fails: Keep individual summaries available
- Always: Save progress so we can see what worked

## Example Session

```yaml
# Start: 8:00 AM
Email Scanner: "Found 23 emails, 3 urgent"
News Gatherer: "Found 5 relevant stories based on your AI meeting"
Summary Writer: "Created briefing highlighting deadline change and AI news"
# Complete: 8:02 AM
```

## Manual Trigger

To run this workflow manually:
```bash
# From the agents directory
# The orchestrator will read this workflow and execute it
Run workflow: daily-briefing
```