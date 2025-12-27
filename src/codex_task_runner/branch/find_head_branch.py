from __future__ import annotations

from codex_task_runner.etc.slugify import slugify
from codex_task_runner.gh.list_branches import list_branches
from .fuzzy_branch import fuzzy_branch


def find_head_branch(repo: str, title: str, task_id: str) -> str | None:
	slug = slugify(title)
	direct = f"codex/{slug}"
	branches = list_branches(repo, limit=100)
	if direct in branches:
		return direct
	return fuzzy_branch(branches, title, task_id)

__all__ = ["find_head_branch"]
