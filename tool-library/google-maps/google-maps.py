#!/usr/bin/env python3
"""
Google Maps CLI Tool

A command-line interface for Google Maps API operations including geocoding,
directions, places search, and more.
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional, Tuple
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
import time


class GoogleMapsAPI:
    """Google Maps API client"""
    
    BASE_URL = "https://maps.googleapis.com/maps/api"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def _request(self, endpoint: str, params: Dict) -> Dict:
        """Make API request and return JSON response"""
        params['key'] = self.api_key
        query_string = urllib.parse.urlencode(params)
        url = f"{self.BASE_URL}/{endpoint}/json?{query_string}"
        
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = json.loads(response.read().decode())
                
            # Check for API errors
            if data.get('status') not in ['OK', 'ZERO_RESULTS']:
                error_msg = data.get('error_message', data.get('status', 'Unknown error'))
                raise Exception(f"API Error: {error_msg}")
                
            return data
            
        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP Error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            raise Exception(f"Connection Error: {e.reason}")
    
    def geocode(self, address: str) -> Dict:
        """Convert address to coordinates"""
        return self._request('geocode', {'address': address})
    
    def reverse_geocode(self, lat: float, lng: float) -> Dict:
        """Convert coordinates to address"""
        return self._request('geocode', {'latlng': f"{lat},{lng}"})
    
    def directions(self, origin: str, destination: str, mode: str = 'driving',
                  waypoints: Optional[List[str]] = None, alternatives: bool = False) -> Dict:
        """Get directions between locations"""
        params = {
            'origin': origin,
            'destination': destination,
            'mode': mode,
            'alternatives': str(alternatives).lower()
        }
        if waypoints:
            params['waypoints'] = '|'.join(waypoints)
        return self._request('directions', params)
    
    def distance_matrix(self, origins: List[str], destinations: List[str], 
                       mode: str = 'driving', units: str = 'metric') -> Dict:
        """Calculate distance and duration between multiple origins and destinations"""
        params = {
            'origins': '|'.join(origins),
            'destinations': '|'.join(destinations),
            'mode': mode,
            'units': units
        }
        return self._request('distancematrix', params)
    
    def place_search(self, query: str, location: Optional[Tuple[float, float]] = None,
                    radius: int = 50000, type_filter: Optional[str] = None) -> Dict:
        """Search for places"""
        params = {'query': query}
        if location:
            params['location'] = f"{location[0]},{location[1]}"
            params['radius'] = radius
        if type_filter:
            params['type'] = type_filter
        return self._request('place/textsearch', params)
    
    def place_details(self, place_id: str, fields: Optional[List[str]] = None) -> Dict:
        """Get detailed information about a place"""
        params = {'place_id': place_id}
        if fields:
            params['fields'] = ','.join(fields)
        return self._request('place/details', params)
    
    def timezone(self, lat: float, lng: float, timestamp: Optional[int] = None) -> Dict:
        """Get timezone for a location"""
        params = {
            'location': f"{lat},{lng}",
            'timestamp': timestamp or int(time.time())
        }
        return self._request('timezone', params)
    
    def elevation(self, locations: List[Tuple[float, float]]) -> Dict:
        """Get elevation for locations"""
        locations_str = '|'.join([f"{lat},{lng}" for lat, lng in locations])
        return self._request('elevation', {'locations': locations_str})


def load_api_key() -> str:
    """Load API key from environment or config file"""
    # Try environment variable first
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    if api_key:
        return api_key
    
    # Try config file
    config_path = Path.home() / '.google-maps' / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            api_key = config.get('api_key')
            if api_key:
                return api_key
    
    print("Error: No API key found. Please set GOOGLE_MAPS_API_KEY environment variable", file=sys.stderr)
    print("or run the setup script: ./setup.sh", file=sys.stderr)
    sys.exit(1)


def format_location(result: Dict) -> str:
    """Format a geocoding result"""
    addr = result.get('formatted_address', 'Unknown')
    geo = result.get('geometry', {}).get('location', {})
    lat = geo.get('lat', 'N/A')
    lng = geo.get('lng', 'N/A')
    return f"{addr}\nCoordinates: {lat}, {lng}"


def format_directions(data: Dict) -> str:
    """Format directions result"""
    output = []
    for i, route in enumerate(data.get('routes', [])):
        if i > 0:
            output.append("\n--- Alternative Route ---")
        
        # Summary
        leg = route['legs'][0]  # For simplicity, using first leg
        output.append(f"Distance: {leg['distance']['text']}")
        output.append(f"Duration: {leg['duration']['text']}")
        output.append(f"Start: {leg['start_address']}")
        output.append(f"End: {leg['end_address']}")
        
        # Steps
        output.append("\nDirections:")
        for j, step in enumerate(leg['steps'], 1):
            instruction = step['html_instructions'].replace('<b>', '').replace('</b>', '')
            instruction = instruction.replace('<div style="font-size:0.9em">', ' - ')
            instruction = instruction.replace('</div>', '')
            output.append(f"{j}. {instruction} ({step['distance']['text']})")
    
    return '\n'.join(output)


def format_place(place: Dict) -> str:
    """Format a place result"""
    output = []
    output.append(f"Name: {place.get('name', 'Unknown')}")
    
    if 'formatted_address' in place:
        output.append(f"Address: {place['formatted_address']}")
    
    if 'rating' in place:
        output.append(f"Rating: {place['rating']} ⭐ ({place.get('user_ratings_total', 0)} reviews)")
    
    if 'types' in place:
        types = [t.replace('_', ' ').title() for t in place['types'][:3]]
        output.append(f"Types: {', '.join(types)}")
    
    if 'opening_hours' in place:
        status = "Open" if place['opening_hours'].get('open_now') else "Closed"
        output.append(f"Status: {status}")
    
    if 'formatted_phone_number' in place:
        output.append(f"Phone: {place['formatted_phone_number']}")
    
    if 'website' in place:
        output.append(f"Website: {place['website']}")
    
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(description='Google Maps CLI')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Geocode command
    geocode_parser = subparsers.add_parser('geocode', help='Convert address to coordinates')
    geocode_parser.add_argument('address', help='Address to geocode')
    
    # Reverse geocode command
    reverse_parser = subparsers.add_parser('reverse-geocode', help='Convert coordinates to address')
    reverse_parser.add_argument('lat', type=float, help='Latitude')
    reverse_parser.add_argument('lng', type=float, help='Longitude')
    
    # Directions command
    directions_parser = subparsers.add_parser('directions', help='Get directions')
    directions_parser.add_argument('origin', help='Starting location')
    directions_parser.add_argument('destination', help='Destination')
    directions_parser.add_argument('--mode', choices=['driving', 'walking', 'bicycling', 'transit'],
                                 default='driving', help='Travel mode')
    directions_parser.add_argument('--waypoints', nargs='+', help='Waypoints')
    directions_parser.add_argument('--alternatives', action='store_true', help='Show alternative routes')
    
    # Distance command
    distance_parser = subparsers.add_parser('distance', help='Calculate distance between places')
    distance_parser.add_argument('origin', help='Origin location')
    distance_parser.add_argument('destination', help='Destination location')
    distance_parser.add_argument('--mode', choices=['driving', 'walking', 'bicycling', 'transit'],
                               default='driving', help='Travel mode')
    distance_parser.add_argument('--units', choices=['metric', 'imperial'], default='metric',
                               help='Unit system')
    
    # Place search command
    search_parser = subparsers.add_parser('place-search', help='Search for places')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--near', help='Location to search near (address or "lat,lng")')
    search_parser.add_argument('--radius', type=int, default=50000, help='Search radius in meters')
    search_parser.add_argument('--type', help='Place type filter (e.g., restaurant, cafe)')
    search_parser.add_argument('--limit', type=int, default=5, help='Maximum results')
    
    # Place details command
    details_parser = subparsers.add_parser('place-details', help='Get place details')
    details_parser.add_argument('place_id', help='Google Place ID')
    details_parser.add_argument('--fields', nargs='+', help='Specific fields to retrieve')
    
    # Timezone command
    tz_parser = subparsers.add_parser('timezone', help='Get timezone for location')
    tz_parser.add_argument('lat', type=float, help='Latitude')
    tz_parser.add_argument('lng', type=float, help='Longitude')
    
    # Elevation command
    elev_parser = subparsers.add_parser('elevation', help='Get elevation for location')
    elev_parser.add_argument('lat', type=float, help='Latitude')
    elev_parser.add_argument('lng', type=float, help='Longitude')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Load API key and create client
        api_key = load_api_key()
        client = GoogleMapsAPI(api_key)
        
        # Execute command
        if args.command == 'geocode':
            data = client.geocode(args.address)
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                results = data.get('results', [])
                if results:
                    print(format_location(results[0]))
                else:
                    print("No results found")
        
        elif args.command == 'reverse-geocode':
            data = client.reverse_geocode(args.lat, args.lng)
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                results = data.get('results', [])
                if results:
                    print(format_location(results[0]))
                else:
                    print("No results found")
        
        elif args.command == 'directions':
            data = client.directions(args.origin, args.destination, args.mode,
                                   args.waypoints, args.alternatives)
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                print(format_directions(data))
        
        elif args.command == 'distance':
            data = client.distance_matrix([args.origin], [args.destination],
                                        args.mode, args.units)
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                element = data['rows'][0]['elements'][0]
                if element['status'] == 'OK':
                    print(f"Distance: {element['distance']['text']}")
                    print(f"Duration: {element['duration']['text']}")
                else:
                    print(f"Error: {element['status']}")
        
        elif args.command == 'place-search':
            # Parse location if provided
            location = None
            if args.near:
                if ',' in args.near:
                    parts = args.near.split(',')
                    location = (float(parts[0]), float(parts[1]))
                else:
                    # Geocode the location
                    geo_data = client.geocode(args.near)
                    if geo_data['results']:
                        loc = geo_data['results'][0]['geometry']['location']
                        location = (loc['lat'], loc['lng'])
            
            data = client.place_search(args.query, location, args.radius, args.type)
            
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                results = data.get('results', [])[:args.limit]
                for i, place in enumerate(results, 1):
                    if i > 1:
                        print("\n" + "-" * 40 + "\n")
                    print(f"{i}. {place['name']}")
                    print(f"   Address: {place.get('formatted_address', 'N/A')}")
                    if 'rating' in place:
                        print(f"   Rating: {place['rating']} ⭐")
                    print(f"   Place ID: {place['place_id']}")
        
        elif args.command == 'place-details':
            data = client.place_details(args.place_id, args.fields)
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                place = data.get('result', {})
                print(format_place(place))
        
        elif args.command == 'timezone':
            data = client.timezone(args.lat, args.lng)
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                print(f"Timezone ID: {data['timeZoneId']}")
                print(f"Timezone Name: {data['timeZoneName']}")
                print(f"UTC Offset: {data['rawOffset'] / 3600} hours")
                if data.get('dstOffset', 0) != 0:
                    print(f"DST Offset: {data['dstOffset'] / 3600} hours")
        
        elif args.command == 'elevation':
            data = client.elevation([(args.lat, args.lng)])
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                result = data['results'][0]
                print(f"Elevation: {result['elevation']:.1f} meters")
                print(f"Resolution: {result['resolution']:.1f} meters")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()