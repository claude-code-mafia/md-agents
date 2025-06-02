# X Poster Agent Team

An agent team that finds and posts daily Claude Code tips to X (Twitter).

## Agents

1. **TipFinder** - Searches X for Claude Code tips and tricks
2. **TipCurator** - Selects the best unique tip to post
3. **TweetPoster** - Formats and posts the tweet
4. **XPosterOrchestrator** - Coordinates the workflow

## Setup

1. Install the twitter-api-mcp server:
   ```bash
   # Installation command depends on the specific MCP server
   ```

2. Configure with your X API credentials

3. Run daily:
   ```bash
   claude-code "Run the XPosterOrchestrator agent from agents/x-poster/"
   ```

## How It Works

1. TipFinder searches X for recent Claude Code content
2. TipCurator checks log.md and picks the best new tip
3. TweetPoster formats it into an engaging tweet and posts
4. The log.md file tracks what's been posted

## Log

All posted tips are tracked in `log.md` to prevent duplicates.

## Manual Controls

- Run anytime (it checks if already posted today)
- Edit log.md to mark tips as posted
- Modify search queries in tip-finder.md
- Adjust scoring in tip-curator.md
- Change tweet style in tweet-poster.md