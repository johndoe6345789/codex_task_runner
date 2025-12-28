"""Command handlers for the CLI.

Each handler module provides a `handle(args, session)` function.
"""

from . import ping, poll, tasks, task, turns, create_pr, run, discover, archive, patch, ui, yolo, dedup_prs, me, prompt, serve

__all__ = ["ping", "poll", "tasks", "task", "turns", "create_pr", "run", "discover", "archive", "patch", "ui", "yolo", "dedup_prs", "me", "prompt", "serve"]
