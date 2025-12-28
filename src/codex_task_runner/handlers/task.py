from typing import Any, Optional

from ..codex.codex_task_detail import get_task
from ..etc.task_aliases import resolve_alias


def handle(args: Any, session) -> Optional[dict]:
    task_id = resolve_alias(args.task_id)
    return get_task(session, task_id)
