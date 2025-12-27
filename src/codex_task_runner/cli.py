#!/usr/bin/env python3
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .codex_cloud import (
    session_from_env,
    ping_url,
    poll_urls,
    get_tasks_list,
    get_task,
    get_turns,
    create_pr_for_turn,
    save_results,
)


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="codex-runner")
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


def main(argv: list[str] | None = None) -> int:
    argv = list(argv) if argv is not None else None
    p = make_parser()
    args = p.parse_args(argv)
    if not args.cmd:
        p.print_help()
        return 1

    sess = session_from_env(getattr(args, "env", ".env"))

    if args.cmd == "ping":
        res = ping_url(sess, args.url)
        print(json.dumps(res, indent=2))
        return 0

    if args.cmd == "poll":
        urls = Path(args.urls_file).read_text().splitlines()
        res = poll_urls(sess, urls)
        save_results(args.out, {"polls": res})
        print(f"saved results to {args.out}")
        return 0

    if args.cmd == "tasks":
        tasks = get_tasks_list(sess, limit=getattr(args, "limit", 20))
        print(json.dumps([t.__dict__ for t in tasks], indent=2))
        return 0

    if args.cmd == "task":
        data = get_task(sess, args.task_id)
        print(json.dumps(data or {}, indent=2))
        return 0

    if args.cmd == "turns":
        data = get_turns(sess, args.task_id)
        print(json.dumps(data or {}, indent=2))
        return 0

    if args.cmd == "create-pr":
        if args.dry_run:
            print("dry-run: not creating PR")
            return 0
        resp = create_pr_for_turn(sess, args.task_id, args.turn_id)
        print(json.dumps(resp or {}, indent=2))
        return 0

    if args.cmd == "run":
        from .runner import make_config, process_tasks

        tasks = get_tasks_list(sess, limit=20)
        if not tasks:
            print("No tasks found or request failed.")
            return 1
        cfg = make_config(require_checks=False, method="merge", keep_branch=False, admin=False, auto=False, dry_run=args.dry_run, output_dir=args.output_dir)
        process_tasks(cfg, tasks)
        print(f"Processed {len(tasks)} tasks (dry-run={args.dry_run}).")
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
from __future__ import annotations
