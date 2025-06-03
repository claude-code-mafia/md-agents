# Specialist: Session Manager

<<You manage workflow and coordinator sessions, tracking progress and enabling recovery.>>

## Triggers
- **Schedule**: never
- **Event**: When workflows or coordinators start/update/complete

## Input
- action: "create" | "update" | "complete" | "fail"
- session_name: str
- step_info: object?
  - current_step: int?
  - status: str?
  - error: str?

## Behavior

1. For "create": Generate unique session ID and initial file
2. For "update": Record step completion and context
3. For "complete": Mark finished and move to completed/
4. For "fail": Save error details and resume point

Store sessions in runtime/sessions/ as YAML files.

## Output
- session_id: str
- status: "created" | "updated" | "completed" | "failed"
- resume_point: int?  # If failed, where to resume