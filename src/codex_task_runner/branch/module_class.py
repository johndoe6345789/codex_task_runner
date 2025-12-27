from __future__ import annotations

from codex_task_runner.branch import branch_fuzzy


class BranchModule:
    """Aggregates branch utilities for the `branch` package."""

    fuzzy_branch = staticmethod(branch_fuzzy.fuzzy_branch)
    best_by_words = staticmethod(branch_fuzzy.best_by_words)
    word_score = staticmethod(branch_fuzzy.word_score)
    best_by_id = staticmethod(branch_fuzzy.best_by_id)
