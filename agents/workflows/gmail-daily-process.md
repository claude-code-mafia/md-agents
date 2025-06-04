# Workflow: Gmail Daily Process

This workflow processes your emails systematically, applying labels and creating drafts.

## Triggers
- **Schedule**: 0 8,14,20 * * *  # Three times daily
- **Command**: "process gmail"

## Input
- mode: "learning" | "active" = "active"  # Active mode - apply labels
- hours_back: int = 6
- create_drafts: bool = true  # Create drafts immediately

## Steps

### Step 0: Get Current Timestamp
- **Execute**: [current-time]
- **Purpose**: Get timestamp for file naming
- **Get**: {timestamp}

### Step 1: Analyze Recent Activity
- **Execute**: [gmail analyze --days 1 --json]
- **Purpose**: Get overview of email volume and patterns
- **Get**: {email_stats}
- **Parse**: Extract sender domains, label distribution

### Step 2: Classify Emails
- **Execute**: %email-classifier%
- **With**: 
  - time_range = "{hours_back} hours"
  - learning_mode = ({mode} == "learning")
  - apply_labels = ({mode} == "active")
- **Get**: {classification_results}

### Step 3: Generate Classification Report (Optional)
- **If**: {mode} == "learning"
- **Execute**: %summary-writer%
- **With**:
  - sources = [{email_stats}, {classification_results}]
  - format = "report"
  - sections = ["summary", "classifications", "uncertain", "recommendations"]
- **Save**: output/gmail-learning-{timestamp}.md

### Step 3b: Apply Filters for Efficiency
- **If**: Patterns are consistent (>90% confidence)
- **Execute**: [gmail filter create] for high-confidence rules
- **Examples**:
  - [gmail filter create --from "noreply@messaging.squareup.com" --add-label "info"]
  - [gmail filter create --from "*@donorbox.org" --add-label "junk"]

### Step 4: Process Reply Candidates
- **If**: {create_drafts} == true
- **For each**: email in {classification_results.reply_needed}
  - If labeled "reply-business" or "reply-personal"
  - Execute: %draft-composer%
  - With:
    - email_id = email.id
    - reply_type = email.category
    - context = email.subject
- **Get**: {draft_results}
- **Track**: draft_ids for user review

### Step 5: Update Memory
- **Execute**: %state-manager%
- **With**:
  - updates = {
      "email_patterns": {classification_results.new_patterns},
      "last_processed": {timestamp},
      "stats": {email_stats}
    }

### Step 6: Summary Notification
- **Execute**: %summary-writer%
- **With**:
  - sources = [all previous results]
  - format = "brief"
  - max_length = 500
- **Save**: output/gmail-summary-{timestamp}.md

## Success Criteria
- [ ] All emails from time range processed
- [ ] Classification confidence > 80% average
- [ ] No critical emails missed
- [ ] Drafts created for urgent replies (if enabled)

## Error Handling
- Gmail API timeout: Retry with smaller batch
- Classification uncertainty: Flag for human review
- Draft creation fails: Log and continue

## Progression Path
1. **Week 1-2**: Learning mode - review reports daily
2. **Week 3**: Enable active labeling
3. **Week 4**: Enable draft creation for high-confidence replies
4. **Month 2**: Full automation with weekly reviews

## Memory Keys Used
- ~memory.email_patterns.junk_domains~
- ~memory.email_patterns.vip_senders~
- ~memory.gmail.last_processed~
- ~memory.gmail.classification_stats~