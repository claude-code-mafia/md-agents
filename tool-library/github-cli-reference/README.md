# GitHub CLI Reference

The GitHub CLI (`gh`) is already installed and available in Claude Code. This reference documents common usage patterns.

## About

GitHub CLI brings GitHub functionality to your terminal, enabling you to:
- Work with issues, pull requests, and discussions
- Create and manage repositories
- Review and merge pull requests
- Work with GitHub Actions
- Access GitHub API directly

## Installation Status

✅ **Already installed in Claude Code** - No additional setup needed

## Common Commands

### Repository Operations
```bash
# Clone a repo
gh repo clone owner/repo

# Create a new repo
gh repo create my-repo --public

# Fork a repo
gh repo fork owner/repo --clone

# View repo info
gh repo view owner/repo
```

### Pull Requests
```bash
# Create a PR
gh pr create --title "Fix bug" --body "Description"

# List PRs
gh pr list

# View PR details
gh pr view 123

# Check out a PR
gh pr checkout 123

# Review a PR
gh pr review 123 --approve
gh pr review 123 --comment -b "Looks good!"

# Merge a PR
gh pr merge 123 --squash
```

### Issues
```bash
# Create an issue
gh issue create --title "Bug report" --body "Description"

# List issues
gh issue list --label bug

# View issue
gh issue view 123

# Comment on issue
gh issue comment 123 --body "Working on this"

# Close issue
gh issue close 123
```

### GitHub Actions
```bash
# List workflow runs
gh run list

# View run details
gh run view 12345

# Watch a run in progress
gh run watch 12345

# Download artifacts
gh run download 12345
```

### Gists
```bash
# Create a gist
gh gist create file.txt --public

# List your gists
gh gist list

# View a gist
gh gist view GIST_ID
```

### API Access
```bash
# Make API requests
gh api repos/owner/repo

# GraphQL queries
gh api graphql -f query='
  query {
    repository(owner: "owner", name: "repo") {
      stargazerCount
    }
  }
'

# With pagination
gh api repos/owner/repo/issues --paginate
```

## Advanced Usage

### Working with Multiple Remotes
```bash
# Add upstream remote
gh repo fork --remote

# Sync fork with upstream
gh repo sync
```

### PR Templates
```bash
# Create PR with template
gh pr create --template .github/pull_request_template.md
```

### Automation
```bash
# Create PR and set reviewers
gh pr create --reviewer user1,user2 --assignee @me

# Batch operations
gh pr list --json number,title | jq -r '.[] | [.number, .title] | @tsv'
```

### Authentication
```bash
# Check auth status
gh auth status

# Login (if needed)
gh auth login

# Use different account
gh auth switch
```

## Output Formats

### JSON Output
```bash
# Get JSON for scripting
gh pr list --json number,title,author

# Common JSON fields
gh issue list --json number,title,state,author,labels,createdAt
```

### Filtering and Formatting
```bash
# Filter by state
gh pr list --state open

# Filter by author
gh issue list --author @me

# Custom format
gh pr list --json number,title --jq '.[] | "#\(.number) \(.title)"'
```

## Integration Examples

### With Shell Scripts
```bash
#!/bin/bash
# Auto-merge approved PRs
for pr in $(gh pr list --json number,reviewDecision -q '.[] | select(.reviewDecision=="APPROVED") | .number'); do
    gh pr merge $pr --auto --squash
done
```

### With Other Tools
```bash
# Create PR from current branch
git push -u origin HEAD && gh pr create --fill

# Open PR in browser
gh pr view --web
```

## Best Practices

1. **Use JSON output** for scripting: `--json` flag
2. **Set default repo**: `gh repo set-default`
3. **Use templates**: Keep PR/issue templates in `.github/`
4. **Leverage aliases**: `gh alias set`
5. **Check rate limits**: `gh api rate_limit`

## Troubleshooting

- **Authentication issues**: Run `gh auth status` and `gh auth login` if needed
- **API rate limits**: Use `--interval` flag for batch operations
- **Permission errors**: Check repo access and token scopes
- **Network issues**: gh respects `HTTP_PROXY` and `HTTPS_PROXY` env vars