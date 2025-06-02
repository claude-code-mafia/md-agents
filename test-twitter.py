#!/usr/bin/env python3
"""Test script to verify mcp-twikit installation and credentials"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path to import from mcp-servers
sys.path.insert(0, str(Path(__file__).parent / 'mcp-servers' / 'twitter'))

# Import and run the env loading function
from server import load_env

print("Testing mcp-twikit setup...")
print("-" * 40)

# Load environment variables
load_env()

# Check credentials
creds = {
    'TWITTER_USERNAME': os.environ.get('TWITTER_USERNAME'),
    'TWITTER_EMAIL': os.environ.get('TWITTER_EMAIL'),
    'TWITTER_PASSWORD': os.environ.get('TWITTER_PASSWORD')
}

print("Credential check:")
for key, value in creds.items():
    if value:
        # Mask sensitive parts
        if key == 'TWITTER_PASSWORD':
            masked = '*' * len(value)
        elif key == 'TWITTER_EMAIL':
            parts = value.split('@')
            if len(parts) == 2:
                masked = parts[0][:3] + '***@' + parts[1]
            else:
                masked = '***'
        else:
            masked = value
        print(f"  ✓ {key}: {masked}")
    else:
        print(f"  ✗ {key}: NOT SET")

print("-" * 40)
print("\nTo test the MCP server, restart Claude Code and check the MCP status.")
print("The server should appear as 'twitter' in the MCP connections.")