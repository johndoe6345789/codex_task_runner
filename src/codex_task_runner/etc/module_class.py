from __future__ import annotations

from codex_task_runner.etc.config_class import Config
from codex_task_runner.etc.make_config import make_config


class EtcModule:
    """Aggregates configuration helpers."""

    Config = Config
    make_config = staticmethod(make_config)
