#!/bin/bash
# scheduler.sh - Control the Claude agents scheduler using tmux

# Get the absolute path to the agents directory
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Session name for tmux
SESSION_NAME="claude-scheduler"

# Default interval is 5 minutes (300 seconds), or use the first argument
INTERVAL=${1:-300}

# Process commands
case "$2" in
    start)
        if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
            echo "❌ Scheduler already running!"
            echo "Stop it first with: $0 stop"
        else
            # Change to the agents directory
            cd "$SCRIPT_DIR"
            
            # Create a new detached tmux session running the scheduler loop
            tmux new-session -d -s "$SESSION_NAME" "
                while true; do
                    echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] Running scheduled task...\"
                    ./scripts/run-agents.sh
                    echo \"Sleeping for $INTERVAL seconds...\"
                    sleep $INTERVAL
                done
            "
            
            echo "✅ Scheduler started! Running every $INTERVAL seconds"
            echo "View logs: tmux attach -t $SESSION_NAME"
            echo "Check activity: tail -f $SCRIPT_DIR/logs/activity.log"
        fi
        ;;
        
    stop)
        if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
            tmux kill-session -t "$SESSION_NAME"
            echo "✅ Scheduler stopped"
        else
            echo "❌ Scheduler is not running"
        fi
        ;;
        
    status)
        if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
            echo "✅ Scheduler is running"
            echo "View live output: tmux attach -t $SESSION_NAME"
            echo "(Press Ctrl+B then D to detach)"
        else
            echo "❌ Scheduler is not running"
        fi
        ;;
        
    logs)
        if [ -f "$SCRIPT_DIR/logs/activity.log" ]; then
            echo "Recent activity:"
            tail -20 "$SCRIPT_DIR/logs/activity.log"
        else
            echo "No activity log found"
        fi
        ;;
        
    *)
        echo "Claude Auto-Scheduler Control Script"
        echo ""
        echo "Usage: $0 [interval_seconds] {start|stop|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the scheduler"
        echo "  stop    - Stop the scheduler"
        echo "  status  - Check if scheduler is running"
        echo "  logs    - View recent activity logs"
        echo ""
        echo "Examples:"
        echo "  $0 start              # Run every 5 minutes (default)"
        echo "  $0 60 start           # Run every 60 seconds"
        echo "  $0 3600 start         # Run every hour"
        echo "  $0 86400 start        # Run every 24 hours"
        echo ""
        echo "Current agents directory: $SCRIPT_DIR"
        ;;
esac