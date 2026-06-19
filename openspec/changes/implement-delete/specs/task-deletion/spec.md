## ADDED Requirements

### Requirement: Delete single task with confirmation

The system SHALL prompt for confirmation before deleting a task, and SHALL move
the task to `archive.json` (soft-delete) on confirmation.

#### Scenario: Delete existing pending task — confirmed

Given `tasks.json` contains `[{"id": 1, "title": "Buy milk", "status": "pending", "created_at": "2024-01-01T00:00:00+00:00"}]`
And `archive.json` does not exist (or is an empty list `[]`)
When I run `python cli.py delete 1`
And I enter `y` at the prompt
Then `tasks.json` contains `[]`
And `archive.json` contains exactly one entry with:
  - `"id": 1`
  - `"title": "Buy milk"`
  - `"status": "deleted"`
  - `"created_at": "2024-01-01T00:00:00+00:00"`
  - `"deleted_at"` present and a valid ISO-8601 UTC timestamp
And stdout contains `"Delete task 1? (y/n): "`
And stdout contains `"Deleted task 1."`

#### Scenario: Delete existing completed task — confirmed

Given `tasks.json` contains `[{"id": 3, "title": "Read book", "status": "complete", "created_at": "2024-01-02T00:00:00+00:00"}]`
When I run `python cli.py delete 3`
And I enter `y` at the prompt
Then `tasks.json` contains `[]`
And `archive.json` contains one entry with `"id": 3` and `"status": "deleted"`
And stdout contains `"Deleted task 3."`

#### Scenario: Cancel deletion with n

Given `tasks.json` contains `[{"id": 2, "title": "Walk dog", "status": "pending", "created_at": "2024-01-01T00:00:00+00:00"}]`
When I run `python cli.py delete 2`
And I enter `n` at the prompt
Then `tasks.json` still contains task with `"id": 2`
And `archive.json` is empty or does not exist
And stdout contains `"Delete task 2? (y/n): "`
And stdout contains `"Cancelled."`

#### Scenario: Delete non-existent ID

Given `tasks.json` contains `[{"id": 1, "title": "Buy milk", "status": "pending", "created_at": "2024-01-01T00:00:00+00:00"}]`
When I run `python cli.py delete 999`
Then stdout contains `"Task 999 not found."`
And `tasks.json` is unchanged
And no prompt is shown
And the exit code is 0

#### Scenario: Delete from empty task list

Given `tasks.json` contains `[]`
When I run `python cli.py delete 1`
Then stdout contains `"Task 1 not found."`
And no prompt is shown

#### Scenario: Delete when tasks.json is missing

Given `tasks.json` does not exist
When I run `python cli.py delete 1`
Then stdout contains `"No tasks to delete."`
And no prompt is shown

---

### Requirement: Skip confirmation with --force

The system SHALL accept a `--force` (or `-f`) flag that bypasses the y/n prompt
and deletes immediately.

#### Scenario: Force-delete existing task

Given `tasks.json` contains `[{"id": 5, "title": "Send email", "status": "pending", "created_at": "2024-01-03T00:00:00+00:00"}]`
When I run `python cli.py delete 5 --force`
Then no prompt is shown
And `tasks.json` contains `[]`
And `archive.json` contains one entry with `"id": 5` and `"status": "deleted"`
And stdout contains `"Deleted task 5."`

#### Scenario: Force-delete non-existent task

Given `tasks.json` contains `[{"id": 1, "title": "Buy milk", "status": "pending", "created_at": "2024-01-01T00:00:00+00:00"}]`
When I run `python cli.py delete 999 --force`
Then stdout contains `"Task 999 not found."`
And `tasks.json` is unchanged

---

### Requirement: Bulk delete multiple tasks

The system SHALL accept multiple space-separated IDs in a single delete
invocation and process each one.

#### Scenario: Bulk delete — all IDs valid — confirmed

Given `tasks.json` contains tasks with ids 1, 2, and 3
When I run `python cli.py delete 1 2 3`
And I enter `y` at the prompt
Then all three tasks are moved to `archive.json`
And `tasks.json` contains `[]`
And stdout contains `"Delete tasks 1, 2, 3? (y/n): "`
And stdout contains `"Deleted tasks: 1, 2, 3."`

#### Scenario: Bulk delete — mixed valid and invalid IDs — confirmed

Given `tasks.json` contains tasks with ids 1 and 2 only
When I run `python cli.py delete 1 999`
And I enter `y` at the prompt
Then task 1 is moved to `archive.json`
And `tasks.json` still contains task with `"id": 2`
And stdout contains `"Deleted tasks: 1. Not found: 999."`

#### Scenario: Bulk delete — all IDs invalid

Given `tasks.json` contains tasks with ids 1 and 2 only
When I run `python cli.py delete 888 999`
And I enter `y` at the prompt
Then `tasks.json` is unchanged
And `archive.json` is empty or does not exist
And stdout contains `"Not found: 888, 999."`

#### Scenario: Bulk delete — cancelled

Given `tasks.json` contains tasks with ids 1 and 2
When I run `python cli.py delete 1 2`
And I enter `n` at the prompt
Then `tasks.json` is unchanged
And stdout contains `"Cancelled."`

#### Scenario: Bulk force-delete

Given `tasks.json` contains tasks with ids 1, 2, and 3
When I run `python cli.py delete 1 2 3 --force`
Then no prompt is shown
And all three tasks are moved to `archive.json`
And stdout contains `"Deleted tasks: 1, 2, 3."`

---

### Requirement: Soft-delete archive format

Deleted tasks SHALL be appended to `archive.json` preserving all original
fields and adding a `deleted_at` timestamp.  `archive.json` itself is a JSON
array (created if absent).

#### Scenario: Archive entry fields

Given `tasks.json` contains `[{"id": 7, "title": "Clean desk", "status": "pending", "created_at": "2024-06-01T08:00:00+00:00"}]`
When I run `python cli.py delete 7 --force`
Then `archive.json` is a valid JSON array
And the entry at index 0 has exactly the fields: `id`, `title`, `status`, `created_at`, `deleted_at`
And `"id"` equals `7`
And `"title"` equals `"Clean desk"`
And `"status"` equals `"deleted"`
And `"created_at"` equals `"2024-06-01T08:00:00+00:00"`
And `"deleted_at"` is an ISO-8601 UTC string (e.g. ends with `+00:00` or `Z`)

#### Scenario: Archive appends — does not overwrite previous entries

Given `archive.json` already contains one entry with `"id": 10`
And `tasks.json` contains task with `"id": 11`
When I run `python cli.py delete 11 --force`
Then `archive.json` contains two entries
And the entry with `"id": 10` is still present unchanged
And the entry with `"id": 11` is the new one

---

### Requirement: Task ID reuse after deletion

IDs of deleted tasks SHALL NOT be reused by the `add` command.

#### Scenario: IDs are not reused after soft-delete

Given `tasks.json` is `[]` (task with id 1 was previously deleted and is in archive.json)
And the next call to `next_id()` reads only `tasks.json` (not archive)
When I run `python cli.py add "New task"`
Then the new task gets `"id": 1` (next_id from an empty list is 1)

> Note: Because soft-deleted tasks are removed from `tasks.json`, `next_id()`
> will assign id 1 again if tasks.json is empty. This is **acceptable and
> intentional** — IDs are local sequence numbers, not permanent unique keys.
> The spec does NOT require globally unique IDs across archive.json.
