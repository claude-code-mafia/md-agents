#!/usr/bin/env python3
"""
Airtable CLI - Direct API implementation with maximum functionality

Uses Personal Access Tokens (PATs) for authentication.
Supports all Airtable Web API features including advanced querying,
batch operations, field management, and more.
"""

import argparse
import json
import sys
import os
import time
import csv
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import requests
from urllib.parse import urlencode

# Constants
API_BASE = "https://api.airtable.com/v0"
META_API_BASE = "https://api.airtable.com/v0/meta"
DEFAULT_PAGE_SIZE = 100
MAX_RECORDS_PER_REQUEST = 10
RATE_LIMIT_DELAY = 30  # seconds

# Color codes for output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colored(text: str, color: str) -> str:
    """Return colored text for terminal output."""
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.ENDC}"
    return text

def get_token() -> str:
    """Get Personal Access Token from environment or fail with helpful message."""
    token = os.environ.get('AIRTABLE_PAT')
    if not token:
        print(colored("Error: AIRTABLE_PAT environment variable not set", Colors.FAIL), file=sys.stderr)
        print("\nTo use the Airtable CLI, you need a Personal Access Token:", file=sys.stderr)
        print("1. Go to: https://airtable.com/create/tokens", file=sys.stderr)
        print("2. Create a new token with appropriate scopes", file=sys.stderr)
        print("3. Export it: export AIRTABLE_PAT='your-token-here'", file=sys.stderr)
        print("\n" + colored("Note: API keys are deprecated as of Feb 2024. Use Personal Access Tokens instead.", Colors.WARNING), file=sys.stderr)
        sys.exit(1)
    
    # Warn if it looks like an old API key
    if token.startswith('key'):
        print(colored("Warning: This looks like a deprecated API key. Please use a Personal Access Token instead.", Colors.WARNING), file=sys.stderr)
        print("Get one at: https://airtable.com/create/tokens\n", file=sys.stderr)
    
    return token

