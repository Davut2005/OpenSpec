## Context

The CLI currently supports add, list, complete, and delete commands. Delete removes tasks permanently by ID with no confirmation. Tasks are stored in `tasks.json`. An `archive.json` file constant exists but is unused.

## Goals / Non-Goals

**Goals:**
- Safe deletion with confirmation prompt
- Bulk delete via space-separated IDs
- Soft-delete to archive.json for recoverability
- Backward-compatible CLI interface

**Non-Goals:**
- Undo/restore from archive (future enhancement)
- Interactive multi-select deletion
- Scheduled/auto-archive

## Decisions

- **Confirmation**: Prompt `y/n` before deletion; `--force` flag skips prompt. Standard UX pattern for destructive operations.
- **Soft-delete**: Move tasks to archive.json with a `deleted_at` timestamp and ghost ID preserved, rather than permanent removal. Enables recovery without complexity.
- **Bulk delete**: Accept multiple IDs via `delete <id1> <id2> ...` (varargs) instead of requiring multiple invocations. Idiomatic for CLI tools.
- **Archive format**: archive.json uses same schema as tasks.json with added `deleted_at` field. Simple, no migration needed.

## Risks / Trade-offs

- Soft-delete grows disk usage over time → Mitigation: archive.json is append-only, size is negligible for typical usage
- Confirmation breaks scripting → Mitigation: `--force` flag restores non-interactive behavior
- Bulk delete with mixed valid/invalid IDs → Mitigation: process all IDs, report which succeeded and which failed
