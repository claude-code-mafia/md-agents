#!/usr/bin/env python3
"""
Claude API v2 - Enhanced with persistent shareable sessions
"""
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from session_manager import ClaudeSessionManager

app = FastAPI(title="Claude API v2", version="2.0.0")
session_manager = ClaudeSessionManager()

# WebSocket connections for real-time updates
active_connections: Dict[str, List[WebSocket]] = {}


class SessionCreateRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    shared: Optional[bool] = False
    tags: Optional[List[str]] = None
    initial_prompt: Optional[str] = None


class MessageRequest(BaseModel):
    prompt: str
    participant: Optional[str] = "anonymous"


class SessionUpdateRequest(BaseModel):
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    shared: Optional[bool] = None


async def execute_claude(prompt: str, workspace: Path, session_id: str, 
                        continue_session: bool = False) -> dict:
    """Execute claude command with session awareness"""
    
    # Build command
    cmd = ["claude", "--print", "--allowedTools", "Bash,Read,Write,Edit,WebSearch,WebFetch"]
    
    # Check if we should resume an existing Claude session
    session_info = session_manager.sessions.get(session_id, {})
    claude_session_id = session_info.get('claude_session_id')
    
    if continue_session and claude_session_id:
        # Use --resume with the actual Claude session ID
        cmd.extend(["--resume", claude_session_id])
    
    # Set up environment
    env = os.environ.copy()
    tool_bin_path = "/Users/pete/Projects/tool-library/bin"
    env["PATH"] = f"{tool_bin_path}:{env.get('PATH', '')}"
    
    # Add session context to environment
    env["CLAUDE_SESSION_ID"] = session_id
    env["CLAUDE_SESSION_NAME"] = session_manager.sessions.get(session_id, {}).get('name', '')
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(workspace),
            env=env
        )
        
        stdout, stderr = await process.communicate(input=prompt.encode())
        
        if process.returncode != 0:
            return {
                "success": False,
                "error": stderr.decode(),
                "response": None
            }
        
        # Update session activity and capture Claude session ID
        if session_id in session_manager.sessions:
            session_manager.sessions[session_id]["last_accessed"] = datetime.utcnow().isoformat()
            session_manager.sessions[session_id]["message_count"] += 1
            
            # If this is the first interaction, find and store Claude's session ID
            if not session_manager.sessions[session_id].get('claude_session_id'):
                # Look for the session ID in Claude's project directory
                claude_projects_dir = Path.home() / ".claude" / "projects"
                workspace_name = str(workspace).replace("/tmp/", "/private/tmp/").replace("/", "-")
                project_dir = claude_projects_dir / workspace_name
                
                if project_dir.exists():
                    # Get the most recent .jsonl file (Claude's session)
                    jsonl_files = list(project_dir.glob("*.jsonl"))
                    if jsonl_files:
                        # Sort by modification time, get the newest
                        newest_file = max(jsonl_files, key=lambda p: p.stat().st_mtime)
                        claude_session_id = newest_file.stem  # filename without .jsonl
                        session_manager.sessions[session_id]["claude_session_id"] = claude_session_id
            
            session_manager.save_metadata()
        
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
        "name": "Claude API v2",
        "version": "2.0.0",
        "features": [
            "Persistent sessions",
            "Shareable sessions", 
            "Session history",
            "Real-time updates via WebSocket",
            "Session cloning",
            "Team collaboration"
        ],
        "endpoints": {
            "POST /sessions": "Create a new persistent session",
            "GET /sessions": "List active sessions",
            "GET /sessions/{id}": "Get session details",
            "POST /sessions/{id}/messages": "Send message to session",
            "GET /sessions/{id}/history": "Get full session history",
            "GET /sessions/{id}/summary": "Get session summary",
            "PUT /sessions/{id}": "Update session metadata",
            "POST /sessions/{id}/clone": "Clone a session",
            "POST /sessions/{id}/archive": "Archive a session",
            "WS /sessions/{id}/ws": "WebSocket for real-time updates"
        }
    }


@app.post("/sessions")
async def create_session(request: SessionCreateRequest):
    """Create a new persistent session"""
    session = await session_manager.create_session(
        name=request.name,
        description=request.description,
        shared=request.shared,
        tags=request.tags
    )
    
    response_data = {"session": session}
    
    # Send initial prompt if provided
    if request.initial_prompt:
        workspace = Path(session['workspace'])
        result = await execute_claude(
            request.initial_prompt, 
            workspace, 
            session['id'],
            continue_session=False
        )
        
        if result["success"]:
            response_data["initial_response"] = result["response"]
        else:
            response_data["error"] = result["error"]
    
    return response_data


