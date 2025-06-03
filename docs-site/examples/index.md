---
layout: docs
title: Examples
description: Learn by example with real-world agent implementations
---

These examples demonstrate the power and flexibility of md agents across various use cases.

## Basic Examples

Start here to understand fundamental patterns.

### Hello World Agent

The simplest possible agent:

```markdown
# Specialist: Greeter

<<You greet people warmly.>>

## Behavior
1. Say hello to {name}
2. Add a friendly message
3. Wish them a great day

## Output
- greeting: str
```

### Weather Agent

Integration with external tools:

```markdown
# Specialist: Weather Reporter

<<You provide weather updates.>>

## Input
- location: str

## Behavior
1. Use [weather-api] to get conditions
2. Format temperature in both F and C
3. Include "feels like" temperature
4. Add clothing recommendations

## Output
- temperature_f: int
- temperature_c: int
- conditions: str
- recommendation: str
```

## Workflow Examples

Sequential multi-agent pipelines.

### Daily Briefing

```markdown
# Workflow: Daily Briefing

Start your day with personalized updates.

## Triggers
- **Schedule**: 0 7 * * *  # 7am daily

## Steps

### Step 1: Gather Information
- **Execute**: %email-scanner%
- **Get**: {emails}

### Step 2: Check Weather
- **Execute**: %weather-reporter%
- **With**: location = ~global.home_city~
- **Get**: {weather}

### Step 3: Get News
- **Execute**: %news-gatherer%
- **With**: 
    - topics = ~memory.interests~
    - max_articles = 5
- **Get**: {news}

### Step 4: Create Summary
- **Execute**: %summary-writer%
- **With**:
    - emails = {emails}
    - weather = {weather}
    - news = {news}
    - style = "conversational"
- **Save**: output/briefing-{date}.md
```

### Research Pipeline

```markdown
# Workflow: Research Pipeline

Deep research on any topic.

## Input
- topic: str
- depth: "quick" | "standard" | "comprehensive"

## Steps

### Step 1: Initial Search
- **Execute**: %web-searcher%
- **With**: 
    - query = {topic}
    - max_results = 20 if {depth} == "comprehensive" else 10
- **Get**: {sources}

### Step 2: Fact Extraction
- **Execute**: %fact-extractor%
- **With**: sources = {sources}
- **Get**: {facts}

### Step 3: Verify Facts
- **If**: {depth} != "quick"
- **Execute**: %fact-checker%
- **With**: facts = {facts}
- **Get**: {verified_facts}

### Step 4: Synthesize
- **Execute**: %research-synthesizer%
- **With**: 
    - facts = {verified_facts} or {facts}
    - style = "academic" if {depth} == "comprehensive" else "summary"
- **Output**: research_report
```

## Coordinator Examples

Dynamic, intelligent orchestration.

### Smart Assistant

```markdown
# Coordinator: Smart Assistant

<<You route requests to appropriate specialists.>>

## Behavior

Analyze user request for intent:

### Information Queries
- Weather → %weather-reporter%
- News → %news-gatherer%  
- Email → %email-scanner%
- Calendar → %calendar-checker%

### Action Requests  
- "Schedule..." → %calendar-manager%
- "Email..." → %email-composer%
- "Remind..." → %reminder-setter%

### Complex Requests
- Multiple intents → Execute in parallel
- Research needs → %research-director%
- Analysis → %data-analyst%

## Example Patterns

"What's my day look like?"
1. %calendar-checker% → meetings
2. %email-scanner% → urgent emails
3. %weather-reporter% → weather
4. Combine into daily overview

"Research competitor analysis for [company]"
1. Delegate to %research-director%
2. Monitor progress
3. Request clarification if needed
```

### Research Director

