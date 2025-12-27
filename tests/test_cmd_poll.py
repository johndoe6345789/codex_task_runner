import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.cli.cmd_poll import poll_cmd


def test_cmd_poll() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.cli.cmd_poll.poll.handle") as mock_handle:
        mock_handle.return_value = {"saved": "/tmp/out.json"}
        result = poll_cmd(session, "/tmp/urls.txt", "/tmp/out.json")
        assert result == 0
