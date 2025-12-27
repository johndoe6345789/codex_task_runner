from __future__ import annotations

import json
from typing import Any

from .proc_run import run_ok, run


def pr_exists_open(repo: str, head: str) -> int | None:
    out = run_ok(["gh", "pr", "list", "--repo", repo, "--head", head,
                  "--state", "open", "--json", "number"])
    data = json.loads(out)
    if not data:
        return None
    return int(data[0]["number"])


def create_pr(repo: str, base: str, head: str, title: str, body: str,
              draft: bool, dry_run: bool) -> int | None:
    if dry_run:
        return None
    cmd = ["gh", "pr", "create", "--repo", repo, "--base", base,
           "--head", head, "--title", title, "--body", body]
    if draft:
        cmd.append("--draft")
    r = run(cmd)
    if r.code != 0:
        return None
    return _parse_created_number(r.out)


def _parse_created_number(out: str) -> int | None:
    for line in out.splitlines():
        if "/pull/" in line:
            m = line.rsplit("/pull/", 1)[-1]
            m = m.strip().split()[0]
            if m.isdigit():
                return int(m)
    return None


def merge_pr(repo: str, number: int, method: Any, delete_branch: bool,
             admin: bool, auto: bool, dry_run: bool) -> bool:
    if dry_run:
        return True
    cmd = ["gh", "pr", "merge", str(number), "--repo", repo,
           f"--{method.value}"]
    cmd += ["--delete-branch"] if delete_branch else []
    cmd += ["--admin"] if admin else []
    cmd += ["--auto"] if auto else []
    r = run(cmd)
    return r.code == 0


def list_branches(repo: str, limit: int) -> list[str]:
    r = run(["gh", "api", f"repos/{repo}/branches",
             "-F", f"per_page={limit}"])
    if r.code != 0:
        if "Not Found (HTTP 404)" in (r.err or ""):
            return []
        raise RuntimeError(f"Command failed: ['gh', 'api', 'repos/{repo}/branches']\n{r.err}")
    data = json.loads(r.out)
    return [str(b.get("name")) for b in data if isinstance(b, dict)]


def _api(args: list[str]) -> Any:
    out = run_ok(["gh", "api", *args])
    return json.loads(out)


def _graphql(query: str, variables: dict[str, Any]) -> Any:
    payload = json.dumps({"query": query, "variables": variables})
    return _api(["graphql", "-f", f"query={query}", "-f", f"variables={payload}"])


def _vars(repo: str, number: int) -> dict[str, Any]:
    owner, name = repo.split("/", 1)
    return {"owner": owner, "name": name, "number": number}
