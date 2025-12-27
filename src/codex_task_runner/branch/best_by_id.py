from __future__ import annotations


def best_by_id(cands: list[str], task_id: str) -> str | None:
    suf = task_id[-8:]
    for b in cands:
        if suf and suf in b:
            return b
    return None
