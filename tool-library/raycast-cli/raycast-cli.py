#!/usr/bin/env python3
"""
Raycast CLI - Run Raycast Script Commands from the terminal
"""

import argparse
import os
import re
import subprocess
import sys
import json
from pathlib import Path
import tempfile

class RaycastScript:
    """Represents a Raycast Script Command"""
    
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.metadata = self._parse_metadata()
        
    def _parse_metadata(self):
        """Parse Raycast metadata from script file"""
        metadata = {
            'title': None,
            'mode': 'compact',
            'packageName': None,
            'arguments': [],
            'schemaVersion': '1'
        }
        
        with open(self.file_path, 'r') as f:
            content = f.read()
            
        # Parse metadata comments
        for line in content.split('\n'):
            if line.startswith('# @raycast.'):
                match = re.match(r'# @raycast\.(\w+)\s+(.*)', line)
                if match:
                    key, value = match.groups()
                    if key.startswith('argument'):
                        # Parse argument JSON
                        try:
                            arg_data = json.loads(value)
                            metadata['arguments'].append(arg_data)
                        except:
                            pass
                    else:
                        metadata[key] = value.strip()
                        
        return metadata
    
    def run(self, args=None):
        """Execute the script with given arguments"""
        cmd = [str(self.file_path)]
        if args:
            cmd.extend(args)
            
        try:
            # Make script executable
            os.chmod(self.file_path, 0o755)
            
            # Run based on mode
            if self.metadata['mode'] == 'silent':
                subprocess.run(cmd, capture_output=True, text=True)
                print(f"✓ {self.metadata['title']} completed")
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(result.stdout)
                else:
                    print(f"Error: {result.stderr}", file=sys.stderr)
                    sys.exit(result.returncode)
        except Exception as e:
            print(f"Error running script: {e}", file=sys.stderr)
            sys.exit(1)

class RaycastCLI:
    """Main CLI for running Raycast scripts"""
    
    def __init__(self):
        # Try different common locations for Raycast scripts
        self.default_dirs = [
            Path.home() / 'Documents' / 'Raycast Scripts',
            Path.home() / 'Library' / 'Script Commands',
            Path.home() / '.raycast' / 'scripts',
        ]
        self.scripts_dir = self.default_dirs[0]  # Default
        self.custom_dirs = []
        
    def find_scripts(self, directories=None):
        """Find all Raycast scripts in given directories"""
        scripts = {}
        dirs_to_search = directories or self.default_dirs + self.custom_dirs
        
        for directory in dirs_to_search:
            if not directory.exists():
                continue
                
            for file_path in directory.rglob('*'):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    try:
                        script = RaycastScript(file_path)
                        if script.metadata['title']:
                            # Use lowercase title as key for easy lookup
                            key = script.metadata['title'].lower().replace(' ', '-')
                            scripts[key] = script
                    except:
                        pass
                        
        return scripts
    
    def list_scripts(self):
        """List all available scripts"""
        scripts = self.find_scripts()
        
        if not scripts:
            print("No Raycast scripts found.")
            print(f"Default location: {self.scripts_dir}")
            return
            
        print("Available Raycast Scripts:")
        print("-" * 50)
        
        # Group by package
        packages = {}
        for key, script in scripts.items():
            package = script.metadata.get('packageName', 'Uncategorized')
            if package not in packages:
                packages[package] = []
            packages[package].append((key, script))
            
        for package, items in sorted(packages.items()):
            print(f"\n📦 {package}")
            for key, script in sorted(items):
                args_desc = ""
                if script.metadata['arguments']:
                    args_desc = " " + " ".join(f"<{arg.get('placeholder', 'arg')}>" 
                                               for arg in script.metadata['arguments'])
                print(f"  {key}{args_desc} - {script.metadata['title']}")
    
    def run_script(self, script_name, args):
        """Run a specific script by name"""
        scripts = self.find_scripts()
        
        # Try exact match first
        if script_name in scripts:
            scripts[script_name].run(args)
            return
            
        # Try fuzzy match
        matches = [k for k in scripts if script_name in k]
        if len(matches) == 1:
            scripts[matches[0]].run(args)
        elif len(matches) > 1:
            print(f"Multiple scripts match '{script_name}':")
            for match in matches:
                print(f"  - {match}")
            print("\nPlease be more specific.")
            sys.exit(1)
        else:
            print(f"No script found matching '{script_name}'")
            print("Use 'raycast list' to see available scripts.")
            sys.exit(1)
    
    def create_script(self, name, language='bash'):
        """Create a new Raycast script from template"""
        templates = {
            'bash': '''#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title {title}
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🚀
# @raycast.packageName My Scripts

# Documentation:
# @raycast.description {description}
# @raycast.author Your Name
# @raycast.authorURL https://github.com/yourusername

echo "Hello from {title}!"
''',
            'python': '''#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title {title}
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🐍
# @raycast.packageName My Scripts

# Documentation:
# @raycast.description {description}
# @raycast.author Your Name
# @raycast.authorURL https://github.com/yourusername

print("Hello from {title}!")
''',
            'node': '''#!/usr/bin/env node

// Required parameters:
// @raycast.schemaVersion 1
// @raycast.title {title}
// @raycast.mode compact

// Optional parameters:
// @raycast.icon 📦
// @raycast.packageName My Scripts

// Documentation:
// @raycast.description {description}
// @raycast.author Your Name
// @raycast.authorURL https://github.com/yourusername

console.log("Hello from {title}!");
'''
        }
        
        if language not in templates:
            print(f"Unknown language: {language}")
            print(f"Available: {', '.join(templates.keys())}")
            sys.exit(1)
            
        # Create scripts directory if needed
        self.scripts_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        filename = name.lower().replace(' ', '-') + ('.py' if language == 'python' else '.sh' if language == 'bash' else '.js')
        file_path = self.scripts_dir / filename
        
        if file_path.exists():
            print(f"Script already exists: {file_path}")
            sys.exit(1)
            
        # Create script
        title = name.title()
        description = f"A new {language} script"
        content = templates[language].format(title=title, description=description)
        
        with open(file_path, 'w') as f:
            f.write(content)
            
        os.chmod(file_path, 0o755)
        print(f"Created script: {file_path}")
        print(f"Edit it and run with: raycast {name.lower().replace(' ', '-')}")

def main():
    parser = argparse.ArgumentParser(description='Run Raycast Script Commands from the terminal')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available scripts')
    
    # Run command (default)
    run_parser = subparsers.add_parser('run', help='Run a script')
    run_parser.add_argument('script', help='Script name or partial match')
    run_parser.add_argument('args', nargs='*', help='Arguments to pass to script')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new script')
    create_parser.add_argument('name', help='Script name')
    create_parser.add_argument('-l', '--language', choices=['bash', 'python', 'node'], 
                              default='bash', help='Script language')
    
    # Path command
    path_parser = subparsers.add_parser('path', help='Show scripts directory path')
    
    # Parse args
    args = parser.parse_args()
    
    cli = RaycastCLI()
    
    if args.command == 'list':
        cli.list_scripts()
    elif args.command == 'create':
        cli.create_script(args.name, args.language)
    elif args.command == 'path':
        print(cli.scripts_dir)
    elif args.command == 'run':
        cli.run_script(args.script, args.args)
    else:
        # Default to run if a script name is provided
        if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
            script_name = sys.argv[1]
            script_args = sys.argv[2:]
            cli.run_script(script_name, script_args)
        else:
            parser.print_help()

if __name__ == '__main__':
    main()