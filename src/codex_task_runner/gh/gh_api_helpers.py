from __future__ import annotations

import json
from typing import Any

from ..proc.proc_run import run_ok


def _api(args: list[str]) -> Any:
    out = run_ok(["gh", "api", *args])
    return json.loads(out)


def _graphql(query: str, variables: dict[str, Any]) -> Any:
    payload = json.dumps({"query": query, "variables": variables})
    return _api(["graphql", "-f", f"query={query}", "-f", f"variables={payload}"])


def _vars(repo: str, number: int) -> dict[str, Any]:
    owner, name = repo.split("/", 1)
    return {"owner": owner, "name": name, "number": number}
