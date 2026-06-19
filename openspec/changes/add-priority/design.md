## Context

The CLI stores tasks in `tasks.json` as a flat JSON array. Tasks currently have
`id`, `title`, `status`, and `created_at`. The `list` command prints them in
insertion order.

## Goals / Non-Goals

**Goals:**
- Allow users to flag urgency at creation time via `--priority`
- Surface high-priority tasks at the top of `list` output
- Graceful backward-compatibility: existing tasks without a priority field work

**Non-Goals:**
- Editing priority after creation (a separate future change)
- Filtering the list by priority
- Priority on `complete` or `delete` commands

## Decisions

- **Accepted values**: `low`, `medium`, `high` only. Invalid values error
  immediately via argparse `choices`.
- **Default**: `medium`. Matches the neutral baseline users expect.
- **Storage**: persisted as a `"priority"` string field on the task object.
- **Sort order**: `high` → `medium` → `low`. Within the same priority bucket
  tasks are shown in insertion order (stable sort).
- **Legacy tasks**: tasks missing `"priority"` are treated as `"medium"` by
  `cmd_list`. No migration of existing data is performed.
- **Display**: the priority label is shown in `list` output:
  `[!] 3. Send email (high)` — the `[!]` marker is used for high-priority
  tasks; medium and low show the regular `[ ]` / `[x]` marker only.

## Risks / Trade-offs

- Existing `tasks.json` files have no priority → handled by defaulting to
  `medium` at read time, so `list` still works on old data.
- `high`/`medium`/`low` strings in JSON are human-readable but not strongly
  typed → acceptable for a single-user CLI tool.
