from __future__ import annotations

from codex_task_runner.handlers import (
    create_pr,
    ping,
    poll,
    run,
    task,
    tasks,
    turns,
)


class HandlersModule:
    """Aggregates handler entrypoints from the `handlers` package."""

    create_pr = staticmethod(create_pr.handle)
    ping = staticmethod(ping.handle)
    poll = staticmethod(poll.handle)
    run = staticmethod(run.handle)
    task = staticmethod(task.handle)
    tasks = staticmethod(tasks.handle)
    turns = staticmethod(turns.handle)
