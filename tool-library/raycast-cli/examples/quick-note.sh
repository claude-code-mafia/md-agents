#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Quick Note
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 📝
# @raycast.packageName Notes
# @raycast.argument1 { "type": "text", "placeholder": "Note content" }

# Documentation:
# @raycast.description Add a quick note to your notes file
# @raycast.author Pete
# @raycast.authorURL https://github.com/pete

# Configuration
NOTES_FILE="$HOME/Documents/quick-notes.md"

# Create notes file if it doesn't exist
if [ ! -f "$NOTES_FILE" ]; then
    echo "# Quick Notes" > "$NOTES_FILE"
    echo "" >> "$NOTES_FILE"
fi

# Add note with timestamp
note="$1"
timestamp=$(date "+%Y-%m-%d %H:%M:%S")

echo "## $timestamp" >> "$NOTES_FILE"
echo "$note" >> "$NOTES_FILE"
echo "" >> "$NOTES_FILE"

echo "✓ Note added to $NOTES_FILE"