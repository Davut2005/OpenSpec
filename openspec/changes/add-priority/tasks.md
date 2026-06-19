## 1. --priority flag on add

- [x] 1.1 Add `--priority` argument to the `add` subparser with `choices=["low","medium","high"]` and `default="medium"`
- [x] 1.2 Store `"priority"` field on the task dict in `cmd_add`

## 2. Priority-sorted list output

- [x] 2.1 Define priority sort order: `high=0`, `medium=1`, `low=2`
- [x] 2.2 Sort tasks by priority in `cmd_list` before iterating (stable sort preserving insertion order within bucket)
- [x] 2.3 Default missing `"priority"` field to `"medium"` in the sort key
- [x] 2.4 Display `(priority)` label after each task title in list output
- [x] 2.5 Use `[!]` marker for pending high-priority tasks; use `[ ]` / `[x]` for all others
