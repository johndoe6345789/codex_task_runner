from __future__ import annotations

import pathlib
import tempfile

from .timeutil import utc_stamp


def default_run_dir() -> pathlib.Path:
    root = pathlib.Path(tempfile.gettempdir())
    return root / "codex-task-runner" / utc_stamp()


def ensure_dir(path: pathlib.Path) -> pathlib.Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def append_text(path: pathlib.Path, text: str) -> None:
    ensure_dir(path.parent)
    with path.open("a", encoding="utf-8") as f:
        f.write(text)
