# Migration Guide: Converting Agents to Natural Language Format

This guide helps convert existing agents to our new natural language specialist format.

## Quick Conversion Checklist

- [ ] Move agent to `/agents/specialists/`
- [ ] Rewrite in first person ("I am...")
- [ ] Focus on what, not how
- [ ] Make tools usage examples, not requirements
- [ ] Add "When I Need Help" section
- [ ] Include concrete examples

## Format Comparison

### Old Format (Technical)
```markdown
# Agent: EmailChecker
## Metadata
- Version: 1.0
- Type: task-executor
- Tools: [gmail-api]

## Behavior
1. Connect to Gmail API with OAuth
2. Query emails with filter parameters
3. Parse response JSON
4. Categorize by rules engine
5. Output structured YAML
```

### New Format (Natural Language)
```markdown
# Agent: Email Scanner

I am a specialist agent that quickly scans your inbox for important emails.

## What I Do
I check your Gmail inbox and identify which emails need your attention, 
like having an assistant who pre-reads your mail.

## How I Work
1. First, I connect to Gmail and fetch recent emails
2. Then, I categorize them by urgency
3. Finally, I create a summary highlighting what needs attention

[Rest of natural language format...]
```

## Key Transformation Principles

### 1. From Technical to Human
❌ "Execute Gmail API query with parameters"
✅ "I check your Gmail for important messages"

### 2. From Rigid to Flexible
❌ "Must output YAML format with schema X"
✅ "After I'm done, you'll have a categorized list of emails"

### 3. From Implementation to Intent
❌ "Parse JSON response and iterate through message array"
✅ "I scan through your messages looking for urgent items"

## Section-by-Section Migration

### Old "Metadata" → New "What I Do"
Transform technical metadata into a friendly introduction:
```
Old: Type: analyzer, Tools: [twitter-api]
New: I analyze posts from Twitter to find the best content
```

### Old "Behavior" → New "How I Work"
Convert step-by-step implementation to natural workflow:
```
Old: 1. Initialize API client
     2. Set parameters
     3. Execute request
     
New: 1. First, I search for relevant content
     2. Then, I filter for quality
     3. Finally, I select the best items
```

### Old "Output Format" → New "What I Produce"
Change technical schemas to user benefits:
```
Old: Returns: YAML with posts array containing id, text, metrics
New: After I'm done, you'll have:
     - Top posts with full content
     - Engagement metrics
     - Direct links to originals
```

## Adding New Sections

### "When I Need Help" (New)
Add collaboration between agents:
```markdown
I'll ask for help from:
- **Other Agent**: When [specific situation]
- **Another Agent**: If [condition occurs]
```

### "Example" (New)
Add concrete scenario:
```markdown
Here's what it looks like when I work:
**Input**: [What you give me]
**What I Do**: [Natural description of process]
**Output**: [What you receive]
```

## Workflow Migration

### Old Orchestrator Pattern
```yaml
steps:
  - agent: EmailChecker
    params: {timeRange: "24h"}
  - agent: NewsGatherer
    deps: [EmailChecker]
```

### New Workflow Pattern
```markdown
### Step 1: Check Emails
- **Who**: Email Scanner
- **What**: Check Gmail for last 24 hours
- **Produces**: Email summary in context/

### Step 2: Gather News
- **Who**: News Gatherer
- **What**: Find news related to email topics
- **Needs**: Email summary from Step 1
```

## Common Patterns

### Tool Usage
Old: Tool is required, specific API
New: Tool is example, natural language focused

### Error Handling
Old: Exception types and error codes
New: Natural descriptions of what goes wrong

### Dependencies
Old: Explicit requires and imports
New: "I need" and "I'll ask for help from"

## Testing Your Migration

Good migration signs:
1. Non-technical person can understand it
2. Focuses on outcomes, not process
3. Feels like instructions to a helpful assistant
4. Examples make usage clear
5. Collaboration is natural, not forced

## Quick Reference

| Old Term | New Term |
|----------|----------|
| Execute | I check/find/create |
| Parameters | What I need |
| Returns | What I produce |
| Dependencies | When I need help |
| Error | If something goes wrong |
| Schema | Example format |