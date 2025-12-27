import pytest
import tempfile
from codex_task_runner.etc.io import read_all


@pytest.mark.parametrize("content", [
    "hello world",
    "line1\nline2\nline3",
    "",
    "unicode: 日本語",
])
def test_io(content: str) -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(content)
        path = f.name
    result = read_all(path)
    assert result == content
