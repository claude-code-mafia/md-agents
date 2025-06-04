#!/usr/bin/env python3
"""Google Maps CLI Tool - Working Version using subprocess"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def load_api_key():
    """Load API key from environment or config file"""
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    if api_key:
        return api_key
    
    config_path = Path.home() / '.google-maps' / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            api_key = config.get('api_key')
            if api_key:
                return api_key
    
    print("Error: No API key found", file=sys.stderr)
    sys.exit(1)


def make_request(endpoint, params):
    """Make API request using curl"""
    api_key = load_api_key()
    params['key'] = api_key
    
    # Build query string with proper encoding
    import urllib.parse
    query_string = urllib.parse.urlencode(params)
    url = f"https://maps.googleapis.com/maps/api/{endpoint}/json?{query_string}"
    
    # Use curl to make the request
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Request failed: {result.stderr}")
    
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description='Google Maps CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Place search command
    search_parser = subparsers.add_parser('place-search', help='Search for places')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--near', help='Location to search near')
    search_parser.add_argument('--limit', type=int, default=5, help='Max results')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'place-search':
            # If location is specified, geocode it first
            if args.near:
                geo_data = make_request('geocode', {'address': args.near})
                if geo_data['status'] == 'OK':
                    loc = geo_data['results'][0]['geometry']['location']
                    location = f"{loc['lat']},{loc['lng']}"
                    print(f"Searching near: {geo_data['results'][0]['formatted_address']}\n")
                else:
                    raise Exception(f"Could not geocode location: {args.near}")
            else:
                location = None
            
            # Search for places
            params = {'query': args.query}
            if location:
                params['location'] = location
                params['radius'] = '5000'
            
            data = make_request('place/textsearch', params)
            
            if data['status'] == 'OK':
                results = data['results'][:args.limit]
                for i, place in enumerate(results, 1):
                    print(f"{i}. {place['name']}")
                    print(f"   Address: {place.get('formatted_address', 'N/A')}")
                    if 'rating' in place:
                        print(f"   Rating: {place['rating']} ⭐")
                    if 'price_level' in place:
                        print(f"   Price: {'$' * place['price_level']}")
                    print()
            else:
                print(f"No results found: {data.get('status')}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()