#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Open Project
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 📂
# @raycast.packageName Development
# @raycast.argument1 { "type": "text", "placeholder": "Project name", "optional": true }

# Documentation:
# @raycast.description Open a project in VS Code
# @raycast.author Pete
# @raycast.authorURL https://github.com/pete

# Configuration - adjust to your project directories
PROJECT_DIRS=(
    "$HOME/Projects"
    "$HOME/Documents/Code"
    "$HOME/Development"
)

project_name="$1"

# Function to find project
find_project() {
    local name="$1"
    
    # If no name provided, open project selector
    if [ -z "$name" ]; then
        # List all projects
        echo "Available projects:"
        for dir in "${PROJECT_DIRS[@]}"; do
            if [ -d "$dir" ]; then
                ls -1 "$dir" 2>/dev/null | sed "s/^/  /"
            fi
        done
        exit 0
    fi
    
    # Search for project
    for dir in "${PROJECT_DIRS[@]}"; do
        if [ -d "$dir/$name" ]; then
            echo "$dir/$name"
            return 0
        fi
    done
    
    # Fuzzy search
    for dir in "${PROJECT_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            match=$(ls -1 "$dir" 2>/dev/null | grep -i "$name" | head -1)
            if [ -n "$match" ]; then
                echo "$dir/$match"
                return 0
            fi
        fi
    done
    
    return 1
}

# Find and open project
if project_path=$(find_project "$project_name"); then
    # Check if VS Code is available
    if command -v code &> /dev/null; then
        code "$project_path"
        echo "✓ Opened $project_path in VS Code"
    else
        # Fallback to Finder
        open "$project_path"
        echo "✓ Opened $project_path in Finder"
    fi
else
    echo "❌ Project '$project_name' not found"
    echo "Searched in: ${PROJECT_DIRS[*]}"
    exit 1
fi