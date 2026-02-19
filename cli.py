from __future__ import annotations

import argparse
import os
import sys

from dotenv import load_dotenv

from clients.todoist_client import TodoistClient, TodoistError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Todoist REST v2 CLI sample")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--filter", dest="filter_query", default=None, help='Filter expression, e.g. "today | overdue"')
    list_parser.add_argument("--limit", type=int, default=10, help="Max number of tasks to display")

    add_parser = subparsers.add_parser("add", help="Add a task")
    add_parser.add_argument("content", help="Task content")
    add_parser.add_argument("--due", dest="due_string", default=None, help='Due string, e.g. "tomorrow at 10am"')

    close_parser = subparsers.add_parser("close", help="Close a task")
    close_parser.add_argument("task_id", help="Task ID to close")

    return parser


def main() -> int:
    load_dotenv(override=True)
    parser = build_parser()
    args = parser.parse_args()

    token = os.getenv("TODOIST_API_TOKEN", "")
    client = TodoistClient(api_token=token)

    try:
        if args.command == "list":
            tasks = client.list_tasks(filter_query=args.filter_query, limit=args.limit)
            if not tasks:
                print("No tasks found.")
                return 0
            for task in tasks:
                print(f'{task.get("id")}: {task.get("content", "")}')
            return 0

        if args.command == "add":
            task = client.add_task(content=args.content, due_string=args.due_string)
            print(f'Created task {task.get("id")}: {task.get("content", "")}')
            return 0

        if args.command == "close":
            client.close_task(task_id=args.task_id)
            print(f"Closed task {args.task_id}.")
            return 0

        parser.print_help()
        return 1

    except TodoistError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

