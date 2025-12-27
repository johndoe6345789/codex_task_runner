import pytest
from codex_task_runner.etc.task_ref import TaskRef


@pytest.mark.parametrize("task_id,title,repo,base,prs", [
    ("t1", "Title", "o/r", "main", ()),
    ("t2", "Other", "foo/bar", "dev", (1, 2, 3)),
])
def test_task_ref(task_id, title, repo, base, prs) -> None:
    t = TaskRef(task_id=task_id, title=title, repo=repo, base_branch=base, pr_numbers=prs)
    assert t.task_id == task_id
    assert t.title == title
    assert t.repo == repo
    assert t.base_branch == base
    assert t.pr_numbers == prs
