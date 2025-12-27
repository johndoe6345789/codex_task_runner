import pytest
from unittest.mock import MagicMock
from codex_task_runner.codex.json_get import _json_get


def test_json_get_success() -> None:
    session = MagicMock()
    session.get.return_value.json.return_value = {"key": "value"}
    session.get.return_value.raise_for_status = MagicMock()
    result = _json_get(session, "http://example.com/api")
    assert result == {"key": "value"}


def test_json_get_failure() -> None:
    session = MagicMock()
    session.get.side_effect = Exception("Network error")
    result = _json_get(session, "http://example.com/api")
    assert result is None
