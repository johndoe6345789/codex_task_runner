import pytest
import tempfile
from unittest.mock import MagicMock, patch
from codex_task_runner.handlers.poll import handle


def test_poll_handler() -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("http://url1.com\nhttp://url2.com\n")
        urls_path = f.name
    
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as out_f:
        out_path = out_f.name
    
    args = MagicMock()
    args.urls_file = urls_path
    args.out = out_path
    session = MagicMock()
    
    with patch("codex_task_runner.handlers.poll.poll_urls") as mock_poll:
        with patch("codex_task_runner.handlers.poll.save_results") as mock_save:
            mock_poll.return_value = [{"url": "http://url1.com", "status": "ok"}]
            result = handle(args, session)
            assert result == {"saved": out_path}
