import pytest
import json
import tempfile
from pathlib import Path
from codex_task_runner.codex.codex_save import save_results


@pytest.mark.parametrize("data", [
    {"key": "value"},
    [1, 2, 3],
    {"nested": {"a": 1}},
])
def test_codex_save(data) -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    save_results(path, data)
    with open(path) as f:
        loaded = json.load(f)
    assert loaded == data
    Path(path).unlink()
