import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.cli.cmd_create_pr import create_pr_cmd


def test_cmd_create_pr_dry_run() -> None:
    session = MagicMock()
    result = create_pr_cmd(session, "task-123", "turn-1", dry_run=True)
    assert result == 0


def test_cmd_create_pr() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.cli.cmd_create_pr.create_pr.handle") as mock_handle:
        mock_handle.return_value = {"pr_url": "http://github.com/pr/1"}
        result = create_pr_cmd(session, "task-123", "turn-1", dry_run=False)
        assert result == 0
