#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title System Info
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 💻
# @raycast.packageName System
# @raycast.refreshTime 10s

# Documentation:
# @raycast.description Show system information
# @raycast.author Pete
# @raycast.authorURL https://github.com/pete

import platform
import subprocess
import psutil
import socket
from datetime import datetime

def get_uptime():
    """Get system uptime on macOS"""
    try:
        result = subprocess.run(['uptime'], capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return "Unknown"

def format_bytes(bytes):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

def main():
    print("💻 System Information")
    print("=" * 50)
    
    # Basic info
    print(f"\n🖥️  System: {platform.system()} {platform.release()}")
    print(f"📦 Machine: {platform.machine()}")
    print(f"🏷️  Hostname: {socket.gethostname()}")
    print(f"🐍 Python: {platform.python_version()}")
    
    # CPU info
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"\n⚡ CPU: {cpu_count} cores, {cpu_percent}% usage")
    
    # Memory info
    memory = psutil.virtual_memory()
    print(f"\n🧠 Memory:")
    print(f"   Total: {format_bytes(memory.total)}")
    print(f"   Used: {format_bytes(memory.used)} ({memory.percent}%)")
    print(f"   Available: {format_bytes(memory.available)}")
    
    # Disk info
    disk = psutil.disk_usage('/')
    print(f"\n💾 Disk (/):")
    print(f"   Total: {format_bytes(disk.total)}")
    print(f"   Used: {format_bytes(disk.used)} ({disk.percent}%)")
    print(f"   Free: {format_bytes(disk.free)}")
    
    # Uptime
    print(f"\n⏱️  Uptime: {get_uptime()}")
    
    # Current time
    print(f"\n🕐 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()