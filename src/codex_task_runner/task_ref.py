from dataclasses import dataclass


@dataclass(frozen=True)
class TaskRef:
    task_id: str
    title: str
    repo: str
    base_branch: str
    pr_numbers: tuple[int, ...]
