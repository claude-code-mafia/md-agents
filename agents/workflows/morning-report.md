# Morning Report Workflow

Checks emails and generates a summary of important items.

## Purpose
Provide a daily morning briefing of emails requiring attention.

## Instructions

1. Use Gmail CLI to list recent emails:
   ```
   ~/Projects/tool-library/gmail-tool/gmail_cli.py list -q "is:unread OR in:inbox after:yesterday"
   ```

2. Categorize emails by:
   - **Urgent**: Requiring immediate response
   - **Important**: Need attention today
   - **FYI**: Informational only

3. Extract key information:
   - Sender
   - Subject
   - Brief summary of content
   - Required action

4. Format as morning briefing

## Output
Save to: `output/morning-report-YYYY-MM-DD_HH-MM.md`

## Success Criteria
- Successfully retrieved emails
- Generated categorized summary
- Saved output file