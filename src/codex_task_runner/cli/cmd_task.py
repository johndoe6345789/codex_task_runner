import json

from codex_task_runner.handlers import task


def task_cmd(sess, task_id: str) -> int:
    """Fetch single task detail."""
    from types import SimpleNamespace
    args = SimpleNamespace(task_id=task_id)
    data = task.handle(args, sess)
    print(json.dumps(data or {}, indent=2))
    return 0
