import pytest
from codex_task_runner.etc.default_run_dir import default_run_dir


def test_default_run_dir() -> None:
    d = default_run_dir()
    assert "codex-task-runner" in str(d)
    assert d.parts[-2] == "codex-task-runner"
