import pytest
from codex_task_runner.etc.pull_request import PullRequest


@pytest.mark.parametrize("number,url,title,author,state,mergeable,checks_state", [
    (1, "http://gh/1", "PR Title", "alice", "open", "MERGEABLE", "SUCCESS"),
    (42, "http://gh/42", "Fix", "bob", "open", "CONFLICTING", None),
])
def test_pull_request(number, url, title, author, state, mergeable, checks_state) -> None:
    pr = PullRequest(number=number, url=url, title=title, author=author, state=state, mergeable=mergeable, checks_state=checks_state)
    assert pr.number == number
    assert pr.url == url
    assert pr.title == title
    assert pr.author == author
    assert pr.state == state
    assert pr.mergeable == mergeable
    assert pr.checks_state == checks_state
