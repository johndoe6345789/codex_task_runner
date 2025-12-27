#!/usr/bin/env python3
"""CLI command implementations that delegate to handlers."""

import json
from typing import Optional

from codex_task_runner.handlers import ping, poll, tasks, task, turns, create_pr, run


def ping_cmd(sess, url: str) -> int:
    """Ping a single URL and print result."""
    from types import SimpleNamespace
    args = SimpleNamespace(url=url)
    res = ping.handle(args, sess)
    print(json.dumps(res, indent=2))
    return 0


def poll_cmd(sess, urls_file: str, out: str) -> int:
    """Poll a list of URLs from a file and save JSON."""
    from types import SimpleNamespace
    args = SimpleNamespace(urls_file=urls_file, out=out)
    res = poll.handle(args, sess)
    print(f"saved results to {res.get('saved', out)}")
    return 0


def tasks_cmd(sess, limit: int) -> int:
    """List tasks from Codex Cloud."""
    from types import SimpleNamespace
    args = SimpleNamespace(limit=limit)
    res = tasks.handle(args, sess)
    print(json.dumps(res, indent=2))
    return 0


def task_cmd(sess, task_id: str) -> int:
    """Fetch single task detail."""
    from types import SimpleNamespace
    args = SimpleNamespace(task_id=task_id)
    data = task.handle(args, sess)
    print(json.dumps(data or {}, indent=2))
    return 0


def turns_cmd(sess, task_id: str) -> int:
    """Fetch turns for a task."""
    from types import SimpleNamespace
    args = SimpleNamespace(task_id=task_id)
    data = turns.handle(args, sess)
    print(json.dumps(data or {}, indent=2))
    return 0


def create_pr_cmd(sess, task_id: str, turn_id: str, dry_run: bool) -> int:
    """Create PR for a task turn (calls Codex API)."""
    from types import SimpleNamespace
    args = SimpleNamespace(task_id=task_id, turn_id=turn_id, dry_run=dry_run)
    if dry_run:
        print("dry-run: not creating PR")
        return 0
    resp = create_pr.handle(args, sess)
    print(json.dumps(resp or {}, indent=2))
    return 0


def run_cmd(sess, dry_run: bool, output_dir: Optional[str]) -> int:
    """Run integration: fetch tasks and process."""
    from types import SimpleNamespace
    args = SimpleNamespace(dry_run=dry_run, output_dir=output_dir)
    res = run.handle(args, sess)
    processed = res.get("processed", 0)
    if res.get("error"):
        print(f"No tasks found or request failed.")
        return 1
    print(f"Processed {processed} tasks (dry-run={dry_run}).")
    return 0
