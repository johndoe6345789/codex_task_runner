import pytest
from unittest.mock import MagicMock
from codex_task_runner.codex.json_post import _json_post


def test_json_post_success() -> None:
    session = MagicMock()
    session.post.return_value.json.return_value = {"result": "ok"}
    session.post.return_value.raise_for_status = MagicMock()
    result = _json_post(session, "http://example.com/api", data={"input": "test"})
    assert result == {"result": "ok"}


def test_json_post_failure() -> None:
    session = MagicMock()
    session.post.side_effect = Exception("Network error")
    result = _json_post(session, "http://example.com/api")
    assert result is None
