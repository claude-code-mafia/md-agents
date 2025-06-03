# Tool Library

This directory contains documentation for all CLI tools available to agents in this repository. These tools are optimized for Claude Code and are executed as command-line interfaces.

## Available Tools

### Social Media
- **[x-tool](./x-tool.md)** - X/Twitter CLI for searching and posting (uses Typefully or other CLI tools)

### System Tools (Built into Claude Code)
- **Read** - Read any file on the system
- **Write/Edit** - Write or modify files
- **Bash** - Execute shell commands
- **WebFetch** - Fetch content from URLs
- **WebSearch** - Search the web for current information

## How Tools Work

1. **CLI-Based**: All tools are command-line interfaces that Claude Code executes via the Bash tool
2. **Documentation**: Each tool has a `.md` file explaining its commands and usage
3. **Natural Language**: Agents reference tools by name and describe what they want in plain English
4. **Pre-installed**: Many tools come pre-installed with Claude Code (see global CLAUDE.md)

## Adding New Tools

To add a new CLI tool:

1. Install the tool (if needed):
   ```bash
   # Example: npm global install
   npm install -g your-cli-tool
   
   # Or pip install
   pip install your-python-tool
   ```

2. Create documentation in this folder:
   ```markdown
   # Tool: Your Tool Name
   
   ## Purpose
   What this tool does...
   
   ## Installation
   How to install if not pre-installed...
   
   ## Commands
   List all available commands...
   
   ## Usage Examples
   Show practical examples...
   ```

3. Reference in agent markdown:
   ```markdown
   ## Tools
   ### your-tool-name
   - Description: What I use this for
   - Commands: Specific commands I need
   ```

## Tool Categories

### External APIs
- Social media platforms
- Cloud services  
- Databases
- Third-party services

### Development Tools
- Version control
- Package managers
- Build systems
- Testing frameworks

### Data Processing
- File converters
- Data analyzers
- Image processors
- Text manipulators

### Communication
- Email services
- Messaging platforms
- Notification systems
- Webhooks