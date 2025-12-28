from __future__ import annotations

from codex_task_runner.pr import (
    ensure_prs,
    fetch_tasks,
    filter_tasks,
    find_existing_pr,
    first_open,
    fmt_pr,
    maybe_create_pr,
    merge_task,
    pr_body,
    process_all_tasks,
    process_task,
    show_tasks,
    task_pr_number,
)


class PrModule:
    """Aggregates PR-related helpers and modules."""

    ensure_prs = ensure_prs
    fetch_tasks = fetch_tasks
    filter_tasks = filter_tasks
    find_existing_pr = find_existing_pr
    first_open = first_open
    fmt_pr = fmt_pr
    maybe_create_pr = maybe_create_pr
    merge_task = merge_task
    pr_body = pr_body
    process_all_tasks = process_all_tasks
    process_task = process_task
    show_tasks = show_tasks
    task_pr_number = task_pr_number
