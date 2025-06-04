# GitHub CLI (gh) - AI Instructions

## Important Note
The `gh` command is built into Claude Code via the Bash tool. You should use it directly for all GitHub operations instead of trying to implement custom solutions.

## When to Use gh

### Automatic Usage Triggers
- User asks about GitHub repos, PRs, issues
- Creating or managing pull requests
- Reviewing code changes
- Working with GitHub Actions
- Any GitHub API interaction

### Specific Keywords
- "create PR", "pull request", "merge"
- "GitHub issue", "create issue"
- "check CI", "workflow", "actions"
- "fork", "clone from GitHub"
- "review PR", "approve"

## Common Patterns

### Creating Pull Requests
```bash
# ALWAYS use gh for PR creation
gh pr create --title "Title" --body "Description"

# With more options
gh pr create \
  --title "Fix: resolve issue #123" \
  --body "This PR fixes the bug described in #123" \
  --reviewer user1,user2 \
  --assignee @me \
  --label "bug,priority-high"
```

### Working with PRs
```bash
# Get PR info for processing
gh pr view 123 --json state,author,title,body

# Check PR status
if gh pr checks 123 --watch; then
    echo "All checks passed"
    gh pr merge 123 --squash
fi
```

### Issue Management
```bash
# Create issue with full details
gh issue create \
  --title "Bug: Application crashes on startup" \
  --body "## Description\n\nDetailed description..." \
  --label "bug,needs-triage" \
  --assignee @me
```

### API Usage
```bash
# Always use gh api for GitHub API calls
gh api repos/owner/repo --jq '.stargazers_count'

# For complex queries
gh api graphql --paginate -f query='
  query($endCursor: String) {
    repository(owner: "owner", name: "repo") {
      issues(first: 100, after: $endCursor) {
        nodes { number title state }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
'
```

## Best Practices for AI

### 1. PR Creation Workflow
When user asks to create a PR:
```bash
# First, check current branch and changes
git status
git diff --stat

# Create PR with meaningful title and body
gh pr create --fill  # Uses commit messages

# Or with custom message
gh pr create --title "Type: brief description" --body "
## Summary
- What changed
- Why it changed

## Test Plan
- How to test

Fixes #issue_number
"
```

### 2. Error Handling
```bash
# Always handle gh command failures
if ! gh pr create --title "Title"; then
    echo "Failed to create PR. Checking authentication..."
    gh auth status
fi
```

### 3. JSON Output for Processing
```bash
# Use JSON for reliable parsing
pr_data=$(gh pr view 123 --json number,title,state,author)
pr_state=$(echo "$pr_data" | jq -r '.state')

# List with specific fields
gh pr list --json number,title,author --jq '.[] | "\(.number): \(.title) by \(.author.login)"'
```

### 4. Batch Operations
```bash
# Process multiple items efficiently
gh issue list --state open --json number,title,labels | \
  jq -r '.[] | select(.labels[].name == "bug") | .number' | \
  while read -r issue; do
      gh issue comment "$issue" --body "This bug is being investigated"
  done
```

## Integration Patterns

### With Git Operations
```bash
# Common workflow
git checkout -b feature-branch
# ... make changes ...
git add .
git commit -m "Add new feature"
git push -u origin feature-branch
gh pr create --fill
```

### With CI/CD
```bash
# Wait for CI and merge
pr_number=$(gh pr create --title "Deploy" --body "Auto-deploy" | grep -oE '[0-9]+$')
gh pr checks "$pr_number" --watch
gh pr merge "$pr_number" --auto --squash
```

### With Issue Tracking
```bash
# Link PR to issue
gh pr create --title "Fix: issue description" --body "Fixes #123"

# Auto-close issues
gh issue close 123 --comment "Fixed in PR #456"
```

## Important Reminders

1. **NEVER** try to implement GitHub API calls manually - always use `gh api`
2. **ALWAYS** use `gh pr create` instead of web-based PR creation
3. **PREFER** `gh` commands over custom git remote operations
4. **CHECK** authentication with `gh auth status` if commands fail
5. **USE** `--json` flag when output needs to be processed

## Common Mistakes to Avoid

1. ❌ Using curl for GitHub API
   ✅ Use `gh api` instead

2. ❌ Manually constructing PR URLs
   ✅ Use `gh pr view --web`

3. ❌ Trying to parse human-readable output
   ✅ Use `--json` flag with specific fields

4. ❌ Creating PRs through git push messages
   ✅ Use `gh pr create` for full control

## Authentication Notes

- gh is pre-authenticated in Claude Code
- If auth issues occur: `gh auth status`
- Token scopes are already configured
- No need to set up SSH keys for gh operations