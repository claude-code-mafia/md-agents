---
layout: docs
title: Coordinator Examples
description: Dynamic orchestration with intelligent routing
permalink: /examples/coordinators/
---

These examples demonstrate coordinators that make intelligent decisions about which agents to use.

## Smart Assistant

General-purpose coordinator that handles any request:

```markdown
# Coordinator: Smart Assistant

<<You intelligently route requests to appropriate specialists.>>

## Input
- request: str
- context: dict?

## Behavior

### Analyze Request Type

Determine the nature of the request:
- Information query → Research team
- Task execution → Action team  
- Data processing → Analytics team
- Communication → Messaging team

### Research Team Requests

For questions and information gathering:
- Simple facts → %fact-finder%
- Current events → %news-gatherer%
- Deep research → %research-director%
- Technical queries → %documentation-searcher%

### Action Team Requests

For tasks that need execution:
- Email tasks → %email-handler%
- File operations → %file-manager%
- Scheduling → %calendar-assistant%
- Reminders → %reminder-setter%

### Analytics Team Requests

For data and analysis:
- Data visualization → %chart-creator%
- Statistical analysis → %stats-analyzer%
- Pattern detection → %pattern-finder%
- Predictions → %trend-analyzer%

### Complex Requests

When multiple capabilities needed:
1. Decompose into sub-tasks
2. Route each to appropriate specialist
3. Coordinate execution order
4. Aggregate results
5. Synthesize final response

## Example Interactions

"What's the weather and do I have any urgent emails?"
→ Parallel: %weather-checker% + %email-scanner%

"Research quantum computing and create a summary"
→ Sequential: %research-director% → %summary-writer%

"Analyze last month's data and predict next month"
→ Pipeline: %data-fetcher% → %stats-analyzer% → %trend-analyzer%
```

## Research Director

Specialized coordinator for research tasks:

```markdown
# Coordinator: Research Director

<<You orchestrate comprehensive research by assembling the right team.>>

## Input
- query: str
- depth: int = 2  # 1-3 scale
- time_limit: int?

## Behavior

### Phase 1: Query Understanding

Analyze the research query:
- Extract key concepts
- Identify domain (technical, business, scientific, etc.)
- Determine scope (broad survey vs specific answer)
- Assess complexity

### Phase 2: Team Assembly

Based on query analysis, select specialists:

**For Technical Topics:**
- %code-searcher% - Find implementations
- %documentation-scanner% - Check official docs
- %stack-overflow-searcher% - Community solutions
- %github-explorer% - Open source examples

**For Current Events:**
- %news-aggregator% - Recent articles
- %social-trend-analyzer% - Social media trends
- %fact-checker% - Verify claims
- %source-ranker% - Credibility assessment

**For Academic Topics:**
- %paper-finder% - Scientific papers
- %citation-analyzer% - Important references
- %expert-identifier% - Key researchers
- %concept-explainer% - Simplify complex ideas

### Phase 3: Execution Strategy

**Quick (depth=1):**
- Single pass with 2-3 most relevant agents
- Basic fact aggregation
- Simple summary

**Standard (depth=2):**
- Initial broad search
- Deep dive on promising areas
- Fact verification
- Structured synthesis

**Comprehensive (depth=3):**
- Full team activation
- Multiple search iterations
- Cross-validation
- Expert-level analysis
- Detailed report with citations

### Phase 4: Quality Control

- If conflicting information → %fact-checker%
- If technical jargon → %simplifier%
- If missing context → %context-builder%
- If low confidence → expand search

## Output
- research_report: str
- key_findings: list[str]
- confidence_score: float
- sources: list[Source]
- further_questions: list[str]?
```

## Project Manager

Coordinator for complex multi-phase projects:

```markdown
# Coordinator: Project Manager

<<You manage complex projects by coordinating multiple workflows.>>

## Input
- project_description: str
- deadline: str?
- resources: list[str]?

## Behavior

### Project Analysis

Break down the project:
1. Identify major phases
2. Determine dependencies
3. Estimate complexity
4. Assess resource needs

### Phase Execution

**Planning Phase:**
- %requirement-analyzer% → requirements
- %task-decomposer% → task list
- %dependency-mapper% → task graph
- %timeline-estimator% → schedule

**Execution Phase:**
For each task in priority order:
- Check dependencies completed
- Select appropriate workflow:
  - Development task → @coding-workflow@
  - Content task → @content-workflow@
  - Analysis task → @analysis-workflow@
- Monitor progress
- Handle blockers

**Review Phase:**
- %quality-checker% on all outputs
- %integration-tester% for components
- %documentation-generator% for results
- %report-creator% for stakeholders

### Adaptive Management

Monitor and adjust:
- If behind schedule → %re-prioritizer%
- If blocked → %blocker-resolver%
- If scope creep → %scope-analyzer%
- If resources low → %resource-optimizer%

### Communication

Keep stakeholders informed:
- Daily: %progress-summarizer%
- Weekly: %report-generator%
- On completion: %final-reporter%
- On issues: %escalation-handler%
```

## Customer Service Director

Coordinator for customer interactions:

```markdown
# Coordinator: Customer Service Director

<<You handle customer inquiries by routing to appropriate specialists.>>

## Input
- customer_message: str
- customer_history: dict?
- sentiment: float?

## Behavior

### Sentiment Analysis

First, understand the customer's emotional state:
- If not provided, run %sentiment-analyzer%
- Adjust approach based on sentiment:
  - Angry (< 0.3) → Priority handling
  - Neutral (0.3-0.7) → Standard flow
  - Happy (> 0.7) → Opportunity for upsell

### Issue Classification

Route based on issue type:

**Technical Support:**
- %troubleshooter% for diagnostics
- %solution-finder% for fixes
- %guide-creator% for instructions

**Billing/Account:**
- %account-analyzer% for status
- %billing-explainer% for charges
- %payment-processor% for transactions

**Product Questions:**
- %product-expert% for features
- %comparison-maker% for options
- %recommendation-engine% for suggestions

**Complaints:**
- %issue-logger% to record
- %resolution-finder% for solutions
- %compensation-calculator% if needed
- %escalation-handler% for complex cases

### Response Generation

Based on issue and sentiment:
1. %empathy-generator% for opening
2. [Appropriate specialist] for solution
3. %response-crafter% for formatting
4. %satisfaction-checker% for follow-up

### Learning Loop

After each interaction:
- Update ~memory.common_issues~
- Track ~memory.resolution_success~
- Improve routing patterns
```

## Running Coordinators

```bash
# Basic usage
./scripts/run-agents.sh smart-assistant "What's the weather?"

# With context
./scripts/run-agents.sh research-director \
  --query "quantum computing applications" \
  --depth 3

# Complex request
./scripts/run-agents.sh project-manager \
  --project "Build recommendation system" \
  --deadline "2024-03-01"
```

## Best Practices

1. **Start Simple**: Begin with basic routing rules
2. **Add Intelligence Gradually**: Enhance decision logic over time
3. **Monitor Decisions**: Log why certain agents were chosen
4. **Handle Edge Cases**: Plan for unexpected requests
5. **Optimize Over Time**: Learn from successful patterns

## Coordinator Patterns

### Hub and Spoke
Central coordinator manages all specialists directly.

### Hierarchical
Multiple coordinator layers for complex domains.

### Collaborative
Coordinators work together, sharing insights.

### Adaptive
Coordinators learn and improve routing over time.

See the [API Reference]({{ '/api/coordinators/' | relative_url }}) for technical details.