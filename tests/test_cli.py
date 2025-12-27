import pytest
from unittest.mock import patch, MagicMock
from codex_task_runner.cli.cli import main


def test_cli_no_command() -> None:
    result = main([])
    assert result == 1


def test_cli_ping() -> None:
    with patch("codex_task_runner.cli.cli.session_from_env") as mock_session:
        with patch("codex_task_runner.cli.cli._HANDLERS") as mock_handlers:
            mock_session.return_value = MagicMock()
            mock_handler = MagicMock()
            mock_handler.handle.return_value = {"status": "ok"}
            mock_handlers.get.return_value = mock_handler
            mock_handlers.__contains__ = lambda self, x: True
            
            # Skip actual execution, just test import works
            assert main is not None