class AirtableAPI:
    """Direct API client for Airtable Web API."""
    
    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
    
    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with automatic retry for rate limits."""
        retries = 0
        max_retries = 3
        
        while retries <= max_retries:
            try:
                response = self.session.request(method, url, **kwargs)
                
                if response.status_code == 429:
                    # Rate limited
                    if retries < max_retries:
                        wait_time = RATE_LIMIT_DELAY * (2 ** retries)  # Exponential backoff
                        print(colored(f"Rate limited. Waiting {wait_time} seconds...", Colors.WARNING), file=sys.stderr)
                        time.sleep(wait_time)
                        retries += 1
                        continue
                    else:
                        response.raise_for_status()
                
                elif response.status_code == 401:
                    print(colored("Authentication failed. Check your Personal Access Token.", Colors.FAIL), file=sys.stderr)
                    sys.exit(1)
                
                elif response.status_code == 403:
                    error_data = response.json().get('error', {})
                    print(colored(f"Permission denied: {error_data.get('message', 'Check token scopes')}", Colors.FAIL), file=sys.stderr)
                    sys.exit(1)
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                print(colored(f"API Error: {e}", Colors.FAIL), file=sys.stderr)
                sys.exit(1)
    
    def list_bases(self) -> List[Dict[str, Any]]:
        """List all accessible bases."""
        url = f"{META_API_BASE}/bases"
        response = self._request('GET', url)
        return response.json().get('bases', [])
    
    def get_base_schema(self, base_id: str) -> Dict[str, Any]:
        """Get complete base schema with tables and fields."""
        url = f"{META_API_BASE}/bases/{base_id}/tables"
        response = self._request('GET', url)
        return response.json()
    
    def list_records(self, base_id: str, table_name: str, **params) -> List[Dict[str, Any]]:
        """List records with pagination support."""
        url = f"{API_BASE}/{base_id}/{table_name}"
        records = []
        
        # Set default page size
        if 'pageSize' not in params:
            params['pageSize'] = DEFAULT_PAGE_SIZE
        
        while True:
            response = self._request('GET', url, params=params)
            data = response.json()
            records.extend(data.get('records', []))
            
            # Check for more pages
            offset = data.get('offset')
            if not offset:
                break
            params['offset'] = offset
        
        return records
    
    def get_record(self, base_id: str, table_name: str, record_id: str) -> Dict[str, Any]:
        """Get a specific record."""
        url = f"{API_BASE}/{base_id}/{table_name}/{record_id}"
        response = self._request('GET', url)
        return response.json()
    
    def create_records(self, base_id: str, table_name: str, records: List[Dict[str, Any]], typecast: bool = False) -> List[Dict[str, Any]]:
        """Create one or more records (max 10)."""
        url = f"{API_BASE}/{base_id}/{table_name}"
        created = []
        
        # Process in batches of 10
        for i in range(0, len(records), MAX_RECORDS_PER_REQUEST):
            batch = records[i:i + MAX_RECORDS_PER_REQUEST]
            data = {
                'records': [{'fields': r} for r in batch],
                'typecast': typecast
            }
            response = self._request('POST', url, json=data)
            created.extend(response.json().get('records', []))
        
        return created
    
    def update_records(self, base_id: str, table_name: str, updates: List[Dict[str, Any]], typecast: bool = False) -> List[Dict[str, Any]]:
        """Update one or more records (max 10)."""
        url = f"{API_BASE}/{base_id}/{table_name}"
        updated = []
        
        # Process in batches of 10
        for i in range(0, len(updates), MAX_RECORDS_PER_REQUEST):
            batch = updates[i:i + MAX_RECORDS_PER_REQUEST]
            data = {
                'records': batch,
                'typecast': typecast
            }
            response = self._request('PATCH', url, json=data)
            updated.extend(response.json().get('records', []))
        
        return updated
    
    def upsert_records(self, base_id: str, table_name: str, records: List[Dict[str, Any]], 
                      fields_to_merge_on: List[str], typecast: bool = False) -> Dict[str, Any]:
        """Update existing records or create new ones."""
        url = f"{API_BASE}/{base_id}/{table_name}"
        data = {
            'performUpsert': {
                'fieldsToMergeOn': fields_to_merge_on
            },
            'records': [{'fields': r} for r in records],
            'typecast': typecast
        }
        response = self._request('PATCH', url, json=data)
        return response.json()
    
    def delete_records(self, base_id: str, table_name: str, record_ids: List[str]) -> List[Dict[str, Any]]:
        """Delete one or more records (max 10)."""
        url = f"{API_BASE}/{base_id}/{table_name}"
        deleted = []
        
        # Process in batches of 10
        for i in range(0, len(record_ids), MAX_RECORDS_PER_REQUEST):
            batch = record_ids[i:i + MAX_RECORDS_PER_REQUEST]
            params = {'records[]': batch}
            response = self._request('DELETE', url, params=params)
            deleted.extend(response.json().get('records', []))
        
        return deleted
    
    def create_field(self, base_id: str, table_id: str, field_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new field in a table."""
        url = f"{META_API_BASE}/bases/{base_id}/tables/{table_id}/fields"
        response = self._request('POST', url, json=field_config)
        return response.json()
    
    def update_field(self, base_id: str, table_id: str, field_id: str, field_config: Dict[str, Any]) -> Dict[str, Any]:
        """Update field configuration."""
        url = f"{META_API_BASE}/bases/{base_id}/tables/{table_id}/fields/{field_id}"
        response = self._request('PATCH', url, json=field_config)
        return response.json()

def format_record(record: Dict[str, Any], show_metadata: bool = True) -> str:
    """Format a record for human-readable output."""
    lines = []
    
    if show_metadata:
        lines.append(colored(f"ID: {record['id']}", Colors.CYAN))
        lines.append(f"Created: {record.get('createdTime', 'N/A')}")
    
    fields = record.get('fields', {})
    if fields:
        lines.append(colored("Fields:", Colors.BOLD))
        for key, value in fields.items():
            if isinstance(value, list):
                if len(value) > 0 and isinstance(value[0], dict):
                    # Probably attachments or complex objects
                    value = f"[{len(value)} items]"
                else:
                    value = ', '.join(str(v) for v in value)
            elif isinstance(value, dict):
                value = json.dumps(value, indent=2)
            lines.append(f"  {colored(key, Colors.BLUE)}: {value}")
    else:
        lines.append("Fields: (empty)")
    
    return '\n'.join(lines)

