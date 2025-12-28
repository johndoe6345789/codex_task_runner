"""Handler for launching the PyQt6 UI."""


def handle(args, session):
    """Launch the desktop UI."""
    from ..ui import launch
    return launch(session)
