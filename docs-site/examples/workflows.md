---
layout: docs
title: Workflow Examples
description: Multi-agent sequential pipelines
---

These examples show how to combine multiple agents into workflows.

## Daily Briefing Workflow

A morning briefing that combines multiple sources:

```markdown
# Workflow: Daily Briefing

Your personalized morning update.

## Triggers
- **Schedule**: 0 7 * * *  # 7am daily
- **Command**: "morning briefing"

## Steps

### Step 1: Check Weather
- **Execute**: %weather-reporter%
- **With**: location = ~global.home_city~
- **Get**: {weather}

### Step 2: Scan Emails  
- **Execute**: %email-scanner%
- **With**: 
    - time_range = "8 hours"
    - categories = ["urgent", "important"]
- **Get**: {emails}

### Step 3: Get News
- **Execute**: %news-gatherer%
- **With**: 
    - topics = ~memory.interests~
    - max_articles = 5
- **Get**: {news}

### Step 4: Create Summary
- **Execute**: %briefing-writer%
- **With**:
    - weather = {weather}
    - emails = {emails}
    - news = {news}
    - style = "conversational"
- **Save**: output/daily-briefing-{date}.md
```

## Research Pipeline

Multi-stage research workflow:

```markdown
# Workflow: Research Pipeline

Comprehensive research on any topic.

## Input
- topic: str
- depth: "quick" | "standard" | "deep" = "standard"

## Steps

### Step 1: Initial Search
- **Execute**: %web-searcher%
- **With**: 
    - query = {topic}
    - max_results = 10 * {depth_multiplier}
- **Get**: {search_results}

### Step 2: Extract Facts
- **Execute**: %fact-extractor%
- **With**: sources = {search_results}
- **Get**: {raw_facts}

### Step 3: Verify Facts
- **If**: {depth} != "quick"
  - **Execute**: %fact-checker%
  - **With**: facts = {raw_facts}
  - **Get**: {verified_facts}
- **Else**:
  - **Set**: {verified_facts} = {raw_facts}

### Step 4: Find Experts
- **If**: {depth} == "deep"
  - **Execute**: %expert-finder%
  - **With**: topic = {topic}
  - **Get**: {experts}

### Step 5: Synthesize
- **Execute**: %research-synthesizer%
- **With**:
    - facts = {verified_facts}
    - experts = {experts}?
    - style = "academic"
- **Save**: output/research-{topic}-{timestamp}.md
```

## Data Processing Pipeline

ETL-style data workflow:

```markdown
# Workflow: Data Pipeline

Extract, transform, and load data.

## Triggers
- **Schedule**: 0 2 * * *  # 2am daily

## Steps

### Step 1: Extract Data
- **Parallel**:
  - %database-extractor% → {db_data}
  - %api-fetcher% → {api_data}
  - %file-reader% → {file_data}

### Step 2: Combine Sources
- **Execute**: %data-merger%
- **With**:
    - sources = [{db_data}, {api_data}, {file_data}]
    - merge_key = "id"
- **Get**: {combined_data}

### Step 3: Clean Data
- **Execute**: %data-cleaner%
- **With**: 
    - data = {combined_data}
    - rules = ~global.cleaning_rules~
- **Get**: {clean_data}

### Step 4: Transform
- **Execute**: %data-transformer%
- **With**:
    - data = {clean_data}
    - schema = ::OutputSchema::
- **Get**: {transformed_data}

### Step 5: Validate
- **Execute**: %data-validator%
- **With**: data = {transformed_data}
- **Get**: {validation_report}

### Step 6: Load
- **If**: {validation_report.errors} == 0
  - **Execute**: %data-loader%
  - **With**: data = {transformed_data}
- **Else**:
  - **Execute**: %error-handler%
  - **With**: report = {validation_report}
```

## Social Media Monitor

Monitor and respond to social media:

```markdown
# Workflow: Social Monitor

Track mentions and engage appropriately.

## Triggers
- **Schedule**: */30 * * * *  # Every 30 minutes

## Steps

### Step 1: Check Mentions
- **Execute**: %mention-scanner%
- **With**: 
    - platforms = ["twitter", "linkedin"]
    - since = ~memory.last_check~
- **Get**: {mentions}

### Step 2: Analyze Sentiment
- **For each**: mention in {mentions}
  - **Execute**: %sentiment-analyzer%
  - **With**: text = {mention.text}
  - **Get**: {mention.sentiment}

### Step 3: Categorize
- **Execute**: %mention-categorizer%
- **With**: mentions = {mentions}
- **Get**: {categorized}

### Step 4: Generate Responses
- **For each**: category in {categorized}
  - **If**: {category.needs_response}
    - **Execute**: %response-generator%
    - **With**: 
        - mentions = {category.mentions}
        - tone = {category.suggested_tone}
    - **Get**: {category.responses}

### Step 5: Review and Send
- **Execute**: %response-reviewer%
- **With**: responses = {all_responses}
- **Get**: {approved_responses}

### Step 6: Post Responses
- **Execute**: %social-poster%
- **With**: responses = {approved_responses}
- **Save**: output/social-responses-{date}.json

### Step 7: Update State
- **Set**: ~memory.last_check~ = {current_time}
```

## Error Recovery Workflow

Workflow with comprehensive error handling:

```markdown
# Workflow: Resilient Processor

Process with automatic error recovery.

## Input
- data_source: str
- max_retries: int = 3

## Steps

### Step 1: Fetch Data
- **Try**:
    - **Execute**: %data-fetcher%
    - **With**: source = {data_source}
    - **Get**: {data}
- **On Error**:
    - **If**: {retry_count} < {max_retries}
      - **Wait**: 5 * {retry_count} seconds
      - **Retry**: Step 1
    - **Else**:
      - **Execute**: %fallback-fetcher%
      - **Get**: {data}

### Step 2: Process
- **Execute**: %processor%
- **With**: data = {data}
- **Get**: {processed}
- **On Error**:
    - **Log**: error to ~session.errors~
    - **Execute**: %error-notifier%
    - **Continue**: with partial data

### Step 3: Save Results
- **Try**:
    - **Save**: {processed} to output/result.json
- **On Error**:
    - **Save**: to backup location
    - **Alert**: administrator
```

## Running Workflows

Execute workflows with:

```bash
# Run by name
./scripts/run-agents.sh daily-briefing

# With parameters
./scripts/run-agents.sh research-pipeline --topic "quantum computing" --depth deep

# Dry run
./scripts/run-agents.sh data-pipeline --dry-run
```

## Best Practices

1. **Test Steps Individually**: Verify each agent works before combining
2. **Handle Partial Failures**: Plan for steps that might fail
3. **Use Meaningful Variables**: Clear names like `{email_summary}` not `{data}`
4. **Add Checkpoints**: Save intermediate results
5. **Monitor Performance**: Log execution times

See [Coordinator Examples](/examples/coordinators/) for dynamic orchestration.