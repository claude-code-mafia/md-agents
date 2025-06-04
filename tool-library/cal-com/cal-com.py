#!/usr/bin/env python3
"""
Cal.com CLI Tool - Manage bookings, events, and availability from the command line.
"""

import argparse
import json
import sys
import os
from datetime import datetime, timedelta
import requests
from pathlib import Path
from urllib.parse import urlencode

class CalComAPI:
    """Cal.com API client for v1 API."""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or self._load_api_key()
        self.base_url = "https://api.cal.com/v1"
        
    def _load_api_key(self):
        """Load API key from config file."""
        config_path = Path.home() / ".cal-com" / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                return config.get("api_key")
        return None
    
    def _request(self, method, endpoint, params=None, data=None):
        """Make API request with authentication."""
        if not self.api_key:
            raise ValueError("No API key configured. Run 'cal-com auth' first.")
        
        # Add API key to params
        if params is None:
            params = {}
        params["apiKey"] = self.api_key
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers={"Content-Type": "application/json"} if data else None,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                raise Exception(f"API error: {e.response.text}")
            raise Exception(f"Request failed: {str(e)}")
    
    def get(self, endpoint, params=None):
        """Make GET request."""
        return self._request("GET", endpoint, params=params)
    
    def post(self, endpoint, data=None):
        """Make POST request."""
        return self._request("POST", endpoint, data=data)
    
    def patch(self, endpoint, data=None):
        """Make PATCH request."""
        return self._request("PATCH", endpoint, data=data)
    
    def delete(self, endpoint):
        """Make DELETE request."""
        return self._request("DELETE", endpoint)


