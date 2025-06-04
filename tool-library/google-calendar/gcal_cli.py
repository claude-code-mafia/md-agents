#!/Users/pete/Projects/tool-library/google-calendar/venv/bin/python
"""
Google Calendar CLI - Unified command-line interface for Google Calendar
"""

import os
import sys
import json
import pickle
import argparse
import csv
from datetime import datetime, timedelta, timezone, UTC
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from collections import defaultdict
import re
from dateutil import parser as date_parser
import requests

from google.auth.transport.requests import Request, AuthorizedSession
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Calendar API scopes
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

# Configuration
CONFIG_DIR = Path.home() / '.gcal-cli'
TOKEN_FILE = CONFIG_DIR / 'token.pickle'
CREDENTIALS_FILE = CONFIG_DIR / 'credentials.json'

# Base URL for Calendar API
BASE_URL = 'https://www.googleapis.com/calendar/v3'

# Color mappings
COLORS = {
    '1': 'Lavender', '2': 'Sage', '3': 'Grape', '4': 'Flamingo',
    '5': 'Banana', '6': 'Tangerine', '7': 'Peacock', '8': 'Graphite',
    '9': 'Blueberry', '10': 'Basil', '11': 'Tomato'
}


class GoogleCalendarCLI:
    """Unified Google Calendar CLI with all features"""
    
    def __init__(self):
        self.session = None
        self.timezone = 'UTC'
        
    def authenticate(self):
        """Authenticate and create authorized session"""
        creds = None
        
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not CREDENTIALS_FILE.exists():
                    print(f"Error: credentials.json not found at {CREDENTIALS_FILE}")
                    print("\nTo set up Google Calendar CLI:")
                    print("1. Go to https://console.cloud.google.com/")
                    print("2. Enable Google Calendar API")
                    print("3. Create OAuth 2.0 credentials")
                    print(f"4. Download credentials.json to {CREDENTIALS_FILE}")
                    sys.exit(1)
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES)
                creds = flow.run_local_server(port=0)
            
            CONFIG_DIR.mkdir(exist_ok=True)
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        
        self.session = AuthorizedSession(creds)
        self.session.headers.update({'Accept': 'application/json'})
        
        # Get timezone
        try:
            response = self.session.get(f'{BASE_URL}/calendars/primary', timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.timezone = data.get('timeZone', 'UTC')
        except:
            self.timezone = 'UTC'
    
    # Core Calendar Operations
    
    def list_events(self, calendar_id='primary', time_min=None, time_max=None,
                   max_results=10, search_query=None, single_events=True):
        """List events from a calendar"""
        if not time_min:
            time_min = datetime.now(UTC).isoformat().replace('+00:00', 'Z')
        else:
            time_min = self._format_datetime(time_min)
            
        params = {
            'timeMin': time_min,
            'maxResults': max_results,
            'singleEvents': single_events,
            'orderBy': 'startTime' if single_events else 'updated'
        }
        
        if time_max:
            params['timeMax'] = self._format_datetime(time_max)
        if search_query:
            params['q'] = search_query
        
        response = self.session.get(
            f'{BASE_URL}/calendars/{calendar_id}/events',
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json().get('items', [])
        return []
    
    def create_event(self, summary, start, end=None, **kwargs):
        """Create an event with all options"""
        event = {'summary': summary}
        
        # Handle dates
        if kwargs.get('all_day'):
            start_date = date_parser.parse(start).date()
            event['start'] = {'date': start_date.isoformat()}
            end_date = date_parser.parse(end).date() if end else start_date + timedelta(days=1)
            event['end'] = {'date': end_date.isoformat()}
        else:
            start_dt = self._parse_local_time(start)
            event['start'] = {
                'dateTime': start_dt.isoformat(),
                'timeZone': self.timezone
            }
            end_dt = self._parse_local_time(end) if end else start_dt + timedelta(hours=1)
            event['end'] = {
                'dateTime': end_dt.isoformat(),
                'timeZone': self.timezone
            }
        
        # Optional fields
        for field in ['description', 'location', 'colorId']:
            if field in kwargs and kwargs[field]:
                event[field] = kwargs[field]
        
        if kwargs.get('attendees'):
            event['attendees'] = [{'email': email} for email in kwargs['attendees']]
        
        if kwargs.get('reminders'):
            event['reminders'] = {
                'useDefault': False,
                'overrides': kwargs['reminders']
            }
        
        if kwargs.get('recurrence'):
            event['recurrence'] = kwargs['recurrence']
        
        response = self.session.post(
            f"{BASE_URL}/calendars/{kwargs.get('calendar_id', 'primary')}/events",
            json=event,
            params={'sendUpdates': 'all' if kwargs.get('attendees') else 'none'},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def quick_add(self, text, calendar_id='primary'):
        """Quick add using natural language"""
        response = self.session.post(
            f'{BASE_URL}/calendars/{calendar_id}/events/quickAdd',
            params={'text': text},
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    
    def update_event(self, event_id, calendar_id='primary', **updates):
        """Update an event"""
        event = self.get_event(event_id, calendar_id)
        if not event:
            return None
        
        # Update fields
        for field in ['summary', 'description', 'location', 'colorId']:
            if field in updates and updates[field] is not None:
                event[field] = updates[field]
        
        # Update times
        if 'start' in updates:
            start_dt = self._parse_local_time(updates['start'])
            if 'date' in event['start']:
                event['start'] = {'date': start_dt.date().isoformat()}
            else:
                event['start'] = {
                    'dateTime': start_dt.isoformat(),
                    'timeZone': self.timezone
                }
        
        if 'end' in updates:
            end_dt = self._parse_local_time(updates['end'])
            if 'date' in event.get('end', {}):
                event['end'] = {'date': end_dt.date().isoformat()}
            else:
                event['end'] = {
                    'dateTime': end_dt.isoformat(),
                    'timeZone': self.timezone
                }
        
        if 'attendees' in updates:
            event['attendees'] = [{'email': email} for email in updates['attendees']]
        
        response = self.session.put(
            f'{BASE_URL}/calendars/{calendar_id}/events/{event_id}',
            json=event,
            params={'sendUpdates': 'all' if updates.get('attendees') else 'none'},
            timeout=30
        )
        
        return response.json() if response.status_code == 200 else None
    
    def delete_event(self, event_id, calendar_id='primary', notify=True):
        """Delete an event"""
        response = self.session.delete(
            f'{BASE_URL}/calendars/{calendar_id}/events/{event_id}',
            params={'sendUpdates': 'all' if notify else 'none'},
            timeout=30
        )
        return response.status_code == 204
    
    def get_event(self, event_id, calendar_id='primary'):
        """Get a specific event"""
        response = self.session.get(
            f'{BASE_URL}/calendars/{calendar_id}/events/{event_id}',
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    
    def list_calendars(self):
        """List all calendars"""
        response = self.session.get(f'{BASE_URL}/users/me/calendarList', timeout=30)
        return response.json().get('items', []) if response.status_code == 200 else []
    
    def get_free_busy(self, time_min, time_max, calendars=None):
        """Get free/busy information"""
        if not calendars:
            calendars = ['primary']
        
        body = {
            'timeMin': self._format_datetime(time_min),
            'timeMax': self._format_datetime(time_max),
            'items': [{'id': cal} for cal in calendars]
        }
        
        response = self.session.post(f'{BASE_URL}/freeBusy', json=body, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return {cal_id: cal_data.get('busy', []) 
                   for cal_id, cal_data in data.get('calendars', {}).items()}
        return {}
    
    # New Feature: Move/Copy Events
    
    def move_event(self, event_id, source_calendar='primary', destination_calendar=None):
        """Move an event to another calendar"""
        if not destination_calendar:
            return None
            
        response = self.session.post(
            f'{BASE_URL}/calendars/{source_calendar}/events/{event_id}/move',
            params={'destination': destination_calendar},
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    
    def copy_event(self, event_id, source_calendar='primary', destination_calendar=None):
        """Copy an event to another calendar"""
        if not destination_calendar:
            destination_calendar = source_calendar
            
        # Get the original event
        event = self.get_event(event_id, source_calendar)
        if not event:
            return None
            
        # Remove ID to create a copy
        event.pop('id', None)
        event.pop('etag', None)
        event.pop('iCalUID', None)
        
        response = self.session.post(
            f'{BASE_URL}/calendars/{destination_calendar}/events',
            json=event,
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    
    # New Feature: Calendar Metadata
    
    def get_calendar(self, calendar_id='primary'):
        """Get calendar details"""
        response = self.session.get(f'{BASE_URL}/calendars/{calendar_id}', timeout=30)
        return response.json() if response.status_code == 200 else None
    
    def create_calendar(self, summary, **kwargs):
        """Create a new calendar"""
        calendar = {'summary': summary}
        
        # Optional fields
        for field in ['description', 'location', 'timeZone']:
            if field in kwargs and kwargs[field]:
                calendar[field] = kwargs[field]
                
        response = self.session.post(f'{BASE_URL}/calendars', json=calendar, timeout=30)
        return response.json() if response.status_code == 200 else None
    
    def update_calendar(self, calendar_id, **updates):
        """Update calendar properties"""
        calendar = self.get_calendar(calendar_id)
        if not calendar:
            return None
            
        for field in ['summary', 'description', 'location', 'timeZone']:
            if field in updates and updates[field] is not None:
                calendar[field] = updates[field]
                
        response = self.session.put(
            f'{BASE_URL}/calendars/{calendar_id}',
            json=calendar,
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    
    def delete_calendar(self, calendar_id):
        """Delete a calendar"""
        response = self.session.delete(f'{BASE_URL}/calendars/{calendar_id}', timeout=30)
        return response.status_code == 204
    
    # New Feature: Event Response Status
    
    def respond_to_event(self, event_id, response_status, calendar_id='primary'):
        """Respond to an event invitation (accept/decline/tentative)"""
        event = self.get_event(event_id, calendar_id)
        if not event:
            return None
            
        # Find current user in attendees
        user_email = None
        for attendee in event.get('attendees', []):
            if attendee.get('self'):
                attendee['responseStatus'] = response_status
                user_email = attendee['email']
                break
                
        if not user_email:
            return None
            
        response = self.session.put(
            f'{BASE_URL}/calendars/{calendar_id}/events/{event_id}',
            json=event,
            params={'sendUpdates': 'all'},
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    
    def list_event_attendees(self, event_id, calendar_id='primary'):
        """List attendees and their response status"""
        event = self.get_event(event_id, calendar_id)
        if not event:
            return []
            
        attendees = []
        for attendee in event.get('attendees', []):
            attendees.append({
                'email': attendee.get('email'),
                'displayName': attendee.get('displayName', ''),
                'responseStatus': attendee.get('responseStatus', 'needsAction'),
                'optional': attendee.get('optional', False),
                'organizer': attendee.get('organizer', False),
                'self': attendee.get('self', False)
            })
        return attendees
    
    # New Feature: Conference Data
    
    def create_event_with_meet(self, summary, start, end=None, **kwargs):
        """Create event with Google Meet"""
        event = {'summary': summary}
        
        # Handle dates
        start_dt = self._parse_local_time(start)
        event['start'] = {
            'dateTime': start_dt.isoformat(),
            'timeZone': self.timezone
        }
        end_dt = self._parse_local_time(end) if end else start_dt + timedelta(hours=1)
        event['end'] = {
            'dateTime': end_dt.isoformat(),
            'timeZone': self.timezone
        }
        
        # Optional fields
        for field in ['description', 'location']:
            if field in kwargs and kwargs[field]:
                event[field] = kwargs[field]
        
        if kwargs.get('attendees'):
            event['attendees'] = [{'email': email} for email in kwargs['attendees']]
        
        # Add conference data
        event['conferenceData'] = {
            'createRequest': {
                'requestId': f"{summary}-{datetime.now().timestamp()}",
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
        
        response = self.session.post(
            f"{BASE_URL}/calendars/{kwargs.get('calendar_id', 'primary')}/events",
            json=event,
            params={
                'conferenceDataVersion': 1,
                'sendUpdates': 'all' if kwargs.get('attendees') else 'none'
            },
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    
    # New Feature: Attachments
    
    def add_attachment(self, event_id, file_url, title, calendar_id='primary', 
                      mime_type='application/octet-stream', icon_link=None):
        """Add attachment to an event"""
        event = self.get_event(event_id, calendar_id)
        if not event:
            return None
            
        attachment = {
            'fileUrl': file_url,
            'title': title,
            'mimeType': mime_type
        }
        
        if icon_link:
            attachment['iconLink'] = icon_link
            
        if 'attachments' not in event:
            event['attachments'] = []
        event['attachments'].append(attachment)
        
        response = self.session.put(
            f'{BASE_URL}/calendars/{calendar_id}/events/{event_id}',
            json=event,
            params={'supportsAttachments': 'true'},
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    
    def list_attachments(self, event_id, calendar_id='primary'):
        """List event attachments"""
        event = self.get_event(event_id, calendar_id)
        if not event:
            return []
        return event.get('attachments', [])
    
    # New Feature: Out of Office / Focus Time
    
    def create_out_of_office(self, start_date, end_date, message=None):
        """Create out of office event"""
        event = {
            'summary': 'Out of Office',
            'start': {'date': start_date},
            'end': {'date': end_date},
            'eventType': 'outOfOffice',
            'transparency': 'opaque'
        }
        
        if message:
            event['description'] = message
            
        response = self.session.post(
            f'{BASE_URL}/calendars/primary/events',
            json=event,
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    
    def create_focus_time(self, summary, start, end, recurrence=None):
        """Create focus time event"""
        event = {
            'summary': summary,
            'start': {'dateTime': self._parse_local_time(start).isoformat()},
            'end': {'dateTime': self._parse_local_time(end).isoformat()},
            'eventType': 'focusTime',
            'transparency': 'opaque',
            'reminders': {'useDefault': False}
        }
        
        if recurrence:
            event['recurrence'] = recurrence
            
        response = self.session.post(
            f'{BASE_URL}/calendars/primary/events',
            json=event,
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    
    # Advanced Features
    
    def analyze_calendar(self, calendar_id='primary', days=30):
        """Analyze calendar patterns and statistics"""
        time_min = datetime.now(UTC)
        time_max = time_min + timedelta(days=days)
        
        events = self.list_events(
            calendar_id=calendar_id,
            time_min=time_min.isoformat(),
            time_max=time_max.isoformat(),
            max_results=2500,
            single_events=True
        )
        
        stats = {
            'total_events': len(events),
            'days_analyzed': days,
            'events_by_day': defaultdict(int),
            'events_by_hour': defaultdict(int),
            'total_hours': 0,
            'meetings_with_others': 0,
            'locations': defaultdict(int),
            'top_attendees': []
        }
        
        total_duration = timedelta()
        attendee_counts = defaultdict(int)
        
        for event in events:
            if 'dateTime' not in event.get('start', {}):
                continue
                
            start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
            duration = end - start
            
            stats['events_by_day'][start.strftime('%A')] += 1
            stats['events_by_hour'][start.hour] += 1
            total_duration += duration
            
            if event.get('attendees'):
                stats['meetings_with_others'] += 1
                for attendee in event['attendees']:
                    if attendee.get('email') and not attendee.get('self'):
                        attendee_counts[attendee['email']] += 1
            
            if event.get('location'):
                stats['locations'][event['location']] += 1
        
        stats['total_hours'] = total_duration.total_seconds() / 3600
        stats['average_duration'] = stats['total_hours'] / len(events) if events else 0
        
        if attendee_counts:
            stats['top_attendees'] = sorted(attendee_counts.items(), 
                                          key=lambda x: x[1], reverse=True)[:5]
        
        return stats
    
    def find_meeting_times(self, duration_minutes, attendees, days_ahead=7, 
                          working_hours=(9, 17)):
        """Find available meeting times"""
        time_min = datetime.now(timezone.utc)
        time_max = time_min + timedelta(days=days_ahead)
        
        # Get free/busy for all calendars
        calendars = ['primary'] + attendees
        free_busy = self.get_free_busy(
            time_min.isoformat(),
            time_max.isoformat(),
            calendars
        )
        
        # Merge all busy times
        all_busy = []
        for busy_times in free_busy.values():
            for busy in busy_times:
                start = datetime.fromisoformat(busy['start'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(busy['end'].replace('Z', '+00:00'))
                all_busy.append((start, end))
        
        all_busy.sort(key=lambda x: x[0])
        
        # Find available slots
        available_slots = []
        current = time_min.replace(hour=working_hours[0], minute=0, second=0)
        
        while current < time_max and len(available_slots) < 10:
            if current.weekday() >= 5:  # Skip weekends
                current += timedelta(days=1)
                current = current.replace(hour=working_hours[0], minute=0)
                continue
            
            if current.hour >= working_hours[1]:
                current += timedelta(days=1)
                current = current.replace(hour=working_hours[0], minute=0)
                continue
            
            slot_end = current + timedelta(minutes=duration_minutes)
            
            # Check conflicts
            conflict = any(not (slot_end <= busy[0] or current >= busy[1]) 
                          for busy in all_busy)
            
            if not conflict and slot_end.hour <= working_hours[1]:
                available_slots.append({
                    'start': current.isoformat(),
                    'end': slot_end.isoformat()
                })
            
            current += timedelta(minutes=30)  # Check every 30 minutes
        
        return available_slots
    
    def export_csv(self, calendar_id='primary', output_file=None, 
                   time_min=None, time_max=None):
        """Export events to CSV"""
        events = self.list_events(
            calendar_id=calendar_id,
            time_min=time_min,
            time_max=time_max,
            max_results=2500,
            single_events=True
        )
        
        if not output_file:
            output_file = f"calendar_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['summary', 'start', 'end', 'duration_hours', 
                         'location', 'description', 'attendees']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for event in events:
                row = {
                    'summary': event.get('summary', ''),
                    'location': event.get('location', ''),
                    'description': event.get('description', '')
                }
                
                if 'dateTime' in event.get('start', {}):
                    start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
                    end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
                    duration = (end - start).total_seconds() / 3600
                    
                    row['start'] = start.strftime('%Y-%m-%d %H:%M')
                    row['end'] = end.strftime('%Y-%m-%d %H:%M')
                    row['duration_hours'] = f"{duration:.2f}"
                else:
                    row['start'] = event['start'].get('date', '')
                    row['end'] = event['end'].get('date', '')
                    row['duration_hours'] = 'All day'
                
                if event.get('attendees'):
                    row['attendees'] = '; '.join(a['email'] for a in event['attendees'])
                
                writer.writerow(row)
        
        return len(events)
    
    # Helper methods
    
    def _format_datetime(self, dt_str):
        """Format datetime string for API"""
        if not dt_str.endswith('Z') and '+' not in dt_str:
            dt = date_parser.parse(dt_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat().replace('+00:00', 'Z')
        return dt_str
    
    def _parse_local_time(self, time_str):
        """Parse time string as local time in calendar timezone"""
        dt = date_parser.parse(time_str)
        if dt.tzinfo is None:
            try:
                from zoneinfo import ZoneInfo
                dt = dt.replace(tzinfo=ZoneInfo(self.timezone))
            except:
                dt = dt.replace(tzinfo=timezone.utc)
        return dt


# Formatting functions

def format_event(event, show_id=False):
    """Format event for display"""
    lines = []
    
    # Title with color
    title = event.get('summary', 'Untitled Event')
    color_id = event.get('colorId', '')
    if color_id in COLORS:
        lines.append(f"{title} [{COLORS[color_id]}]")
    else:
        lines.append(title)
    
    # Time
    if 'dateTime' in event.get('start', {}):
        start = date_parser.parse(event['start']['dateTime'])
        end = date_parser.parse(event['end']['dateTime'])
        duration = (end - start).total_seconds() / 3600
        lines.append(f"  {start.strftime('%a %b %d, %Y %I:%M %p')} - {end.strftime('%I:%M %p')} ({duration:.1f}h)")
    else:
        start = date_parser.parse(event['start']['date'])
        lines.append(f"  {start.strftime('%a %b %d, %Y')} (All day)")
    
    # Details
    if event.get('location'):
        lines.append(f"  📍 {event['location']}")
    if event.get('description'):
        desc = event['description'].split('\n')[0][:80]
        lines.append(f"  📝 {desc}")
    if event.get('attendees'):
        attendees = [a['email'] for a in event['attendees'][:3]]
        if len(event['attendees']) > 3:
            attendees.append(f"+{len(event['attendees']) - 3} more")
        lines.append(f"  👥 {', '.join(attendees)}")
    
    if show_id:
        lines.append(f"  ID: {event['id']}")
    
    return '\n'.join(lines)


def format_calendar(calendar):
    """Format calendar for display"""
    lines = [calendar['summary']]
    if calendar.get('description'):
        lines.append(f"  {calendar['description']}")
    lines.append(f"  ID: {calendar['id']}")
    lines.append(f"  Access: {calendar['accessRole']}")
    if calendar.get('primary'):
        lines.append(f"  ⭐ Primary calendar")
    return '\n'.join(lines)


def parse_reminder(reminder_str):
    """Parse reminder string like '10m' into dict"""
    match = re.match(r'^(\d+)([mhd])$', reminder_str.lower())
    if not match:
        return None
    
    value = int(match.group(1))
    unit = match.group(2)
    minutes = value * {'m': 1, 'h': 60, 'd': 1440}[unit]
    
    return {'method': 'popup', 'minutes': minutes}


# Main CLI

def main():
    parser = argparse.ArgumentParser(
        prog='gcal',
        description='Google Calendar CLI - Unified interface'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Event commands
    
    # List
    list_parser = subparsers.add_parser('list', help='List events')
    list_parser.add_argument('-n', '--number', type=int, default=10)
    list_parser.add_argument('-s', '--search', help='Search query')
    list_parser.add_argument('--from', dest='time_min', help='Start date')
    list_parser.add_argument('--to', dest='time_max', help='End date')
    list_parser.add_argument('--show-id', action='store_true')
    list_parser.add_argument('--json', action='store_true')
    
    # Create
    create_parser = subparsers.add_parser('create', help='Create event')
    create_parser.add_argument('summary', help='Event title')
    create_parser.add_argument('start', help='Start time')
    create_parser.add_argument('-e', '--end', help='End time')
    create_parser.add_argument('-d', '--description')
    create_parser.add_argument('-l', '--location')
    create_parser.add_argument('-a', '--attendees', nargs='+')
    create_parser.add_argument('-r', '--reminders', nargs='+')
    create_parser.add_argument('--color', choices=[str(i) for i in range(1, 12)])
    create_parser.add_argument('--all-day', action='store_true')
    create_parser.add_argument('--recurrence', help='RRULE')
    
    # Quick
    quick_parser = subparsers.add_parser('quick', help='Quick add')
    quick_parser.add_argument('text', help='Natural language')
    
    # Update
    update_parser = subparsers.add_parser('update', help='Update event')
    update_parser.add_argument('event_id')
    update_parser.add_argument('-s', '--summary')
    update_parser.add_argument('--start')
    update_parser.add_argument('--end')
    update_parser.add_argument('-d', '--description')
    update_parser.add_argument('-l', '--location')
    update_parser.add_argument('--color', choices=[str(i) for i in range(1, 12)])
    
    # Delete
    delete_parser = subparsers.add_parser('delete', help='Delete event')
    delete_parser.add_argument('event_id')
    delete_parser.add_argument('--no-notify', action='store_true')
    
    # Calendar commands
    
    # Calendars
    cal_parser = subparsers.add_parser('calendars', help='List calendars')
    cal_parser.add_argument('--json', action='store_true')
    
    # Busy
    busy_parser = subparsers.add_parser('busy', help='Check free/busy')
    busy_parser.add_argument('time_min')
    busy_parser.add_argument('time_max')
    busy_parser.add_argument('-c', '--calendars', nargs='+')
    
    # Advanced commands
    
    # Analyze
    analyze_parser = subparsers.add_parser('analyze', help='Analyze calendar')
    analyze_parser.add_argument('-d', '--days', type=int, default=30)
    analyze_parser.add_argument('--json', action='store_true')
    
    # Find times
    find_parser = subparsers.add_parser('find-times', help='Find meeting slots')
    find_parser.add_argument('duration', type=int, help='Minutes')
    find_parser.add_argument('-a', '--attendees', nargs='+', required=True)
    find_parser.add_argument('-d', '--days', type=int, default=7)
    
    # Export
    export_parser = subparsers.add_parser('export', help='Export to CSV')
    export_parser.add_argument('-o', '--output', help='Output file')
    export_parser.add_argument('--from', dest='time_min')
    export_parser.add_argument('--to', dest='time_max')
    
    # New Feature Commands
    
    # Move event
    move_parser = subparsers.add_parser('move', help='Move event to another calendar')
    move_parser.add_argument('event_id', help='Event ID to move')
    move_parser.add_argument('--to', dest='destination', required=True, help='Destination calendar ID')
    move_parser.add_argument('--from', dest='source', default='primary', help='Source calendar ID')
    
    # Copy event
    copy_parser = subparsers.add_parser('copy', help='Copy event to another calendar')
    copy_parser.add_argument('event_id', help='Event ID to copy')
    copy_parser.add_argument('--to', dest='destination', help='Destination calendar ID')
    copy_parser.add_argument('--from', dest='source', default='primary', help='Source calendar ID')
    
    # Calendar management subcommands
    calendar_parser = subparsers.add_parser('calendar', help='Manage calendars')
    calendar_subparsers = calendar_parser.add_subparsers(dest='calendar_command')
    
    # Create calendar
    cal_create_parser = calendar_subparsers.add_parser('create', help='Create new calendar')
    cal_create_parser.add_argument('summary', help='Calendar name')
    cal_create_parser.add_argument('-d', '--description', help='Calendar description')
    cal_create_parser.add_argument('-l', '--location', help='Calendar location')
    cal_create_parser.add_argument('-t', '--timezone', help='Calendar timezone')
    
    # Update calendar
    cal_update_parser = calendar_subparsers.add_parser('update', help='Update calendar')
    cal_update_parser.add_argument('calendar_id', help='Calendar ID to update')
    cal_update_parser.add_argument('-s', '--summary', help='New calendar name')
    cal_update_parser.add_argument('-d', '--description', help='New description')
    cal_update_parser.add_argument('-l', '--location', help='New location')
    cal_update_parser.add_argument('-t', '--timezone', help='New timezone')
    
    # Delete calendar
    cal_delete_parser = calendar_subparsers.add_parser('delete', help='Delete calendar')
    cal_delete_parser.add_argument('calendar_id', help='Calendar ID to delete')
    cal_delete_parser.add_argument('--yes', action='store_true', help='Skip confirmation')
    
    # Get calendar details
    cal_get_parser = calendar_subparsers.add_parser('get', help='Get calendar details')
    cal_get_parser.add_argument('calendar_id', help='Calendar ID to get details for')
    
    # Respond to event
    respond_parser = subparsers.add_parser('respond', help='Respond to event invitation')
    respond_parser.add_argument('event_id', help='Event ID')
    respond_parser.add_argument('--status', choices=['accepted', 'declined', 'tentative'], required=True)
    respond_parser.add_argument('--calendar', default='primary', help='Calendar ID')
    
    # List attendees
    attendees_parser = subparsers.add_parser('attendees', help='List event attendees')
    attendees_parser.add_argument('event_id', help='Event ID')
    attendees_parser.add_argument('--calendar', default='primary', help='Calendar ID')
    attendees_parser.add_argument('--json', action='store_true')
    
    # Create with Meet
    meet_parser = subparsers.add_parser('create-meet', help='Create event with Google Meet')
    meet_parser.add_argument('summary', help='Event title')
    meet_parser.add_argument('start', help='Start time')
    meet_parser.add_argument('-e', '--end', help='End time')
    meet_parser.add_argument('-d', '--description')
    meet_parser.add_argument('-a', '--attendees', nargs='+')
    
    # Attachments
    attach_parser = subparsers.add_parser('attach', help='Add attachment to event')
    attach_parser.add_argument('event_id', help='Event ID')
    attach_parser.add_argument('file_url', help='File URL to attach')
    attach_parser.add_argument('--title', required=True, help='Attachment title')
    attach_parser.add_argument('--mime-type', default='application/octet-stream')
    attach_parser.add_argument('--icon', help='Icon URL')
    attach_parser.add_argument('--calendar', default='primary')
    
    # List attachments
    attach_list_parser = subparsers.add_parser('attachments', help='List event attachments')
    attach_list_parser.add_argument('event_id', help='Event ID')
    attach_list_parser.add_argument('--calendar', default='primary')
    attach_list_parser.add_argument('--json', action='store_true')
    
    # Out of office
    ooo_parser = subparsers.add_parser('out-of-office', help='Create out of office event')
    ooo_parser.add_argument('start_date', help='Start date (YYYY-MM-DD)')
    ooo_parser.add_argument('end_date', help='End date (YYYY-MM-DD)')
    ooo_parser.add_argument('-m', '--message', help='Out of office message')
    
    # Focus time
    focus_parser = subparsers.add_parser('focus-time', help='Create focus time block')
    focus_parser.add_argument('summary', help='Focus time description')
    focus_parser.add_argument('start', help='Start time')
    focus_parser.add_argument('end', help='End time')
    focus_parser.add_argument('--recurrence', help='RRULE for recurring focus time')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize and authenticate
    gcal = GoogleCalendarCLI()
    gcal.authenticate()
    
    # Execute commands
    try:
        if args.command == 'list':
            events = gcal.list_events(
                max_results=args.number,
                search_query=args.search,
                time_min=args.time_min,
                time_max=args.time_max
            )
            
            if args.json:
                print(json.dumps(events, indent=2))
            else:
                for event in events:
                    print(format_event(event, args.show_id))
                    print()
                if not events:
                    print("No events found.")
        
        elif args.command == 'create':
            reminders = None
            if args.reminders:
                reminders = []
                for r in args.reminders:
                    rem = parse_reminder(r)
                    if rem:
                        reminders.append(rem)
                    else:
                        print(f"Invalid reminder: {r}")
                        sys.exit(1)
            
            recurrence = None
            if args.recurrence:
                recurrence = [f"RRULE:{args.recurrence}"]
            
            event = gcal.create_event(
                args.summary,
                args.start,
                args.end,
                description=args.description,
                location=args.location,
                attendees=args.attendees,
                reminders=reminders,
                colorId=args.color,
                recurrence=recurrence,
                all_day=args.all_day
            )
            
            if event:
                print(f"Event created successfully!")
                print(f"ID: {event['id']}")
                if 'htmlLink' in event:
                    print(f"Link: {event['htmlLink']}")
        
        elif args.command == 'quick':
            event = gcal.quick_add(args.text)
            if event:
                print(f"Event created: {event.get('summary', 'Untitled')}")
                print(f"ID: {event['id']}")
        
        elif args.command == 'update':
            updates = {}
            for field in ['summary', 'start', 'end', 'description', 'location']:
                if getattr(args, field, None):
                    updates[field] = getattr(args, field)
            if args.color:
                updates['colorId'] = args.color
            
            event = gcal.update_event(args.event_id, **updates)
            if event:
                print("Event updated successfully!")
                print(format_event(event, show_id=True))
        
        elif args.command == 'delete':
            if not args.no_notify:
                confirm = input(f"Delete event {args.event_id}? (y/N): ")
                if confirm.lower() != 'y':
                    print("Cancelled.")
                    sys.exit(0)
            
            if gcal.delete_event(args.event_id, notify=not args.no_notify):
                print("Event deleted successfully.")
        
        elif args.command == 'calendars':
            calendars = gcal.list_calendars()
            if args.json:
                print(json.dumps(calendars, indent=2))
            else:
                for cal in calendars:
                    print(format_calendar(cal))
                    print()
        
        elif args.command == 'busy':
            free_busy = gcal.get_free_busy(args.time_min, args.time_max, args.calendars)
            for cal_id, busy_times in free_busy.items():
                print(f"\nCalendar: {cal_id}")
                if busy_times:
                    print("Busy times:")
                    for busy in busy_times:
                        start = date_parser.parse(busy['start'])
                        end = date_parser.parse(busy['end'])
                        print(f"  {start.strftime('%Y-%m-%d %I:%M %p')} - {end.strftime('%I:%M %p')}")
                else:
                    print("  No busy times")
        
        elif args.command == 'analyze':
            stats = gcal.analyze_calendar(days=args.days)
            if args.json:
                print(json.dumps(stats, indent=2, default=str))
            else:
                print(f"\n📊 Calendar Analysis ({args.days} days)")
                print("=" * 50)
                print(f"Total events: {stats['total_events']}")
                print(f"Total hours: {stats['total_hours']:.1f}")
                print(f"Average duration: {stats['average_duration']:.1f} hours")
                print(f"Meetings with others: {stats['meetings_with_others']}")
                
                if stats['top_attendees']:
                    print("\nTop attendees:")
                    for email, count in stats['top_attendees']:
                        print(f"  {email}: {count} meetings")
        
        elif args.command == 'find-times':
            slots = gcal.find_meeting_times(args.duration, args.attendees, args.days)
            print(f"\n📅 Available {args.duration}-minute slots:")
            for slot in slots:
                start = date_parser.parse(slot['start'])
                end = date_parser.parse(slot['end'])
                print(f"{start.strftime('%a %b %d, %I:%M %p')} - {end.strftime('%I:%M %p')}")
        
        elif args.command == 'export':
            count = gcal.export_csv(
                output_file=args.output,
                time_min=args.time_min,
                time_max=args.time_max
            )
            print(f"Exported {count} events.")
        
        # New feature command handlers
        
        elif args.command == 'move':
            event = gcal.move_event(args.event_id, args.source, args.destination)
            if event:
                print(f"Event moved successfully to calendar: {args.destination}")
                print(f"ID: {event['id']}")
            else:
                print(f"Failed to move event {args.event_id}")
        
        elif args.command == 'copy':
            event = gcal.copy_event(args.event_id, args.source, args.destination)
            if event:
                print(f"Event copied successfully!")
                print(f"New event ID: {event['id']}")
            else:
                print(f"Failed to copy event {args.event_id}")
        
        elif args.command == 'calendar':
            if args.calendar_command == 'create':
                kwargs = {}
                if args.description:
                    kwargs['description'] = args.description
                if args.location:
                    kwargs['location'] = args.location
                if args.timezone:
                    kwargs['timeZone'] = args.timezone
                
                calendar = gcal.create_calendar(args.summary, **kwargs)
                if calendar:
                    print(f"Calendar created successfully!")
                    print(f"ID: {calendar['id']}")
                    print(f"Name: {calendar['summary']}")
            
            elif args.calendar_command == 'update':
                updates = {}
                if args.summary:
                    updates['summary'] = args.summary
                if args.description:
                    updates['description'] = args.description
                if args.location:
                    updates['location'] = args.location
                if args.timezone:
                    updates['timeZone'] = args.timezone
                
                calendar = gcal.update_calendar(args.calendar_id, **updates)
                if calendar:
                    print("Calendar updated successfully!")
                    print(format_calendar(calendar))
            
            elif args.calendar_command == 'delete':
                if not args.yes:
                    confirm = input(f"Delete calendar {args.calendar_id}? This cannot be undone! (y/N): ")
                    if confirm.lower() != 'y':
                        print("Cancelled.")
                        sys.exit(0)
                
                if gcal.delete_calendar(args.calendar_id):
                    print("Calendar deleted successfully.")
                else:
                    print(f"Failed to delete calendar {args.calendar_id}")
            
            elif args.calendar_command == 'get':
                calendar = gcal.get_calendar(args.calendar_id)
                if calendar:
                    print(format_calendar(calendar))
                else:
                    print(f"Calendar {args.calendar_id} not found")
        
        elif args.command == 'respond':
            event = gcal.respond_to_event(args.event_id, args.status, args.calendar)
            if event:
                print(f"Response updated to: {args.status}")
            else:
                print(f"Failed to update response for event {args.event_id}")
        
        elif args.command == 'attendees':
            attendees = gcal.list_event_attendees(args.event_id, args.calendar)
            if args.json:
                print(json.dumps(attendees, indent=2))
            else:
                print(f"\n👥 Attendees for event {args.event_id}:")
                for attendee in attendees:
                    status_emoji = {
                        'accepted': '✅',
                        'declined': '❌',
                        'tentative': '❓',
                        'needsAction': '⏳'
                    }.get(attendee['responseStatus'], '?')
                    
                    info = f"{status_emoji} {attendee['email']}"
                    if attendee['displayName']:
                        info += f" ({attendee['displayName']})"
                    if attendee['organizer']:
                        info += " [Organizer]"
                    if attendee['self']:
                        info += " [You]"
                    if attendee['optional']:
                        info += " [Optional]"
                    print(f"  {info}")
        
        elif args.command == 'create-meet':
            event = gcal.create_event_with_meet(
                args.summary,
                args.start,
                args.end,
                description=args.description,
                attendees=args.attendees
            )
            if event:
                print(f"Event with Google Meet created successfully!")
                print(f"ID: {event['id']}")
                if 'conferenceData' in event:
                    meet_link = event['conferenceData'].get('entryPoints', [{}])[0].get('uri', '')
                    if meet_link:
                        print(f"Google Meet: {meet_link}")
        
        elif args.command == 'attach':
            event = gcal.add_attachment(
                args.event_id,
                args.file_url,
                args.title,
                calendar_id=args.calendar,
                mime_type=args.mime_type.replace('_', '/'),
                icon_link=args.icon
            )
            if event:
                print(f"Attachment added successfully!")
                print(f"Title: {args.title}")
                print(f"URL: {args.file_url}")
        
        elif args.command == 'attachments':
            attachments = gcal.list_attachments(args.event_id, args.calendar)
            if args.json:
                print(json.dumps(attachments, indent=2))
            else:
                print(f"\n📎 Attachments for event {args.event_id}:")
                if attachments:
                    for att in attachments:
                        print(f"  - {att.get('title', 'Untitled')}")
                        print(f"    URL: {att.get('fileUrl', '')}")
                        print(f"    Type: {att.get('mimeType', 'Unknown')}")
                else:
                    print("  No attachments found.")
        
        elif args.command == 'out-of-office':
            event = gcal.create_out_of_office(args.start_date, args.end_date, args.message)
            if event:
                print(f"Out of office event created successfully!")
                print(f"ID: {event['id']}")
                print(f"Period: {args.start_date} to {args.end_date}")
        
        elif args.command == 'focus-time':
            recurrence = None
            if args.recurrence:
                recurrence = [f"RRULE:{args.recurrence}"]
            
            event = gcal.create_focus_time(args.summary, args.start, args.end, recurrence)
            if event:
                print(f"Focus time block created successfully!")
                print(f"ID: {event['id']}")
                print(f"Title: {args.summary}")
                print(f"Time: {args.start} to {args.end}")
                if recurrence:
                    print(f"Recurring: Yes")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()