# Airtable CLI

Powerful command-line interface for Airtable using direct API calls with Personal Access Token authentication.

## Purpose

This tool provides comprehensive access to the Airtable Web API, enabling you to:
- Manage bases, tables, and records with full CRUD operations
- Use advanced filtering with Airtable formulas
- Perform batch operations (create, update, delete)
- Export data to CSV or JSON
- Upsert records (update or create based on field matching)
- View complete schema including field metadata
- Handle rate limiting automatically with exponential backoff

## Important: Authentication Change

**As of February 2024, Airtable deprecated API keys in favor of Personal Access Tokens (PATs).**

This CLI uses Personal Access Tokens exclusively. If you have old API keys (starting with "key"), you must create a new Personal Access Token.

## Installation

```bash
# From the tool-library directory
./install-tool.sh airtable
```

## Configuration

### Personal Access Token Setup

1. **Create a Personal Access Token**:
   - Go to: https://airtable.com/create/tokens
   - Click "Create new token"
   - Name your token (e.g., "CLI Access")
   - Select scopes based on your needs (see below)
   - Choose which bases to grant access to

2. **Set the environment variable**:
   ```bash
   export AIRTABLE_PAT='patXXXXXXXXXXXXXX'
   ```

3. **Add to your shell profile** for persistence:
   ```bash
   echo "export AIRTABLE_PAT='patXXXXXXXXXXXXXX'" >> ~/.bashrc
   ```

### Required Token Scopes

Select scopes based on your intended usage:

- **Basic Operations**:
  - `data.records:read` - List and view records
  - `data.records:write` - Create, update, delete records

- **Schema Operations**:
  - `schema.bases:read` - View base and table schemas
  - `schema.bases:write` - Create and modify fields (advanced)

- **Additional Scopes**:
  - `data.recordComments:read` - Read record comments
  - `data.recordComments:write` - Add comments to records
  - `webhook:manage` - Create and manage webhooks

## Usage

### Authentication Test
```bash
# Test your token and see accessible bases count
airtable whoami
```

### Base Operations
```bash
# List all accessible bases
airtable bases

# Get complete schema for a base
airtable schema appXXXXXXXXXXXXXX
```

### Record Operations

#### List Records
```bash
# Basic listing
airtable list appXXXXXXXXXXXXXX "Table Name"

# With filtering
airtable list appXXXXXXXXXXXXXX "Contacts" --filter-formula "Status='Active'"

# Complex filter with AND/OR
airtable list appXXXXXXXXXXXXXX "Tasks" \
  --filter-formula "AND({Status}='In Progress', {Priority}='High')"

# Limit results
airtable list appXXXXXXXXXXXXXX "Products" --max-records 10

# Sort by field
airtable list appXXXXXXXXXXXXXX "Events" --sort "Date:desc" "Name:asc"

# Use a specific view
airtable list appXXXXXXXXXXXXXX "Projects" --view "Active Projects"

# Select specific fields only
airtable list appXXXXXXXXXXXXXX "Users" --fields "Name" "Email" "Status"

# Table format output
airtable list appXXXXXXXXXXXXXX "Items" --format table
```

#### Get Single Record
```bash
airtable get appXXXXXXXXXXXXXX "Table Name" recXXXXXXXXXXXXXX
```

#### Create Records
```bash
# Create single record
airtable create appXXXXXXXXXXXXXX "Contacts" \
  --data '{"Name": "John Doe", "Email": "john@example.com", "Status": "Active"}'

# Create with automatic type conversion
airtable create appXXXXXXXXXXXXXX "Orders" \
  --data '{"Order Date": "2024-01-15", "Amount": "99.99"}' \
  --typecast

# Batch create from file
echo '[
  {"Name": "Alice", "Department": "Engineering"},
  {"Name": "Bob", "Department": "Sales"}
]' > records.json
airtable create appXXXXXXXXXXXXXX "Employees" --file records.json
```

#### Update Records
```bash
# Update single record
airtable update appXXXXXXXXXXXXXX "Tasks" recXXXXXXXXXXXXXX \
  --data '{"Status": "Completed", "Completed Date": "2024-01-15"}'

# Batch update from file
echo '[
  {"id": "recXXXXXX", "fields": {"Status": "Active"}},
  {"id": "recYYYYYY", "fields": {"Status": "Inactive"}}
]' > updates.json
airtable update appXXXXXXXXXXXXXX "Contacts" --file updates.json
```

#### Upsert Records
```bash
# Update existing or create new based on Email field
airtable upsert appXXXXXXXXXXXXXX "Contacts" \
  --data '[{"Email": "john@example.com", "Name": "John Updated", "Status": "Active"}]' \
  --merge-on "Email"

# Upsert with multiple match fields
airtable upsert appXXXXXXXXXXXXXX "Products" \
  --file products.json \
  --merge-on "SKU" "Variant" \
  --typecast
```

#### Delete Records
```bash
# Delete single record
airtable delete appXXXXXXXXXXXXXX "Table Name" recXXXXXXXXXXXXXX

# Delete multiple records
airtable delete appXXXXXXXXXXXXXX "Old Records" recXXXXXX recYYYYYY recZZZZZZ

# Delete with confirmation skip
airtable delete appXXXXXXXXXXXXXX "Temp Data" recXXXXXX --force

# Batch delete from file
echo '["recXXXXXX", "recYYYYYY"]' > to_delete.json
airtable delete appXXXXXXXXXXXXXX "Archive" --file to_delete.json
```

