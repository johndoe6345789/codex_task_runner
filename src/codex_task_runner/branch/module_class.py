from __future__ import annotations

from codex_task_runner.branch.fuzzy_branch import fuzzy_branch
from codex_task_runner.branch.best_by_words import best_by_words
from codex_task_runner.branch.word_score import word_score
from codex_task_runner.branch.best_by_id import best_by_id


class BranchModule:
    """Aggregates branch utilities for the `branch` package."""

    fuzzy_branch = staticmethod(fuzzy_branch)
    best_by_words = staticmethod(best_by_words)
    word_score = staticmethod(word_score)
    best_by_id = staticmethod(best_by_id)
