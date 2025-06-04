# Square CLI

Command-line interface for Square API - manage payments, customers, catalog items, and more.

## Installation

```bash
./install-tool.sh square
```

## Configuration

Set your Square access token as an environment variable:

```bash
export SQUARE_ACCESS_TOKEN='your-access-token'
```

Get your access token from: https://developer.squareup.com/apps

### Environment Options

- `SQUARE_ACCESS_TOKEN` (required): Your Square API access token
- `SQUARE_ENVIRONMENT` (optional): Set to 'sandbox' for testing (default: 'production')

## Usage

```bash
square [command] [subcommand] [options]
```

### Global Options

- `--json`: Output results in JSON format

## Commands

### Payments

List recent payments:
```bash
square payments list
square payments list --limit 20
square payments list --json
```

Get payment details:
```bash
square payments get PAYMENT_ID
square payments get PAYMENT_ID --json
```

### Customers

List customers:
```bash
square customers list
square customers list --limit 50
```

Create a new customer:
```bash
square customers create customer@example.com
square customers create customer@example.com --given-name John --family-name Doe
square customers create customer@example.com --phone "+1234567890"
```

### Catalog

List catalog items:
```bash
square catalog list
square catalog list --limit 30 --json
```

### Locations

List business locations:
```bash
square locations list
square locations list --json
```

### Orders

List orders for a location:
```bash
square orders list LOCATION_ID
square orders list LOCATION_ID --limit 25
```

## Examples

### Payment Processing Workflow

1. List recent payments:
```bash
square payments list --limit 5
```

2. Get details for a specific payment:
```bash
square payments get pm_1234567890
```

3. Export payment data as JSON:
```bash
square payments list --json > payments.json
```

### Customer Management

1. Create a new customer:
```bash
square customers create john@example.com --given-name John --family-name Doe
```

2. List all customers:
```bash
square customers list --limit 100 --json
```

### Inventory Management

1. List all catalog items:
```bash
square catalog list
```

2. Export catalog as JSON:
```bash
square catalog list --json > catalog.json
```

## Pagination

For commands that support pagination, use the `--cursor` option with the cursor value from the previous response:

```bash
# First page
square payments list --limit 10 --json > page1.json

# Get cursor from response and fetch next page
square payments list --limit 10 --cursor "CURSOR_VALUE"
```

## Error Handling

The CLI provides clear error messages for common issues:

- Missing authentication token
- Invalid API credentials
- Network connectivity issues
- Invalid command syntax
- API rate limits

## Output Formats

### Human-Readable (Default)

Formatted output designed for terminal display:
```
ID: pm_1234567890
Amount: $25.00 USD
Status: COMPLETED
Created: 2025-01-06 10:30:45
Receipt: https://squareup.com/receipt/...
```

### JSON Format

Machine-readable JSON output for integration:
```bash
square payments get pm_1234567890 --json
```

## API Limits

Square API has rate limits. The CLI will display appropriate error messages if limits are exceeded.

## Sandbox Testing

To test with Square's sandbox environment:

```bash
export SQUARE_ENVIRONMENT='sandbox'
export SQUARE_ACCESS_TOKEN='your-sandbox-token'
```

## Troubleshooting

### Authentication Error
```
Error: SQUARE_ACCESS_TOKEN environment variable not set
```
Solution: Set your access token as shown in the Configuration section.

### Invalid Environment
```
Error: Invalid SQUARE_ENVIRONMENT: testing
```
Solution: Use only 'production' or 'sandbox' for the environment.

### API Errors
The CLI will display specific error messages from the Square API, including validation errors and missing required fields.

## Support

- Square API Documentation: https://developer.squareup.com/reference/square
- Square Developer Dashboard: https://developer.squareup.com/apps
- API Status: https://developer.squareup.com/status