import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.cli.cmd_task import task_cmd


def test_cmd_task() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.cli.cmd_task.task.handle") as mock_handle:
        mock_handle.return_value = {"id": "task-123", "title": "Test"}
        result = task_cmd(session, "task-123")
        assert result == 0


def test_cmd_task_not_found() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.cli.cmd_task.task.handle") as mock_handle:
        mock_handle.return_value = None
        result = task_cmd(session, "nonexistent")
        assert result == 0
