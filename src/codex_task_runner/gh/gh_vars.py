from __future__ import annotations

from typing import Any


def gh_vars(repo: str, number: int) -> dict[str, Any]:
    owner, name = repo.split("/", 1)
    return {"owner": owner, "name": name, "number": number}
