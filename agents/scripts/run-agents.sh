#!/bin/bash
# run-agents.sh - Run Claude agents via orchestrator

# Navigate to the agents directory
cd "$(dirname "$0")/.."

# Generate timestamp
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")

# Log the start
echo "[$TIMESTAMP] Running agents..." >> logs/activity.log

# Run Claude with the task instructions
# Using --dangerously-skip-permissions to run without confirmation
# Claude will use the CLAUDE.md in the agents directory
claude --dangerously-skip-permissions -p "Execute orchestrator.md" >> logs/activity.log 2>&1

# Log completion
echo "[$TIMESTAMP] Agents completed" >> logs/activity.log
echo "---" >> logs/activity.log