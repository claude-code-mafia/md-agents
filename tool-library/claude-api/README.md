# Claude API Server

A simple HTTP API server that exposes Claude Code functionality via REST endpoints.

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the server
```bash
python claude_api.py
```

The server will start on `http://localhost:8000`

### 3. Test the API
```bash
# Run automated tests
python test_client.py

# Or interactive mode
python test_client.py interactive
```

## API Endpoints

### Create Session
```bash
POST /sessions
{
  "initial_prompt": "Hello Claude!",
  "session_name": "My Project"
}
```

### Send Message
```bash
POST /sessions/{session_id}/messages
{
  "prompt": "Create a Python function"
}
```

### List Sessions
```bash
GET /sessions
```

### Get Session Info
```bash
GET /sessions/{session_id}
```

### Delete Session
```bash
DELETE /sessions/{session_id}
```

## Example Usage

```python
import requests

# Create a session
response = requests.post("http://localhost:8000/sessions", json={
    "initial_prompt": "Let's work on a Python project"
})
session_id = response.json()["session"]["id"]

# Send messages
response = requests.post(
    f"http://localhost:8000/sessions/{session_id}/messages",
    json={"prompt": "Create a Flask hello world app"}
)
print(response.json()["response"])
```

## Using with curl

```bash
# Create session
curl -X POST http://localhost:8000/sessions \
  -H "Content-Type: application/json" \
  -d '{"initial_prompt": "Hello Claude"}'

# Send message (replace SESSION_ID)
curl -X POST http://localhost:8000/sessions/SESSION_ID/messages \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What can you help me with?"}'
```

## Architecture

- Each session gets its own workspace directory in `/tmp/claude-workspaces/`
- Sessions maintain conversation context using Claude's `--continue` flag
- The API server manages session lifecycle and workspace isolation

## Next Steps

- Add authentication/API keys
- Add rate limiting
- Add WebSocket support for streaming responses
- Add file upload/download for session workspaces
- Deploy with Docker for production use