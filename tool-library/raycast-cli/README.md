# Raycast CLI

Run Raycast Script Commands from the terminal, enabling you to use your favorite Raycast scripts as regular CLI tools.

## Features

- **Run Raycast scripts from terminal** - Execute any Raycast Script Command without opening Raycast
- **Automatic script discovery** - Finds scripts in standard Raycast directories
- **Preserves Raycast metadata** - Respects script modes, arguments, and other settings
- **Create new scripts** - Generate script templates for bash, Python, or Node.js
- **Cross-platform execution** - Scripts work both in Raycast and terminal

## Installation

```bash
./install-tool.sh raycast-cli
```

## Usage

### List available scripts
```bash
raycast list
```

### Run a script
```bash
raycast run script-name [arguments]

# Examples:
raycast run google-search "Raycast Script Commands"
raycast run quick-note "Remember to buy milk"
raycast run system-info
```

### Create a new script
```bash
raycast create "My Script" --language python
raycast create "Web Tool" --language bash
raycast create "Data Processor" --language node
```

### Show scripts directory
```bash
raycast path
```

## Script Locations

The CLI searches for scripts in these locations:
1. `~/Documents/Raycast Scripts/` (default)
2. `~/Library/Script Commands/`
3. `~/.raycast/scripts/`

## Example Scripts

The `examples/` directory contains several ready-to-use scripts:

- **google-search.sh** - Search Google from the terminal
- **quick-note.sh** - Add timestamped notes to a file
- **clipboard-history.py** - Show current clipboard content
- **system-info.py** - Display system information
- **open-project.sh** - Open projects in VS Code

## Creating Scripts

Scripts are regular executable files with Raycast metadata comments:

```bash
#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title My Script
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🚀
# @raycast.packageName My Tools
# @raycast.argument1 { "type": "text", "placeholder": "Input" }

echo "Hello from My Script!"
```

### Metadata Options

- **schemaVersion**: Always "1"
- **title**: Script name shown in Raycast
- **mode**: `silent`, `compact`, `fullOutput`, or `inline`
- **icon**: Emoji or SF Symbol
- **packageName**: Group scripts together
- **argument1-3**: Define up to 3 arguments
- **refreshTime**: For inline mode (e.g., "10s")

## Script vs Extension

| Use Script Commands for | Use Extensions for |
|------------------------|-------------------|
| Simple automation tasks | Complex UI needs |
| Shell/CLI integration | Rich interactions |
| Quick utilities | Full applications |
| Personal tools | Store distribution |

## Advanced Usage

### Custom Script Directories

Edit `raycast-cli.py` to add custom directories:

```python
self.custom_dirs = [
    Path.home() / 'my-scripts',
    Path('/path/to/team/scripts')
]
```

### Integration with Other Tools

Since scripts are just executables, you can:
- Call them from other scripts
- Use them in automation workflows
- Schedule them with cron
- Integrate with CI/CD pipelines

## Limitations

- Script Commands cannot directly access Raycast's built-in features (Notes, Clipboard History, etc.)
- No rich UI - text output only
- Scripts run in non-interactive mode
- For deep Raycast integration, use the Extension API

## Tips

1. **Testing**: Scripts work identically in terminal and Raycast
2. **Debugging**: Add debug output when not in silent mode
3. **Performance**: Keep scripts fast for better UX
4. **Security**: Never hardcode sensitive data in scripts
5. **Sharing**: Scripts can be shared via Git repositories