def format_table(records: List[Dict[str, Any]], fields: Optional[List[str]] = None) -> str:
    """Format records as a table."""
    if not records:
        return "No records found"
    
    # Collect all field names if not specified
    if not fields:
        all_fields = set()
        for record in records:
            all_fields.update(record.get('fields', {}).keys())
        fields = sorted(list(all_fields))
    
    if not fields:
        return "No fields found in records"
    
    # Calculate column widths
    widths = {'ID': 15}
    for field in fields:
        max_width = len(field)
        for record in records:
            value = str(record.get('fields', {}).get(field, ''))
            if len(value) > 50:  # Truncate long values
                value = value[:47] + '...'
            max_width = max(max_width, len(value))
        widths[field] = min(max_width, 50)
    
    # Print header
    header = f"{'ID':<15} "
    header += ' '.join(f"{field:<{widths[field]}}" for field in fields)
    print(colored(header, Colors.BOLD))
    print('-' * len(header))
    
    # Print records
    for record in records:
        row = f"{record['id']:<15} "
        for field in fields:
            value = str(record.get('fields', {}).get(field, ''))
            if len(value) > widths[field]:
                value = value[:widths[field]-3] + '...'
            row += f"{value:<{widths[field]}} "
        print(row)
    
    return f"\n{colored(f'Total: {len(records)} records', Colors.GREEN)}"

# Command implementations
def cmd_whoami(api: AirtableAPI, args) -> None:
    """Test authentication and show user info."""
    try:
        # Try to list bases as a test
        bases = api.list_bases()
        
        if args.json:
            print(json.dumps({
                'authenticated': True,
                'bases_count': len(bases),
                'token_type': 'Personal Access Token'
            }, indent=2))
        else:
            print(colored("✓ Authentication successful!", Colors.GREEN))
            print(f"Token type: Personal Access Token")
            print(f"Accessible bases: {len(bases)}")
    except Exception as e:
        if args.json:
            print(json.dumps({'authenticated': False, 'error': str(e)}, indent=2))
        else:
            print(colored("✗ Authentication failed", Colors.FAIL))
        sys.exit(1)

def cmd_bases(api: AirtableAPI, args) -> None:
    """List all accessible bases."""
    bases = api.list_bases()
    
    if args.json:
        print(json.dumps(bases, indent=2))
    else:
        if not bases:
            print("No bases found")
            return
        
        print(colored(f"Found {len(bases)} bases:\n", Colors.BOLD))
        for base in bases:
            print(colored(f"ID: {base['id']}", Colors.CYAN))
            print(f"Name: {base['name']}")
            print(f"Permission: {base.get('permissionLevel', 'N/A')}")
            print()

def cmd_schema(api: AirtableAPI, args) -> None:
    """Get complete base schema."""
    schema = api.get_base_schema(args.base_id)
    
    if args.json:
        print(json.dumps(schema, indent=2))
    else:
        tables = schema.get('tables', [])
        print(colored(f"Base: {args.base_id}", Colors.BOLD))
        print(colored(f"Tables: {len(tables)}\n", Colors.BOLD))
        
        for table in tables:
            print(colored(f"Table: {table['name']}", Colors.CYAN))
            print(f"  ID: {table['id']}")
            if table.get('description'):
                print(f"  Description: {table['description']}")
            
            fields = table.get('fields', [])
            print(f"  Fields ({len(fields)}):")
            for field in fields:
                print(f"    - {colored(field['name'], Colors.BLUE)} ({field['type']})")
                if field.get('description'):
                    print(f"      {field['description']}")
            
            views = table.get('views', [])
            if views:
                print(f"  Views ({len(views)}):")
                for view in views:
                    print(f"    - {view['name']} ({view['type']})")
            print()

def cmd_list(api: AirtableAPI, args) -> None:
    """List records with advanced filtering."""
    params = {}
    
    if args.fields:
        params['fields'] = args.fields
    if args.filter_formula:
        params['filterByFormula'] = args.filter_formula
    if args.max_records:
        params['maxRecords'] = args.max_records
    if args.page_size:
        params['pageSize'] = min(args.page_size, 100)
    if args.sort:
        # Parse sort format: field:direction,field:direction
        sort_list = []
        for sort_item in args.sort:
            parts = sort_item.split(':')
            if len(parts) == 2:
                sort_list.append({'field': parts[0], 'direction': parts[1]})
            else:
                sort_list.append({'field': sort_item, 'direction': 'asc'})
        params['sort'] = sort_list
    if args.view:
        params['view'] = args.view
    
    records = api.list_records(args.base_id, args.table_name, **params)
    
    if args.json:
        print(json.dumps(records, indent=2))
    else:
        if args.format == 'table':
            print(format_table(records, args.fields))
        else:
            for i, record in enumerate(records):
                if i > 0:
                    print('-' * 40)
                print(format_record(record))
            
            print(f"\n{colored(f'Total: {len(records)} records', Colors.GREEN)}")

