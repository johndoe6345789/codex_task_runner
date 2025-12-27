from typing import Any, Optional

from ..codex.codex_cloud import get_task


def handle(args: Any, session) -> Optional[dict]:
    return get_task(session, args.task_id)