### Field Operations
```bash
# List all fields with metadata
airtable fields appXXXXXXXXXXXXXX "Table Name"
```

### Export Operations
```bash
# Export to JSON (default)
airtable export appXXXXXXXXXXXXXX "Contacts" --output contacts.json

# Export to CSV
airtable export appXXXXXXXXXXXXXX "Orders" --output orders.csv

# Export with filtering
airtable export appXXXXXXXXXXXXXX "Products" \
  --output active_products.csv \
  --filter-formula "Status='Active'"

# Export specific view
airtable export appXXXXXXXXXXXXXX "Projects" \
  --output q1_projects.json \
  --view "Q1 Projects"

# Export to stdout for piping
airtable export appXXXXXXXXXXXXXX "Data" --format json | jq '.[] | .fields'
```

## Advanced Usage

### Complex Filtering with Formulas

Airtable formulas support complex logic:

```bash
# Date filtering
airtable list appXXXXXX "Events" \
  --filter-formula "IS_AFTER({Event Date}, '2024-01-01')"

# Multiple conditions
airtable list appXXXXXX "Tasks" \
  --filter-formula "OR(AND({Status}='Open', {Priority}='High'), {Overdue}=TRUE())"

# Text searching
airtable list appXXXXXX "Notes" \
  --filter-formula "FIND('important', LOWER({Content})) > 0"

# Null checking
airtable list appXXXXXX "Contacts" \
  --filter-formula "NOT({Email} = BLANK())"
```

### Working with Linked Records

```bash
# Create with linked records (use record IDs)
airtable create appXXXXXX "Orders" --data '{
  "Product": ["recPRODUCT123"],
  "Customer": ["recCUSTOMER456"],
  "Quantity": 2
}'

# Query with linked record fields
airtable list appXXXXXX "Orders" \
  --fields "Order Number" "Product" "Customer" "Total"
```

### Handling Attachments

```bash
# Create record with attachment
airtable create appXXXXXX "Documents" --data '{
  "Name": "Report",
  "Attachments": [
    {
      "url": "https://example.com/report.pdf",
      "filename": "report.pdf"
    }
  ]
}'
```

### Automation Examples

#### Daily Backup
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
for table in "Contacts" "Orders" "Products"; do
  airtable export appXXXXXX "$table" \
    --output "backup_${table}_${DATE}.json"
done
```

#### Sync Between Bases
```bash
# Export from source
airtable export appSOURCE "Contacts" --output temp.json

# Transform and import to destination
cat temp.json | jq '.[] | .fields' | \
  airtable create appDEST "Contacts" --file -
```

#### Monitor Changes
```bash
# Simple change detection
while true; do
  airtable list appXXXXXX "Tasks" \
    --filter-formula "Status='New'" \
    --json > new_tasks.json
  
  if [ -s new_tasks.json ]; then
    echo "New tasks detected!"
    # Process new tasks...
  fi
  
  sleep 300  # Check every 5 minutes
done
```

## Output Formats

### JSON Output (--json flag)
All commands support JSON output for scripting:

```bash
# Parse with jq
airtable list appXXXXXX "Table" --json | \
  jq '.[] | select(.fields.Status == "Active")'

# Count records
airtable list appXXXXXX "Orders" --json | jq length
```

### Human-Readable Output
Default output is formatted for readability with colors:
- Record IDs in cyan
- Field names in blue
- Success messages in green
- Errors in red
- Warnings in yellow

## Error Handling

The CLI handles common errors gracefully:

### Rate Limiting
- Automatically retries with exponential backoff
- Maximum 3 retries with 30, 60, 120 second delays
- Shows wait time in terminal

### Authentication Errors
- Clear message if token is invalid
- Warning if using deprecated API key format
- Instructions for creating Personal Access Token

### Permission Errors
- Shows which scopes are missing
- Links to token management page

## Best Practices

1. **Use Personal Access Tokens** - API keys are deprecated
2. **Limit token scope** - Only grant necessary permissions
3. **Use typecast for data imports** - Ensures proper field types
4. **Batch operations** - Process up to 10 records per request
5. **Cache base IDs** - They don't change, save API calls
6. **Use views for filtering** - More efficient than formulas
7. **Export regularly** - Backup important data

## Limitations

- Maximum 10 records per create/update/delete request
- 100 records per page when listing
- 5 requests per second per base
- Attachment URLs expire after 2 hours
- Cannot modify table structure via API (use Airtable UI)

## Troubleshooting

### "Authentication failed"
- Verify your token starts with `pat` not `key`
- Check token hasn't been revoked
- Ensure AIRTABLE_PAT is exported correctly

### "Permission denied"
- Token lacks required scopes
- Token doesn't have access to the base
- Check user permissions in Airtable

### "Rate limited"
- The CLI auto-retries, just wait
- For bulk operations, add delays between batches
- Consider using fewer parallel operations

### "Invalid formula"
- Test formulas in Airtable UI first
- Escape quotes properly in shell
- Check field names are exact matches

## Security Notes

- Store tokens in environment variables or secure vaults
- Never commit tokens to version control
- Use read-only tokens when possible
- Rotate tokens periodically
- Tokens inherit your Airtable permissions