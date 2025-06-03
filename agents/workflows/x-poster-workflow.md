# Workflow: X Poster

This workflow finds and posts daily Claude Code tips to X.

## Triggers
- **Schedule**: 0 10 * * *  # 10am daily
- **Command**: "post claude tip"

## Input
- search_hours: int = 48
- max_tips: int = 20

## Steps

### Step 1: Find Tips
- **Execute**: %x-tip-finder%
- **With**: 
  - time_range = "{search_hours} hours"
  - max_results = {max_tips}
- **Get**: {found_tips}

### Step 2: Select Best Tip
- **Execute**: %x-tip-curator%
- **With**: 
  - tips = {found_tips}
  - history_file = "logs/x-poster-history.md"
- **Get**: {selected_tip}

### Step 3: Write Post
- **Execute**: %x-post-writer%
- **With**: tip = {selected_tip}
- **Get**: {tweet_content}

### Step 4: Publish
- **Execute**: %x-poster%
- **With**: 
  - content = {tweet_content}
  - update_log = true
- **Save**: logs/x-poster-history.md

## Success
- [ ] Found tips
- [ ] Selected unique tip
- [ ] Posted to X
- [ ] Updated history

## If Things Go Wrong
- No tips found: Exit gracefully
- No unique tips: Log and skip
- Post fails: Save for manual posting