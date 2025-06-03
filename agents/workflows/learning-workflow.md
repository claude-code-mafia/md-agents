# Workflow: Learning Workflow

This workflow demonstrates agents learning and sharing state.

*Note: This example references some hypothetical agents (pattern-analyzer, preference-updater) to demonstrate concepts.*

## Triggers
- **Schedule**: 0 18 * * *  # 6pm daily
- **Command**: "learn from today"

## Input
- categories: list[str] = ["emails", "tasks", "research"]

## Steps

### Step 1: Analyze Email Patterns
- **Execute**: %email-scanner%
- **With**: 
  - time_range = "7 days"
  - max_results = 200
- **Get**: {email_patterns}
- **Learn**: Update ~memory.email_patterns.common_senders~

### Step 2: Extract Topics
- **Execute**: %pattern-analyzer%
- **With**: 
  - data = {email_patterns}
  - look_for = ["recurring_topics", "urgent_keywords", "meeting_patterns"]
- **Get**: {patterns}
- **Share**: Store in ~global.learned_topics~

### Step 3: Update Preferences
- **Execute**: %preference-updater%
- **With**:
  - new_patterns = {patterns}
  - current = ~memory.user_preferences~
- **Get**: {updated_prefs}
- **Save**: ~memory.user_preferences~

### Step 4: Prepare Tomorrow
- **Execute**: %daily-assistant%
- **With**:
  - request = "What should I prepare for tomorrow based on patterns?"
  - context = {patterns}
- **Get**: {tomorrow_prep}
- **Save**: ~cache.tomorrow_briefing_hints~

## State Updates
This workflow updates multiple state locations:
- ~memory.email_patterns~ - Email trends
- ~global.learned_topics~ - Shared topic knowledge
- ~memory.user_preferences~ - Refined preferences
- ~cache.tomorrow_briefing_hints~ - Next day prep

## Success
- [ ] Patterns identified
- [ ] State updated across agents
- [ ] Tomorrow's prep ready

## Example State Changes

Before:
```yaml
~memory.email_patterns.common_senders~: ["boss@company.com"]
~global.learned_topics~: ["AI", "cloud"]
```

After:
```yaml
~memory.email_patterns.common_senders~: ["boss@company.com", "client@important.com"]
~global.learned_topics~: ["AI", "cloud", "deadline-june-10", "budget-review"]
~cache.tomorrow_briefing_hints~: ["Check budget docs", "AI meeting prep"]
```