import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.codex.codex_poll import poll_urls


def test_codex_poll() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.codex.codex_poll.ping_url") as mock_ping:
        mock_ping.side_effect = [
            {"url": "http://a.com", "ok": True},
            {"url": "http://b.com", "ok": True},
        ]
        result = poll_urls(session, ["http://a.com", "http://b.com"])
        assert len(result) == 2


def test_codex_poll_skips_empty() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.codex.codex_poll.ping_url") as mock_ping:
        mock_ping.return_value = {"url": "http://a.com", "ok": True}
        result = poll_urls(session, ["http://a.com", "", "  "])
        assert len(result) == 1
