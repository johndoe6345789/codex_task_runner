import pytest
import tempfile
from pathlib import Path
from codex_task_runner.etc.ensure_dir import ensure_dir


def test_ensure_dir() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "a" / "b" / "c"
        result = ensure_dir(path)
        assert result == path
        assert path.exists()
        assert path.is_dir()
