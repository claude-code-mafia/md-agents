# 🤖 Claude Auto-Scheduler Setup Instructions

Run Claude Code automatically on a schedule to perform tasks defined in a simple text file.

## Prerequisites

- Claude Code CLI installed and authenticated (`claude` command works)
- tmux installed (`brew install tmux` on macOS)
- Basic command line knowledge

## Quick Start (5 minutes)

### 1. Clone or Download These Files

Create a new directory and add these essential files:

```bash
mkdir claude-auto-tasks
cd claude-auto-tasks
```

### 2. Create Core Files

**`CLAUDE.md`** - Your task instructions:
```markdown
# Task Instructions

When you run, please do this task:

**[YOUR TASK HERE]**

Save your output to: `output/YYYY-MM-DD_HH-MM.md`
```

**`scripts/simple-test.sh`**:
```bash
#!/bin/bash
cd "$(dirname "$0")/.."
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
echo "[$TIMESTAMP] Running task..." >> logs/activity.log
claude --dangerously-skip-permissions -p "Please follow the instructions in CLAUDE.md" --output-format text >> logs/activity.log 2>&1
echo "[$TIMESTAMP] Task completed" >> logs/activity.log
echo "---" >> logs/activity.log
```

**`scripts/claude-scheduler.sh`**:
```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SESSION_NAME="claude-scheduler"
INTERVAL=${1:-300}  # Default 5 minutes, or pass custom interval

case "$2" in
    start)
        if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
            echo "Scheduler already running!"
        else
            cd "$SCRIPT_DIR"
            tmux new-session -d -s "$SESSION_NAME" "
                while true; do
                    echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] Running scheduled task...\"
                    ./scripts/simple-test.sh
                    echo \"Sleeping for $INTERVAL seconds...\"
                    sleep $INTERVAL
                done
            "
            echo "✅ Scheduler started! Running every $INTERVAL seconds"
            echo "View logs: tmux attach -t $SESSION_NAME"
        fi
        ;;
    stop)
        tmux kill-session -t "$SESSION_NAME" 2>/dev/null
        echo "✅ Scheduler stopped"
        ;;
    status)
        if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
            echo "✅ Scheduler is running"
        else
            echo "❌ Scheduler is not running"
        fi
        ;;
    *)
        echo "Usage: $0 [interval_seconds] {start|stop|status}"
        echo "Example: $0 60 start  # Run every 60 seconds"
        ;;
esac
```

### 3. Set Up Directory Structure

```bash
# Create directories
mkdir -p scripts logs output

# Make scripts executable
chmod +x scripts/*.sh
```

### 4. Start the Scheduler

```bash
# Run every 5 minutes (default)
./scripts/claude-scheduler.sh start

# Or run every minute
./scripts/claude-scheduler.sh 60 start

# Or run every hour
./scripts/claude-scheduler.sh 3600 start
```

### 5. Monitor & Control

```bash
# Check if running
./scripts/claude-scheduler.sh status

# Watch live logs
tmux attach -t claude-scheduler
# (Press Ctrl+B then D to detach)

# View activity log
tail -f logs/activity.log

# Stop scheduler
./scripts/claude-scheduler.sh stop
```

## Example Tasks

### Weather Reporter
```markdown
# Task Instructions
Search for current weather in San Francisco and New York.
Create an entertaining weather report with jokes and emojis.
Save your output to: `output/YYYY-MM-DD_HH-MM.md`
```

### Daily Motivator
```markdown
# Task Instructions
Generate an inspirational quote and explain its meaning.
Include the current date and time.
Save your output to: `output/YYYY-MM-DD_HH-MM.md`
```

### News Summarizer
```markdown
# Task Instructions
Search for today's top technology news.
Summarize the 3 most important stories.
Save your output to: `output/YYYY-MM-DD_HH-MM.md`
```

## Directory Structure

```
claude-auto-tasks/
├── CLAUDE.md           # Your task instructions
├── scripts/
│   ├── simple-test.sh  # Runs Claude with instructions
│   └── claude-scheduler.sh  # Scheduler control script
├── logs/
│   └── activity.log    # Execution history
└── output/            # Task outputs with timestamps
```

## Troubleshooting

**"Scheduler already running!"**
- Stop it first: `./scripts/claude-scheduler.sh stop`

**"command not found: tmux"**
- Install tmux: `brew install tmux` (macOS) or `apt install tmux` (Linux)

**"Invalid API key"**
- Make sure you're logged into Claude: Run `claude` manually first

**Nothing happening?**
- Check logs: `tail -f logs/activity.log`
- Verify Claude works: `claude -p "Hello"`

## Advanced Usage

### Multiple Tasks
Create different CLAUDE.md files and schedulers:
```bash
cp CLAUDE.md CLAUDE-weather.md
cp CLAUDE.md CLAUDE-news.md
# Edit each file with different tasks
# Run multiple schedulers with different session names
```

### Custom Intervals
```bash
# Every 30 seconds (testing)
./scripts/claude-scheduler.sh 30 start

# Every 10 minutes
./scripts/claude-scheduler.sh 600 start

# Every 24 hours
./scripts/claude-scheduler.sh 86400 start
```

### Startup Reminder
Since Claude requires authentication, the scheduler stops on reboot. Create a reminder:

1. Add to your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
# Check if Claude scheduler is running
if ! tmux has-session -t "claude-scheduler" 2>/dev/null; then
    echo "⚠️  Claude scheduler is not running! Start with:"
    echo "cd ~/claude-auto-tasks && ./scripts/claude-scheduler.sh start"
fi
```

## Important Notes

- Claude needs to be authenticated (logged in) for this to work
- The scheduler runs in the background using tmux
- Stops on system reboot (needs manual restart)
- Each task execution uses Claude API credits
- Output files accumulate over time (consider cleanup)

## Get Creative!

Change `CLAUDE.md` to any task you want:
- Generate reports
- Monitor websites
- Create content
- Answer questions
- Analyze data
- Whatever you can describe in text!

The scheduler will keep running your task at the specified interval until you stop it.

---

*Built with Claude Code - Because AI assistants need schedules too! 🤖📅*