@app.get("/sessions")
async def list_sessions(active_only: bool = True, tag: Optional[str] = None):
    """List sessions with optional filtering"""
    if tag:
        sessions = session_manager.search_sessions(tags=[tag])
    elif active_only:
        sessions = session_manager.list_active_sessions()
    else:
        sessions = list(session_manager.sessions.values())
    
    return {
        "sessions": sessions,
        "count": len(sessions)
    }


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    session = session_manager.sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    """Get full session conversation history"""
    history = await session_manager.get_session_history(session_id)
    if not history:
        raise HTTPException(status_code=404, detail="Session history not found")
    
    # Format history for easy reading
    formatted_history = []
    for entry in history:
        if entry.get('type') == 'user':
            formatted_history.append({
                "role": "user",
                "content": entry['message']['content'],
                "timestamp": entry['timestamp']
            })
        elif entry.get('type') == 'assistant':
            message = entry.get('message', {})
            content_items = message.get('content', [])
            content_text = ""
            tools_used = []
            
            for item in content_items:
                if item.get('type') == 'text':
                    content_text += item.get('text', '')
                elif item.get('type') == 'tool_use':
                    tools_used.append({
                        "tool": item.get('name'),
                        "input": item.get('input')
                    })
            
            formatted_history.append({
                "role": "assistant",
                "content": content_text,
                "tools_used": tools_used,
                "timestamp": entry['timestamp']
            })
    
    return {
        "session_id": session_id,
        "history": formatted_history,
        "message_count": len(formatted_history)
    }


