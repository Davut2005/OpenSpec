<!-- Delta spec: describes only what changes relative to existing behaviour.
     ## ADDED = brand-new requirements that didn't exist before.
     ## MODIFIED = existing behaviour that is being changed.
-->

---

## ADDED

### Requirement: --priority flag on add

The `add` command SHALL accept an optional `--priority` flag with allowed
values `low`, `medium`, `high`.  If omitted the default is `medium`.
The value SHALL be stored as a `"priority"` string field on the task in
`tasks.json`.

#### Scenario: Add task with explicit high priority

Given `tasks.json` is `[]`
When I run `python cli.py add "Send invoice" --priority high`
Then `tasks.json` contains exactly one task with:
  - `"title": "Send invoice"`
  - `"priority": "high"`
  - `"status": "pending"`
And stdout contains `"Added task 1: Send invoice"`

#### Scenario: Add task with explicit low priority

Given `tasks.json` is `[]`
When I run `python cli.py add "Read newsletter" --priority low`
Then `tasks.json` contains one task with `"priority": "low"`

#### Scenario: Add task with no --priority flag (default medium)

Given `tasks.json` is `[]`
When I run `python cli.py add "Buy groceries"`
Then `tasks.json` contains one task with `"priority": "medium"`
And stdout contains `"Added task 1: Buy groceries"`

#### Scenario: Add task with invalid priority value

When I run `python cli.py add "Some task" --priority urgent`
Then the process exits with a non-zero exit code
And stderr contains an error message (argparse choices error)
And `tasks.json` is unchanged

---

## ADDED

### Requirement: Priority-sorted list output

The `list` command SHALL display tasks sorted by priority: `high` first, then
`medium`, then `low`.  Within the same priority bucket, tasks appear in
insertion order (stable sort).  Tasks that are missing the `"priority"` field
(created before this feature) SHALL be treated as `medium`.

A high-priority task SHALL be visually distinguished with a `[!]` marker
instead of `[ ]` or `[x]`.

#### Scenario: List shows high-priority tasks first

Given `tasks.json` contains (in this insertion order):
  - `{"id":1, "title":"Low task",    "status":"pending",  "priority":"low"}`
  - `{"id":2, "title":"Medium task", "status":"pending",  "priority":"medium"}`
  - `{"id":3, "title":"High task",   "status":"pending",  "priority":"high"}`
When I run `python cli.py list`
Then stdout is exactly:
```
  [!] 3. High task (high)
  [ ] 2. Medium task (medium)
  [ ] 1. Low task (low)
```

#### Scenario: Completed high-priority task uses [x] not [!]

Given `tasks.json` contains:
  - `{"id":1, "title":"Urgent done", "status":"complete", "priority":"high"}`
When I run `python cli.py list`
Then stdout contains `[x] 1. Urgent done (high)`
And does NOT contain `[!] 1.`

#### Scenario: Within same priority bucket, insertion order is preserved

Given `tasks.json` contains:
  - `{"id":1, "title":"Alpha", "status":"pending", "priority":"medium"}`
  - `{"id":2, "title":"Beta",  "status":"pending", "priority":"medium"}`
  - `{"id":3, "title":"Gamma", "status":"pending", "priority":"high"}`
  - `{"id":4, "title":"Delta", "status":"pending", "priority":"medium"}`
When I run `python cli.py list`
Then stdout is exactly:
```
  [!] 3. Gamma (high)
  [ ] 1. Alpha (medium)
  [ ] 2. Beta (medium)
  [ ] 4. Delta (medium)
```

#### Scenario: Priority label shown in list output

Given `tasks.json` contains a task with `"priority":"low"` and `"status":"pending"`
When I run `python cli.py list`
Then the line for that task ends with `(low)`

---

## MODIFIED

### Existing behaviour: task-list — insertion-order output (CHANGED)

**Before:** `list` printed tasks in the order they appear in `tasks.json`.

**After:** `list` prints tasks sorted by priority (high → medium → low),
with insertion order preserved within each bucket.

> No new scenario needed — the ADDED scenarios above fully specify the new
> behaviour.  Any test that relied on exact insertion-order output must be
> updated to expect priority-sorted output.

---

## MODIFIED

### Existing behaviour: task storage schema (EXTENDED)

**Before:** task objects had fields `id`, `title`, `status`, `created_at`.

**After:** task objects created by `add` also have `"priority": "<value>"`.
Tasks created before this change (missing `"priority"`) continue to work;
`list` treats them as `medium`.

#### Scenario: Legacy task (no priority field) appears between medium tasks

Given `tasks.json` contains:
  - `{"id":1, "title":"Old task", "status":"pending", "created_at":"2024-01-01T00:00:00+00:00"}`
  - `{"id":2, "title":"New high", "status":"pending", "priority":"high",   "created_at":"2024-06-01T00:00:00+00:00"}`
  - `{"id":3, "title":"New low",  "status":"pending", "priority":"low",    "created_at":"2024-06-01T00:00:00+00:00"}`
When I run `python cli.py list`
Then stdout is exactly:
```
  [!] 2. New high (high)
  [ ] 1. Old task (medium)
  [ ] 3. New low (low)
```

> "Old task" is treated as medium and sorts after the high-priority task but
> before the low-priority task.
