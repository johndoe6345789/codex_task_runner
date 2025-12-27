from __future__ import annotations

import json

from codex_task_runner.proc.run import run


def list_branches(repo: str, limit: int) -> list[str]:
    r = run(["gh", "api", f"repos/{repo}/branches",
             "-F", f"per_page={limit}"])
    if r.code != 0:
        if "Not Found (HTTP 404)" in (r.err or ""):
            return []
        raise RuntimeError(f"Command failed: ['gh', 'api', 'repos/{repo}/branches']\n{r.err}")
    data = json.loads(r.out)
    return [str(b.get("name")) for b in data if isinstance(b, dict)]
