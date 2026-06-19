## 1. Soft-delete & Archive Support

- [ ] 1.1 Add `deleted_at` timestamp field when moving tasks to archive
- [ ] 1.2 Implement `load_archive()` and `save_archive()` helpers
- [ ] 1.3 Modify `cmd_delete` to move task to archive.json instead of permanent removal

## 2. Confirmation Prompt

- [ ] 2.1 Add `--force` / `-f` flag to the delete subparser
- [ ] 2.2 Implement confirmation prompt before deletion unless `--force` is set
- [ ] 2.3 Handle `y`/`n` input and print "Cancelled." on rejection

## 3. Bulk Delete

- [ ] 3.1 Change `id` argument to `nargs="+"` for multiple IDs
- [ ] 3.2 Implement bulk delete loop with success/failure reporting
- [ ] 3.3 Print "Deleted tasks: <ids>. Not found: <ids>." for mixed results
