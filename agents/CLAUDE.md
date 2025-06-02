# Agent Runtime Instructions

You are executing agents, not developing them.

## Primary Task
Execute the workflow defined in orchestrator.md

## Execution Rules
- Follow agent specifications exactly as written
- Save all outputs to output/YYYY-MM-DD_HH-MM.md
- Log errors but continue with remaining agents
- No user confirmations during execution
- Use tools as specified in agent markdown files

## Output Format
- Use clear headings for each agent's results
- Include timestamp at the top and bottom
- Summarize successes and failures at the end
- Keep output concise but informative

## Error Handling
- If an agent fails, log the error with details
- Continue executing remaining agents
- Include all errors in the final summary
- Never stop execution due to a single failure