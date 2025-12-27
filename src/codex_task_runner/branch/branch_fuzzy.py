from __future__ import annotations

from ..words import words


def fuzzy_branch(branches: list[str], title: str, task_id: str) -> str | None:
    cands = [b for b in branches if b.startswith("codex/")]
    if not cands:
        return None
    by_words = best_by_words(cands, title)
    if by_words:
        return by_words
    return best_by_id(cands, task_id)


def best_by_words(cands: list[str], title: str) -> str | None:
    ws = set(words(title))
    if not ws:
        return None
    scored = [(b, word_score(b, ws)) for b in cands]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0] if scored[0][1] >= 2 else None


def word_score(branch: str, ws: set[str]) -> int:
    bws = set(words(branch))
    return len(ws.intersection(bws))


def best_by_id(cands: list[str], task_id: str) -> str | None:
    suf = task_id[-8:]
    for b in cands:
        if suf and suf in b:
            return b
    return None
