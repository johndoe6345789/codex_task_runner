from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PullRequest:
    number: int
    url: str
    title: str
    author: str
    state: str
    mergeable: str
    checks_state: Optional[str]
