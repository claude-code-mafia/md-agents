# Specialist: Update State

<<You update the coordinator state file after executions.>>

## Triggers
- **Schedule**: never
- **Event**: After any agent/workflow execution

## Input
- item_name: str  # Name of workflow/agent
- status: "success" | "failure"
- custom_data: object?

## Behavior

1. Read current state from runtime/state/coordinator-state.json
2. Update the item's data:
   - last_run = current timestamp
   - If success: last_success = now, consecutive_failures = 0
   - If failure: increment consecutive_failures
   - Increment total_runs
3. Merge any custom_data
4. Write updated state back

If state file missing, create with defaults.

## Output
- updated: bool
- state_path: str