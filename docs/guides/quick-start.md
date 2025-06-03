# Quick Start Guide

Build your first agent in 5 minutes.

## 1. Create a Specialist

Create `agents/specialists/hello-agent.md`:

```markdown
# Specialist: Hello Agent

<<You greet users and make them feel welcome.>>

## Triggers
- **Schedule**: never
- **Event**: When user says hello

## Input
- name: str = "friend"
- language: str = "english"

## Behavior

1. Greet the user by name
2. Add a welcoming message
3. Suggest what they could do next

## Output
- greeting: str
- suggestions: list[str]
```

## 2. Create a Workflow

Create `agents/workflows/morning-routine.md`:

```markdown
# Workflow: Morning Routine

This workflow runs your morning agents.

## Triggers
- **Schedule**: 0 8 * * *  # 8am daily
- **Command**: "morning routine"

## Steps

### Step 1: Greet
- **Execute**: %hello-agent%
- **With**: name = ~global.user_name~
- **Get**: {greeting}

### Step 2: Check Email
- **Execute**: %email-scanner%
- **Get**: {emails}

### Step 3: Summarize
- **Execute**: %summary-writer%
- **With**: sources = [{greeting}, {emails}]
- **Save**: output/morning-{timestamp}.md
```

## 3. Run Your Agents

```bash
# Execute the workflow
./scripts/run-agents.sh "morning routine"

# Or run a single agent
./scripts/run-agents.sh hello-agent
```

## Next Steps

- Add more agents to `/agents/specialists/`
- Create workflows in `/agents/workflows/`
- Add coordinators for dynamic behavior
- Set up schedules in `/runtime/schedule.md`

That's it! You've created a working agent system.