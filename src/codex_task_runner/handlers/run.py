from typing import Any, List

from ..codex.codex_tasks_list import get_tasks_list


def handle(args: Any, session) -> dict:
    from ..runner.do_process_tasks import process_tasks
    from ..etc.make_config import make_config

    tasks = get_tasks_list(session, limit=20)
    if not tasks:
        return {"processed": 0, "error": "no tasks"}
    cfg = make_config(require_checks=False, method="merge", keep_branch=False, admin=False, auto=False, dry_run=args.dry_run, output_dir=args.output_dir)
    process_tasks(cfg, tasks)
    return {"processed": len(tasks), "dry_run": args.dry_run}
