import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.cli.cmd_ping import ping_cmd


def test_cmd_ping() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.cli.cmd_ping.ping.handle") as mock_handle:
        mock_handle.return_value = {"status": "ok", "url": "http://example.com"}
        result = ping_cmd(session, "http://example.com")
        assert result == 0
