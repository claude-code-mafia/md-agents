# Tool Name

Brief one-line description of what this tool does.

## Purpose

Explain why this tool exists and what specific problem it solves. This helps users understand when to use this tool versus alternatives.

## Installation

```bash
# From the tool-library directory
./install-tool.sh tool-name
```

## Usage

```bash
# Basic usage
tool-name input.txt

# With options
tool-name data.csv --output results.json --json

# Verbose mode
tool-name --verbose input.txt
```

## Options

- `input` - Input file or data (optional)
- `-o, --output` - Output file (default: stdout)
- `--json` - Output in JSON format
- `-v, --verbose` - Enable verbose output
- `--version` - Show version information
- `-h, --help` - Show help message

## Examples

### Basic Usage
```bash
$ tool-name data.txt
Status: success
Message: Tool executed successfully
```

### JSON Output
```bash
$ tool-name data.txt --json
{
  "status": "success",
  "input": "data.txt",
  "message": "Tool executed successfully"
}
```

### Save to File
```bash
$ tool-name input.csv --output results.json --json
$ cat results.json
{
  "status": "success",
  "input": "input.csv",
  "message": "Tool executed successfully"
}
```

## Configuration

### Environment Variables
- `TOOL_NAME_CONFIG` - Path to configuration file (optional)
- `TOOL_NAME_API_KEY` - API key if needed

### Config File
Create `~/.tool-name/config.json`:
```json
{
  "default_format": "json",
  "verbose": false
}
```

## Output Format

### Human-Readable (default)
```
Status: success
Message: Tool executed successfully
```

### JSON Format (--json)
```json
{
  "status": "success|error",
  "input": "filename",
  "message": "descriptive message",
  "data": {}
}
```

## Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid input |

Common errors:
- **File not found**: Check that the input file exists
- **Invalid format**: Ensure input matches expected format
- **Permission denied**: Check file permissions

## Technical Details

- **Language**: Python 3.6+
- **Dependencies**: None (uses standard library only)
- **Performance**: Processes ~1MB/second
- **Limitations**: Maximum file size 100MB

## Development

To modify this tool:
1. Edit the source in `tool-name.py`
2. Run tests: `python -m pytest tests/`
3. Update documentation if behavior changes