def cmd_get(api: AirtableAPI, args) -> None:
    """Get a specific record."""
    record = api.get_record(args.base_id, args.table_name, args.record_id)
    
    if args.json:
        print(json.dumps(record, indent=2))
    else:
        print(format_record(record))

def cmd_create(api: AirtableAPI, args) -> None:
    """Create one or more records."""
    # Parse input data
    if args.data:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(colored(f"Invalid JSON: {e}", Colors.FAIL), file=sys.stderr)
            sys.exit(1)
    elif args.file:
        with open(args.file, 'r') as f:
            data = json.load(f)
    else:
        print(colored("Error: Provide --data or --file", Colors.FAIL), file=sys.stderr)
        sys.exit(1)
    
    # Ensure data is a list
    if isinstance(data, dict):
        data = [data]
    
    created = api.create_records(args.base_id, args.table_name, data, args.typecast)
    
    if args.json:
        print(json.dumps(created, indent=2))
    else:
        print(colored(f"Created {len(created)} record(s):", Colors.GREEN))
        for record in created:
            print(f"\n{format_record(record)}")

def cmd_update(api: AirtableAPI, args) -> None:
    """Update one or more records."""
    # Parse input data
    if args.data:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(colored(f"Invalid JSON: {e}", Colors.FAIL), file=sys.stderr)
            sys.exit(1)
    elif args.file:
        with open(args.file, 'r') as f:
            data = json.load(f)
    else:
        print(colored("Error: Provide --data or --file", Colors.FAIL), file=sys.stderr)
        sys.exit(1)
    
    # Handle single record update
    if args.record_id:
        updates = [{'id': args.record_id, 'fields': data}]
    else:
        # Batch update - data should be list of {id, fields}
        if not isinstance(data, list):
            print(colored("Error: Batch update requires array of {id, fields} objects", Colors.FAIL), file=sys.stderr)
            sys.exit(1)
        updates = data
    
    updated = api.update_records(args.base_id, args.table_name, updates, args.typecast)
    
    if args.json:
        print(json.dumps(updated, indent=2))
    else:
        print(colored(f"Updated {len(updated)} record(s):", Colors.GREEN))
        for record in updated:
            print(f"\n{format_record(record)}")

def cmd_upsert(api: AirtableAPI, args) -> None:
    """Update existing records or create new ones."""
    # Parse input data
    if args.data:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(colored(f"Invalid JSON: {e}", Colors.FAIL), file=sys.stderr)
            sys.exit(1)
    elif args.file:
        with open(args.file, 'r') as f:
            data = json.load(f)
    else:
        print(colored("Error: Provide --data or --file", Colors.FAIL), file=sys.stderr)
        sys.exit(1)
    
    # Ensure data is a list
    if isinstance(data, dict):
        data = [data]
    
    result = api.upsert_records(args.base_id, args.table_name, data, args.merge_on, args.typecast)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        created = result.get('createdRecords', [])
        updated = result.get('updatedRecords', [])
        
        print(colored(f"Upsert complete:", Colors.GREEN))
        print(f"  Created: {len(created)} records")
        print(f"  Updated: {len(updated)} records")
        
        if created:
            print(colored("\nCreated records:", Colors.BOLD))
            for record in created:
                print(f"\n{format_record(record)}")
        
        if updated:
            print(colored("\nUpdated records:", Colors.BOLD))
            for record in updated:
                print(f"\n{format_record(record)}")

