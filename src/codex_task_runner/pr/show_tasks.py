"""Show task list and return summary."""
from ..etc.log import log


def show_tasks(tasks: list) -> tuple[list, list]:
    """Log task list and return (needs_pr, has_pr) lists."""
    log.info("")
    log.info("Tasks to process:")
    needs_pr = []
    has_pr = []
    for t in tasks:
        if t.pr_numbers:
            has_pr.append(t)
            log.info(f"  - {t.repo}: {t.title[:50]} (PR #{t.pr_numbers[0]})")
        else:
            needs_pr.append(t)
            log.info(f"  - {t.repo}: {t.title[:50]} (needs PR)")
    log.info("")
    return needs_pr, has_pr
