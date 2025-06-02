# Quick Start: Build Your First Agent in 5 Minutes

Let's create a working agent system from scratch!

## 1. Create a Simple Agent (2 minutes)

Create file: `agents/specialists/joke-teller.md`

```markdown
# Agent: Joke Teller

I am a specialist agent that tells programming jokes to brighten your day.

## What I Do

I keep a collection of programming jokes and share ones that match your mood or topic. Think of me as the team member who lightens the mood during long coding sessions.

## What I Need

To do my job, I need:
- A topic or programming language (optional)
- Your current mood (optional)
- How many jokes you want (default: 1)

## How I Work

1. First, I consider what kind of joke would work best
2. Then, I select from my collection or create a new one
3. Finally, I deliver it with good timing

## What I Produce

After I'm done, you'll have:
- A programming joke to share
- A moment of levity
- Maybe a groan (dad jokes are still jokes!)

## Example

Here's what it looks like when I work:

**Input**: "Tell me a Python joke"

**What I Do**: I think about Python's characteristics and select a relevant joke.

**Output**: 
"Why do Python developers wear glasses?
Because they can't C! 👓"
```

## 2. Create a Workflow (2 minutes)

Create file: `agents/workflows/mood-booster.md`

```markdown
# Workflow: Mood Booster

This workflow brightens your day with a joke and a fun fact.

## When to Run

Run this workflow when:
- You need a break
- Before starting a difficult task
- Daily at 3 PM (afternoon slump)

## The Team

This workflow uses these specialist agents:
- **Joke Teller**: Shares a programming joke
- **Fun Fact Finder**: Finds an interesting tech fact

## The Process

### Step 1: Tell a Joke
- **Who**: Joke Teller
- **What**: Share a programming joke
- **Produces**: `context/joke.md`

### Step 2: Find Fun Fact
- **Who**: Fun Fact Finder  
- **What**: Find interesting tech trivia
- **Produces**: `context/fun-fact.md`

### Step 3: Combine
- **Who**: Summary Writer
- **What**: Create a "brightness break" message
- **Produces**: `output/mood-boost-YYYY-MM-DD.md`

## Success Looks Like

The workflow succeeded when:
- [ ] You smiled or groaned at the joke
- [ ] You learned something interesting
- [ ] You feel ready to tackle the next task
```

## 3. Run Your Workflow (1 minute)

### Using the Orchestrator

The orchestrator reads and executes workflows:

```bash
# In your terminal
cd agents
Execute workflow: mood-booster
```

### What Happens

1. **Session Created**: `mood-booster-2025-06-03-1500`
2. **Joke Teller Runs**: Saves joke to context/
3. **Fun Fact Finder Runs**: Saves fact to context/
4. **Summary Writer Runs**: Combines into final output
5. **Success!**: Your mood boost is ready

### Sample Output

```markdown
# Mood Boost - June 3, 2025

## 😄 Programming Joke

Why do programmers prefer dark mode?
Because light attracts bugs! 🐛

## 🤓 Fun Tech Fact

Did you know? The first computer bug was an actual bug - a moth
trapped in Harvard's Mark II computer in 1947. Grace Hopper's
team taped it in their log book with the note "First actual case
of bug being found."

---
Time for your brightness break! Take a deep breath and tackle
that next challenge. You've got this! 💪
```

## 4. Extend Your System

### Add Another Agent

Create `agents/specialists/motivator.md`:
```markdown
# Agent: Motivator

I am a specialist agent that provides coding motivation.

## What I Do
I share encouraging messages and remind you why you love coding.
[...]
```

### Update Your Workflow

Add to `mood-booster.md`:
```markdown
### Step 4: Add Motivation
- **Who**: Motivator
- **What**: Share an encouraging message
- **Produces**: `context/motivation.md`
```

## 5. Advanced Features

### Parallel Execution
Run agents simultaneously:
```markdown
### Parallel Group: Brightness Crew
Run these at the same time:
- Joke Teller
- Fun Fact Finder
- Motivator
```

### Error Handling
Make it resilient:
```markdown
### Step 1: Tell a Joke
- **Error Handling**: 
  - If no jokes available: Use default joke
  - Always continue to next step
```

## Tips for Success

1. **Start Simple**: One agent, one job
2. **Use Examples**: Show what success looks like
3. **Natural Language**: Write like you're explaining to a friend
4. **Test Often**: Run workflows as you build
5. **Have Fun**: The system should be enjoyable to use

## Next Steps

- Explore existing agents in `specialists/`
- Check out complex workflows in `workflows/`
- Read the best practices guide
- Build something useful for your daily work

## Common Patterns

### Information Gatherer
```markdown
I gather [type] information from [source].
```

### Analyzer
```markdown
I analyze [input] and identify [insights].
```

### Creator
```markdown
I create [output] based on [inputs].
```

### Coordinator
```markdown
I coordinate [agents] to accomplish [goal].
```

## You're Ready!

You now have:
- ✅ A working agent (Joke Teller)
- ✅ A workflow that uses it
- ✅ Understanding of the system
- ✅ Ideas for expansion

Build something amazing with natural language agents! 🚀