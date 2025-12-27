from typing import Any

from .run import handle as run_handle
from ..codex.codex_tasks_list import get_tasks_list
from ..codex.codex_turns import get_turns
from ..codex.codex_create_pr import create_pr_for_turn
from ..etc.log import log


def _ensure_prs(session, tasks) -> dict:
    """Create PRs via Codex API for tasks that don't have one."""
    created = 0
    skipped = 0
    errors = []
    
    for t in tasks:
        if t.pr_numbers:
            log.debug(f"SKIP {t.task_id}: already has PR {t.pr_numbers}")
            skipped += 1
            continue
        
        # Get turns for this task
        log.info(f"GET turns for {t.task_id}: {t.title[:40]}")
        turns_data = get_turns(session, t.task_id)
        if not turns_data:
            log.warning(f"FAIL {t.task_id}: no turns data")
            errors.append(f"{t.task_id}: no turns")
            continue
        
        # Find the last turn
        turns_list = turns_data.get("turns") or turns_data.get("items") or []
        if not turns_list:
            log.warning(f"FAIL {t.task_id}: empty turns list")
            errors.append(f"{t.task_id}: empty turns")
            continue
        
        last_turn = turns_list[-1]
        turn_id = last_turn.get("id") or last_turn.get("turn_id")
        if not turn_id:
            log.warning(f"FAIL {t.task_id}: no turn_id in {last_turn}")
            errors.append(f"{t.task_id}: no turn_id")
            continue
        
        # Create PR via Codex API
        log.info(f"CREATE PR for {t.task_id} turn {turn_id}")
        result = create_pr_for_turn(session, t.task_id, str(turn_id))
        if result:
            created += 1
            log.info(f"OK {t.task_id}: PR created")
        else:
            log.error(f"FAIL {t.task_id}: API returned None")
            errors.append(f"{t.task_id}: API failed")
    
    return {"created": created, "skipped": skipped, "errors": errors}


def handle(args: Any, session) -> dict:
    """YOLO mode: create PRs via Codex, then merge all tasks."""
    from ..etc.set_level import set_level
    
    # Enable debug logging if verbose
    if getattr(args, "verbose", False):
        set_level("DEBUG")
    
    # First, get tasks and create PRs for those without
    log.info("Fetching tasks...")
    tasks = get_tasks_list(session, limit=20)
    if not tasks:
        log.error("No tasks found")
        return {"processed": 0, "error": "no tasks"}
    
    log.info(f"Found {len(tasks)} tasks")
    pr_result = _ensure_prs(session, tasks)
    log.info(f"PRs: {pr_result['created']} created, {pr_result['skipped']} already had PR")
    if pr_result['errors']:
        log.warning(f"Errors: {pr_result['errors']}")
    
    # Now run the merge process
    log.info("Starting merge process...")
    args.yolo = True
    args.dry_run = False
    result = run_handle(args, session)
    result["prs_created"] = pr_result["created"]
    log.info(f"Done: {result}")
    return result

