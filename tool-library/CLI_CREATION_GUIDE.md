# CLI Tool Creation Guide

This guide documents the standardized process for creating and installing CLI tools in the tool-library.

## Standard Directory Structure

```
tool-library/
├── bin/                      # Global command wrappers
├── templates/               # Tool templates
└── tool-name/              # Individual tool directory
    ├── tool-executable     # Main executable (with shebang)
    ├── README.md          # Human documentation
    ├── CLAUDE.md          # AI-specific instructions
    ├── requirements.txt   # Python dependencies (if applicable)
    ├── setup.sh          # Tool-specific setup (if needed)
    └── venv/             # Virtual environment (Python tools)
```

## Creating a New CLI Tool

### Step 1: Create Tool Directory
```bash
mkdir tool-library/new-tool-name
cd tool-library/new-tool-name
```

### Step 2: Create the Executable
Create your main executable with appropriate shebang:

**Python tool:**
```python
#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description='Tool description')
    # Add arguments
    args = parser.parse_args()
    # Tool logic here

if __name__ == '__main__':
    main()
```

**Shell tool:**
```bash
#!/bin/bash
# Tool description

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            echo "Usage: tool-name [options]"
            exit 0
            ;;
        *)
            # Handle other arguments
            ;;
    esac
    shift
done

# Tool logic here
```

### Step 3: Make Executable
```bash
chmod +x tool-executable
```

### Step 4: Create Documentation

**README.md:**
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
# Example 1
tool-name --option value

# Example 2
tool-name input.txt --output result.txt
```

## Configuration
- Environment variables
- Config file locations
- API key requirements

## Output
Description of output format and examples

## Error Handling
Common errors and solutions

## Technical Details
- Dependencies
- API usage/limits
- Performance considerations
```

**CLAUDE.md:**
```markdown
# Tool Name - AI Instructions

## When to Use This Tool
- Specific triggers or keywords from user
- Types of tasks this tool handles
- Integration with other tools

## Usage Patterns
```bash
# Common usage pattern
tool-name --json  # For structured output
```

## Maintenance Guidelines
- How to modify safely
- Testing requirements
- Version compatibility

## Integration Notes
- Output parsing
- Error handling in automation
- Chaining with other tools
```

### Step 5: Install the Tool

Use the standardized installation script:
```bash
# Install globally (default)
./install-tool.sh tool-name

# Install for project only
./install-tool.sh tool-name --project
```

## Installation Process

The `install-tool.sh` script handles:

1. **Creates bin wrapper** (always global):
   ```bash
   #!/bin/bash
   exec /full/path/to/tool-executable "$@"
   ```

2. **Updates CLAUDE.md**:
   - Global: Updates `~/.claude/CLAUDE.md`
   - Project: Updates project's `CLAUDE.md`

3. **Adds to PATH** (if not already):
   - Modifies appropriate shell RC file
   - Sources for immediate use

## Best Practices

### 1. Naming Conventions
- Use lowercase with hyphens: `tool-name`
- Be descriptive but concise
- Avoid conflicts with system commands

### 2. Error Handling
```python
import sys

try:
    # Tool logic
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

### 3. Output Formats
- Human-readable by default
- JSON with `--json` flag
- Quiet mode with `-q/--quiet`

### 4. Dependencies
- Minimize external dependencies
- Use virtual environments for Python
- Document all requirements

### 5. Security
- Never hardcode credentials
- Use environment variables or secure storage
- Validate all inputs

## Python Tool Template

See `templates/python-tool/` for a complete example:
```
templates/python-tool/
├── tool-name.py
├── README.md
├── CLAUDE.md
├── requirements.txt
└── setup.sh
```

## Shell Tool Template

See `templates/shell-tool/` for a complete example:
```
templates/shell-tool/
├── tool-name.sh
├── README.md
└── CLAUDE.md
```

## Testing Checklist

Before considering a tool complete:
- [ ] Tool runs without errors
- [ ] Help text is clear (`--help`)
- [ ] Error messages are helpful
- [ ] Works with various inputs
- [ ] README has usage examples
- [ ] CLAUDE.md has AI instructions
- [ ] Installed and accessible via command
- [ ] Global CLAUDE.md is updated

## Maintenance

When updating tools:
1. Test changes thoroughly
2. Update version in tool if applicable
3. Update documentation
4. Ensure backward compatibility
5. Test the wrapper still works