## Why

The task manager has no way to express urgency. All tasks are treated equally
in the `list` output, making it hard to focus on what matters most.

## What Changes

- Add an optional `--priority` flag to `add` that accepts `low`, `medium`, or
  `high` (default `medium`)
- Store the priority as a `"priority"` field on each task in `tasks.json`
- Modify `list` to show high-priority tasks first, then medium, then low
- Tasks created before this change (missing the `priority` field) are treated
  as `medium` at display time

## Capabilities

### New Capabilities
- `task-priority`: Covers the `--priority` flag on `add` and priority-sorted
  `list` output

### Modified Capabilities
- `task-list`: List output now sorted by priority (was insertion order)

## Impact

- `cli.py`: Modify `cmd_add` (store priority) and `cmd_list` (sort + display)
- `tasks.json`: New optional field `priority` on each task entry
- No new files; no external dependencies
