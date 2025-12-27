from typing import Any, List

from ..codex.codex_tasks_list import get_tasks_list


def handle(args: Any, session) -> dict:
    from ..runner.do_process_tasks import process_tasks
    from ..etc.make_config import make_config

    yolo = getattr(args, "yolo", False)
    dry_run = getattr(args, "dry_run", False) and not yolo

    tasks = get_tasks_list(session, limit=20)
    if not tasks:
        return {"processed": 0, "error": "no tasks"}

    cfg = make_config(
        require_checks=not yolo,  # skip checks in yolo mode
        method="squash" if yolo else "merge",
        keep_branch=False,
        admin=yolo,  # use admin powers in yolo mode
        auto=yolo,   # auto-merge in yolo mode
        dry_run=dry_run,
        output_dir=args.output_dir,
    )
    process_tasks(cfg, tasks)
    return {"processed": len(tasks), "dry_run": dry_run, "yolo": yolo}
