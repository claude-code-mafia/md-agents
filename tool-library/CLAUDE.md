# Tool Library Instructions

This directory contains CLI tools that extend Claude Code's capabilities. Each tool is self-contained and follows standardized conventions for easy installation and usage.

## Quick Start - Installing a Tool

**Always create a global command wrapper by default:**
```bash
./install-tool.sh tool-name           # Installs globally (default)
./install-tool.sh tool-name --project # Updates project CLAUDE.md only
```

This will:
1. Create a command wrapper in `bin/` directory
2. Add `bin/` to PATH if needed
3. Update appropriate CLAUDE.md file
4. Run any tool-specific setup

## Creating a New CLI Tool

When the user asks to create a new CLI tool, follow these steps:

### 1. Create Tool Directory
```bash
mkdir tool-library/new-tool-name
cd tool-library/new-tool-name
```

### 2. Create the Main Executable
Name it consistently: `tool-name.py`, `tool-name.sh`, or just `tool-name`

**Python example:**
```python
#!/usr/bin/env python3
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Tool description')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()
    
    try:
        # Tool logic here
        print("Result")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

**Shell example:**
```bash
#!/bin/bash
set -e

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --json) JSON_OUTPUT=true; shift ;;
        -h|--help) echo "Usage: $0 [options]"; exit 0 ;;
        *) break ;;
    esac
done

# Tool logic here
echo "Result"
```

### 3. Make Executable
```bash
chmod +x tool-name
```

### 4. Create Documentation

**README.md** (for humans):
```markdown
# Tool Name

Brief description of what this tool does.

## Installation
```bash
./install-tool.sh tool-name
```

## Usage
```bash
tool-name [options] arguments
```

## Examples
```bash
# Example usage
tool-name input.txt --output result.json
```

## Configuration
- Environment variables needed
- Config file locations
- API key requirements

## Output
Description and examples of output format

## Error Handling
Common errors and how to resolve them
```

**CLAUDE.md** (for AI):
```markdown
# Tool Name - AI Instructions

## When to Use This Tool
- Specific user triggers or keywords
- Types of tasks this handles
- Automatic usage scenarios

## Usage Patterns
```bash
# For automation/integration
tool-name --json
```

## Integration Notes
- Output parsing details
- Chaining with other tools
- Error handling in scripts
```

### 5. Install the Tool
```bash
# From tool-library directory
./install-tool.sh tool-name
```

This automatically:
- Creates `bin/tool-name` wrapper
- Makes it globally accessible
- Updates global CLAUDE.md
- Runs any setup.sh if present

## Standard Patterns

### Directory Structure
```
tool-library/
├── bin/                    # Command wrappers (auto-created)
├── install-tool.sh         # Universal installer
├── CLI_CREATION_GUIDE.md   # Detailed guide
├── tool-name/
│   ├── tool-name.py       # Main executable
│   ├── README.md          # Human docs
│   ├── CLAUDE.md          # AI instructions
│   ├── requirements.txt   # Python deps
│   ├── setup.sh          # Optional setup
│   └── venv/             # Python virtualenv
```

### Naming Conventions
- Tool directory: `tool-name` (lowercase, hyphens)
- Main executable: Same as directory name
- Command name: Same as directory name (no suffix)

### Tool Requirements
- **Self-contained**: Minimize dependencies
- **Clear purpose**: One tool, one job
- **Error handling**: Helpful error messages
- **Output formats**: Human + JSON (`--json`)

### Installation Behavior
- **Default**: Creates global command + updates global CLAUDE.md
- **--project**: Creates global command + updates project CLAUDE.md
- **Always**: Command wrapper goes in global `bin/`

## Current Tools

- **gmail / gmail-advanced**: Email management
- **grok**: xAI chat and X/Twitter analysis  
- **image-gen**: DALL-E image generation
- **current-time**: Network time retrieval
- **typefully**: Twitter/X content creation

## Best Practices

1. **Always use install-tool.sh** - Don't manually create wrappers
2. **Consistent naming** - Directory, executable, and command should match
3. **Error handling** - Exit with proper codes, use stderr
4. **Documentation** - Both README.md and CLAUDE.md are required
5. **JSON output** - Support `--json` flag for automation
6. **Security** - No hardcoded credentials, use env vars

## Tool Development Workflow

**When asked to "build a CLI for X", follow the standardized workflow:**

1. **Research** the API/service documentation
2. **Plan** the implementation with core operations
3. **Review** plan against library conventions
4. **Revise** plan based on review
5. **Implement** following standard patterns
6. **Test** all functionality and error cases
7. **Document** with README.md and CLAUDE.md
8. **Install** using `./install-tool.sh tool-name`
9. **Verify** the command works globally
10. **Commit** with descriptive message

See `TOOL_DEVELOPMENT_WORKFLOW.md` for the complete step-by-step process.

## Templates

- `CLI_CREATION_GUIDE.md` - Quick reference and examples
- `TOOL_DEVELOPMENT_WORKFLOW.md` - Detailed development process
- `templates/python-tool/` - Python tool template
- `templates/shell-tool/` - Shell tool template