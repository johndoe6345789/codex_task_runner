from __future__ import annotations

from typing import Any

from codex_task_runner.etc.pull_request import PullRequest
from .gh_graphql import gh_graphql
from .gh_vars import gh_vars


_PR_QUERY = """query($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      number
      title
      url
      mergeable
      author { login }
      commits(last: 1) {
        nodes {
          commit {
            statusCheckRollup { state }
          }
        }
      }
    }
  }
}
"""


def get_pr(repo: str, number: int) -> PullRequest:
    v = gh_vars(repo, number)
    data = gh_graphql(_PR_QUERY, v)
    node = data["data"]["repository"]["pullRequest"]
    return _parse_pr(node)


def _parse_pr(node: Any) -> PullRequest:
    checks = _checks_state(node.get("commits"))
    return PullRequest(
        number=int(node["number"]),
        url=str(node["url"]),
        title=str(node["title"]),
        author=str(node["author"]["login"]),
        mergeable=str(node.get("mergeable") or ""),
        checks_state=checks,
    )


def _checks_state(commits: Any) -> str | None:
    nodes = (commits or {}).get("nodes") or []
    if not nodes:
        return None
    rollup = nodes[0].get("commit", {}).get("statusCheckRollup")
    return None if rollup is None else str(rollup.get("state"))
