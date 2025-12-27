"""Processor compatibility wrapper.

Public entrypoints are provided by `process_tasks` in `process_tasks.py`.
Internal implementation is in `process_one.py`.
"""

from .process_tasks import process_tasks

__all__ = ["process_tasks"]
