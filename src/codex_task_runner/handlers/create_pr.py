from typing import Any, Optional

from ..codex_cloud import create_pr_for_turn


def handle(args: Any, session) -> Optional[dict]:
    if getattr(args, "dry_run", False):
        return {"dry_run": True}
    return create_pr_for_turn(session, args.task_id, args.turn_id)
