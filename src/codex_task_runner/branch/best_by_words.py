from __future__ import annotations

from codex_task_runner.etc.words import words
from .word_score import word_score


def best_by_words(cands: list[str], title: str) -> str | None:
    ws = set(words(title))
    if not ws:
        return None
    if not cands:
        return None
    scored = [(b, word_score(b, ws)) for b in cands]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0] if scored[0][1] >= 2 else None
