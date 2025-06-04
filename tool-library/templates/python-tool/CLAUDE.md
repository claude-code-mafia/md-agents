# Tool Name - AI Instructions

## When to Use This Tool

### Automatic Usage Triggers
- User mentions "[specific keywords]"
- Tasks involve [specific data types or operations]
- When [specific conditions] are met

### Example User Requests
- "Process this data file"
- "Convert X to Y format"
- "Analyze the contents of..."

## Usage Patterns

### Basic Command
```bash
tool-name input.txt
```

### For Automation/Integration
```bash
# Always use JSON for parsing
tool-name input.txt --json

# Pipe-friendly usage
cat data.txt | tool-name --json | jq '.data'
```

### Common Workflows
```bash
# Workflow 1: Process and save
tool-name input.csv --output processed.json --json

# Workflow 2: Batch processing
for file in *.txt; do
    tool-name "$file" --json > "${file%.txt}.json"
done
```

## Output Parsing

### JSON Structure
```json
{
  "status": "success|error",
  "message": "Human-readable message",
  "data": {
    // Tool-specific data
  },
  "error": "Only present on error"
}
```

### Parsing Examples
```python
# Python
import json
import subprocess

result = subprocess.run(['tool-name', 'input.txt', '--json'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)
if data['status'] == 'success':
    process_data(data['data'])
```

## Integration with Other Tools

### Chaining Tools
```bash
# Use with other tool-library tools
tool-name input.txt --json | other-tool --from-json

# Combine with system tools
tool-name data.csv --json | jq '.data[] | select(.value > 100)'
```

### Error Handling in Scripts
```bash
if output=$(tool-name input.txt --json 2>&1); then
    echo "$output" | process_success
else
    echo "Error: $output" >&2
    exit 1
fi
```

## Maintenance Guidelines

### Modifying the Tool
1. Preserve JSON output structure for backward compatibility
2. Add new fields to JSON rather than changing existing ones
3. Test with various input sizes and formats
4. Update version number in --version output

### Testing Requirements
- Test normal operation: `tool-name test.txt`
- Test JSON output: `tool-name test.txt --json`
- Test error cases: missing files, invalid input
- Test piping: `echo "data" | tool-name`

### Version Compatibility
- Supports Python 3.6+
- JSON output format: v1.0 (stable)
- Breaking changes require major version bump

## Performance Considerations

- Processes files up to 100MB efficiently
- For larger files, consider streaming or chunking
- JSON output adds ~10% overhead

## Security Notes

- Validates all input files before processing
- Does not execute arbitrary code from input
- Sanitizes output to prevent injection

## Common Issues

1. **Empty output**: Check if input file is empty
2. **JSON parse errors**: Ensure --json flag is used
3. **Slow performance**: Check file size, consider chunking