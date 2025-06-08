#!/usr/bin/env python3
"""
Enhanced Session Manager for Claude API
Handles persistent, shareable sessions with full history
"""
import json
import os
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import uuid
import shutil

class ClaudeSessionManager:
    def __init__(self):
        self.sessions_dir = Path("/tmp/claude-sessions")
        self.sessions_dir.mkdir(exist_ok=True)
        self.metadata_file = self.sessions_dir / "sessions.json"
        self.load_metadata()
    
    def load_metadata(self):
        """Load session metadata from disk"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.sessions = json.load(f)
        else:
            self.sessions = {}
    
    def save_metadata(self):
        """Save session metadata to disk"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)
    
    async def create_session(self, name: str, description: str = "", 
                           shared: bool = False, tags: List[str] = None) -> Dict:
        """Create a new persistent session"""
        session_id = str(uuid.uuid4())
        workspace = self.sessions_dir / session_id
        workspace.mkdir(exist_ok=True)
        
        # Create session metadata
        session_info = {
            "id": session_id,
            "name": name,
            "description": description,
            "created_at": datetime.utcnow().isoformat(),
            "last_accessed": datetime.utcnow().isoformat(),
            "shared": shared,
            "tags": tags or [],
            "workspace": str(workspace),
            "participants": [],
            "claude_session_id": None,  # Will be populated after first Claude interaction
            "message_count": 0,
            "tool_usage": {},
            "status": "active"
        }
        
        self.sessions[session_id] = session_info
        self.save_metadata()
        
        # Create CLAUDE.md with session context
        await self.create_session_context(workspace, session_info)
        
        return session_info
    
    async def create_session_context(self, workspace: Path, session_info: Dict):
        """Create a rich CLAUDE.md with session context"""
        claude_md = f"""# Session: {session_info['name']}

## Session Information
- **ID**: {session_info['id']}
- **Created**: {session_info['created_at']}
- **Description**: {session_info['description']}
- **Tags**: {', '.join(session_info['tags'])}
- **Shared**: {'Yes' if session_info['shared'] else 'No'}

## CRITICAL: Register Your Session ID

As your FIRST action, please execute these commands to enable conversation memory:
```bash
# Create a marker file with your Claude session ID
echo "CLAUDE_SESSION_REGISTERED" > .session/registration_marker.txt

# Send your session ID to the API
curl -X POST http://localhost:8001/sessions/{session_info['id']}/register-claude-session \\
  -H "Content-Type: application/json" \\
  -d '{{"marker_file": ".session/registration_marker.txt"}}'
```

This step is ESSENTIAL for conversation memory to work across API calls.

## Session Guidelines
You are participating in a persistent session that may involve multiple participants over time.
- Maintain context across all interactions
- Reference previous decisions and discussions
- Keep track of action items and progress
- Update session state when significant changes occur

## Available Tools
All standard tools are available, plus:
- `session-update` - Update session metadata
- `session-note` - Add notes to session history
- `session-invite` - Invite participants (if shared)

## Session State
You can store and retrieve session state:
```bash
# Store state
echo '{{"key": "value"}}' > .session/state.json

# Retrieve state  
cat .session/state.json
```

## Collaboration
When multiple participants are involved:
- Summarize recent changes when a new participant joins
- Maintain a decision log in .session/decisions.md
- Track action items in .session/todos.md
"""
        
        (workspace / "CLAUDE.md").write_text(claude_md)
        
        # Create session subdirectories
        (workspace / ".session").mkdir(exist_ok=True)
        (workspace / ".session" / "state.json").write_text("{}")
        (workspace / ".session" / "decisions.md").write_text(f"# Decisions Log - {session_info['name']}\n\n")
        (workspace / ".session" / "todos.md").write_text(f"# Action Items - {session_info['name']}\n\n")
    
    async def get_session_history(self, session_id: str) -> List[Dict]:
        """Get full conversation history from Claude's storage"""
        session = self.sessions.get(session_id)
        if not session:
            return []
        
        # Find Claude's session file
        claude_projects_dir = Path.home() / ".claude" / "projects"
        session_workspace = session['workspace'].replace("/tmp/", "/private/tmp/")
        escaped_workspace = session_workspace.replace("/", "-")
        
        project_dir = claude_projects_dir / escaped_workspace
        if not project_dir.exists():
            return []
        
        # Read all JSONL files
        history = []
        for jsonl_file in project_dir.glob("*.jsonl"):
            with open(jsonl_file, 'r') as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        history.append(entry)
        
        # Sort by timestamp
        history.sort(key=lambda x: x.get('timestamp', ''))
        return history
    
    async def add_participant(self, session_id: str, participant: str, role: str = "contributor"):
        """Add a participant to a shared session"""
        if session_id in self.sessions:
            self.sessions[session_id]["participants"].append({
                "name": participant,
                "role": role,
                "joined_at": datetime.utcnow().isoformat()
            })
            self.save_metadata()
    
    async def get_session_summary(self, session_id: str) -> Dict:
        """Get a summary of session activity"""
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        history = await self.get_session_history(session_id)
        
        # Analyze history
        message_count = len([h for h in history if h.get('type') == 'user'])
        tool_uses = {}
        
        for entry in history:
            if entry.get('type') == 'assistant':
                message = entry.get('message', {})
                content = message.get('content', [])
                for item in content:
                    if item.get('type') == 'tool_use':
                        tool_name = item.get('name', 'unknown')
                        tool_uses[tool_name] = tool_uses.get(tool_name, 0) + 1
        
        # Read session state
        state_file = Path(session['workspace']) / ".session" / "state.json"
        state = {}
        if state_file.exists():
            with open(state_file, 'r') as f:
                state = json.load(f)
        
        return {
            "session": session,
            "message_count": message_count,
            "tool_usage": tool_uses,
            "state": state,
            "last_activity": history[-1].get('timestamp') if history else None
        }
    
    async def clone_session(self, session_id: str, new_name: str) -> Dict:
        """Clone an existing session with its full state"""
        original = self.sessions.get(session_id)
        if not original:
            raise ValueError("Session not found")
        
        # Create new session
        new_session = await self.create_session(
            name=new_name,
            description=f"Cloned from {original['name']}",
            shared=original['shared'],
            tags=original['tags'] + ['cloned']
        )
        
        # Preserve the Claude session ID so the fork can continue the conversation
        if original.get('claude_session_id'):
            new_session['claude_session_id'] = original['claude_session_id']
            self.sessions[new_session['id']] = new_session
            self.save_metadata()
        
        # Copy workspace contents
        original_workspace = Path(original['workspace'])
        new_workspace = Path(new_session['workspace'])
        
        for item in original_workspace.iterdir():
            if item.is_file():
                shutil.copy2(item, new_workspace / item.name)
            elif item.is_dir() and item.name != '.claude':
                shutil.copytree(item, new_workspace / item.name, dirs_exist_ok=True)
        
        return new_session
    
    async def archive_session(self, session_id: str):
        """Archive a session (mark as inactive but preserve)"""
        if session_id in self.sessions:
            self.sessions[session_id]["status"] = "archived"
            self.sessions[session_id]["archived_at"] = datetime.utcnow().isoformat()
            self.save_metadata()
    
    def list_active_sessions(self) -> List[Dict]:
        """List all active sessions"""
        return [s for s in self.sessions.values() if s['status'] == 'active']
    
    def search_sessions(self, query: str = None, tags: List[str] = None) -> List[Dict]:
        """Search sessions by name, description, or tags"""
        results = []
        for session in self.sessions.values():
            if query and query.lower() in (session['name'] + ' ' + session['description']).lower():
                results.append(session)
            elif tags and any(tag in session['tags'] for tag in tags):
                results.append(session)
        return results


# Example usage
if __name__ == "__main__":
    async def demo():
        manager = ClaudeSessionManager()
        
        # Create a project session
        project = await manager.create_session(
            name="NextJS Dashboard Project",
            description="Building a real-time analytics dashboard",
            shared=True,
            tags=["development", "nextjs", "dashboard"]
        )
        print(f"Created session: {project['id']}")
        
        # Add team members
        await manager.add_participant(project['id'], "Alice", "lead")
        await manager.add_participant(project['id'], "Bob", "contributor")
        
        # Get summary
        summary = await manager.get_session_summary(project['id'])
        print(f"Session summary: {json.dumps(summary, indent=2)}")
    
    asyncio.run(demo())