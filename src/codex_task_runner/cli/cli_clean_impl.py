#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Optional

from codex_task_runner.codex.codex_cloud import (
    session_from_env,
    ping_url,
    poll_urls,
    get_tasks_list,
    get_task,
    get_turns,
    create_pr_for_turn,
    save_results,
)


def ping_cmd(sess, url: str) -> int:
    res = ping_url(sess, url)
    print(json.dumps(res, indent=2))
    return 0


def poll_cmd(sess, urls_file: str, out: str) -> int:
    urls = Path(urls_file).read_text().splitlines()
    res = poll_urls(sess, urls)
    save_results(out, {"polls": res})
    print(f"saved results to {out}")
    return 0


def tasks_cmd(sess, limit: int) -> int:
    tasks = get_tasks_list(sess, limit=limit)
    print(json.dumps([t.__dict__ for t in tasks], indent=2))
    return 0


def task_cmd(sess, task_id: str) -> int:
    data = get_task(sess, task_id)
    print(json.dumps(data or {}, indent=2))
    return 0


def turns_cmd(sess, task_id: str) -> int:
    data = get_turns(sess, task_id)
    print(json.dumps(data or {}, indent=2))
    return 0


def create_pr_cmd(sess, task_id: str, turn_id: str, dry_run: bool) -> int:
    if dry_run:
        print("dry-run: not creating PR")
        return 0
    resp = create_pr_for_turn(sess, task_id, turn_id)
    print(json.dumps(resp or {}, indent=2))
    return 0


def run_cmd(sess, dry_run: bool, output_dir: Optional[str]) -> int:
    from .runner import make_config, process_tasks

    tasks = get_tasks_list(sess, limit=20)
    if not tasks:
        print("No tasks found or request failed.")
        return 1
    cfg = make_config(require_checks=False, method="merge", keep_branch=False, admin=False, auto=False, dry_run=dry_run, output_dir=output_dir)
    process_tasks(cfg, tasks)
    print(f"Processed {len(tasks)} tasks (dry-run={dry_run}).")
    return 0
