# Tool Library

This directory contains markdown documentation for all MCP (Model Context Protocol) tools available to agents in this repository.

## Available Tools

### Social Media
- **[twitter-api-mcp](./twitter-api-mcp.md)** - X/Twitter API access for searching and posting

### System Tools (Built into Claude Code)
These don't need MCP servers:
- **file-reader** - Read any file on the system
- **file-writer** - Write content to files
- **bash** - Execute shell commands
- **web-fetch** - Fetch content from URLs

## How Tools Work

1. **Generic Documentation**: Each tool in this library has a generic `.md` file explaining its capabilities
2. **Team Customization**: Agent teams can create customized versions in their `/tools/` folder
3. **Natural Language**: Agents reference tools by name and describe what they want in plain English

## Adding New Tools

To add a new MCP tool:

1. Install the MCP server:
   ```bash
   npm install @mcp/your-tool-name
   ```

2. Create documentation in this folder:
   ```markdown
   # Tool: Your Tool Name
   
   ## Metadata
   - Version: 1.0
   - Type: external-api
   - MCP-Server: your-tool-mcp
   
   ## Purpose
   What this tool does...
   
   ## Operations
   List all available operations...
   ```

3. Configure in your Claude Code MCP settings

4. Reference in agent markdown:
   ```markdown
   ## Tools
   ### your-tool-name
   - Description: What I use this for
   - Operations: Specific operations I need
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