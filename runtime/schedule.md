# Schedule

Simple time-based triggers for agents and workflows. The coordinator decides what actually runs.

## Daily Tasks

```
08:00 → @daily-briefing@
10:00 → @x-poster@
```

## Specialist Schedules

```
*/30 → %email-scanner%
07:00 → %news-gatherer%
```

## How It Works

1. Coordinator reads this schedule
2. Checks if current time matches any entry
3. Evaluates conditions for matched items
4. Executes approved agents/workflows only

## Time Matching Rules

- Daily times: Match hour (with 10-minute window)
- Hourly (*:00): Match any hour at :00
- Weekly: Match day + hour

## Notes

- All times are in system local timezone
- This is just a mapping - coordinator handles all logic
- No workflow automatically runs just because time matches