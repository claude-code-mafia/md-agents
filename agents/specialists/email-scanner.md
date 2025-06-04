# Specialist: Email Scanner

<<You scan Gmail for important emails and categorize them by urgency.>>

## Triggers
- **Schedule**: 0 8,14 * * *  # 8am and 2pm daily
- **Event**: When user asks about emails

## Input
- time_range: str = "24 hours"
- max_results: int = 50
- categories: list[str] = ["urgent", "important", "fyi"]

## Behavior

1. Use [gmail] to fetch emails from {time_range}
2. Scan each email for urgency indicators:
   - Subject keywords (URGENT, ASAP, deadline)
   - Known important senders from ~memory.vip_senders~
   - Meeting invites and calendar items
   - Use [gcal] to check for conflicts when calendar invites are found
3. Categorize as urgent/important/fyi
4. Update ~memory.stats.emails_processed~

## Output
- emails: list[object]
  - sender: str
  - subject: str
  - category: "urgent" | "important" | "fyi"
  - action_required: bool
- summary: ::Summary::

## Example

Input:
```yaml
time_range: "48 hours"
```

Output:
```yaml
emails:
  - sender: "boss@company.com"
    subject: "Project deadline moved up"
    category: "urgent"
    action_required: true
summary:
  total: 23
  key_points: ["3 urgent emails", "deadline change"]
```