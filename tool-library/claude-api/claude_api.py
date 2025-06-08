#!/usr/bin/env python3
"""
Claude API Server - Simple HTTP API for Claude Code
"""
import asyncio
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Claude API", version="0.1.0")

# Configuration
WORKSPACES_DIR = Path("/tmp/claude-workspaces")
WORKSPACES_DIR.mkdir(exist_ok=True)

# In-memory session tracking (could be Redis in production)
sessions: Dict[str, dict] = {}


class SessionCreateRequest(BaseModel):
    initial_prompt: Optional[str] = None
    session_name: Optional[str] = None


class MessageRequest(BaseModel):
    prompt: str


class SessionInfo:
    def __init__(self, session_id: str, name: Optional[str] = None):
        self.id = session_id
        self.name = name or f"Session {session_id[:8]}"
        self.workspace = WORKSPACES_DIR / session_id
        self.created_at = datetime.utcnow()
        self.last_used = datetime.utcnow()
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat(),
            "workspace": str(self.workspace)
        }


def create_session_claude_md(workspace: Path):
    """Create a CLAUDE.md file in the session workspace with tool library access"""
    claude_md_content = """# Session Instructions

## Available CLI Tools

You have access to the following CLI tools from the tool library:

### Core Tools
- **airtable** - Manage Airtable bases, tables, and records
- **cal-com** - Cal.com booking and availability management  
- **gcal / google-calendar** - Google Calendar with events, scheduling, and Google Meet
- **gmail** - Full Gmail management with search, send, drafts, and analysis
- **google-maps** - Geocoding, directions, and place search
- **grok** - xAI's Grok for chat and X/Twitter analysis
- **image-gen** - DALL-E image generation
- **square** - Square payment and customer management
- **typefully** - Twitter/X content creation and scheduling
- **current-time** - Network-based accurate time

### Using Tools
All tools are available as direct commands. For example:
- `gmail list` - List recent emails
- `gcal create "Meeting" "2pm"` - Create calendar event
- `image-gen "a beautiful sunset"` - Generate an image

### Business CLI Tool
You have access to a business management CLI:
```bash
# Get business info
business-cli get 12345

# Update business
business-cli update 12345 --name "New Name" --phone "555-1234"

# Create new business
business-cli create "Pete's Coffee" --phone "555-0000" --address "123 Main St"

# Search businesses
business-cli search "coffee" --json
```

### Direct API Callback (alternative)
You can also make callbacks to the host API:
```bash
curl -X POST http://localhost:8000/callback \
  -H "Content-Type: application/json" \
  -d '{"action": "update_record", "data": {...}}'
```

## Important Notes
- All tools respect the global Claude configuration
- Tool outputs can be piped and combined
- Use --json flag for structured output when available
"""
    
    claude_md_path = workspace / "CLAUDE.md"
    claude_md_path.write_text(claude_md_content)


async def execute_claude(prompt: str, workspace: Path, continue_session: bool = False) -> dict:
    """Execute claude command and return the response"""
    
    # Ensure CLAUDE.md exists for tool access
    if not (workspace / "CLAUDE.md").exists():
        create_session_claude_md(workspace)
    
    # Build command with allowed tools - using stdin for prompt
    cmd = ["claude", "--print", "--allowedTools", "Bash,Read,Write,Edit,WebSearch,WebFetch"]
    if continue_session and (workspace / ".claude").exists():
        cmd.append("--continue")
    
    # Set up environment with tool library in PATH
    env = os.environ.copy()
    tool_bin_path = "/Users/pete/Projects/tool-library/bin"
    if "PATH" in env:
        env["PATH"] = f"{tool_bin_path}:{env['PATH']}"
    else:
        env["PATH"] = tool_bin_path
    
    try:
        # Debug: print the command
        print(f"Executing command: {' '.join(cmd)}")
        print(f"With prompt: {prompt}")
        
        # Execute command with stdin
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(workspace),
            env=env
        )
        
        # Send prompt via stdin
        stdout, stderr = await process.communicate(input=prompt.encode())
        
        if process.returncode != 0:
            return {
                "success": False,
                "error": stderr.decode(),
                "response": None
            }
        
        return {
            "success": True,
            "response": stdout.decode(),
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response": None
        }


@app.get("/")
async def root():
    """API info"""
    return {
        "name": "Claude API",
        "version": "0.1.0",
        "endpoints": {
            "POST /sessions": "Create a new session",
            "GET /sessions": "List all sessions",
            "POST /sessions/{session_id}/messages": "Send message to session",
            "GET /sessions/{session_id}": "Get session info",
            "DELETE /sessions/{session_id}": "Delete session"
        }
    }


@app.post("/sessions")
async def create_session(request: SessionCreateRequest):
    """Create a new Claude session"""
    session_id = str(uuid.uuid4())
    session = SessionInfo(session_id, request.session_name)
    
    # Create workspace directory
    session.workspace.mkdir(exist_ok=True)
    
    # Store session info
    sessions[session_id] = session.to_dict()
    
    response_data = {
        "session": session.to_dict(),
        "initial_response": None
    }
    
    # Send initial prompt if provided
    if request.initial_prompt:
        result = await execute_claude(request.initial_prompt, session.workspace, continue_session=False)
        if result["success"]:
            response_data["initial_response"] = result["response"]
        else:
            # Still return session, but include error
            response_data["error"] = result["error"]
    
    return response_data


@app.get("/sessions")
async def list_sessions():
    """List all active sessions"""
    return {
        "sessions": list(sessions.values()),
        "count": len(sessions)
    }


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return sessions[session_id]


@app.post("/sessions/{session_id}/messages")
async def send_message(session_id: str, request: MessageRequest):
    """Send a message to an existing session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    workspace = WORKSPACES_DIR / session_id
    if not workspace.exists():
        raise HTTPException(status_code=500, detail="Session workspace not found")
    
    # Update last used time
    sessions[session_id]["last_used"] = datetime.utcnow().isoformat()
    
    # Execute claude with --continue flag
    result = await execute_claude(request.prompt, workspace, continue_session=True)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return {
        "session_id": session_id,
        "prompt": request.prompt,
        "response": result["response"],
        "timestamp": datetime.utcnow().isoformat()
    }


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session and its workspace"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Remove workspace
    workspace = WORKSPACES_DIR / session_id
    if workspace.exists():
        import shutil
        shutil.rmtree(workspace)
    
    # Remove from sessions
    del sessions[session_id]
    
    return {"message": "Session deleted", "session_id": session_id}


class CallbackRequest(BaseModel):
    action: str
    data: dict
    session_id: Optional[str] = None


@app.post("/callback")
async def handle_callback(request: CallbackRequest):
    """Handle callbacks from Claude sessions"""
    print(f"Received callback: {request.action} with data: {request.data}")
    
    # Example callback handling
    if request.action == "update_business":
        # Here you would update your database
        return {
            "status": "success",
            "message": f"Business updated with data: {request.data}",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    elif request.action == "fetch_business_info":
        # Example: return mock business data
        return {
            "status": "success",
            "data": {
                "business_id": request.data.get("business_id"),
                "name": "Example Business Inc.",
                "address": "123 Main St, City, State",
                "phone": "555-0123",
                "hours": "9 AM - 5 PM",
                "rating": 4.5
            }
        }
    
    else:
        return {
            "status": "error",
            "message": f"Unknown action: {request.action}"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)