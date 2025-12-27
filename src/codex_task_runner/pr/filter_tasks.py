"""Filter tasks by repo."""


def filter_tasks(tasks: list, repo: str | None) -> list:
    """Filter tasks by repo. Returns filtered list."""
    if not repo:
        return tasks
    return [t for t in tasks if t.repo == repo]
