# Tool Name

Brief one-line description of what this tool does.

## Purpose

Explain why this tool exists and what specific problem it solves. Shell tools are ideal for:
- System operations
- File manipulation
- Quick text processing
- Piping and composition with other Unix tools

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
tool-name --output results.txt input.txt

# JSON output
tool-name --json data.txt

# From stdin
cat data.txt | tool-name
```

## Options

- `INPUT` - Input file (optional, defaults to stdin)
- `-o, --output FILE` - Output to file (default: stdout)
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
$ tool-name --json data.txt
{
  "status": "success",
  "message": "Tool executed successfully",
  "data": {"processed": true}
}
```

### Piping
```bash
$ echo "test data" | tool-name
Status: success
Message: Tool executed successfully

$ cat large.txt | tool-name --json | jq '.data'
{
  "processed": true
}
```

### Save to File
```bash
$ tool-name --output results.txt input.txt
$ cat results.txt
Status: success
Message: Tool executed successfully
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
  "message": "descriptive message",
  "data": {}
}
```

## Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |

Common errors:
- **File not found**: Check that the input file exists
- **Permission denied**: Check file permissions
- **Invalid arguments**: Check command syntax

## Technical Details

- **Shell**: Bash 4.0+
- **Dependencies**: Standard Unix tools (grep, sed, awk)
- **Performance**: Very fast for small to medium files
- **Limitations**: Best for files under 10MB

## Integration

### With Other Tools
```bash
# Chain with other tool-library tools
tool-name input.txt | other-tool

# Use with standard Unix tools
tool-name data.csv | grep pattern | sort | uniq
```

### In Scripts
```bash
#!/bin/bash
if result=$(tool-name input.txt --json); then
    echo "$result" | jq '.data'
else
    echo "Processing failed"
    exit 1
fi
```

## Development

To modify this tool:
1. Edit the source in `tool-name.sh`
2. Test with various inputs
3. Ensure POSIX compliance for portability
4. Update documentation if behavior changes