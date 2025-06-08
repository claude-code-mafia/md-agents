#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Clipboard History
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 📋
# @raycast.packageName Utilities

# Documentation:
# @raycast.description Show recent clipboard items (macOS)
# @raycast.author Pete
# @raycast.authorURL https://github.com/pete

import subprocess
import json
from datetime import datetime

# Note: This is a simplified example. Real clipboard history would need
# a background process to track changes over time.

def get_current_clipboard():
    """Get current clipboard content"""
    try:
        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
        return result.stdout
    except:
        return None

def main():
    current = get_current_clipboard()
    
    print("📋 Clipboard History")
    print("=" * 50)
    
    if current:
        print(f"\n🔵 Current clipboard:")
        print(f"{current[:100]}{'...' if len(current) > 100 else ''}")
        print(f"Length: {len(current)} characters")
    else:
        print("Clipboard is empty")
    
    print("\n💡 Tip: For full clipboard history, consider using a dedicated")
    print("clipboard manager like Raycast's built-in clipboard history.")

if __name__ == '__main__':
    main()