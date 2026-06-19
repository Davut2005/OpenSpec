import argparse
import json
from datetime import datetime, timezone

TASKS_FILE = "tasks.json"
ARCHIVE_FILE = "archive.json"


def load(path):
    with open(path) as f:
        return json.load(f)


def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


# ── Task 1.2: archive helpers ────────────────────────────────────────────────

def load_archive():
    """Load archive.json, returning [] if the file is missing."""
    try:
        return load(ARCHIVE_FILE)
    except FileNotFoundError:
        return []


def save_archive(data):
    save(ARCHIVE_FILE, data)


# ────────────────────────────────────────────────────────────────────────────

# Tasks 2.1 / 2.3: sort order; missing field defaults to "medium"
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def cmd_add(args):
    tasks = load(TASKS_FILE)
    # Task 1.2: store priority on the task object
    task = {
        "id": next_id(tasks),
        "title": args.title,
        "status": "pending",
        "priority": args.priority,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    tasks.append(task)
    save(TASKS_FILE, tasks)
    print(f"Added task {task['id']}: {task['title']}")


def cmd_list(args):
    tasks = load(TASKS_FILE)
    if not tasks:
        print("No tasks.")
        return
    # Task 2.2: stable sort by priority; Task 2.3: missing field → "medium"
    sorted_tasks = sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.get("priority", "medium"), 1))
    for t in sorted_tasks:
        priority = t.get("priority", "medium")
        # Task 2.5: [!] for pending high-priority; [x] for complete; [ ] otherwise
        if t["status"] == "complete":
            mark = "x"
        elif priority == "high" and t["status"] == "pending":
            mark = "!"
        else:
            mark = " "
        # Task 2.4: show (priority) label after title
        print(f"  [{mark}] {t['id']}. {t['title']} ({priority})")


def cmd_complete(args):
    tasks = load(TASKS_FILE)
    for t in tasks:
        if t["id"] == args.id:
            t["status"] = "complete"
            save(TASKS_FILE, tasks)
            print(f"Completed task {args.id}.")
            return
    print(f"Task {args.id} not found.")


# ── Task 1.3 / 2.x / 3.x: cmd_delete ───────────────────────────────────────

def cmd_delete(args):
    # Task 1.3 / 3.x: load tasks; handle missing file
    try:
        tasks = load(TASKS_FILE)
    except FileNotFoundError:
        print("No tasks to delete.")
        return

    # Task 3.1: ids is a list (nargs="+"), each element is int
    ids = args.id  # list[int]

    # Resolve which IDs exist
    found = [t for t in tasks if t["id"] in ids]
    found_ids = [t["id"] for t in found]
    not_found_ids = sorted(i for i in ids if i not in found_ids)

    # If none of the IDs exist, report and exit without prompting
    if not found:
        if len(ids) == 1:
            print(f"Task {ids[0]} not found.")
        else:
            print(f"Not found: {', '.join(str(i) for i in sorted(not_found_ids))}.")
        return

    # Task 2.1 / 2.2: confirmation prompt unless --force is set
    if not args.force:
        # Task 3.2: prompt lists all IDs being attempted
        if len(ids) == 1:
            prompt = f"Delete task {ids[0]}? (y/n): "
        else:
            prompt = f"Delete tasks {', '.join(str(i) for i in ids)}? (y/n): "
        answer = input(prompt).strip().lower()
        # Task 2.3: cancel on anything other than y
        if answer != "y":
            print("Cancelled.")
            return

    # Perform soft-delete: move found tasks to archive.json
    # Task 1.1: add deleted_at timestamp; Task 1.3: set status = "deleted"
    archive = load_archive()
    now = datetime.now(timezone.utc).isoformat()
    for task in found:
        archived_task = {**task, "status": "deleted", "deleted_at": now}
        archive.append(archived_task)
    save_archive(archive)

    # Remove deleted tasks from tasks.json
    remaining = [t for t in tasks if t["id"] not in found_ids]
    save(TASKS_FILE, remaining)

    # Task 3.3: output messages
    if len(ids) == 1:
        # Single-ID invocation
        if found_ids:
            print(f"Deleted task {found_ids[0]}.")
        # not_found case already handled above (early return)
    else:
        # Bulk invocation — always show Deleted / Not found breakdown
        parts = []
        if found_ids:
            parts.append(f"Deleted tasks: {', '.join(str(i) for i in sorted(found_ids))}.")
        if not_found_ids:
            parts.append(f"Not found: {', '.join(str(i) for i in not_found_ids)}.")
        print(" ".join(parts))


# ────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Task manager")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add")
    p_add.add_argument("title")
    # Task 1.1: --priority flag with choices and default
    p_add.add_argument("--priority", choices=["low", "medium", "high"],
                       default="medium", help="Task priority (default: medium)")

    p_list = sub.add_parser("list")

    p_complete = sub.add_parser("complete")
    p_complete.add_argument("id", type=int)

    # Task 3.1: nargs="+" for multiple IDs; Task 2.1: --force/-f flag
    p_delete = sub.add_parser("delete")
    p_delete.add_argument("id", nargs="+", type=int)
    p_delete.add_argument("--force", "-f", action="store_true",
                          help="Skip confirmation prompt")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return

    {"add": cmd_add, "list": cmd_list, "complete": cmd_complete, "delete": cmd_delete}[
        args.command
    ](args)


if __name__ == "__main__":
    main()
