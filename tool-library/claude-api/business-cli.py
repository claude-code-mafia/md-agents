#!/usr/bin/env python3
"""
Business API CLI - A tool Claude can use to interact with the business system
"""
import argparse
import requests
import json
import sys

API_BASE = "http://localhost:8000"

def main():
    parser = argparse.ArgumentParser(description='Business API CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Get business info
    get_parser = subparsers.add_parser('get', help='Get business info')
    get_parser.add_argument('business_id', help='Business ID')
    
    # Update business
    update_parser = subparsers.add_parser('update', help='Update business')
    update_parser.add_argument('business_id', help='Business ID')
    update_parser.add_argument('--name', help='New name')
    update_parser.add_argument('--phone', help='New phone')
    update_parser.add_argument('--address', help='New address')
    
    # Create business
    create_parser = subparsers.add_parser('create', help='Create business')
    create_parser.add_argument('name', help='Business name')
    create_parser.add_argument('--phone', help='Phone number')
    create_parser.add_argument('--address', help='Address')
    
    # Search businesses
    search_parser = subparsers.add_parser('search', help='Search businesses')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    if args.command == 'get':
        response = requests.post(f"{API_BASE}/callback", json={
            "action": "fetch_business_info",
            "data": {"business_id": args.business_id}
        })
        data = response.json()
        if data.get("status") == "success":
            business = data["data"]
            print(f"Business: {business['name']}")
            print(f"Address: {business['address']}")
            print(f"Phone: {business['phone']}")
            print(f"Hours: {business['hours']}")
            print(f"Rating: {business['rating']}")
        else:
            print(f"Error: {data.get('message')}")
            
    elif args.command == 'update':
        update_data = {"business_id": args.business_id}
        if args.name:
            update_data["name"] = args.name
        if args.phone:
            update_data["phone"] = args.phone
        if args.address:
            update_data["address"] = args.address
            
        response = requests.post(f"{API_BASE}/callback", json={
            "action": "update_business",
            "data": update_data
        })
        print(response.json().get("message"))
        
    elif args.command == 'create':
        create_data = {"name": args.name}
        if args.phone:
            create_data["phone"] = args.phone
        if args.address:
            create_data["address"] = args.address
            
        response = requests.post(f"{API_BASE}/callback", json={
            "action": "create_business",
            "data": create_data
        })
        result = response.json()
        if result.get("status") == "success":
            print(f"Created business with ID: {result.get('business_id')}")
        else:
            print(f"Error: {result.get('message')}")
            
    elif args.command == 'search':
        response = requests.post(f"{API_BASE}/callback", json={
            "action": "search_businesses",
            "data": {"query": args.query}
        })
        result = response.json()
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get("status") == "success":
                businesses = result.get("data", [])
                for b in businesses:
                    print(f"ID: {b['id']} - {b['name']} ({b['address']})")
            else:
                print(f"Error: {result.get('message')}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()