# Airtable CLI - AI Instructions

## Critical: Authentication Requirements

**ALWAYS use Personal Access Tokens (PATs)**:
- Environment variable: `AIRTABLE_PAT` (NOT `AIRTABLE_API_KEY`)
- Tokens start with `pat`, not `key`
- API keys (starting with `key`) are deprecated as of Feb 2024

## When to Use This Tool

### Automatic Usage Triggers
- User mentions "Airtable" operations
- Managing spreadsheet-like data in the cloud
- Need for database operations without SQL
- Syncing data between services
- Automating record management
- Bulk data operations

### Example User Requests
- "Add this to my Airtable"
- "Show me what's in my CRM base"
- "Update all records where status is pending"
- "Export my inventory to CSV"
- "Create a new entry in Airtable"
- "Find all contacts from last month"

## Usage Patterns

### Authentication Check
```bash
# ALWAYS start with authentication test
airtable whoami --json

# If it fails, check the error - likely missing PAT
# Guide user to create one at https://airtable.com/create/tokens
```

### Discovery Flow
When user mentions Airtable without specifics:
```bash
# 1. List their bases
airtable bases --json

# 2. Get schema for the relevant base
airtable schema BASE_ID --json

# 3. List records or perform requested operation
airtable list BASE_ID "Table Name" --json
```

### Common Operations

#### Adding Records
```bash
# Single record
airtable create BASE_ID "Contacts" \
  --data '{"Name": "John Doe", "Email": "john@example.com"}' \
  --typecast --json

# Multiple records (more efficient)
airtable create BASE_ID "Orders" \
  --data '[{"Product": "Widget", "Qty": 5}, {"Product": "Gadget", "Qty": 3}]' \
  --typecast --json
```

#### Finding Records
```bash
# Use filter formulas for precise queries
airtable list BASE_ID "Customers" \
  --filter-formula "AND({Status}='Active', {City}='New York')" \
  --json

# Date-based queries
airtable list BASE_ID "Tasks" \
  --filter-formula "IS_AFTER({Due Date}, TODAY())" \
  --json
```

#### Updating Records
```bash
# First find the record
records=$(airtable list BASE_ID "Projects" \
  --filter-formula "{Name}='Project Alpha'" --json)
record_id=$(echo "$records" | jq -r '.[0].id')

# Then update it
airtable update BASE_ID "Projects" "$record_id" \
  --data '{"Status": "Completed"}' --json
```

#### Bulk Operations
```bash
# Export for backup
airtable export BASE_ID "Inventory" --output backup.json

# Batch update from file
cat updates.json | \
  airtable update BASE_ID "Products" --file - --json

# Upsert (update or create)
airtable upsert BASE_ID "Contacts" \
  --data '[{"Email": "test@example.com", "Name": "Test User"}]' \
  --merge-on "Email" --json
```

## Advanced Patterns

### Complex Filtering
```bash
# Multiple conditions with OR
airtable list BASE_ID "Leads" \
  --filter-formula "OR({Priority}='High', AND({Score}>80, {Status}='New'))" \
  --json

# Text search
airtable list BASE_ID "Notes" \
  --filter-formula "FIND('urgent', LOWER({Content})) > 0" \
  --json

# Empty field check
airtable list BASE_ID "Contacts" \
  --filter-formula "{Phone} = BLANK()" \
  --json
```

### Working with Views
```bash
# Use pre-configured views for complex filters
airtable list BASE_ID "Orders" --view "This Month" --json
airtable export BASE_ID "Tasks" --view "Overdue" --output overdue.csv
```

### Schema Inspection
```bash
# Get full schema to understand structure
schema=$(airtable schema BASE_ID --json)

# Extract table names
echo "$schema" | jq -r '.tables[].name'

# Find field types
echo "$schema" | jq '.tables[] | select(.name=="Contacts") | .fields[] | {name, type}'
```

## Error Handling

### Rate Limiting
The tool automatically handles rate limits with exponential backoff. If you see rate limit messages, the tool is working correctly - just waiting.

### Common Errors and Solutions

1. **Authentication Failed**
   ```bash
   # Check if using old API key
   if [[ "$AIRTABLE_PAT" == key* ]]; then
     echo "Error: Using deprecated API key. Create a Personal Access Token instead."
   fi
   ```

2. **Permission Denied**
   - Token lacks required scopes
   - Guide user to add scopes at token settings

3. **Base Not Found**
   - List bases to verify access
   - Check if base ID is correct

4. **Invalid Formula**
   - Test in Airtable UI first
   - Ensure field names match exactly

## Integration Patterns

### Data Pipeline
```bash
# Extract from Airtable
airtable export BASE_ID "Source" --output data.json

# Transform with jq
cat data.json | jq '.[] | .fields | {
  name: .Name,
  email: .Email,
  status: (.Status // "Unknown")
}' > transformed.json

# Load to another table
airtable create BASE_ID "Destination" --file transformed.json
```

### Monitoring Script
```bash
# Check for new records periodically
while true; do
  new_count=$(airtable list BASE_ID "Submissions" \
    --filter-formula "CREATED_TIME() > '${last_check}'" \
    --json | jq length)
  
  if [ "$new_count" -gt 0 ]; then
    echo "Found $new_count new submissions"
    # Process them...
  fi
  
  last_check=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")
  sleep 300
done
```

### Sync with External Services
```bash
# Get records modified recently
airtable list BASE_ID "Products" \
  --filter-formula "LAST_MODIFIED_TIME() > '2024-01-01'" \
  --json | \
jq '.[] | {
  id: .id,
  sku: .fields.SKU,
  price: .fields.Price,
  updated: .fields["Last Modified"]
}' | \
# Send to external API
while read -r product; do
  curl -X POST https://api.example.com/products \
    -H "Content-Type: application/json" \
    -d "$product"
done
```

## Best Practices for AI

1. **Always use --json flag** for reliable parsing
2. **Check authentication first** with `whoami`
3. **Use --typecast** when creating/updating to avoid type errors
4. **Batch operations** when possible (up to 10 records)
5. **Cache base/table IDs** - they don't change
6. **Use filter formulas** instead of fetching all records
7. **Handle errors gracefully** - check exit codes

## Important Notes

### Field Names
- Case-sensitive and must match exactly
- Use quotes for fields with spaces: `"{Field Name}"`
- Special characters need escaping in formulas

### Formulas
- Test complex formulas in Airtable UI first
- Use single quotes inside formulas: `"{Status}='Active'"`
- Escape properly in shell: `--filter-formula "{Name}=\"John's Shop\""`

### Limits
- 10 records max per create/update/delete request
- 100 records max per page when listing
- 5 requests/second per base
- Filter formulas have complexity limits

### Data Types
- Dates: ISO 8601 format (2024-01-15)
- Checkboxes: true/false
- Numbers: No quotes needed with --typecast
- Linked records: Array of record IDs
- Attachments: Array of {url, filename} objects

## Security Reminders

- Never log or display the PAT
- Warn users if they paste an API key (starts with 'key')
- PATs are scoped - may not have all permissions
- Tokens inherit user's base permissions