import pytest
from unittest.mock import patch
from codex_task_runner.proc.run_ok import run_ok
from codex_task_runner.proc.proc_result import ProcResult


def test_run_ok_success() -> None:
    with patch("codex_task_runner.proc.run_ok.run") as mock_run:
        mock_run.return_value = ProcResult(code=0, out="output", err="")
        result = run_ok(["echo", "hello"])
        assert result == "output"


def test_run_ok_failure() -> None:
    with patch("codex_task_runner.proc.run_ok.run") as mock_run:
        mock_run.return_value = ProcResult(code=1, out="", err="error msg")
        with pytest.raises(RuntimeError, match="Command failed"):
            run_ok(["false"])
