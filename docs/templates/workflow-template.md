# Workflow: [Name]

This workflow [what it does] by executing [key steps].

## Triggers
- **Schedule**: [cron pattern or "never"]
- **Command**: "[trigger phrase]"

## Input
- param1: type
- param2: type? = default

## Steps

### Step 1: [Name]
- **Execute**: %agent-name%
- **With**: param1 from input
- **Get**: {result1}

### Step 2: [Name]
- **Execute**: %another-agent%
- **With**: {result1} from step 1
- **Get**: {result2}

### Step 3: [Name]
- **Execute**: %final-agent%
- **With**: both {result1} and {result2}
- **Save**: output/[name]-{timestamp}.md

## Success
- [ ] All steps complete
- [ ] Output saved

## If Things Go Wrong
- Step 1 fails: [what to do]
- Step 2 fails: [what to do]
- Step 3 fails: [what to do]