def cmd_delete(api: AirtableAPI, args) -> None:
    """Delete one or more records."""
    if args.record_ids:
        record_ids = args.record_ids
    elif args.file:
        with open(args.file, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                record_ids = data
            else:
                print(colored("Error: File must contain array of record IDs", Colors.FAIL), file=sys.stderr)
                sys.exit(1)
    else:
        print(colored("Error: Provide record IDs or --file", Colors.FAIL), file=sys.stderr)
        sys.exit(1)
    
    # Confirm deletion
    if not args.force and not args.json:
        print(f"About to delete {len(record_ids)} record(s):")
        for rid in record_ids[:5]:
            print(f"  - {rid}")
        if len(record_ids) > 5:
            print(f"  ... and {len(record_ids) - 5} more")
        
        response = input(colored("\nAre you sure? (y/N): ", Colors.WARNING))
        if response.lower() != 'y':
            print("Deletion cancelled")
            return
    
    deleted = api.delete_records(args.base_id, args.table_name, record_ids)
    
    if args.json:
        print(json.dumps(deleted, indent=2))
    else:
        print(colored(f"Deleted {len(deleted)} record(s):", Colors.GREEN))
        for record in deleted:
            print(f"  - {record['id']}")

def cmd_fields(api: AirtableAPI, args) -> None:
    """List all fields with metadata."""
    schema = api.get_base_schema(args.base_id)
    
    # Find the table
    table = None
    for t in schema.get('tables', []):
        if t['id'] == args.table_name or t['name'] == args.table_name:
            table = t
            break
    
    if not table:
        print(colored(f"Table '{args.table_name}' not found", Colors.FAIL), file=sys.stderr)
        sys.exit(1)
    
    fields = table.get('fields', [])
    
    if args.json:
        print(json.dumps(fields, indent=2))
    else:
        print(colored(f"Fields in {table['name']} ({len(fields)} total):\n", Colors.BOLD))
        for field in fields:
            print(colored(f"{field['name']}", Colors.CYAN))
            print(f"  ID: {field['id']}")
            print(f"  Type: {field['type']}")
            if field.get('description'):
                print(f"  Description: {field['description']}")
            
            # Show type-specific options
            options = field.get('options', {})
            if options:
                print(f"  Options:")
                for key, value in options.items():
                    print(f"    {key}: {value}")
            print()

def cmd_export(api: AirtableAPI, args) -> None:
    """Export table data to CSV or JSON."""
    # Get all records
    params = {}
    if args.view:
        params['view'] = args.view
    if args.filter_formula:
        params['filterByFormula'] = args.filter_formula
    
    records = api.list_records(args.base_id, args.table_name, **params)
    
    # Determine format
    format = args.format
    if not format and args.output:
        if args.output.endswith('.csv'):
            format = 'csv'
        else:
            format = 'json'
    else:
        format = format or 'json'
    
    if format == 'csv':
        # Collect all field names
        all_fields = set()
        for record in records:
            all_fields.update(record.get('fields', {}).keys())
        
        fieldnames = ['id', 'createdTime'] + sorted(list(all_fields))
        
        if args.output:
            with open(args.output, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for record in records:
                    row = {'id': record['id'], 'createdTime': record['createdTime']}
                    row.update(record.get('fields', {}))
                    writer.writerow(row)
            print(colored(f"Exported {len(records)} records to {args.output}", Colors.GREEN))
        else:
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                row = {'id': record['id'], 'createdTime': record['createdTime']}
                row.update(record.get('fields', {}))
                writer.writerow(row)
    else:  # JSON
        output = json.dumps(records, indent=2)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(colored(f"Exported {len(records)} records to {args.output}", Colors.GREEN))
        else:
            print(output)

def main():
    parser = argparse.ArgumentParser(
        description='Airtable CLI - Powerful command-line interface for Airtable',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  airtable whoami                                   # Test authentication
  airtable bases                                    # List all bases
  airtable schema appXXXXXX                        # Show base schema
  airtable list appXXXXXX "Table Name"            # List records
  airtable list appXXXXXX "Table" --filter-formula "Status='Active'"
  airtable create appXXXXXX "Table" --data '{"Name": "Test"}'
  airtable update appXXXXXX "Table" recXXXXXX --data '{"Status": "Done"}'
  airtable delete appXXXXXX "Table" recXXXXXX recYYYYYY
  airtable export appXXXXXX "Table" --output data.csv

Environment:
  AIRTABLE_PAT    Personal Access Token (required)
        """
    )
    
    parser.add_argument('--token', help='Personal Access Token (overrides AIRTABLE_PAT)')
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Common arguments for output format
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # whoami command
    whoami_parser = subparsers.add_parser('whoami', help='Test authentication', parents=[common_parser])
    
    # bases command
    bases_parser = subparsers.add_parser('bases', help='List all accessible bases', parents=[common_parser])
    
    # schema command
    schema_parser = subparsers.add_parser('schema', help='Get complete base schema', parents=[common_parser])
    schema_parser.add_argument('base_id', help='Base ID')
    
    # list command
    list_parser = subparsers.add_parser('list', help='List records with filtering', parents=[common_parser])
    list_parser.add_argument('base_id', help='Base ID')
    list_parser.add_argument('table_name', help='Table name or ID')
    list_parser.add_argument('--fields', nargs='+', help='Specific fields to return')
    list_parser.add_argument('--filter-formula', help='Airtable formula for filtering')
    list_parser.add_argument('--max-records', type=int, help='Maximum records to return')
    list_parser.add_argument('--page-size', type=int, help='Records per page (max 100)')
    list_parser.add_argument('--sort', nargs='+', help='Sort by field:direction (e.g., Name:asc)')
    list_parser.add_argument('--view', help='Use a specific view')
    list_parser.add_argument('--format', choices=['table', 'full'], default='full', help='Output format')
    
    # get command
    get_parser = subparsers.add_parser('get', help='Get a specific record', parents=[common_parser])
    get_parser.add_argument('base_id', help='Base ID')
    get_parser.add_argument('table_name', help='Table name or ID')
    get_parser.add_argument('record_id', help='Record ID')
    
    # create command
    create_parser = subparsers.add_parser('create', help='Create records', parents=[common_parser])
    create_parser.add_argument('base_id', help='Base ID')
    create_parser.add_argument('table_name', help='Table name or ID')
    create_parser.add_argument('--data', help='JSON data for fields')
    create_parser.add_argument('--file', help='JSON file with record data')
    create_parser.add_argument('--typecast', action='store_true', help='Enable automatic type conversion')
    
    # update command
    update_parser = subparsers.add_parser('update', help='Update records', parents=[common_parser])
    update_parser.add_argument('base_id', help='Base ID')
    update_parser.add_argument('table_name', help='Table name or ID')
    update_parser.add_argument('record_id', nargs='?', help='Record ID (for single update)')
    update_parser.add_argument('--data', help='JSON data for fields')
    update_parser.add_argument('--file', help='JSON file with update data')
    update_parser.add_argument('--typecast', action='store_true', help='Enable automatic type conversion')
    
    # upsert command
    upsert_parser = subparsers.add_parser('upsert', help='Update or create records', parents=[common_parser])
    upsert_parser.add_argument('base_id', help='Base ID')
    upsert_parser.add_argument('table_name', help='Table name or ID')
    upsert_parser.add_argument('--data', help='JSON data for fields')
    upsert_parser.add_argument('--file', help='JSON file with record data')
    upsert_parser.add_argument('--merge-on', nargs='+', required=True, help='Fields to match for update')
    upsert_parser.add_argument('--typecast', action='store_true', help='Enable automatic type conversion')
    
    # delete command
    delete_parser = subparsers.add_parser('delete', help='Delete records', parents=[common_parser])
    delete_parser.add_argument('base_id', help='Base ID')
    delete_parser.add_argument('table_name', help='Table name or ID')
    delete_parser.add_argument('record_ids', nargs='*', help='Record IDs to delete')
    delete_parser.add_argument('--file', help='JSON file with record IDs')
    delete_parser.add_argument('--force', action='store_true', help='Skip confirmation')
    
    # fields command
    fields_parser = subparsers.add_parser('fields', help='List fields with metadata', parents=[common_parser])
    fields_parser.add_argument('base_id', help='Base ID')
    fields_parser.add_argument('table_name', help='Table name or ID')
    
    # export command
    export_parser = subparsers.add_parser('export', help='Export table data', parents=[common_parser])
    export_parser.add_argument('base_id', help='Base ID')
    export_parser.add_argument('table_name', help='Table name or ID')
    export_parser.add_argument('--output', help='Output file')
    export_parser.add_argument('--format', choices=['json', 'csv'], help='Export format')
    export_parser.add_argument('--view', help='Use a specific view')
    export_parser.add_argument('--filter-formula', help='Airtable formula for filtering')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Get token
    token = args.token if hasattr(args, 'token') and args.token else get_token()
    api = AirtableAPI(token)
    
    # Route to appropriate command
    commands = {
        'whoami': cmd_whoami,
        'bases': cmd_bases,
        'schema': cmd_schema,
        'list': cmd_list,
        'get': cmd_get,
        'create': cmd_create,
        'update': cmd_update,
        'upsert': cmd_upsert,
        'delete': cmd_delete,
        'fields': cmd_fields,
        'export': cmd_export,
    }
    
    command_func = commands.get(args.command)
    if command_func:
        try:
            command_func(api, args)
        except KeyboardInterrupt:
            print(colored("\nOperation cancelled", Colors.WARNING), file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()