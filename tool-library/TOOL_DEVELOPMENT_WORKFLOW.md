# Tool Development Workflow

This document outlines the standardized process for developing new CLI tools for the tool-library.

## Overview

When asked to "build a CLI for X", follow these steps in order to ensure consistency and quality.

## Step-by-Step Workflow

### 1. Research the API/Service
- Visit the official API documentation
- **Check for SDKs** (in order of preference):
  1. Official SDK from the company
  2. Well-established community SDK (500+ stars, active maintenance)
  3. Direct API calls (if no good SDK exists)
- **Evaluate SDK quality:**
  - GitHub stars, commit activity, issue response time
  - Download stats (npm weekly downloads, PyPI stats)
  - Documentation quality and examples
  - Test coverage and CI/CD presence
- Identify key endpoints and capabilities
- Note authentication requirements
- Check rate limits and usage restrictions

**Output:** Summary of API capabilities and SDK recommendation

### 2. Create Implementation Plan
- Define the tool's core purpose (one tool, one job)
- **Choose implementation approach:**
  - If official SDK exists: Plan around SDK methods
  - If no SDK: Plan direct API integration
- List the most useful operations for CLI usage
- Plan the command structure and subcommands
- Determine authentication approach
- Decide on output formats (human + JSON)
- Consider error handling scenarios

**Output:** Detailed implementation plan

### 3. Review Against Library Conventions
Check that your plan follows these standards:
- ✓ Tool name follows pattern: `service-name` (lowercase, hyphens)
- ✓ Main executable matches directory name
- ✓ Supports `--json` flag for automation
- ✓ Uses environment variables for API keys
- ✓ Has clear error messages with exit codes
- ✓ Outputs to stdout (errors to stderr)
- ✓ Minimal external dependencies

**Output:** Conformance checklist

### 4. Revise Implementation Plan
Based on the review:
- Adjust naming to match conventions
- Ensure consistent argument patterns
- Add missing standard features (--json, --help, etc.)
- Align with existing tools' patterns

**Output:** Final implementation plan

### 5. Implement the Tool
```bash
# Create tool directory
mkdir tool-library/service-name

# Create main executable
cd tool-library/service-name
touch service-name.py  # or .sh
chmod +x service-name.py

# If Python, create requirements.txt
# For official SDK:
echo "official-service-sdk>=1.0.0" > requirements.txt
# For direct API:
echo "requests>=2.28.0" > requirements.txt

# Create virtual environment (Python)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Implementation checklist:
- [ ] Shebang line (#!/usr/bin/env python3 or #!/bin/bash)
- [ ] Argument parsing with help text
- [ ] Environment variable for API key
- [ ] Human-readable output (default)
- [ ] JSON output (--json flag)
- [ ] Proper error handling with exit codes
- [ ] Informative error messages

### 6. Test the Tool
Before installation:
```bash
# Test basic functionality
./service-name.py --help
./service-name.py list
./service-name.py get ID --json

# Test error cases
./service-name.py invalid-command
unset API_KEY && ./service-name.py list

# Test output formats
./service-name.py list > output.txt
./service-name.py list --json | jq '.'
```

Test checklist:
- [ ] Help text displays correctly
- [ ] All commands work as expected
- [ ] JSON output is valid
- [ ] Error messages are helpful
- [ ] Exit codes are appropriate
- [ ] Works with pipes and redirection

### 7. Create Documentation

**README.md** - For humans:
- Clear purpose statement
- Installation instructions
- Usage examples with real commands
- Configuration details
- Common error solutions
- API limitations/quotas

**CLAUDE.md** - For AI:
- When to automatically use the tool
- Integration patterns
- Output parsing examples
- Common workflows
- Maintenance guidelines

### 8. Install the Tool
```bash
# From tool-library directory
./install-tool.sh service-name

# This will:
# 1. Create bin/service-name wrapper
# 2. Add bin/ to PATH if needed
# 3. Update global CLAUDE.md
# 4. Run any setup.sh if present
```

### 9. Verify Installation
```bash
# Test the command is available
which service-name
service-name --help

