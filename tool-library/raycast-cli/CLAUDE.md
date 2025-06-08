# Raycast CLI - AI Instructions

## When to Use This Tool

Use the Raycast CLI when the user:
- Wants to run Raycast scripts from the terminal
- Needs to automate Raycast Script Commands
- Wants to create new Raycast scripts
- Asks about integrating Raycast with other tools
- Mentions "raycast", "script commands", or similar terms

## Key Commands

```bash
# List all available Raycast scripts
raycast list

# Run a specific script
raycast run <script-name> [arguments]

# Create a new script template
raycast create "Script Name" --language [bash|python|node]

# Show scripts directory path
raycast path
```

## Usage Examples

```bash
# Quick note-taking
raycast run quick-note "Meeting at 3pm tomorrow"

# Web search
raycast run google-search "Python async await tutorial"

# System information
raycast run system-info

# Open project in VS Code
raycast run open-project "my-project"
```

## Integration Notes

### Output Parsing
- Scripts respect Raycast modes (silent, compact, fullOutput)
- Silent mode scripts print minimal output
- Full output scripts can be parsed for automation

### Chaining with Other Tools
```bash
# Capture system info to file
raycast run system-info > system-report.txt

# Use in scripts
if raycast run check-vpn | grep -q "Connected"; then
    echo "VPN is active"
fi
```

### Creating Scripts Programmatically
```python
# Generate script content
script_content = f'''#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title {title}
# @raycast.mode silent

{code}
'''
```

## Script Development Tips

1. **Test in Both Environments**: Always test scripts work in both Raycast and CLI
2. **Handle Missing Dependencies**: Check for required tools before using
3. **Use Appropriate Modes**:
   - `silent` for background tasks
   - `compact` for quick feedback
   - `fullOutput` for detailed results
   - `inline` for live updates
4. **Error Handling**: Exit with proper codes (0 for success, 1+ for errors)

## Common Patterns

### API Integration Script
```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title API Status
# @raycast.mode compact
# @raycast.argument1 { "type": "text", "placeholder": "API endpoint" }

response=$(curl -s -o /dev/null -w "%{http_code}" "$1")
echo "API Status: $response"
```

### File Processing Script
```python
#!/usr/bin/env python3
# @raycast.schemaVersion 1
# @raycast.title Process Files
# @raycast.mode fullOutput
# @raycast.argument1 { "type": "text", "placeholder": "File pattern" }

import glob
import sys

pattern = sys.argv[1] if len(sys.argv) > 1 else "*"
files = glob.glob(pattern)
print(f"Found {len(files)} files")
```

## Limitations and Workarounds

### Cannot Access Raycast Built-in Features
- No direct access to Raycast Notes, Clipboard History, etc.
- Workaround: Use system alternatives (pbpaste, file-based notes)

### No Interactive Input
- Scripts run non-interactively
- Workaround: Use arguments or configuration files

### Limited UI
- Text output only
- Workaround: Use ANSI colors, ASCII art, or generate HTML reports

## When to Recommend Extensions Instead

Suggest Raycast Extensions when the user needs:
- Complex user interfaces
- Direct integration with Raycast features
- Persistent state management
- Distribution via Raycast Store
- Real-time interactions

The Raycast CLI is best for:
- Command-line automation
- Simple utilities
- Personal productivity scripts
- Integration with existing tools
- Quick prototyping