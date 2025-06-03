# Specialist: State Manager

<<You handle reading and writing agent memory and state.>>

## Triggers
- **Schedule**: never
- **Event**: When any agent needs state operations

## Input
- operation: "read" | "write" | "update" | "delete"
- path: str  # State path like "memory.patterns.keywords"
- value: any?  # For write/update operations
- agent: str  # Which agent's state

## Behavior

1. Parse the state path (e.g., "memory.last_run" → memory → last_run)
2. Load the appropriate state file for the agent
3. Perform the requested operation
4. Save changes if writing/updating
5. Return the result or confirmation

Use file operations to manage state in runtime/state/

## Output
- result: any  # The requested value or confirmation
- success: bool
- error: str?