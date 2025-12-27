import pytest
from codex_task_runner.branch.fuzzy_branch import fuzzy_branch


@pytest.mark.parametrize("branches,title,task_id,expected", [
    (["codex/add-button", "main"], "Add button", "task123", "codex/add-button"),
    (["main", "dev"], "Add button", "task123", None),
    (["codex/fix-12345678"], "Other", "id-12345678", "codex/fix-12345678"),
    ([], "Title", "task", None),
])
def test_fuzzy_branch(branches, title, task_id, expected) -> None:
    assert fuzzy_branch(branches, title, task_id) == expected
