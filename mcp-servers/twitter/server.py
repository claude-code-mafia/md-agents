#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value.strip()

def main():
    # Load environment variables
    load_env()
    
    # Verify required environment variables
    required_vars = ['TWITTER_USERNAME', 'TWITTER_EMAIL', 'TWITTER_PASSWORD']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}", file=sys.stderr)
        print("Please set these in mcp-servers/.env file", file=sys.stderr)
        sys.exit(1)
    
    # Run mcp-twikit using uvx
    try:
        subprocess.run([
            "uvx",
            "--from", "git+https://github.com/adhikasp/mcp-twikit",
            "mcp-twikit"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running mcp-twikit: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: uvx not found. Please install it with: pip install uvx", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()