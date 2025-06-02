# Schedule

Simple time-to-workflow mappings. The orchestrator decides if workflows actually run based on conditions.

## Daily Workflows

```
09:00 → morning-report
10:00 → x-poster
18:00 → evening-summary
23:00 → daily-cleanup
```

## Hourly Checks

```
*:00 → health-check
```

## Weekly Tasks

```
MON 09:00 → weekly-summary
FRI 17:00 → week-wrap-up
```

## How It Works

1. Orchestrator reads this schedule
2. Checks if current time matches any entry
3. Evaluates conditions for matched workflows
4. Runs approved workflows only

## Time Matching Rules

- Daily times: Match hour (with 10-minute window)
- Hourly (*:00): Match any hour at :00
- Weekly: Match day + hour

## Notes

- All times are in system local timezone
- This is just a mapping - orchestrator handles all logic
- No workflow automatically runs just because time matches