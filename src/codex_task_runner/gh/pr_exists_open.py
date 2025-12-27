from __future__ import annotations

import json

from codex_task_runner.proc.run_ok import run_ok


def pr_exists_open(repo: str, head: str) -> int | None:
    out = run_ok(["gh", "pr", "list", "--repo", repo, "--head", head,
                  "--state", "open", "--json", "number"])
    data = json.loads(out)
    if not data:
        return None
    return int(data[0]["number"])
