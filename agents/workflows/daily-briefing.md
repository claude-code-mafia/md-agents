# Workflow: Daily Briefing

This workflow creates a morning briefing by scanning emails and gathering news.

## Triggers
- **Schedule**: 0 8 * * 1-5  # 8am weekdays
- **Command**: "prepare my daily briefing"

## Input
- email_range: str = "24 hours"
- news_topics: list[str]? = null  # Auto-detect from emails

## Steps

### Step 1: Scan Emails
- **Execute**: %email-scanner%
- **With**: time_range = {email_range}
- **Get**: {email_results}

### Step 2: Gather News
- **Execute**: %news-gatherer%
- **With**: 
  - topics = {news_topics} or extract from {email_results.key_points}
  - time_range = "24 hours"
- **Get**: {news_results}

### Step 3: Create Briefing
- **Execute**: %summary-writer%
- **With**: 
  - sources = [{email_results}, {news_results}]
  - format = "detailed"
- **Save**: output/daily-briefing-{timestamp}.md

## Success
- [ ] All steps complete
- [ ] Briefing saved to output

## If Things Go Wrong
- Email scan fails: Continue with news only
- News fails: Use just emails
- Summary fails: Save raw results