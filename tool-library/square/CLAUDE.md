# Square CLI - AI Instructions

## When to Use This Tool

Use the Square CLI when the user:
- Asks about Square payments, transactions, or financial data
- Needs to manage Square customers or customer lists
- Wants to work with Square catalog items or inventory
- Requires information about Square business locations
- Needs to track or manage Square orders
- Mentions "Square" in context of payment processing or POS systems

## Usage Patterns

### For Automation/Integration
Always use `--json` flag when:
- Integrating with other tools
- Processing data programmatically
- Exporting data for analysis
- Creating reports

```bash
# Get payment data for processing
square payments list --json | jq '.payments[] | {id, amount: .amount_money}'

# Export customer list
square customers list --limit 100 --json > customers.json

# Get location ID for subsequent commands
LOCATION_ID=$(square locations list --json | jq -r '.locations[0].id')
square orders list "$LOCATION_ID" --json
```

### Common Workflows

1. **Payment Reconciliation**
```bash
# List today's payments
square payments list --limit 50 --json | jq '.payments[] | select(.created_at | startswith("2025-01-06"))'
```

2. **Customer Data Export**
```bash
# Export all customers with pagination
square customers list --limit 100 --json > customers_page1.json
# Use cursor from response for next pages
```

3. **Inventory Check**
```bash
# Get catalog items with prices
square catalog list --json | jq '.objects[] | {name: .item_data.name, price: .item_data.variations[0].item_variation_data.price_money}'
```

## Integration Notes

### Authentication
- Always check for `SQUARE_ACCESS_TOKEN` environment variable
- Remind user to set token if missing
- Support both production and sandbox environments

### Error Handling
- Square API errors are formatted for clarity
- JSON mode includes error details in stderr
- Exit codes: 0 (success), 1 (error)

### Output Parsing
When in JSON mode:
- Valid JSON to stdout
- Errors to stderr as JSON
- Use with `jq` for data extraction

### Pagination
For large datasets:
- First request returns cursor in response
- Use `--cursor` parameter for subsequent pages
- Continue until no cursor returned

## Automatic Usage Scenarios

1. **When user mentions Square payments**: Automatically list recent payments
2. **Customer lookup**: Use customer list with appropriate filters
3. **Business overview**: Start with locations list to get context
4. **Order tracking**: Requires location ID first

## Best Practices

1. **Always get location ID first** when working with location-specific data (orders)
2. **Use appropriate limits** - default is 10, max varies by endpoint
3. **Check environment** - production vs sandbox for testing
4. **Parse JSON carefully** - Square uses nested structures

## Common Patterns

### Get First Location ID
```bash
square locations list --json | jq -r '.locations[0].id'
```

### Sum Payment Amounts
```bash
square payments list --limit 100 --json | jq '[.payments[].amount_money.amount] | add / 100'
```

### Filter Customers by Email Domain
```bash
square customers list --json | jq '.customers[] | select(.email_address | endswith("@company.com"))'
```

### Extract Order Line Items
```bash
square orders list LOCATION_ID --json | jq '.orders[].line_items[] | {name, quantity}'
```

## Limitations

- Rate limits apply (varies by endpoint)
- Some operations require additional permissions
- Sandbox environment has limited data
- Not all Square features are exposed via CLI

## Troubleshooting Tips

1. **No data returned**: Check if using correct environment (sandbox vs production)
2. **Authentication fails**: Verify token has necessary permissions
3. **Location required**: Many endpoints need location_id parameter
4. **Pagination needed**: Default limits may not show all data

## Security Notes

- Never log or display full access tokens
- Use environment variables for sensitive data
- Be cautious with customer PII in outputs
- JSON output may contain sensitive information