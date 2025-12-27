from __future__ import annotations

from typing import Any, List

from .codex_parse_item import parse_item


def parse_tasks(obj: Any) -> List:
    items = obj.get("items") or []
    return [parse_item(i) for i in items if isinstance(i, dict)]
