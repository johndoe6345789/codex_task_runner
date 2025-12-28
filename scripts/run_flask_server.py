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

import argparse
import sys
from pathlib import Path

# Add src to path if running directly
src_path = Path(__file__).parent.parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))


def main():
    parser = argparse.ArgumentParser(
        description="Run the codex-task-runner Flask API server"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to bind to (default: 5000)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "--env",
        default=".env",
        help="Path to .env file (default: .env)"
    )
    
    args = parser.parse_args()
    
    from codex_task_runner.flask_app.app import run_app
    
    print(f"🚀 Starting codex-task-runner API server")
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   Debug: {args.debug}")
    print(f"   Env: {args.env}")
    print(f"\n   API available at: http://{args.host}:{args.port}/")
    print(f"   Press Ctrl+C to stop\n")
    
    run_app(
        host=args.host,
        port=args.port,
        debug=args.debug,
        env_path=args.env
    )


if __name__ == "__main__":
    main()
