from __future__ import annotations

import re


def slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "task"


def words(text: str) -> list[str]:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return [w for w in s.split() if w]
