## ADDED Requirements

### Requirement: Delete single task
The system SHALL delete a single task by its numeric ID.

#### Scenario: Delete existing task by ID
- **WHEN** user runs `delete 1`
- **THEN** the task with ID 1 SHALL be moved to archive.json
- **THEN** the system SHALL print "Deleted task 1."

#### Scenario: Delete non-existent task ID
- **WHEN** user runs `delete 999`
- **THEN** the system SHALL print "Task 999 not found."

#### Scenario: Delete from empty task list
- **WHEN** user runs `delete 1` with no tasks in tasks.json
- **THEN** the system SHALL print "No tasks to delete."

### Requirement: Confirmation before deletion
The system SHALL prompt for confirmation before deleting, unless `--force` is provided.

#### Scenario: Confirm deletion with y
- **WHEN** user runs `delete 1`
- **THEN** the system SHALL prompt "Delete task 1? (y/n): "
- **WHEN** user enters `y`
- **THEN** the task SHALL be deleted

#### Scenario: Cancel deletion with n
- **WHEN** user runs `delete 1`
- **WHEN** user enters `n`
- **THEN** the system SHALL print "Cancelled."
- **THEN** the task SHALL NOT be deleted

#### Scenario: Skip confirmation with --force
- **WHEN** user runs `delete 1 --force`
- **THEN** the task SHALL be deleted without prompting

### Requirement: Bulk delete multiple tasks
The system SHALL accept multiple space-separated task IDs for deletion.

#### Scenario: Delete multiple valid IDs
- **WHEN** user runs `delete 1 2 3`
- **THEN** tasks 1, 2, and 3 SHALL be deleted
- **THEN** the system SHALL print "Deleted tasks: 1, 2, 3."

#### Scenario: Bulk delete with mixed valid and invalid IDs
- **WHEN** user runs `delete 1 999`
- **THEN** task 1 SHALL be deleted
- **THEN** the system SHALL print "Deleted tasks: 1. Not found: 999."

### Requirement: Soft-delete to archive
Deleted tasks SHALL be moved to archive.json with a `deleted_at` timestamp.

#### Scenario: Deleted task appears in archive
- **WHEN** user runs `delete 1`
- **THEN** archive.json SHALL contain the task with original data plus `deleted_at` field
- **THEN** the task SHALL be removed from tasks.json
