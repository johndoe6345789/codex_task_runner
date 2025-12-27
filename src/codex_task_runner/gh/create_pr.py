from __future__ import annotations

from codex_task_runner.proc.run import run


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
