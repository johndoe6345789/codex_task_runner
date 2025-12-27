import pytest
from codex_task_runner.types import PullRequest
from codex_task_runner.pr.fmt_pr import fmt_pr


@pytest.mark.parametrize("number,title,url,author", [
    (1, "Add feature", "http://gh/1", "alice"),
    (42, "Fix bug", "http://gh/42", "bob"),
])
def test_fmt_pr(number: int, title: str, url: str, author: str) -> None:
    pr = PullRequest(number=number, title=title, url=url, author=author, mergeable="MERGEABLE", checks_state="SUCCESS")
    result = fmt_pr(pr)
    assert str(number) in result
    assert title in result
    assert author in result
