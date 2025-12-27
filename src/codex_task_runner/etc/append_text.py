from __future__ import annotations

import pathlib

from .ensure_dir import ensure_dir


def append_text(path: pathlib.Path, text: str) -> None:
    ensure_dir(path.parent)
    with path.open("a", encoding="utf-8") as f:
        f.write(text)
