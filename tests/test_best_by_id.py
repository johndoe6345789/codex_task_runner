import pytest
from codex_task_runner.branch.best_by_id import best_by_id


@pytest.mark.parametrize("cands,task_id,expected", [
    (["codex/fix-abc12345", "main"], "task-abc12345", "codex/fix-abc12345"),
    (["main", "dev"], "task-abc12345", None),
    (["codex/xyz-12345678"], "id-12345678", "codex/xyz-12345678"),
    ([], "abc", None),
])
def test_best_by_id(cands: list, task_id: str, expected: str | None) -> None:
    assert best_by_id(cands, task_id) == expected
