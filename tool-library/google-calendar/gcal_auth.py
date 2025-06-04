#!/Users/pete/Projects/tool-library/google-calendar/venv/bin/python
"""
Google Calendar CLI Authentication Helper
"""

import os
import sys
import pickle
import webbrowser
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar API scopes
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

# Configuration
CONFIG_DIR = Path.home() / '.gcal-cli'
TOKEN_FILE = CONFIG_DIR / 'token.pickle'
CREDENTIALS_FILE = CONFIG_DIR / 'credentials.json'


def authenticate():
    """Run authentication flow"""
    print("Google Calendar CLI - Authentication Setup")
    print("=" * 50)
    
    # Check for credentials file
    if not CREDENTIALS_FILE.exists():
        print(f"Error: credentials.json not found at {CREDENTIALS_FILE}")
        print("\nTo set up Google Calendar CLI:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing")
        print("3. Enable Google Calendar API")
        print("4. Create OAuth 2.0 credentials (Desktop application)")
        print(f"5. Download credentials.json to {CREDENTIALS_FILE}")
        sys.exit(1)
    
    print("✓ Found credentials.json")
    
    # Check for existing token
    if TOKEN_FILE.exists():
        print("✓ Found existing token")
        try:
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
            if creds and creds.valid:
                print("✓ Token is valid")
                print("\nAuthentication is already complete!")
                return
            elif creds and creds.expired and creds.refresh_token:
                print("Token expired, refreshing...")
                creds.refresh(Request())
                with open(TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
                print("✓ Token refreshed successfully")
                return
        except Exception as e:
            print(f"Error loading token: {e}")
            print("Will create new token...")
    
    # Run OAuth flow
    print("\nStarting OAuth authentication flow...")
    print("This will open your browser to authorize access.")
    print("\nIMPORTANT: After authorizing in your browser:")
    print("1. You'll see a 'localhost refused to connect' error - this is NORMAL")
    print("2. Just return to this terminal")
    print("3. The authentication will complete automatically")
    print("\nPress Enter to open your browser...")
    input()
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_FILE), SCOPES)
        
        # Try to use a fixed port
        creds = flow.run_local_server(
            port=8080,
            authorization_prompt_message='Please visit this URL to authorize: {url}',
            success_message='Authorization complete! You can close this window and return to the terminal.',
            open_browser=True
        )
        
        # Save the credentials
        CONFIG_DIR.mkdir(exist_ok=True)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        
        print("\n✓ Authentication successful!")
        print("✓ Token saved to", TOKEN_FILE)
        
        # Test the connection
        print("\nTesting connection...")
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        print(f"✓ Connected to calendar: {calendar.get('summary', 'Primary')}")
        print(f"✓ Time zone: {calendar.get('timeZone', 'Unknown')}")
        
        print("\nSetup complete! You can now use 'gcal' commands.")
        
    except Exception as e:
        print(f"\nError during authentication: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're allowing pop-ups in your browser")
        print("2. Try copying the URL manually if the browser doesn't open")
        print("3. Check that port 8080 is not in use")
        sys.exit(1)


if __name__ == '__main__':
    authenticate()