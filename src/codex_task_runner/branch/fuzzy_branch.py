from __future__ import annotations

from .best_by_words import best_by_words
from .best_by_id import best_by_id


def fuzzy_branch(branches: list[str], title: str, task_id: str) -> str | None:
    cands = [b for b in branches if b.startswith("codex/")]
    if not cands:
        return None
    by_words = best_by_words(cands, title)
    if by_words:
        return by_words
    return best_by_id(cands, task_id)
