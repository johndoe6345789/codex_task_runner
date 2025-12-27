from __future__ import annotations

import json
from typing import Any

from .gh_api_call import gh_api


def gh_graphql(query: str, variables: dict[str, Any]) -> Any:
    payload = json.dumps({"query": query, "variables": variables})
    return gh_api(["graphql", "-f", f"query={query}", "-f", f"variables={payload}"])