```markdown
# Coordinator: Research Director

<<You orchestrate comprehensive research projects.>>

## Input
- query: str
- depth: int = 2  # 1-3 scale
- time_limit: int = 300  # seconds

## Behavior

### Phase 1: Query Analysis
Understand the research need:
- Is it factual? → Start with %fact-finder%
- Is it current? → Prioritize %news-gatherer%
- Is it analytical? → Include %data-analyst%
- Is it controversial? → Add %fact-checker%

### Phase 2: Initial Research
Based on query type, execute:
- %web-searcher% with focused queries
- %academic-searcher% for scholarly needs
- %news-gatherer% for current events

### Phase 3: Deep Dive
If depth > 1:
- Extract key themes from initial research
- Spawn targeted searches for each theme
- Run %fact-checker% on critical claims

### Phase 4: Synthesis
Always conclude with:
- %research-synthesizer% to combine findings
- %citation-formatter% for sources
- %summary-writer% for executive summary

## State Tracking
- Store research trail in ~session.research_path~
- Cache verified facts in ~cache.verified_facts~
- Update ~memory.research_topics~ for future context
```

## Integration Examples

### Slack Bot Agent

```markdown
# Specialist: Slack Bot

<<You respond to Slack messages intelligently.>>

## Triggers
- **Event**: Slack message received

## Input
- message: str
- user: str
- channel: str

## Behavior

1. Parse message for @mentions and commands
2. If question about weather → %weather-reporter%
3. If request for summary → %summary-writer%
4. If scheduling → %calendar-manager%
5. Format response for Slack (markdown)
6. Use [slack-api] to post response

## Error Handling
- If agent fails → Post friendly error
- If rate limited → Queue for retry
- Always → Log in ~memory.slack_interactions~
```

### Email Auto-Responder

```markdown
# Workflow: Email Auto-Responder

Intelligently respond to emails.

## Triggers
- **Schedule**: */15 * * * *  # Every 15 minutes

## Steps

### Step 1: Check Emails
- **Execute**: %email-scanner%
- **With**: 
    - time_range = "15 minutes"
    - unread_only = true
- **Get**: {new_emails}

### Step 2: Classify Each Email
- **For each**: email in {new_emails}
- **Execute**: %email-classifier%
- **Get**: {classification}

### Step 3: Generate Responses
- **If**: {classification} == "auto-reply"
- **Execute**: %email-composer%
- **With**:
    - context = {email}
    - tone = "professional"
    - include_signature = true
- **Get**: {draft}

### Step 4: Send Responses
- **Execute**: %email-sender%
- **With**: 
    - draft = {draft}
    - delay_minutes = 5  # Appear human
```

## Advanced Patterns

### Parallel Execution

```markdown
## Steps

### Step 1: Parallel Research
- **Parallel**:
  - %news-gatherer% → {news}
  - %social-monitor% → {social}
  - %competitor-tracker% → {competitors}

### Step 2: Analyze Together
- **Execute**: %trend-analyzer%
- **With**: all_data = {news} + {social} + {competitors}
```

### Conditional Flows

```markdown
### Step 3: Verify If Needed
- **If**: {confidence} < 0.8
  - **Execute**: %fact-checker%
  - **Get**: {verified}
- **Else**:
  - **Set**: {verified} = {original}
```

### State Persistence

```markdown
## Behavior
1. Check ~memory.last_analysis_time~
2. If older than 1 hour:
   - Run fresh analysis
   - Update ~memory.last_analysis_time~
3. Else:
   - Use ~cache.recent_analysis~
```

## Testing Your Agents

### Test Individual Agents
```bash
./scripts/run-agents.sh weather-reporter --location "Tokyo"
```

### Test Workflows
```bash
./scripts/run-agents.sh daily-briefing --dry-run
```

### Test Coordinators
```bash
./scripts/run-agents.sh smart-assistant "What's the weather and news?"
```

## Best Practices from Examples

1. **Start Simple**: Begin with basic agents, then compose
2. **Clear Interfaces**: Define explicit inputs/outputs
3. **Handle Errors**: Always have fallback behavior
4. **Use State Wisely**: Only persist what's necessary
5. **Test Incrementally**: Verify each agent works alone

## Create Your Own

Use these examples as templates:

1. Copy an example that's similar to your need
2. Modify the behavior section
3. Adjust inputs/outputs
4. Test with sample data
5. Integrate into workflows

Ready to dive deeper? Check our [API Reference]({{ '/api/' | relative_url }}) for detailed specifications.