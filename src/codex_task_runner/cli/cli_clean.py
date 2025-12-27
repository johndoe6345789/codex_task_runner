#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import Optional, List

from codex_task_runner.codex.codex_cloud import session_from_env
from .cli_clean_impl import (
    ping_cmd,
    poll_cmd,
    tasks_cmd,
    task_cmd,
    turns_cmd,
    create_pr_cmd,
    run_cmd,
)


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="codex-runner-clean")
    p.add_argument("--env", default=".env", help="Path to .env with cookies/tokens")
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("ping", help="Ping a single URL and print result")
    sp.add_argument("url")

    sp = sub.add_parser("poll", help="Poll a list of URLs from a file and save JSON")
    sp.add_argument("urls_file")
    sp.add_argument("out", help="Output JSON file", default="poll.json")

    sp = sub.add_parser("tasks", help="List tasks from Codex Cloud")
    sp.add_argument("--limit", type=int, default=20)

    sp = sub.add_parser("task", help="Fetch single task detail")
    sp.add_argument("task_id")

    sp = sub.add_parser("turns", help="Fetch turns for a task")
    sp.add_argument("task_id")

    sp = sub.add_parser("create-pr", help="Create PR for a task turn (calls Codex API)")
    sp.add_argument("task_id")
    sp.add_argument("turn_id")
    sp.add_argument("--dry-run", action="store_true")

    sp = sub.add_parser("run", help="Run integration: fetch tasks and process (dry-run default)")
    sp.add_argument("--dry-run", action="store_true", default=True)
    sp.add_argument("--output-dir", default=None)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(argv) if argv is not None else None
    p = make_parser()
    args = p.parse_args(argv)
    if not args.cmd:
        p.print_help()
        return 1

    sess = session_from_env(getattr(args, "env", ".env"))

    if args.cmd == "ping":
        return ping_cmd(sess, args.url)

    if args.cmd == "poll":
        return poll_cmd(sess, args.urls_file, args.out)

    if args.cmd == "tasks":
        return tasks_cmd(sess, getattr(args, "limit", 20))

    if args.cmd == "task":
        return task_cmd(sess, args.task_id)

    if args.cmd == "turns":
        return turns_cmd(sess, args.task_id)

    if args.cmd == "create-pr":
        return create_pr_cmd(sess, args.task_id, args.turn_id, args.dry_run)

    if args.cmd == "run":
        return run_cmd(sess, args.dry_run, args.output_dir)

    p.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
