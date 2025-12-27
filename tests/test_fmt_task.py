import pytest
from codex_task_runner.types import TaskRef
from codex_task_runner.process.fmt_task import fmt_task


@pytest.mark.parametrize("task_id,title,repo,base,prs", [
    ("t1", "Add feature", "o/r", "main", ()),
    ("t2", "Fix bug", "foo/bar", "dev", (1, 2)),
])
def test_fmt_task(task_id: str, title: str, repo: str, base: str, prs: tuple) -> None:
    t = TaskRef(task_id=task_id, title=title, repo=repo, base_branch=base, pr_numbers=prs)
    result = fmt_task(t)
    assert task_id in result
    assert title in result
    assert repo in result
