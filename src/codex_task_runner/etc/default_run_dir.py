from __future__ import annotations

import pathlib
import tempfile

from .timeutil import utc_stamp


def default_run_dir() -> pathlib.Path:
    root = pathlib.Path(tempfile.gettempdir())
    return root / "codex-task-runner" / utc_stamp()
