import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.handlers.ping import handle


def test_ping_handler() -> None:
    args = MagicMock()
    args.url = "http://example.com"
    session = MagicMock()
    
    with patch("codex_task_runner.handlers.ping.ping_url") as mock_ping:
        mock_ping.return_value = {"status": "ok"}
        result = handle(args, session)
        assert result == {"status": "ok"}
