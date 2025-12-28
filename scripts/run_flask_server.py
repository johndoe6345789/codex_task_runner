#!/usr/bin/env python3
"""Standalone script to run the Flask API server.

Usage:
    python -m codex_task_runner.flask_app.run_server [options]
    
    # Or directly:
    python scripts/run_flask_server.py [options]

Options:
    --host HOST     Host to bind to (default: 127.0.0.1)
    --port PORT     Port to bind to (default: 5000)
    --debug         Enable debug mode
    --env PATH      Path to .env file (default: .env)
"""


# Add src to path if running directly


    
    
    
    


"""Shim to start the Flask server via the package CLI.

This script remains for compatibility; it delegates to the package CLI.
"""
from __future__ import annotations

import sys

from codex_task_runner.cli.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