# Test actual functionality
service-name list
service-name get ID --json
```

### 10. Commit to Git
```bash
# Review changes
git status
git diff

# Stage files
git add tool-library/service-name/
git add -u  # for modified files

# Create descriptive commit
git commit -m "Add service-name CLI tool

- Implements core operations: list, get, create, update, delete
- Supports both human-readable and JSON output
- Uses SERVICE_API_KEY environment variable
- Includes comprehensive documentation"
```

## Standard Patterns

### SDK vs Direct API

**When to use an SDK:**
1. **Official SDK** (preferred):
   - Maintained by the company itself
   - Check GitHub org, npm scope, PyPI owner
   
2. **Community SDK** (acceptable if well-established):
   - 500+ GitHub stars
   - Active maintenance (commits within last 3 months)
   - Good issue response time
   - Substantial download stats (npm/PyPI)
   - Clean codebase and good documentation
   - Used by other notable projects

**Evaluating SDKs:**
```bash
# Check GitHub stats
# - Stars, forks, issues, last commit
# - Contributors and commit frequency
# - Open vs closed issues ratio

# Check package stats
# PyPI: pip show package-name / check PyPI page
# npm: npm info package-name / check npm weekly downloads
# Look for: download counts, version history, dependencies
```

**Red flags to avoid:**
- Last updated > 1 year ago
- Many open issues with no responses
- Poor documentation
- No tests or CI/CD
- Single maintainer who's inactive

**Using SDK in implementation:**
```python
# With official SDK
from airtable import Airtable  # Official SDK
client = Airtable(api_key=api_key)
records = client.list_records(base_id, table_name)

# Without SDK (direct API)
import requests
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(f"{API_BASE}/bases/{base_id}/tables/{table_name}")
```

### Authentication
```python
api_key = os.environ.get('SERVICE_API_KEY')
if not api_key:
    print("Error: SERVICE_API_KEY environment variable not set", file=sys.stderr)
    print("Get your API key from: https://service.com/api", file=sys.stderr)
    sys.exit(1)
```

### Output Handling
```python
if args.json:
    print(json.dumps(result, indent=2))
else:
    # Human-readable format
    for item in result:
        print(f"ID: {item['id']}")
        print(f"Name: {item['name']}")
        print()
```

### Error Handling
```python
try:
    result = api_call()
except requests.exceptions.HTTPError as e:
    if args.json:
        error = {"error": str(e), "status_code": e.response.status_code}
        print(json.dumps(error), file=sys.stderr)
    else:
        print(f"API Error: {e}", file=sys.stderr)
    sys.exit(1)
```

## Quality Checklist

Before considering a tool complete:

### Code Quality
- [ ] Follows naming conventions
- [ ] Has consistent code style
- [ ] Includes helpful comments
- [ ] Handles edge cases

### Functionality
- [ ] Core operations work correctly
- [ ] Authentication is secure
- [ ] Output formats are correct
- [ ] Error handling is comprehensive

### Documentation
- [ ] README.md is complete
- [ ] CLAUDE.md has AI instructions
- [ ] Examples are tested and working
- [ ] Configuration is documented

### Integration
- [ ] Installs correctly with install-tool.sh
- [ ] Command is globally accessible
- [ ] Works in automation/scripts
- [ ] CLAUDE.md is updated

## Common Pitfalls to Avoid

1. **Hardcoding API endpoints** - Use constants or config
2. **Poor error messages** - Be specific about what went wrong
3. **Missing --json flag** - Always support automation
4. **Ignoring rate limits** - Document and handle appropriately
5. **Complex dependencies** - Keep it minimal
6. **Unclear command structure** - Follow REST-like patterns

## Examples of Good Tools

Review these for patterns:
- `gmail-tool/` - OAuth authentication, complex operations
- `grok-tool/` - API key auth, multiple subcommands
- `typefully-tool/` - Config file approach, scheduling features
- `image-gen-tool/` - Simple focused tool, minimal deps

## Getting Help

If unsure about any step:
1. Check existing tools for patterns
2. Review the templates in `templates/`
3. Consult API best practices
4. Prioritize user experience