@app.get("/sessions/{session_id}/summary")
async def get_session_summary(session_id: str):
    """Get session activity summary"""
    summary = await session_manager.get_session_summary(session_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Session not found")
    return summary


@app.post("/sessions/{session_id}/messages")
async def send_message(session_id: str, request: MessageRequest):
    """Send a message to an existing session"""
    session = session_manager.sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    workspace = Path(session['workspace'])
    if not workspace.exists():
        raise HTTPException(status_code=500, detail="Session workspace not found")
    
    # Add participant info if shared session
    if session['shared'] and request.participant:
        participant_exists = any(
            p['name'] == request.participant 
            for p in session['participants']
        )
        if not participant_exists:
            await session_manager.add_participant(session_id, request.participant)
    
    # Execute claude with session context
    result = await execute_claude(
        f"[{request.participant}]: {request.prompt}" if session['shared'] else request.prompt,
        workspace,
        session_id,
        continue_session=True
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    response = {
        "session_id": session_id,
        "participant": request.participant,
        "prompt": request.prompt,
        "response": result["response"],
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Notify WebSocket clients
    await notify_session_update(session_id, response)
    
    return response


@app.put("/sessions/{session_id}")
async def update_session(session_id: str, request: SessionUpdateRequest):
    """Update session metadata"""
    session = session_manager.sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if request.description is not None:
        session['description'] = request.description
    if request.tags is not None:
        session['tags'] = request.tags
    if request.shared is not None:
        session['shared'] = request.shared
    
    session_manager.save_metadata()
    return session


@app.post("/sessions/{session_id}/clone")
async def clone_session(session_id: str, new_name: str):
    """Clone a session and instruct the original to transfer knowledge"""
    try:
        # Create the new session
        new_session = await session_manager.clone_session(session_id, new_name)
        
        # Get workspace paths
        original_workspace = Path(session_manager.sessions[session_id]['workspace'])
        new_workspace = Path(new_session['workspace'])
        
        # Create a transfer instruction file in the new session
        transfer_file = new_workspace / ".session" / "awaiting_transfer.json"
        transfer_data = {
            "from_session_id": session_id,
            "to_session_id": new_session['id'],
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending"
        }
        with open(transfer_file, 'w') as f:
            json.dump(transfer_data, f, indent=2)
        
        # Tell the original Claude to fork its knowledge
        fork_prompt = f"""IMPORTANT: You need to fork your knowledge to a new session.

A new session has been created as a fork of your current session. You need to transfer your knowledge to it.

Please execute the following steps:
1. Summarize everything important from our conversation
2. Send this knowledge to the fork using this command:

```bash
curl -X POST http://localhost:8001/sessions/{new_session['id']}/receive-knowledge \\
  -H "Content-Type: application/json" \\
  -d '{{"from_session": "{session_id}", "knowledge": "<YOUR_SUMMARY_HERE>"}}'
```

Replace <YOUR_SUMMARY_HERE> with a comprehensive summary including:
- All shared facts and context
- Project state and decisions
- Important files and their purposes
- Current objectives and progress
- Any other relevant information

This will ensure your fork has all necessary context to continue the work."""
        
        # Send fork instruction to original session
        fork_result = await execute_claude(
            fork_prompt,
            original_workspace,
            session_id,
            continue_session=True
        )
        
        new_session["fork_instruction_sent"] = fork_result["success"]
        new_session["awaiting_knowledge_transfer"] = True
        
        return new_session
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


class ReceiveKnowledgeRequest(BaseModel):
    from_session: str
    knowledge: str


@app.post("/sessions/{session_id}/receive-knowledge")
async def receive_knowledge(session_id: str, request: ReceiveKnowledgeRequest):
    """Receive knowledge transfer from parent session"""
    session = session_manager.sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    workspace = Path(session['workspace'])
    
    # Check if this session is expecting a transfer
    transfer_file = workspace / ".session" / "awaiting_transfer.json"
    if transfer_file.exists():
        with open(transfer_file, 'r') as f:
            transfer_data = json.load(f)
        
        # Verify the transfer is from the expected parent
        if transfer_data["from_session_id"] != request.from_session:
            raise HTTPException(status_code=403, detail="Unexpected knowledge source")
        
        # Update transfer status
        transfer_data["status"] = "received"
        transfer_data["received_at"] = datetime.utcnow().isoformat()
        with open(transfer_file, 'w') as f:
            json.dump(transfer_data, f, indent=2)
    
    # Initialize the fork with the transferred knowledge
    init_prompt = f"""You are a fork of another Claude session. You have just received a knowledge transfer from your parent session.

---KNOWLEDGE TRANSFER FROM PARENT---
{request.knowledge}
---END TRANSFER---

Please:
1. Acknowledge receipt of this knowledge
2. Summarize what you now know
3. Register your session ID as instructed in CLAUDE.md
4. Indicate you're ready to continue the work"""
    
    # Send to Claude in this session
    result = await execute_claude(
        init_prompt,
        workspace,
        session_id,
        continue_session=False
    )
    
    if result["success"]:
        # Update session metadata
        session_manager.sessions[session_id]["knowledge_received"] = True
        session_manager.sessions[session_id]["parent_session"] = request.from_session
        session_manager.sessions[session_id]["knowledge_transfer"] = request.knowledge[:500] + "..." if len(request.knowledge) > 500 else request.knowledge
        session_manager.save_metadata()
        
        return {
            "status": "success",
            "message": "Knowledge transfer received",
            "fork_response": result["response"]
        }
    else:
        raise HTTPException(status_code=500, detail=result["error"])


@app.post("/sessions/{session_id}/archive")
async def archive_session(session_id: str):
    """Archive a session"""
    await session_manager.archive_session(session_id)
    return {"message": "Session archived", "session_id": session_id}


class RegisterClaudeSessionRequest(BaseModel):
    marker_file: str


@app.post("/sessions/{session_id}/register-claude-session")
async def register_claude_session(session_id: str, request: RegisterClaudeSessionRequest):
    """Register Claude's session ID by checking for the marker file"""
    session = session_manager.sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if marker file exists
    workspace = Path(session['workspace'])
    marker_path = workspace / request.marker_file
    
    if not marker_path.exists():
        raise HTTPException(status_code=400, detail="Marker file not found")
    
    # Find Claude's session ID from the project directory
    claude_projects_dir = Path.home() / ".claude" / "projects"
    workspace_name = str(workspace).replace("/tmp/", "/private/tmp/").replace("/", "-")
    project_dir = claude_projects_dir / workspace_name
    
    if project_dir.exists():
        # Get the most recent .jsonl file
        jsonl_files = list(project_dir.glob("*.jsonl"))
        if jsonl_files:
            newest_file = max(jsonl_files, key=lambda p: p.stat().st_mtime)
            claude_session_id = newest_file.stem
            
            # Update session with Claude session ID
            session_manager.sessions[session_id]["claude_session_id"] = claude_session_id
            session_manager.save_metadata()
            
            return {
                "status": "success",
                "message": "Claude session ID registered",
                "claude_session_id": claude_session_id,
                "api_session_id": session_id
            }
    
    raise HTTPException(status_code=500, detail="Could not find Claude session")


@app.websocket("/sessions/{session_id}/ws")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket for real-time session updates"""
    await websocket.accept()
    
    # Add to active connections
    if session_id not in active_connections:
        active_connections[session_id] = []
    active_connections[session_id].append(websocket)
    
    try:
        # Send initial session info
        session = session_manager.sessions.get(session_id)
        if session:
            await websocket.send_json({
                "type": "session_info",
                "data": session
            })
        
        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            # Echo back or handle commands
            await websocket.send_text(f"Echo: {data}")
            
    except WebSocketDisconnect:
        active_connections[session_id].remove(websocket)
        if not active_connections[session_id]:
            del active_connections[session_id]


async def notify_session_update(session_id: str, data: dict):
    """Notify all WebSocket clients of session updates"""
    if session_id in active_connections:
        for connection in active_connections[session_id]:
            try:
                await connection.send_json({
                    "type": "message",
                    "data": data
                })
            except:
                # Remove dead connections
                active_connections[session_id].remove(connection)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)