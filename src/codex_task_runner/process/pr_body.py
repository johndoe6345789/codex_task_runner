from __future__ import annotations


def pr_body(task_id: str) -> str:
    return f"\n------\n[Codex Task](https://chatgpt.com/codex/tasks/{task_id})\n"
