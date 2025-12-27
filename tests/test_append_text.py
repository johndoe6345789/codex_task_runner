import pytest
import tempfile
from pathlib import Path
from codex_task_runner.etc.append_text import append_text


@pytest.mark.parametrize("texts", [
    (["hello", " world"]),
    (["line1\n", "line2\n"]),
])
def test_append_text(texts: list) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "sub" / "file.txt"
        for t in texts:
            append_text(path, t)
        assert path.exists()
        assert path.read_text() == "".join(texts)
