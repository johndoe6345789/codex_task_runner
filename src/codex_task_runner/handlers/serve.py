"""Handler for the 'serve' CLI command - starts Flask API server."""

from typing import Any


def handle(args: Any, session) -> dict:
    """Start the Flask API server.
    
    Note: This handler doesn't use the session as it starts a long-running server.
    The session is created per-request in the Flask app.
    """
    from codex_task_runner.flask_app.app import run_app
    
    host = getattr(args, "host", "127.0.0.1")
    port = getattr(args, "port", 5000)
    debug = getattr(args, "debug", False)
    env_path = getattr(args, "env", ".env")
    
    print(f"Starting Flask server at http://{host}:{port}")
    print(f"Using env file: {env_path}")
    print("Press Ctrl+C to stop")
    
    # This blocks until server is stopped
    run_app(host=host, port=port, debug=debug, env_path=env_path)
    
    return {"status": "stopped"}
