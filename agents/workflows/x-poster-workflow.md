# Workflow: X Poster

This workflow finds and posts daily Claude Code tips to X (Twitter).

## When to Run

Run this workflow when:
- Every day at 10:00 AM
- Manually when you want to post a tip
- Never more than once per 20 hours

## The Team

This workflow uses these specialist agents:
- **X Tip Finder**: Searches X for Claude Code tips
- **X Tip Curator**: Selects the best unique tip
- **X Post Writer**: Crafts an engaging post
- **Session Manager**: Tracks workflow progress

## The Process

### Step 1: Find Tips
- **Who**: X Tip Finder
- **What**: Search X for Claude Code tips from last 48 hours
- **Needs**: Twitter API access
- **Produces**: List of 20 posts saved to `context/found-tips.yaml`

### Step 2: Select Best Tip
- **Who**: X Tip Curator
- **What**: Review tips and select best one we haven't posted
- **Needs**: 
  - Found tips from Step 1
  - Read `agents/x-poster/log.md` for history
- **Produces**: Selected tip saved to `context/selected-tip.yaml`

### Step 3: Write Post
- **Who**: X Post Writer
- **What**: Transform tip into engaging X post
- **Needs**: Selected tip from Step 2
- **Produces**: Ready-to-post content in `context/tweet.md`

### Step 4: Publish Post
- **Who**: X Poster (using Twitter API)
- **What**: Post to X and update log
- **Needs**: 
  - Tweet content from Step 3
  - Twitter API credentials
- **Produces**: 
  - Posted to X
  - Updated `agents/x-poster/log.md`

## Success Looks Like

The workflow succeeded when:
- [ ] Found at least 5 Claude Code tips
- [ ] Selected a unique, valuable tip
- [ ] Created engaging post within character limit
- [ ] Successfully posted to X
- [ ] Updated log with new post

## If Something Goes Wrong

- If Tip Finder fails: Check Twitter API access
- If no unique tips found: Log "No new tips today" and exit gracefully
- If posting fails: Save tweet for manual posting
- Always: Update log with what happened

## Example Session

```
[10:00:00] Starting X Poster workflow
[10:00:01] X Tip Finder: Searching last 48 hours
[10:00:08] X Tip Finder: Found 23 Claude Code posts
[10:00:09] X Tip Curator: Checking against posting history
[10:00:11] X Tip Curator: Selected tip about multi-repo workflow
[10:00:12] X Post Writer: Crafting engaging post
[10:00:13] X Poster: Publishing to X
[10:00:15] Success! Posted at https://x.com/YourHandle/status/123
[10:00:16] Workflow complete
```

## Manual Override

To post a specific tip:
```
Execute workflow: x-poster
Parameters:
  manual_tip: "Your specific tip here"
  skip_search: true
```