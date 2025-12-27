"""Prompt user for confirmation."""
from ..etc.log import log


def confirm(message: str) -> bool:
    """Prompt user for confirmation. Returns True if confirmed."""
    try:
        response = input(f"{message} [y/N] ")
        return response.lower() == 'y'
    except (EOFError, KeyboardInterrupt):
        log.info("Aborted")
        return False
