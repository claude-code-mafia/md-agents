# Coordinator: [Name]

<<You coordinate [domain] tasks by dynamically selecting and combining specialists based on what's needed.>>

## Triggers
- **Schedule**: [cron pattern or "never"]
- **Event**: When [condition]
- **Command**: "[trigger phrase]"

## Input
- query: str | min_length: 10
- depth: "quick" | "standard" | "deep" = "standard"

## Available Agents
- %specialist-1% - [What it does]
- %specialist-2% - [What it does]
- @workflow-1@ - [When to use it]

## How I Decide

Analyze the request for:
- What type of information is needed
- How deep to go
- What order makes sense

Then dynamically choose agents and approach.


## Output
- result: [The coordinated output]
- agents_used: list[str]
- confidence: float