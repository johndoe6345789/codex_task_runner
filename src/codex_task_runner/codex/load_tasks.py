from __future__ import annotations

import json
from typing import List

from .parse_tasks import parse_tasks


def load_tasks(raw: str) -> List:
    obj = json.loads(raw)
    return parse_tasks(obj)
