---
layout: docs
title: Debugging
description: Troubleshooting and debugging md agents
permalink: /debugging/
---

Learn how to debug and troubleshoot issues with your agents.

## Viewing Logs

md agents provides comprehensive logging:

```bash
# View activity log
tail -f logs/activity.log

# Search for errors
grep ERROR logs/activity.log

# View specific agent logs
grep "email-scanner" logs/activity.log
```

## Common Issues

### Agent Not Found

**Problem**: "Agent not found: agent-name"

**Solutions**:
- Check file exists in `/agents/` directory
- Verify filename matches agent name
- Ensure `.md` extension is present
- Check for typos in agent name

### Tool Errors

**Problem**: "Tool [tool-name] not found"

**Solutions**:
- Verify tool is installed
- Check tool documentation in `/tool-library/`
- Ensure tool is in PATH
- Test tool directly in terminal

### State Access Issues

**Problem**: "Cannot read state ~memory.key~"

**Solutions**:
- Check `/runtime/state/` permissions
- Verify state key exists
- Initialize state if needed
- Check for typos in state path

### Workflow Failures

**Problem**: Workflow stops unexpectedly

**Solutions**:
- Check each step individually
- Verify variable names match
- Ensure agents return expected output
- Add error handling to steps

## Debug Mode

Run agents with debug output:

```bash
# Enable verbose logging
./scripts/run-agents.sh --debug agent-name

# Dry run without execution
./scripts/run-agents.sh --dry-run workflow-name

# Step through workflow
./scripts/run-agents.sh --step workflow-name
```

## Testing Agents

### Unit Testing
Test individual agents:
```bash
# Test with specific input
echo '{"input": "test data"}' | ./scripts/run-agents.sh agent-name

# Test error handling
./scripts/run-agents.sh agent-name --invalid-input
```

### Integration Testing
Test agent combinations:
```bash
# Test workflow steps
./scripts/run-agents.sh workflow-name --test
```

## Performance Monitoring

Track agent performance:

```bash
# View execution times
grep "Execution time" logs/activity.log

# Monitor resource usage
./scripts/monitor-agents.sh
```

## Best Practices

1. **Add Logging**: Include log points in behavior
2. **Check Inputs**: Validate before processing
3. **Handle Errors**: Always have fallback behavior
4. **Test Incrementally**: Verify each component
5. **Use Descriptive Names**: Make debugging easier

## Getting Help

- Check [Common Issues](https://github.com/peteknowsai/md-agents/wiki/Common-Issues)
- Search [GitHub Issues](https://github.com/peteknowsai/md-agents/issues)
- Ask in [Discussions](https://github.com/peteknowsai/md-agents/discussions)