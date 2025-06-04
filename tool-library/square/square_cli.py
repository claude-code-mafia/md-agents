#!/usr/bin/env python3
"""Square CLI - Command-line interface for Square API."""

import sys
import os
import json
import argparse
from datetime import datetime
from typing import Optional, Dict, Any, List, Union

import square


def get_client():
    """Initialize Square client with authentication."""
    access_token = os.environ.get('SQUARE_ACCESS_TOKEN')
    if not access_token:
        print("Error: SQUARE_ACCESS_TOKEN environment variable not set", file=sys.stderr)
        print("Get your access token from: https://developer.squareup.com/apps", file=sys.stderr)
        sys.exit(1)
    
    environment = os.environ.get('SQUARE_ENVIRONMENT', 'production').lower()
    if environment not in ['production', 'sandbox']:
        print(f"Error: Invalid SQUARE_ENVIRONMENT: {environment}", file=sys.stderr)
        print("Use 'production' or 'sandbox'", file=sys.stderr)
        sys.exit(1)
    
    env_map = {
        'production': square.environment.SquareEnvironment.PRODUCTION,
        'sandbox': square.environment.SquareEnvironment.SANDBOX
    }
    
    return square.Square(
        token=access_token,
        environment=env_map[environment]
    )


def format_money(money: Any) -> str:
    """Format Square Money object as human-readable string."""
    if not money:
        return "$0.00"
    
    # Handle both dict and object formats
    if isinstance(money, dict):
        amount = money.get('amount', 0)
        currency = money.get('currency', 'USD')
    else:
        amount = getattr(money, 'amount', 0)
        currency = getattr(money, 'currency', 'USD')
    
    # Convert cents to dollars
    dollars = amount / 100
    return f"${dollars:.2f} {currency}"


def format_datetime(iso_string: str) -> str:
    """Format ISO datetime string as human-readable."""
    if not iso_string:
        return "N/A"
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return iso_string


