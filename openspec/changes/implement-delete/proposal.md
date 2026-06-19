## Why

The current delete command is basic — it deletes a single task by ID with no confirmation, no bulk support, and no recovery option. This makes accidental data loss easy and limits the CLI's usability for power users managing many tasks.

## What Changes

- Add confirmation prompt before deleting tasks (skip with `--force`)
- Support deleting multiple tasks in one command via space-separated IDs
- Soft-delete tasks by moving them to archive.json instead of permanent removal
- Add `deleted` status to tasks before archiving

## Capabilities

### New Capabilities
- `task-deletion`: Covers task deletion workflow including confirmation, bulk delete, and soft-delete with archiving

### Modified Capabilities
<!-- No existing specs to modify -->

## Impact

- `cli.py`: Modify `cmd_delete` and related argument parsing
- `archive.json`: New data file for soft-deleted tasks
- No external dependencies or API changes
