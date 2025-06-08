# Agentic Forking - How It Works

## Overview

Agentic forking solves the session persistence limitation by having Claude actively transfer knowledge to its forks, similar to biological cell division.

## The Process

### 1. Fork Request
When you request a fork:
```bash
POST /sessions/{session_id}/clone?new_name=NewFork
```

### 2. Parent Receives Instructions
The parent Claude gets a message:
- "You need to fork your knowledge to session X"
- "Summarize everything important"
- "Execute this curl command to transfer"

### 3. Parent Creates Summary
Claude intelligently summarizes:
- Key facts and context
- Project state
- Decisions made
- Files created
- Current objectives

### 4. Active Transfer
Parent Claude executes:
```bash
curl -X POST http://localhost:8001/sessions/{fork_id}/receive-knowledge \
  -d '{"from_session": "parent_id", "knowledge": "summary..."}'
```

### 5. Fork Initialization
The fork receives the knowledge and:
- Acknowledges receipt
- Summarizes what it knows
- Registers its session
- Indicates readiness to continue

## Benefits

### vs. Mechanical Session Copying
- **Intelligent**: Only transfers what's important
- **Contextual**: Can tailor knowledge for fork's purpose
- **Explicit**: Clear record of what was transferred
- **Flexible**: Fork can immediately diverge

### vs. Replay Approaches
- **Efficient**: No need to replay entire conversation
- **Semantic**: Transfers understanding, not just text
- **Adaptive**: Parent can decide what's relevant

## Example Use Cases

### 1. Feature Branching
```
Main: "Working on authentication"
  └── Fork: "Experiment with OAuth instead of JWT"
```

### 2. Parallel Development
```
Main: "Building API"
  ├── Fork A: "Focus on frontend integration"
  └── Fork B: "Focus on database optimization"
```

### 3. Team Handoffs
```
Alice's Session: "Built the data model"
  └── Bob's Fork: "Implement the API endpoints"
```

## Technical Details

### Knowledge Transfer Format
The parent creates a structured summary including:
- Project details
- Current state
- Team information
- Technical decisions
- File inventory
- Next steps

### Session Metadata
Each fork tracks:
- `parent_session`: Where it came from
- `knowledge_received`: Confirmation of transfer
- `knowledge_transfer`: The actual summary (truncated)

### API Endpoints
- `POST /sessions/{id}/clone` - Initiate fork with instructions
- `POST /sessions/{id}/receive-knowledge` - Receive knowledge push

## Future Enhancements

1. **Selective Forking**: Parent could ask "What aspect should the fork focus on?"
2. **Multi-Fork Coordination**: Parent could coordinate multiple forks
3. **Knowledge Merging**: Forks could merge learnings back to parent
4. **Fork Networks**: Forks of forks with knowledge lineage
5. **Specialized Transfers**: Different knowledge for different fork purposes

## Conclusion

Agentic forking turns a technical limitation into a feature. Instead of fighting with session mechanics, we leverage Claude's intelligence to create meaningful knowledge transfer between parallel work streams.