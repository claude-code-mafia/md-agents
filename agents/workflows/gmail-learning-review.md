# Workflow: Gmail Learning Review

This workflow generates a daily report showing how the system would handle your emails.

## Triggers
- **Schedule**: 0 21 * * *  # 9pm daily during learning phase
- **Command**: "gmail learning report"

## Input
- days_back: int = 1
- include_examples: bool = true
- max_examples: int = 5

## Steps

### Step 1: Gather Classification Data
- **Execute**: %email-classifier%
- **With**:
  - time_range = "{days_back} days"
  - learning_mode = true
  - apply_labels = false
- **Get**: {classifications}

### Step 2: Analyze Patterns
- **Execute**: [gmail-advanced analyze --days {days_back}]
- **Get**: {email_analysis}

### Step 3: Compare with Existing Labels
- **Execute**: [gmail list -n 100]
- **Process**: Compare system classifications with any existing labels
- **Get**: {accuracy_check}

### Step 4: Generate Learning Report
Create report with sections:

1. **Summary Stats**
   - Total emails analyzed
   - Classification breakdown
   - Confidence scores

2. **Classification Examples**
   - Show {max_examples} from each category
   - Include: From, Subject, Proposed Label, Confidence
   - Highlight uncertain ones

3. **Pattern Recognition**
   - New domains discovered
   - Sender frequency patterns
   - Subject line patterns by category

4. **Recommendations**
   - Suggested new rules
   - Low-confidence patterns needing confirmation
   - Ready to move to active labeling?

5. **Next Steps**
   - Review uncertain classifications
   - Confirm or correct examples
   - Adjust rules if needed

### Step 5: Save Report
- **Save**: output/gmail-learning-{date}.md
- **Also**: Store key metrics in ~memory.gmail.learning_history~

## Output Example
```markdown
# Gmail Learning Report - June 3, 2025

## Summary
Analyzed 156 emails from the last 24 hours.

### Proposed Classifications:
- **Junk**: 67 (43%) - Marketing, newsletters, promotions
- **Info**: 52 (33%) - Notifications, confirmations, statements  
- **Reply-Business**: 28 (18%) - Work emails, recruiters, clients
- **Reply-Personal**: 9 (6%) - Friends, family

### Confidence: 87% average

## Examples Need Review:

1. **From**: jason@realpeoplereallife.org  
   **Subject**: Re: Meeting notes  
   **Proposed**: reply-business (65% confidence)  
   **Note**: Unclear if business or personal relationship

2. **From**: noreply@messaging.squareup.com  
   **Subject**: Important account update  
   **Proposed**: info (72% confidence)  
   **Note**: "Important" might indicate action needed

## Patterns Discovered:
- Square/Stripe emails: Mix of info (payments) and action needed (disputes)
- Substack: High volume, mostly info but some account-related
- Personal domain @peteknowsai.xyz receives business email

## Recommendation:
System is 87% confident. Consider:
1. Moving to active labeling for high-confidence categories (>90%)
2. Manual review for Square/Stripe payment vs action emails
3. Add @realpeoplereallife.org to personal contacts if appropriate

Ready to enable active labeling? Current accuracy suggests waiting 2-3 more days.
```

## Success Metrics
- [ ] Clear classification examples
- [ ] Identified edge cases
- [ ] Actionable recommendations
- [ ] Confidence trajectory tracked