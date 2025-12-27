from __future__ import annotations

from .gh_api import list_branches
from .textutil import slugify, words


def find_head_branch(repo: str, title: str, task_id: str) -> str | None:
    slug = slugify(title)
    direct = f"codex/{slug}"
    branches = list_branches(repo, limit=100)
    if direct in branches:
        return direct
    return _fuzzy(branches, title, task_id)


def _fuzzy(branches: list[str], title: str, task_id: str) -> str | None:
    cands = [b for b in branches if b.startswith("codex/")]
    if not cands:
        return None
    by_words = _best_by_words(cands, title)
    if by_words:
        return by_words
    return _best_by_id(cands, task_id)


def _best_by_words(cands: list[str], title: str) -> str | None:
    ws = set(words(title))
    if not ws:
        return None
    scored = [(b, _word_score(b, ws)) for b in cands]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0] if scored[0][1] >= 2 else None


def _word_score(branch: str, ws: set[str]) -> int:
    bws = set(words(branch))
    return len(ws.intersection(bws))


def _best_by_id(cands: list[str], task_id: str) -> str | None:
    suf = task_id[-8:]
    for b in cands:
        if suf and suf in b:
            return b
    return None
