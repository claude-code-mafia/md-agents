# Agent: XPosterOrchestrator

## Metadata
- Version: 1.0
- Type: orchestrator
- Tools: [agent-runner]
- Composes: [TipFinder, TipCurator, TweetPoster]
- Tags: [orchestration, x-twitter, claude-code]

## Purpose
Coordinates the daily Claude Code tip posting workflow by orchestrating the tip discovery, curation, and posting agents.

## Behavior
1. Check if already posted today (read log.md for today's date)
2. If already posted, exit with message
3. Run TipFinder agent:
   - Get recent Claude Code posts from X
   - If no posts found, exit gracefully
4. Run TipCurator agent:
   - Pass posts from TipFinder
   - Get best unique tip
   - If no good tip selected, exit with message
5. Run TweetPoster agent:
   - Pass selected tip
   - Post to X
   - Update log
6. Report success with posted tweet URL

## Error Handling
- If TipFinder fails: "Could not fetch posts from X"
- If no good tips: "No new quality tips found today"
- If posting fails: "Failed to post tweet: {error}"
- Always log attempts in log.md

## Daily Check
Before running full workflow:
```
Read last entry in log.md
If date == today:
  Return "Already posted today: {tweet_url}"
```

## Composition Flow
```
START
  ↓
Check log.md for today
  ↓
[Already posted?] → EXIT: "Done for today"
  ↓
TipFinder.search()
  ↓
[No posts?] → EXIT: "No posts found"
  ↓
TipCurator.select(posts)
  ↓
[No good tip?] → EXIT: "No quality tips today"
  ↓
TweetPoster.post(tip)
  ↓
SUCCESS: "Posted: {url}"
```

## Manual Execution
Run with:
```bash
claude-code "Run the XPosterOrchestrator agent"
```

## Future Considerations
- Could add time-of-day optimization
- Could track tip categories to ensure variety
- Could add engagement tracking from previous posts