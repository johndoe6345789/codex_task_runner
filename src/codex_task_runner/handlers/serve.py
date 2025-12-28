"""Handler for the 'serve' CLI command - starts Flask API server."""

import socket
from typing import Any


def find_available_port(host: str, start_port: int, max_attempts: int = 100) -> int:
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No available port found in range {start_port}-{start_port + max_attempts}")


def handle(args: Any, session) -> dict:
    """Start the Flask API server.
    
    Note: This handler doesn't use the session as it starts a long-running server.
    The session is created per-request in the Flask app.
    """
    from codex_task_runner.flask_app.app import run_app
    
    host = getattr(args, "host", "127.0.0.1")
    requested_port = getattr(args, "port", 5000)
    debug = getattr(args, "debug", False)
    env_path = getattr(args, "env", ".env")
    
    # Find available port
    port = find_available_port(host, requested_port)
    
    if port != requested_port:
        print(f"⚠️  Port {requested_port} is in use, using port {port} instead")
    
    url = f"http://{host}:{port}"
    print(f"\n🚀 Starting Codex Task Runner API server")
    print(f"   URL: \033[1;36m{url}\033[0m")
    print(f"   Env: {env_path}")
    print(f"\n   Press Ctrl+C to stop\n")
    
    # This blocks until server is stopped
    run_app(host=host, port=port, debug=debug, env_path=env_path)
    
    return {"status": "stopped"}
