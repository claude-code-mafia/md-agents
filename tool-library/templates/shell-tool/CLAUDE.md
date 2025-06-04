# Tool Name - AI Instructions

## When to Use This Tool

### Automatic Usage Triggers
- User needs to [specific operation]
- Tasks involve [specific file types or patterns]
- System operations requiring [specific capabilities]

### Example User Requests
- "Process these log files"
- "Extract data from..."
- "Check system status for..."

## Usage Patterns

### Basic Command
```bash
tool-name input.txt
```

### For Automation/Integration
```bash
# Always use JSON for reliable parsing
tool-name --json input.txt

# Handle both success and error
if output=$(tool-name --json file.txt 2>&1); then
    echo "$output" | jq '.data'
else
    echo "Failed: $output"
fi
```

### Common Workflows
```bash
# Workflow 1: Batch processing
for file in *.log; do
    tool-name --json "$file" > "${file%.log}.json"
done

# Workflow 2: Pipeline processing
find . -name "*.txt" -print0 | xargs -0 -I {} tool-name {} --json
```

## Output Parsing

### JSON Structure
```json
{
  "status": "success|error",
  "message": "Human-readable message",
  "data": {
    // Tool-specific data
  }
}
```

### Parsing in Different Contexts
```bash
# Using jq
tool-name --json input.txt | jq -r '.message'

# In shell scripts
result=$(tool-name --json input.txt)
status=$(echo "$result" | jq -r '.status')
if [ "$status" = "success" ]; then
    # Process success
fi

# With error handling
tool-name --json input.txt 2>error.log || {
    echo "Tool failed, check error.log"
    exit 1
}
```

## Integration with Other Tools

### Chaining with Unix Tools
```bash
# Pre-process with standard tools
grep "pattern" input.txt | tool-name --json

# Post-process output
tool-name data.csv | cut -d',' -f2 | sort -u
```

### Combining with Other tool-library Tools
```bash
# Sequential processing
tool-name input.txt --json | other-tool --from-json

# Parallel processing
tool-name file1.txt --json &
tool-name file2.txt --json &
wait
```

## Maintenance Guidelines

### Modifying the Tool
1. Maintain POSIX compliance for portability
2. Test on both macOS and Linux
3. Preserve exit codes for scripting
4. Keep JSON output structure stable

### Testing Requirements
- Test with empty input: `echo "" | tool-name`
- Test with large files: `tool-name large.txt`
- Test error cases: permissions, missing files
- Test in pipelines: `cat file | tool-name | grep pattern`

### Shell Compatibility
- Requires Bash 4.0+ for associative arrays
- Falls back gracefully on older systems
- Avoid GNU-specific extensions

## Performance Considerations

- Efficient for files up to 10MB
- Use streaming for larger files
- Minimize subshell spawning
- Consider using awk/sed for text processing

## Security Notes

- Quote all variables to prevent splitting
- Validate input to prevent injection
- Use `set -e` for error safety
- Avoid eval and similar constructs

## Common Issues

1. **No output**: Check if input is empty or stdin is waiting
2. **Slow performance**: Large files may need different approach
3. **Platform differences**: Test on both macOS and Linux
4. **Encoding issues**: Ensure UTF-8 handling

## Best Practices

- Always provide --json flag when calling from scripts
- Check exit codes, not just output
- Use verbose mode for debugging
- Redirect stderr when capturing output