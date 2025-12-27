from __future__ import annotations

from codex_task_runner.etc.words import words


def word_score(branch: str, ws: set[str]) -> int:
    bws = set(words(branch))
    return len(ws.intersection(bws))
