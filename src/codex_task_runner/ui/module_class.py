from __future__ import annotations

from codex_task_runner.ui import main
from codex_task_runner.ui import fakemui
from codex_task_runner.ui import qml
from codex_task_runner.ui import controllers
from codex_task_runner.ui import services


class UiModule:
    """Aggregates UI entrypoints and helpers."""

    main = main
    fakemui = fakemui
    qml = qml
    controllers = controllers
    services = services
