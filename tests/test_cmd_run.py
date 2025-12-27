import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.cli.cmd_run import run_cmd


def test_cmd_run_success() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.cli.cmd_run.run.handle") as mock_handle:
        mock_handle.return_value = {"processed": 5}
        result = run_cmd(session, dry_run=True, output_dir="/tmp")
        assert result == 0


def test_cmd_run_no_tasks() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.cli.cmd_run.run.handle") as mock_handle:
        mock_handle.return_value = {"processed": 0, "error": "no tasks"}
        result = run_cmd(session, dry_run=False, output_dir=None)
        assert result == 1
