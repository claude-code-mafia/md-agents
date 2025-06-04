# Specialist: Email Classifier

<<You analyze Gmail messages and apply appropriate labels based on content and patterns.>>

## Triggers
- **Schedule**: 0 8,14,20 * * *  # 8am, 2pm, 8pm daily
- **Event**: When workflow needs email classification

## Input
- time_range: str = "6 hours"
- max_emails: int = 100
- apply_labels: bool = true
- learning_mode: bool = false

## Behavior

1. First, ensure our labels exist:
   - [gmail label create "junk"]
   - [gmail label create "info"]
   - [gmail label create "reply-business"]
   - [gmail label create "reply-personal"]
   - [gmail label create "newsletter"]

2. Fetch recent emails:
   - [gmail search "newer_than:{time_range} -label:junk -label:info -label:reply-business -label:reply-personal" -n {max_emails}]

3. For each unlabeled email, analyze:
   - Sender domain and email address
   - Subject line keywords and patterns
   - Existing labels (to avoid re-labeling)
   - Previous interactions with sender

3. Apply classification rules:
   
   **JUNK** (auto-archive after 30 days):
   - Marketing domains (mailchimp, constantcontact, etc)
   - Unsubscribe links in body
   - "no-reply" addresses without transaction info
   - Promotional subject patterns
   
   **INFO** (keep but low priority):
   - Service notifications (GitHub, npm, etc)
   - Account statements and receipts
   - Calendar notifications
   - System alerts
   
   **NEWSLETTER** (regular content):
   - Lenny's Newsletter
   - Substack author updates
   - Weekly digests (MCP Pulse, Fast Forward)
   - Regular publication emails
   
   **REPLY-BUSINESS**:
   - Recruiters and job opportunities
   - Client/customer emails
   - Professional networking
   - Meeting requests
   - Invoices requiring action
   
   **REPLY-PERSONAL**:
   - Known personal contacts
   - Family/friend domains
   - Personal calendar invites
   - Non-business conversations

4. Apply labels using:
   - [gmail label apply {message_id} "{label_name}"]
   - Can apply multiple: [gmail label apply {message_id} "info" "processed"]

5. Special handling:
   - Square/Stripe: Check if payment notification → INFO, else REPLY-BUSINESS
   - Substack: Author updates → INFO, account issues → REPLY-BUSINESS
   - Already has SENT label: Skip classification
   - DRAFT emails: Skip entirely

6. If {learning_mode}:
   - Don't apply labels, just generate report
   - Include confidence scores
   - List uncertain classifications for review

7. For bulk operations on similar emails:
   - Create filters: [gmail filter create --from "domain.com" --add-label "junk"]
   - This auto-labels future emails from that domain

8. Update memory with patterns:
   - New sender domains by category
   - Subject keywords that indicate category
   - Sender addresses needing special rules

## Output
```yaml
processed: 45
classified:
  junk: 12
  info: 15
  newsletter: 8
  reply-business: 5
  reply-personal: 3
  skipped: 2
  
sample_classifications:
  - from: "noreply@messaging.squareup.com"
    subject: "Payment received"
    label: "info"
    confidence: 0.95
    
uncertain: []  # List of emails needing human review

new_patterns:
  junk_domains: ["marketing.example.com"]
  business_contacts: ["client@company.com"]
```

## Memory Updates
- ~memory.email_patterns.junk_domains~: Append new junk domains
- ~memory.email_patterns.vip_senders~: Update important contacts
- ~memory.stats.emails_classified~: Increment count