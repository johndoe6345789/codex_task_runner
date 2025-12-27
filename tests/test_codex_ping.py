import pytest
from unittest.mock import MagicMock
from codex_task_runner.codex.codex_ping import ping_url


def test_codex_ping_success() -> None:
    session = MagicMock()
    response = MagicMock()
    response.status_code = 200
    response.ok = True
    response.text = "Hello World"
    session.get.return_value = response
    
    result = ping_url(session, "http://example.com")
    assert result["url"] == "http://example.com"
    assert result["status_code"] == 200
    assert result["ok"] is True


def test_codex_ping_error() -> None:
    session = MagicMock()
    session.get.side_effect = Exception("Connection error")
    
    result = ping_url(session, "http://example.com")
    assert result["url"] == "http://example.com"
    assert "error" in result
