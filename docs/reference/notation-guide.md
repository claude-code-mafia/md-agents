# Agent Notation Guide

Essential symbols for the agent system.

## Core Symbols

| Symbol | Purpose | Example |
|--------|---------|---------|
| `[tool]` | External tools | `[gmail-cli]`, `[weather-api]` |
| `%agent%` | Agent reference | `%email-scanner%`, `%researcher%` |
| `%workflow%` | Workflow reference | `%daily-briefing%` |
| `{variable}` | Dynamic values | `{input.query}`, `{result}` |
| `~memory~` | State/memory | `~memory.last_run~` |
| `<<prompt>>` | System prompt | `<<You are a researcher>>` |
| `::Type::` | Type reference | `::EmailMessage::` |


That's it.