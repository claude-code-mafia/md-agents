# Update State Utility

Updates the orchestrator state file after workflow execution.

## Purpose
Maintain accurate tracking of workflow executions in orchestrator-state.json.

## Instructions

Given inputs:
- Workflow name
- Execution status (success/failure)
- Optional: Custom data (e.g., last_post_time)

Steps:
1. Read current orchestrator-state.json
2. Update the specified workflow's data:
   - Set last_run to current timestamp
   - If success: 
     - Set last_success to current timestamp
     - Reset consecutive_failures to 0
     - Increment total_successes
   - If failure:
     - Increment consecutive_failures
   - Always increment total_runs
3. Update metadata.last_updated
4. Write updated state back to file

## Error Handling
- If state file doesn't exist, create it with default structure
- If JSON is corrupted, log error and create fresh file
- Always preserve data for other workflows