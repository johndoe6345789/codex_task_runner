from __future__ import annotations

import json
from typing import Any

from ..proc.run_ok import run_ok


def gh_api(args: list[str]) -> Any:
    out = run_ok(["gh", "api", *args])
    return json.loads(out)
