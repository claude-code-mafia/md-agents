# Claude Session Management - Exploration Notes

## Current Status (Committed)

### What's Working ✅
1. **Session Persistence Within Workspace** - Claude remembers context when using --resume with captured session ID
2. **Session ID Self-Registration** - Claude can report its own session ID via API callback
3. **Fork/Clone with Session Reference** - New workspaces inherit the Claude session ID
4. **Full History Tracking** - All conversations are logged and retrievable

### Current Limitation ⚠️
- `--resume SESSION_ID` seems to require the session to be in the expected directory structure
- Forked sessions can't access the conversation history even with the same session ID

## Future Exploration Paths

### 1. Session File Investigation
- Claude stores sessions in `~/.claude/projects/*/SESSION_ID.jsonl`
- Could we symlink or copy these files to make sessions portable?
- Need to understand Claude's session discovery mechanism

### 2. Directory Structure Mapping
- Sessions seem tied to specific workspace paths
- Investigate if we can trick Claude into finding sessions in different locations
- Possibly use bind mounts or symlinks

### 3. Session Proxy Approach
- Create a proxy layer that intercepts Claude's session management
- Could rewrite paths or redirect session lookups
- More complex but potentially more powerful

### 4. Hybrid Approach
- Use --resume when possible (same workspace)
- Fall back to context injection for cross-workspace scenarios
- Maintain our own session continuity layer

### 5. Claude Code Internals
- Investigate how Claude Code implements --resume
- Look for environment variables or configs that control session paths
- Check if there's an undocumented way to specify session locations

## Key Questions to Answer

1. **Session Portability**: Can Claude sessions be made portable across workspaces?
2. **Session Discovery**: How does Claude find and validate sessions for --resume?
3. **Session Format**: Can we create/modify session files directly?
4. **Alternative Flags**: Are there other CLI flags that might help with session management?

## Why This Matters

True session persistence with forking enables:
- **Long-running AI agents** that maintain context over days/weeks
- **Collaborative AI workflows** where multiple people/processes share context
- **Branching explorations** without losing the main thread
- **Audit trails** with full conversation history
- **Stateful API interactions** that feel like ongoing conversations

## Next Steps

1. Deep dive into Claude's session file format and storage
2. Experiment with symlinks and directory structures
3. Test edge cases with --resume flag
4. Consider building a session management layer if needed
5. Explore if MCP (Model Context Protocol) offers better session handling

This is foundational work for the future of AI-powered development workflows.