def handle_api_errors(func):
    """Decorator to handle Square API errors consistently."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'body'):
                try:
                    error_body = json.loads(e.body)
                    if 'errors' in error_body:
                        errors = error_body['errors']
                        error_msg = "; ".join([err.get('detail', str(err)) for err in errors])
                except:
                    pass
            
            json_output = kwargs.get('json_output') or (args[-1] if args and isinstance(args[-1], bool) else False)
            if json_output:
                print(json.dumps({"error": error_msg}), file=sys.stderr)
            else:
                print(f"API Error: {error_msg}", file=sys.stderr)
            sys.exit(1)
    return wrapper


@handle_api_errors
def list_payments(client, limit: int = 10, cursor: Optional[str] = None, json_output: bool = False):
    """List recent payments."""
    # The list method returns a pager that yields results
    payments = []
    try:
        if cursor:
            # For cursor-based pagination, we need to use the appropriate method
            result = client.payments.list(limit=limit)
            for payment in result:
                payments.append(payment)
                if len(payments) >= limit:
                    break
        else:
            result = client.payments.list(limit=limit)
            for payment in result:
                payments.append(payment)
                if len(payments) >= limit:
                    break
    except Exception as e:
        raise Exception(str(e))
    
    if json_output:
        # Convert payments to dict format
        data = {'payments': []}
        for payment in payments:
            if hasattr(payment, 'model_dump'):
                data['payments'].append(payment.model_dump())
            elif hasattr(payment, 'dict'):
                data['payments'].append(payment.dict())
            else:
                data['payments'].append(vars(payment))
        print(json.dumps(data, indent=2))
    else:
        if not payments:
            print("No payments found.")
            return
        
        for payment in payments:
            print(f"ID: {payment.id}")
            print(f"Amount: {format_money(getattr(payment, 'amount_money', None))}")
            print(f"Status: {getattr(payment, 'status', 'UNKNOWN')}")
            print(f"Created: {format_datetime(getattr(payment, 'created_at', ''))}")
            print(f"Receipt: {getattr(payment, 'receipt_url', 'N/A')}")
            print()


@handle_api_errors
def get_payment(client, payment_id: str, json_output: bool = False):
    """Get details of a specific payment."""
    try:
        response = client.payments.get(payment_id=payment_id)
        payment = response.payment
    except Exception as e:
        raise Exception(str(e))
    
    if json_output:
        if hasattr(payment, 'model_dump'):
            print(json.dumps(payment.model_dump(), indent=2))
        elif hasattr(payment, 'dict'):
            print(json.dumps(payment.dict(), indent=2))
        else:
            print(json.dumps(vars(payment), indent=2))
    else:
        print(f"ID: {payment.id}")
        print(f"Amount: {format_money(getattr(payment, 'amount_money', None))}")
        print(f"Status: {getattr(payment, 'status', 'UNKNOWN')}")
        print(f"Created: {format_datetime(getattr(payment, 'created_at', ''))}")
        print(f"Updated: {format_datetime(getattr(payment, 'updated_at', ''))}")
        print(f"Receipt: {getattr(payment, 'receipt_url', 'N/A')}")
        
        card_details = getattr(payment, 'card_details', None)
        if card_details:
            card = getattr(card_details, 'card', None)
            if card:
                print(f"Card: **** {getattr(card, 'last_4', 'XXXX')}")
                print(f"Brand: {getattr(card, 'card_brand', 'UNKNOWN')}")
        
        buyer_email = getattr(payment, 'buyer_email_address', None)
        if buyer_email:
            print(f"Email: {buyer_email}")


@handle_api_errors
def list_customers(client, limit: int = 10, cursor: Optional[str] = None, json_output: bool = False):
    """List customers."""
    # The list method returns a pager that yields results
    customers = []
    try:
        result = client.customers.list(limit=limit)
        for customer in result:
            customers.append(customer)
            if len(customers) >= limit:
                break
    except Exception as e:
        raise Exception(str(e))
    
    if json_output:
        # Convert to dict format
        data = {'customers': []}
        for customer in customers:
            if hasattr(customer, 'model_dump'):
                data['customers'].append(customer.model_dump())
            elif hasattr(customer, 'dict'):
                data['customers'].append(customer.dict())
            else:
                data['customers'].append(vars(customer))
        print(json.dumps(data, indent=2))
    else:
        if not customers:
            print("No customers found.")
            return
        
        for customer in customers:
            print(f"ID: {customer.id}")
            given_name = getattr(customer, 'given_name', '')
            family_name = getattr(customer, 'family_name', '')
            name = f"{given_name} {family_name}".strip()
            print(f"Name: {name or 'N/A'}")
            print(f"Email: {getattr(customer, 'email_address', 'N/A')}")
            print(f"Phone: {getattr(customer, 'phone_number', 'N/A')}")
            print(f"Created: {format_datetime(getattr(customer, 'created_at', ''))}")
            print()


@handle_api_errors
def create_customer(client, email: str, given_name: Optional[str] = None, 
                   family_name: Optional[str] = None, phone: Optional[str] = None,
                   json_output: bool = False):
    """Create a new customer."""
    body = {
        'email_address': email
    }
    
    if given_name:
        body['given_name'] = given_name
    if family_name:
        body['family_name'] = family_name
    if phone:
        body['phone_number'] = phone
    
    result = client.customers.create(**body)
    customer = result.customer
    
    if json_output:
        if hasattr(customer, 'model_dump'):
            print(json.dumps({'customer': customer.model_dump()}, indent=2))
        elif hasattr(customer, 'dict'):
            print(json.dumps({'customer': customer.dict()}, indent=2))
        else:
            print(json.dumps({'customer': vars(customer)}, indent=2))
    else:
        print(f"Customer created successfully!")
        print(f"ID: {customer.id}")
        given_name = getattr(customer, 'given_name', '')
        family_name = getattr(customer, 'family_name', '')
        name = f"{given_name} {family_name}".strip()
        print(f"Name: {name or 'N/A'}")
        print(f"Email: {getattr(customer, 'email_address', 'N/A')}")
        print(f"Phone: {getattr(customer, 'phone_number', 'N/A')}")


@handle_api_errors
def list_catalog_items(client, limit: int = 10, cursor: Optional[str] = None, json_output: bool = False):
    """List catalog items."""
    items = []
    try:
        # Use list() which returns a pager
        result = client.catalog.list(types='ITEM')
        for item in result:
            items.append(item)
            if len(items) >= limit:
                break
    except Exception as e:
        raise Exception(str(e))
    
    if json_output:
        # Convert to dict format
        data = {'objects': []}
        for item in items:
            if hasattr(item, 'model_dump'):
                data['objects'].append(item.model_dump())
            elif hasattr(item, 'dict'):
                data['objects'].append(item.dict())
            else:
                data['objects'].append(vars(item))
        print(json.dumps(data, indent=2))
    else:
        if not items:
            print("No catalog items found.")
            return
        
        for item in items:
            item_data = getattr(item, 'item_data', None)
            print(f"ID: {item.id}")
            if item_data:
                print(f"Name: {getattr(item_data, 'name', 'N/A')}")
                print(f"Description: {getattr(item_data, 'description', 'N/A')}")
                
                # Get price from variations
                variations = getattr(item_data, 'variations', [])
                if variations and len(variations) > 0:
                    var_data = getattr(variations[0], 'item_variation_data', None)
                    if var_data:
                        price_money = getattr(var_data, 'price_money', None)
                        if price_money:
                            print(f"Price: {format_money(price_money)}")
            
            print()


@handle_api_errors
def list_locations(client, json_output: bool = False):
    """List business locations."""
    result = client.locations.list()
    
    if hasattr(result, 'is_error') and result.is_error():
        raise Exception(result.errors)
    
    locations = result.locations or []
    
    if json_output:
        # Convert to dict for JSON serialization
        data = {'locations': []}
        for loc in locations:
            # Use model_dump if available, otherwise convert manually
            if hasattr(loc, 'model_dump'):
                data['locations'].append(loc.model_dump())
            elif hasattr(loc, 'dict'):
                data['locations'].append(loc.dict())
            else:
                data['locations'].append(vars(loc))
        print(json.dumps(data, indent=2))
    else:
        if not locations:
            print("No locations found.")
            return
        
        for location in locations:
            print(f"ID: {location.id}")
            print(f"Name: {getattr(location, 'name', 'N/A')}")
            print(f"Status: {getattr(location, 'status', 'N/A')}")
            
            address = getattr(location, 'address', None)
            if address:
                addr_lines = []
                if hasattr(address, 'address_line_1') and address.address_line_1:
                    addr_lines.append(address.address_line_1)
                if hasattr(address, 'address_line_2') and address.address_line_2:
                    addr_lines.append(address.address_line_2)
                if hasattr(address, 'locality') and hasattr(address, 'administrative_district_level_1'):
                    if address.locality and address.administrative_district_level_1:
                        postal = getattr(address, 'postal_code', '')
                        addr_lines.append(f"{address.locality}, {address.administrative_district_level_1} {postal}")
                if addr_lines:
                    print(f"Address: {', '.join(addr_lines)}")
            
            print(f"Phone: {getattr(location, 'phone_number', 'N/A')}")
            print()


@handle_api_errors
def list_orders(client, location_id: str, limit: int = 10, cursor: Optional[str] = None, json_output: bool = False):
    """List orders for a location."""
    try:
        result = client.orders.search(
            location_ids=[location_id],
            limit=limit,
            cursor=cursor
        )
        orders = result.orders or []
    except Exception as e:
        raise Exception(str(e))
    
    if json_output:
        # Convert to dict format
        data = {'orders': []}
        for order in orders:
            if hasattr(order, 'model_dump'):
                data['orders'].append(order.model_dump())
            elif hasattr(order, 'dict'):
                data['orders'].append(order.dict())
            else:
                data['orders'].append(vars(order))
        print(json.dumps(data, indent=2))
    else:
        if not orders:
            print("No orders found.")
            return
        
        for order in orders:
            print(f"ID: {order.id}")
            print(f"State: {getattr(order, 'state', 'N/A')}")
            print(f"Total: {format_money(getattr(order, 'total_money', None))}")
            print(f"Created: {format_datetime(getattr(order, 'created_at', ''))}")
            
            line_items = getattr(order, 'line_items', [])
            if line_items:
                print("Items:")
                for item in line_items[:3]:  # Show first 3 items
                    name = getattr(item, 'name', 'N/A')
                    quantity = getattr(item, 'quantity', '1')
                    print(f"  - {name} x{quantity}")
                if len(line_items) > 3:
                    print(f"  ... and {len(line_items) - 3} more items")
            
            print()


@handle_api_errors
def list_invoices(client, location_id: str, limit: int = 10, cursor: Optional[str] = None, json_output: bool = False):
    """List invoices for a location."""
    try:
        # Use list to get all invoices (search has complex parameters)
        invoices = []
        result = client.invoices.list(location_id=location_id, limit=limit, cursor=cursor)
        
        # Filter for last month
        from datetime import datetime, timedelta, timezone
        one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)
        
        for invoice in result:
            # Check if created in last month
            created_at = getattr(invoice, 'created_at', '')
            if created_at:
                invoice_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                if invoice_date >= one_month_ago:
                    invoices.append(invoice)
            if len(invoices) >= limit:
                break
    except Exception as e:
        raise Exception(str(e))
    
    if json_output:
        # Convert to dict format
        data = {'invoices': []}
        for invoice in invoices:
            if hasattr(invoice, 'model_dump'):
                data['invoices'].append(invoice.model_dump())
            elif hasattr(invoice, 'dict'):
                data['invoices'].append(invoice.dict())
            else:
                data['invoices'].append(vars(invoice))
        print(json.dumps(data, indent=2))
    else:
        if not invoices:
            print("No invoices found.")
            return
        
        for invoice in invoices:
            print(f"ID: {invoice.id}")
            print(f"Number: {getattr(invoice, 'invoice_number', 'N/A')}")
            print(f"Status: {getattr(invoice, 'status', 'N/A')}")
            print(f"Total: {format_money(getattr(invoice, 'total_money', None))}")
            print(f"Created: {format_datetime(getattr(invoice, 'created_at', ''))}")
            
            recipient = getattr(invoice, 'primary_recipient', None)
            if recipient:
                customer_id = getattr(recipient, 'customer_id', None)
                if customer_id:
                    print(f"Customer ID: {customer_id}")
            
            payment_requests = getattr(invoice, 'payment_requests', [])
            if payment_requests and len(payment_requests) > 0:
                due_date = getattr(payment_requests[0], 'due_date', 'N/A')
                print(f"Due Date: {due_date}")
            else:
                print(f"Due Date: N/A")
            print()


@handle_api_errors
def create_invoice(client, location_id: str, customer_id: str, description: str, 
                  amount: float, due_date: Optional[str] = None, json_output: bool = False):
    """Create a new invoice."""
    try:
        from datetime import datetime, timedelta, timezone
        
        # Convert dollar amount to cents
        amount_cents = int(amount * 100)
        
        # Set due date to 30 days from now if not specified
        if not due_date:
            due_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        # First create an order
        order_request = {
            'order': {
                'location_id': location_id,
                'customer_id': customer_id,
                'line_items': [
                    {
                        'quantity': '1',
                        'base_price_money': {
                            'amount': amount_cents,
                            'currency': 'USD'
                        },
                        'name': description
                    }
                ]
            }
        }
        
        order_result = client.orders.create(**order_request)
        order = order_result.order
        
        # Now create invoice with the order
        scheduled_at = datetime.now(timezone.utc).isoformat()
        
        invoice_request = {
            'invoice': {
                'location_id': location_id,
                'order_id': order.id,
                'delivery_method': 'EMAIL',
                'payment_requests': [
                    {
                        'request_type': 'BALANCE',
                        'due_date': due_date
                    }
                ],
                'primary_recipient': {
                    'customer_id': customer_id
                },
                'title': 'Invoice',
                'description': description,
                'scheduled_at': scheduled_at,
                'accepted_payment_methods': {
                    'card': True,
                    'square_gift_card': False,
                    'bank_account': True,
                    'buy_now_pay_later': False
                }
            }
        }
        
        # Create the invoice
        result = client.invoices.create(**invoice_request)
        invoice = result.invoice
        
    except Exception as e:
        raise Exception(str(e))
    
    if json_output:
        if hasattr(invoice, 'model_dump'):
            print(json.dumps({'invoice': invoice.model_dump()}, indent=2))
        elif hasattr(invoice, 'dict'):
            print(json.dumps({'invoice': invoice.dict()}, indent=2))
        else:
            print(json.dumps({'invoice': vars(invoice)}, indent=2))
    else:
        print(f"Invoice created successfully!")
        print(f"ID: {invoice.id}")
        print(f"Number: {getattr(invoice, 'invoice_number', 'N/A')}")
        print(f"Status: {getattr(invoice, 'status', 'N/A')}")
        print(f"Total: {format_money(getattr(invoice, 'total_money', None))}")
        print(f"Due Date: {due_date}")
        print(f"Customer ID: {customer_id}")
        
        # Send the invoice
        try:
            send_result = client.invoices.publish(invoice_id=invoice.id, version=invoice.version)
            print(f"\nInvoice sent successfully to customer!")
        except:
            print(f"\nInvoice created but needs to be sent manually.")


@handle_api_errors
def send_invoice(client, invoice_id: str, json_output: bool = False):
    """Send a draft invoice to the customer."""
    try:
        from datetime import datetime, timedelta, timezone
        
        # First get the invoice to get its version
        get_result = client.invoices.get(invoice_id=invoice_id)
        invoice = get_result.invoice
        
        # Update scheduled_at to a future time (5 minutes from now)
        future_time = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
        
        update_request = {
            'invoice': {
                'version': invoice.version,
                'scheduled_at': future_time
            }
        }
        
        # Update the invoice first
        update_result = client.invoices.update(invoice_id=invoice_id, **update_request)
        updated_invoice = update_result.invoice
        
        # Now publish it
        result = client.invoices.publish(invoice_id=invoice_id, version=updated_invoice.version)
        invoice = result.invoice
    except Exception as e:
        raise Exception(str(e))
    
    if json_output:
        if hasattr(invoice, 'model_dump'):
            print(json.dumps({'invoice': invoice.model_dump()}, indent=2))
        elif hasattr(invoice, 'dict'):
            print(json.dumps({'invoice': invoice.dict()}, indent=2))
        else:
            print(json.dumps({'invoice': vars(invoice)}, indent=2))
    else:
        print(f"Invoice sent successfully!")
        print(f"ID: {invoice.id}")
        print(f"Number: {getattr(invoice, 'invoice_number', 'N/A')}")
        print(f"Status: {getattr(invoice, 'status', 'N/A')}")
        print(f"Total: {format_money(getattr(invoice, 'total_money', None))}")


@handle_api_errors
def update_invoice_note(client, invoice_id: str, note: str, json_output: bool = False):
    """Update an invoice with a note in the description."""
    try:
        # Get current invoice
        get_result = client.invoices.get(invoice_id=invoice_id)
        invoice = get_result.invoice
        
        # Append note to description
        current_desc = getattr(invoice, 'description', '')
        new_description = f"{current_desc}\n\n{note}"
        
        # Update the description
        update_request = {
            'invoice': {
                'version': invoice.version,
                'description': new_description
            }
        }
        
        result = client.invoices.update(invoice_id=invoice_id, **update_request)
        updated_invoice = result.invoice
        
    except Exception as e:
        raise Exception(str(e))
    
    if json_output:
        if hasattr(updated_invoice, 'model_dump'):
            print(json.dumps({'invoice': updated_invoice.model_dump()}, indent=2))
        elif hasattr(updated_invoice, 'dict'):
            print(json.dumps({'invoice': updated_invoice.dict()}, indent=2))
        else:
            print(json.dumps({'invoice': vars(updated_invoice)}, indent=2))
    else:
        print(f"Invoice updated successfully!")
        print(f"ID: {updated_invoice.id}")
        print(f"Note added to invoice")


def main():
    parser = argparse.ArgumentParser(description='Square CLI - Command-line interface for Square API')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Payments commands
    payments_parser = subparsers.add_parser('payments', help='Manage payments')
    payments_sub = payments_parser.add_subparsers(dest='subcommand')
    
    payments_list = payments_sub.add_parser('list', help='List recent payments')
    payments_list.add_argument('--limit', type=int, default=10, help='Number of results (default: 10)')
    payments_list.add_argument('--cursor', help='Pagination cursor')
    
    payments_get = payments_sub.add_parser('get', help='Get payment details')
    payments_get.add_argument('payment_id', help='Payment ID')
    
    # Customers commands
    customers_parser = subparsers.add_parser('customers', help='Manage customers')
    customers_sub = customers_parser.add_subparsers(dest='subcommand')
    
    customers_list = customers_sub.add_parser('list', help='List customers')
    customers_list.add_argument('--limit', type=int, default=10, help='Number of results (default: 10)')
    customers_list.add_argument('--cursor', help='Pagination cursor')
    
    customers_create = customers_sub.add_parser('create', help='Create new customer')
    customers_create.add_argument('email', help='Customer email address')
    customers_create.add_argument('--given-name', help='First name')
    customers_create.add_argument('--family-name', help='Last name')
    customers_create.add_argument('--phone', help='Phone number')
    
    # Catalog commands
    catalog_parser = subparsers.add_parser('catalog', help='Manage catalog')
    catalog_sub = catalog_parser.add_subparsers(dest='subcommand')
    
    catalog_list = catalog_sub.add_parser('list', help='List catalog items')
    catalog_list.add_argument('--limit', type=int, default=10, help='Number of results (default: 10)')
    catalog_list.add_argument('--cursor', help='Pagination cursor')
    
    # Locations commands
    locations_parser = subparsers.add_parser('locations', help='Manage locations')
    locations_sub = locations_parser.add_subparsers(dest='subcommand')
    
    locations_list = locations_sub.add_parser('list', help='List business locations')
    
    # Orders commands
    orders_parser = subparsers.add_parser('orders', help='Manage orders')
    orders_sub = orders_parser.add_subparsers(dest='subcommand')
    
    orders_list = orders_sub.add_parser('list', help='List orders')
    orders_list.add_argument('location_id', help='Location ID')
    orders_list.add_argument('--limit', type=int, default=10, help='Number of results (default: 10)')
    orders_list.add_argument('--cursor', help='Pagination cursor')
    
    # Invoices commands
    invoices_parser = subparsers.add_parser('invoices', help='Manage invoices')
    invoices_sub = invoices_parser.add_subparsers(dest='subcommand')
    
    invoices_list = invoices_sub.add_parser('list', help='List invoices from last month')
    invoices_list.add_argument('location_id', help='Location ID')
    invoices_list.add_argument('--limit', type=int, default=10, help='Number of results (default: 10)')
    invoices_list.add_argument('--cursor', help='Pagination cursor')
    
    invoices_create = invoices_sub.add_parser('create', help='Create a new invoice')
    invoices_create.add_argument('location_id', help='Location ID')
    invoices_create.add_argument('customer_id', help='Customer ID')
    invoices_create.add_argument('description', help='Description of work/services')
    invoices_create.add_argument('amount', type=float, help='Total amount in dollars')
    invoices_create.add_argument('--due-date', help='Due date (YYYY-MM-DD), defaults to 30 days from now')
    
    invoices_send = invoices_sub.add_parser('send', help='Send a draft invoice')
    invoices_send.add_argument('invoice_id', help='Invoice ID to send')
    
    invoices_note = invoices_sub.add_parser('add-note', help='Add a note to an invoice')
    invoices_note.add_argument('invoice_id', help='Invoice ID')
    invoices_note.add_argument('note', help='Note text to add')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    client = get_client()
    json_output = args.json
    
    try:
        if args.command == 'payments':
            if args.subcommand == 'list':
                list_payments(client, args.limit, args.cursor, json_output)
            elif args.subcommand == 'get':
                get_payment(client, args.payment_id, json_output)
            else:
                payments_parser.print_help()
                
        elif args.command == 'customers':
            if args.subcommand == 'list':
                list_customers(client, args.limit, args.cursor, json_output)
            elif args.subcommand == 'create':
                create_customer(client, args.email, args.given_name, 
                              args.family_name, args.phone, json_output)
            else:
                customers_parser.print_help()
                
        elif args.command == 'catalog':
            if args.subcommand == 'list':
                list_catalog_items(client, args.limit, args.cursor, json_output)
            else:
                catalog_parser.print_help()
                
        elif args.command == 'locations':
            if args.subcommand == 'list':
                list_locations(client, json_output)
            else:
                locations_parser.print_help()
                
        elif args.command == 'orders':
            if args.subcommand == 'list':
                list_orders(client, args.location_id, args.limit, args.cursor, json_output)
            else:
                orders_parser.print_help()
                
        elif args.command == 'invoices':
            if args.subcommand == 'list':
                list_invoices(client, args.location_id, args.limit, args.cursor, json_output)
            elif args.subcommand == 'create':
                create_invoice(client, args.location_id, args.customer_id, 
                             args.description, args.amount, args.due_date, json_output)
            elif args.subcommand == 'send':
                send_invoice(client, args.invoice_id, json_output)
            elif args.subcommand == 'add-note':
                update_invoice_note(client, args.invoice_id, args.note, json_output)
            else:
                invoices_parser.print_help()
        
    except KeyboardInterrupt:
        print("\nOperation cancelled.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()