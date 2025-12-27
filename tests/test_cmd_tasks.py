import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.cli.cmd_tasks import tasks_cmd


def test_cmd_tasks() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.cli.cmd_tasks.tasks.handle") as mock_handle:
        mock_handle.return_value = [{"task_id": "t1"}, {"task_id": "t2"}]
        result = tasks_cmd(session, limit=10)
        assert result == 0