class CalComCLI:
    """Main CLI application."""
    
    def __init__(self):
        self.api = CalComAPI()
    
    def auth(self, args):
        """Configure API authentication."""
        if args.key:
            api_key = args.key
        else:
            api_key = input("Enter your Cal.com API key: ").strip()
        
        # Test the API key
        test_api = CalComAPI(api_key=api_key)
        try:
            test_api.get("me")
            
            # Save to config
            config_dir = Path.home() / ".cal-com"
            config_dir.mkdir(exist_ok=True)
            config_path = config_dir / "config.json"
            
            with open(config_path, "w") as f:
                json.dump({"api_key": api_key}, f)
            
            print("✓ Authentication successful")
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
            sys.exit(1)
    
    def bookings_list(self, args):
        """List bookings."""
        params = {}
        if args.status:
            params["status"] = args.status
        if args.limit:
            params["take"] = args.limit
        
        result = self.api.get("bookings", params=params)
        bookings = result.get("bookings", [])
        
        if args.json:
            print(json.dumps(bookings, indent=2))
        else:
            if not bookings:
                print("No bookings found")
                return
            
            for booking in bookings:
                print(f"\nBooking ID: {booking.get('id')}")
                print(f"Title: {booking.get('title', 'N/A')}")
                print(f"Start: {booking.get('startTime', 'N/A')}")
                print(f"End: {booking.get('endTime', 'N/A')}")
                print(f"Status: {booking.get('status', 'N/A')}")
                if booking.get('attendees'):
                    attendees = [a.get('email', 'N/A') for a in booking['attendees']]
                    print(f"Attendees: {', '.join(attendees)}")
                print("-" * 40)
    
    def bookings_get(self, args):
        """Get booking details."""
        result = self.api.get(f"bookings/{args.id}")
        booking = result.get("booking", {})
        
        if args.json:
            print(json.dumps(booking, indent=2))
        else:
            print(f"Booking ID: {booking.get('id')}")
            print(f"Title: {booking.get('title', 'N/A')}")
            print(f"Description: {booking.get('description', 'N/A')}")
            print(f"Start: {booking.get('startTime', 'N/A')}")
            print(f"End: {booking.get('endTime', 'N/A')}")
            print(f"Status: {booking.get('status', 'N/A')}")
            print(f"Location: {booking.get('location', 'N/A')}")
            
            if booking.get('attendees'):
                print("\nAttendees:")
                for attendee in booking['attendees']:
                    print(f"  - {attendee.get('name', 'N/A')} ({attendee.get('email', 'N/A')})")
    
    def bookings_cancel(self, args):
        """Cancel a booking."""
        data = {"id": args.id}
        if args.reason:
            data["cancellationReason"] = args.reason
        
        result = self.api.delete(f"bookings/{args.id}")
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"✓ Booking {args.id} cancelled successfully")
    
    def events_list(self, args):
        """List event types."""
        result = self.api.get("event-types")
        event_types = result.get("event_types", [])
        
        if args.json:
            print(json.dumps(event_types, indent=2))
        else:
            if not event_types:
                print("No event types found")
                return
            
            for event in event_types:
                print(f"\nEvent Type ID: {event.get('id')}")
                print(f"Title: {event.get('title', 'N/A')}")
                print(f"Slug: {event.get('slug', 'N/A')}")
                print(f"Length: {event.get('length', 'N/A')} minutes")
                print(f"Description: {event.get('description', 'N/A')}")
                print(f"Hidden: {event.get('hidden', False)}")
                print("-" * 40)
    
    def events_create(self, args):
        """Create an event type."""
        data = {
            "title": args.title,
            "slug": args.slug,
            "length": args.length
        }
        
        if args.description:
            data["description"] = args.description
        
        result = self.api.post("event-types", data=data)
        event = result.get("event_type", {})
        
        if args.json:
            print(json.dumps(event, indent=2))
        else:
            print(f"✓ Event type created successfully")
            print(f"ID: {event.get('id')}")
            print(f"Title: {event.get('title')}")
            print(f"Slug: {event.get('slug')}")
            print(f"URL: https://cal.com/{event.get('slug')}")
    
    def events_update(self, args):
        """Update an event type."""
        data = {}
        if args.title:
            data["title"] = args.title
        if args.description:
            data["description"] = args.description
        if args.length:
            data["length"] = args.length
        if args.hidden is not None:
            data["hidden"] = args.hidden
        
        result = self.api.patch(f"event-types/{args.id}", data=data)
        event = result.get("event_type", {})
        
        if args.json:
            print(json.dumps(event, indent=2))
        else:
            print(f"✓ Event type updated successfully")
    
    def events_delete(self, args):
        """Delete an event type."""
        result = self.api.delete(f"event-types/{args.id}")
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"✓ Event type {args.id} deleted successfully")
    
    def availability_list(self, args):
        """List availabilities."""
        result = self.api.get("availability")
        availabilities = result.get("availabilities", [])
        
        if args.json:
            print(json.dumps(availabilities, indent=2))
        else:
            if not availabilities:
                print("No availabilities found")
                return
            
            for avail in availabilities:
                print(f"\nAvailability ID: {avail.get('id')}")
                print(f"User ID: {avail.get('userId', 'N/A')}")
                print(f"Event Type ID: {avail.get('eventTypeId', 'N/A')}")
                print(f"Days: {avail.get('days', [])}")
                print(f"Start Time: {avail.get('startTime', 'N/A')}")
                print(f"End Time: {avail.get('endTime', 'N/A')}")
                print("-" * 40)
    
    def schedules_list(self, args):
        """List schedules."""
        result = self.api.get("schedules")
        schedules = result.get("schedules", [])
        
        if args.json:
            print(json.dumps(schedules, indent=2))
        else:
            if not schedules:
                print("No schedules found")
                return
            
            for schedule in schedules:
                print(f"\nSchedule ID: {schedule.get('id')}")
                print(f"Name: {schedule.get('name', 'N/A')}")
                print(f"Time Zone: {schedule.get('timeZone', 'N/A')}")
                print(f"Is Default: {schedule.get('isDefault', False)}")
                print("-" * 40)
    
    def users_me(self, args):
        """Get current user information."""
        result = self.api.get("me")
        user = result.get("user", {})
        
        if args.json:
            print(json.dumps(user, indent=2))
        else:
            print(f"User ID: {user.get('id')}")
            print(f"Username: {user.get('username', 'N/A')}")
            print(f"Email: {user.get('email', 'N/A')}")
            print(f"Name: {user.get('name', 'N/A')}")
            print(f"Time Zone: {user.get('timeZone', 'N/A')}")
            print(f"Created: {user.get('createdDate', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description="Cal.com CLI - Manage bookings, events, and availability"
    )
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Auth command
    auth_parser = subparsers.add_parser('auth', help='Configure API authentication')
    auth_parser.add_argument('--key', help='API key (will prompt if not provided)')
    
    # Bookings commands
    bookings_parser = subparsers.add_parser('bookings', help='Manage bookings')
    bookings_subparsers = bookings_parser.add_subparsers(dest='subcommand')
    
    bookings_list_parser = bookings_subparsers.add_parser('list', help='List bookings')
    bookings_list_parser.add_argument('--status', choices=['upcoming', 'past', 'cancelled'], help='Filter by status')
    bookings_list_parser.add_argument('--limit', type=int, help='Limit number of results')
    
    bookings_get_parser = bookings_subparsers.add_parser('get', help='Get booking details')
    bookings_get_parser.add_argument('id', help='Booking ID')
    
    bookings_cancel_parser = bookings_subparsers.add_parser('cancel', help='Cancel a booking')
    bookings_cancel_parser.add_argument('id', help='Booking ID')
    bookings_cancel_parser.add_argument('--reason', help='Cancellation reason')
    
    # Events commands
    events_parser = subparsers.add_parser('events', help='Manage event types')
    events_subparsers = events_parser.add_subparsers(dest='subcommand')
    
    events_list_parser = events_subparsers.add_parser('list', help='List event types')
    
    events_create_parser = events_subparsers.add_parser('create', help='Create event type')
    events_create_parser.add_argument('title', help='Event title')
    events_create_parser.add_argument('slug', help='URL slug')
    events_create_parser.add_argument('length', type=int, help='Duration in minutes')
    events_create_parser.add_argument('--description', help='Event description')
    
    events_update_parser = events_subparsers.add_parser('update', help='Update event type')
    events_update_parser.add_argument('id', help='Event type ID')
    events_update_parser.add_argument('--title', help='New title')
    events_update_parser.add_argument('--description', help='New description')
    events_update_parser.add_argument('--length', type=int, help='New duration in minutes')
    events_update_parser.add_argument('--hidden', type=bool, help='Hide/show event')
    
    events_delete_parser = events_subparsers.add_parser('delete', help='Delete event type')
    events_delete_parser.add_argument('id', help='Event type ID')
    
    # Availability commands
    availability_parser = subparsers.add_parser('availability', help='Manage availability')
    availability_subparsers = availability_parser.add_subparsers(dest='subcommand')
    
    availability_list_parser = availability_subparsers.add_parser('list', help='List availabilities')
    
    # Schedules commands
    schedules_parser = subparsers.add_parser('schedules', help='Manage schedules')
    schedules_subparsers = schedules_parser.add_subparsers(dest='subcommand')
    
    schedules_list_parser = schedules_subparsers.add_parser('list', help='List schedules')
    
    # Users commands
    users_parser = subparsers.add_parser('users', help='User information')
    users_subparsers = users_parser.add_subparsers(dest='subcommand')
    
    users_me_parser = users_subparsers.add_parser('me', help='Get current user info')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    cli = CalComCLI()
    
    try:
        # Route commands
        if args.command == 'auth':
            cli.auth(args)
        elif args.command == 'bookings':
            if args.subcommand == 'list':
                cli.bookings_list(args)
            elif args.subcommand == 'get':
                cli.bookings_get(args)
            elif args.subcommand == 'cancel':
                cli.bookings_cancel(args)
            else:
                bookings_parser.print_help()
        elif args.command == 'events':
            if args.subcommand == 'list':
                cli.events_list(args)
            elif args.subcommand == 'create':
                cli.events_create(args)
            elif args.subcommand == 'update':
                cli.events_update(args)
            elif args.subcommand == 'delete':
                cli.events_delete(args)
            else:
                events_parser.print_help()
        elif args.command == 'availability':
            if args.subcommand == 'list':
                cli.availability_list(args)
            else:
                availability_parser.print_help()
        elif args.command == 'schedules':
            if args.subcommand == 'list':
                cli.schedules_list(args)
            else:
                schedules_parser.print_help()
        elif args.command == 'users':
            if args.subcommand == 'me':
                cli.users_me(args)
            else:
                users_parser.print_help()
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()