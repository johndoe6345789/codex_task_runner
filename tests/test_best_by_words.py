import pytest
from codex_task_runner.branch.best_by_words import best_by_words


@pytest.mark.parametrize("cands,title,expected", [
    (["codex/add-button-feature", "main"], "Add button feature", "codex/add-button-feature"),
    (["main", "dev"], "Something else", None),
    (["codex/fix-login-bug"], "Fix login bug", "codex/fix-login-bug"),
    ([], "Add feature", None),
    (["main"], "", None),
])
def test_best_by_words(cands: list, title: str, expected: str | None) -> None:
    assert best_by_words(cands, title) == expected
