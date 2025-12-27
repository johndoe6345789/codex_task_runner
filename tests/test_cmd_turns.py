import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.cli.cmd_turns import turns_cmd


def test_cmd_turns() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.cli.cmd_turns.turns.handle") as mock_handle:
        mock_handle.return_value = {"turns": [{"id": 1}]}
        result = turns_cmd(session, "task-123")
        assert result == 0
