from __future__ import annotations

import json
from typing import Any

from .gh_api_call import gh_api


def gh_graphql(query: str, variables: dict[str, Any]) -> Any:
    # Build the command with individual -F flags for each variable
    cmd = ["graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        # Use -F for non-string values (numbers, etc.) and -f for strings
        if isinstance(value, str):
            cmd.extend(["-f", f"{key}={value}"])
        else:
            cmd.extend(["-F", f"{key}={value}"])
    return gh_api(cmd)
