from typing import Any

from .run import handle as run_handle


def handle(args: Any, session) -> dict:
    """YOLO mode: full auto merge all tasks."""
    args.yolo = True
    args.dry_run = False
    return run_handle(args, session)
