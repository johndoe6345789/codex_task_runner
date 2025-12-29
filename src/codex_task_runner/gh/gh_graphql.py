from __future__ import annotations

import json
from typing import Any

from .gh_api_call import gh_api


def gh_graphql(query: str, variables: dict[str, Any]) -> Any:
    variables_json = json.dumps(variables)
    return gh_api(["graphql", "-f", f"query={query}", "-f", f"variables={variables_json}"])
