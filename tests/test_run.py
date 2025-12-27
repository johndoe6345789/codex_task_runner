import pytest
from unittest.mock import patch, MagicMock
from codex_task_runner.proc.run import run


def test_run_success() -> None:
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="hello", stderr="")
        result = run(["echo", "hello"])
        assert result.code == 0
        assert result.out == "hello"
        assert result.err == ""


def test_run_failure() -> None:
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")
        result = run(["false"])
        assert result.code == 1
        assert result.err == "error"
