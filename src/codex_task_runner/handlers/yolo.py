"""YOLO mode: create PRs, dedup, merge - full automation."""
from typing import Any

from ..pr.fetch_tasks import fetch_tasks
from ..pr.show_tasks import show_tasks
from ..pr.process_all_tasks import process_all_tasks
from ..etc.parse_yolo_args import parse_yolo_args
from ..etc.confirm import confirm
from ..etc.log import log


def handle(args: Any, session) -> dict:
    """YOLO mode: create PRs via Codex, then merge all tasks."""
    from ..etc.set_level import set_level
    
    opts = parse_yolo_args(args)
    if opts.verbose:
        set_level("DEBUG")
    
    tasks = fetch_tasks(session, opts.limit, opts.repo_filter)
    if not tasks:
        return {"processed": 0, "error": "no tasks"}
    
    needs_pr, has_pr = show_tasks(tasks)
    
    if opts.dry_run:
        log.info(f"DRY RUN: Would create {len(needs_pr)} PRs, merge {len(tasks)} total")
        return {"dry_run": True, "would_create": len(needs_pr), "would_merge": len(has_pr)}
    
    if not opts.no_confirm and not confirm(f"Proceed with {len(tasks)} tasks?"):
        return {"aborted": True}
    
    return process_all_tasks(session, tasks, opts.repo_filter, opts.limit)

