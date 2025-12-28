from __future__ import annotations

from codex_task_runner.flask_app import app


class FlaskAppModule:
    """Aggregates Flask app entrypoint."""

    app = app
