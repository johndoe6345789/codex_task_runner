"""Flask wrapper for codex-task-runner CLI."""

from .app import create_app

__all__ = ["create_app"]
