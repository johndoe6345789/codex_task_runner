#!/usr/bin/env python3
from __future__ import annotations

import sys
from codex_task_runner.codex_cloud import session_from_env, get_tasks_list
from codex_task_runner.runner import make_config, process_tasks

# Simple runner that pulls tasks from Codex Cloud and hands them to the local runner.

if __name__ == "__main__":
    env_path = ".env"
    sess = session_from_env(env_path)
    tasks = get_tasks_list(sess, limit=20)
    if not tasks:
        print("No tasks found or request failed.")
        sys.exit(1)
    cfg = make_config(require_checks=False, method="merge", keep_branch=False, admin=False, auto=False, dry_run=True, output_dir=None)
    # dry_run=True by default to avoid opening real PRs; set dry_run=False after review
    process_tasks(cfg, tasks)
    print(f"Processed {len(tasks)} tasks (dry-run).")
