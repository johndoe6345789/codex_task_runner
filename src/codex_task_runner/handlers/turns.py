from typing import Any, Optional

from ..codex.codex_turns import get_turns
from ..etc.task_aliases import resolve_alias


def handle(args: Any, session) -> Optional[dict]:
    task_id = resolve_alias(args.task_id)
    return get_turns(session, task_id)
