import pytest
import tempfile
import os
from codex_task_runner.codex.codex_session import session_from_env


def test_codex_session_basic() -> None:
    session = session_from_env(None)
    assert session is not None
    assert "User-Agent" in session.headers


def test_codex_session_with_env_file() -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("COOKIE=foo=bar\n")
        f.write("BEARER=test-token\n")
        env_path = f.name
    
    session = session_from_env(env_path)
    assert session is not None
    assert session.headers.get("Authorization") == "Bearer test-token"
    os.unlink(env_path)
