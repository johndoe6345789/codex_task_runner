"""Flask application factory for codex-task-runner API."""

from __future__ import annotations

import json
import os
from argparse import Namespace
from functools import wraps
from pathlib import Path
from typing import Any, Callable

from flask import Flask, jsonify, request, send_from_directory

from codex_task_runner.codex.codex_session import session_from_env
from codex_task_runner.handlers import (
    archive,
    create_pr,
    dedup_prs,
    discover,
    me,
    patch,
    ping,
    poll,
    prompt,
    run,
    task,
    tasks,
    turns,
    yolo,
)


def create_app(env_path: str | None = None) -> Flask:
    """Create and configure the Flask application.
    
    Args:
        env_path: Path to .env file with cookies/tokens. 
                  Defaults to .env in current directory.
    
    Returns:
        Configured Flask application.
    """
    static_folder = Path(__file__).parent / "static"
    app = Flask(__name__, static_folder=str(static_folder), static_url_path='')
    app.config["ENV_PATH"] = env_path or os.environ.get("CODEX_ENV_PATH", ".env")
    
    # Enable CORS for development
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        return response
    
    @app.before_request
    def handle_preflight():
        if request.method == 'OPTIONS':
            return '', 204
    
    def get_session():
        """Get a configured requests session for Codex API."""
        return session_from_env(app.config["ENV_PATH"])
    
    def handler_route(handler_module: Any, required_args: list[str] | None = None):
        """Decorator factory to create routes from handler modules.
        
        Args:
            handler_module: Handler module with a handle(args, session) function
            required_args: List of required argument names
        """
        required_args = required_args or []
        
        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def wrapper(*args, **kwargs):
                try:
                    # Build args namespace from URL params, query params, and JSON body
                    ns_dict = {}
                    
                    # Add URL path parameters
                    ns_dict.update(kwargs)
                    
                    # Add query parameters
                    for key in request.args:
                        val = request.args.get(key)
                        # Convert types
                        if val and val.isdigit():
                            ns_dict[key] = int(val)
                        elif val and val.lower() in ("true", "false"):
                            ns_dict[key] = val.lower() == "true"
                        else:
                            ns_dict[key] = val
                    
                    # Add JSON body parameters (if any)
                    if request.is_json and request.json:
                        ns_dict.update(request.json)
                    
                    # Check required arguments
                    missing = [arg for arg in required_args if arg not in ns_dict]
                    if missing:
                        return jsonify({
                            "error": "Missing required arguments",
                            "missing": missing
                        }), 400
                    
                    # Create args namespace
                    args_ns = Namespace(**ns_dict)
                    
                    # Get session and call handler
                    session = get_session()
                    result = handler_module.handle(args_ns, session)
                    
                    return jsonify({"success": True, "data": result})
                    
                except Exception as e:
                    return jsonify({
                        "success": False,
                        "error": str(e),
                        "error_type": type(e).__name__
                    }), 500
            
            return wrapper
        return decorator
    
    # Health check and static file serving
    @app.route("/")
    def index():
        # Serve React app if built
        index_path = static_folder / "index.html"
        if index_path.exists():
            return send_from_directory(app.static_folder, 'index.html')
        # Otherwise return API info
        return jsonify({
            "service": "codex-task-runner",
            "version": "1.0",
            "ui": "Build frontend with: cd frontend && npm install && npm run build",
            "endpoints": {
                "GET /": "This help message (or React UI if built)",
                "GET /api": "API endpoints list",
                "GET /health": "Health check",
                "GET /me": "Current user info",
                "GET /tasks": "List tasks (query: limit, filter)",
                "GET /tasks/<task_id>": "Get single task detail",
                "GET /tasks/<task_id>/turns": "Get turns for a task",
                "GET /tasks/<task_id>/patch": "Extract git patch (query: turn_id, raw)",
                "POST /tasks/<task_id>/archive": "Archive a task",
                "POST /tasks/<task_id>/create-pr": "Create PR for task (body: turn_id, dry_run)",
                "POST /prompt": "Send prompt to create new task (body: prompt_text, env_id, branch, best_of)",
                "GET /ping": "Ping a URL (query: url)",
                "POST /poll": "Poll URLs (body: urls, out)",
                "POST /yolo": "YOLO mode - auto process tasks (body: limit, repo, dry_run, no_confirm)",
                "POST /dedup-prs": "Find and close duplicate PRs (body: repo, dry_run)",
                "POST /run": "Run integration (body: dry_run, yolo, output_dir)",
            }
        })
    
    @app.route("/api")
    def api_info():
        return jsonify({
            "service": "codex-task-runner",
            "version": "1.0",
            "endpoints": {
                "GET /me": "Current user info",
                "GET /tasks": "List tasks (query: limit, filter)",
                "GET /tasks/<task_id>": "Get single task detail",
                "GET /tasks/<task_id>/turns": "Get turns for a task",
                "GET /tasks/<task_id>/patch": "Extract git patch",
                "POST /tasks/<task_id>/archive": "Archive a task",
                "POST /tasks/<task_id>/create-pr": "Create PR for task",
                "POST /prompt": "Send prompt to create new task",
            }
        })
    
    # Catch-all for SPA routing (must be before other routes don't match)
    @app.route('/<path:path>')
    def serve_static(path):
        # Try to serve static file
        file_path = static_folder / path
        if file_path.exists() and file_path.is_file():
            return send_from_directory(app.static_folder, path)
        # For SPA routing, serve index.html for non-API routes
        index_path = static_folder / "index.html"
        if index_path.exists() and not path.startswith(('api/', 'tasks/', 'me', 'ping', 'poll', 'yolo', 'prompt', 'health', 'run', 'dedup')):
            return send_from_directory(app.static_folder, 'index.html')
        # Otherwise 404
        return jsonify({"error": "Not found"}), 404
    
    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})
    
    # User info
    @app.route("/me")
    @handler_route(me)
    def get_me():
        pass
    
    # Tasks endpoints
    @app.route("/tasks")
    @handler_route(tasks)
    def list_tasks():
        """List tasks. Query params: limit (int), filter (current|archived|all)"""
        pass
    
    @app.route("/tasks/<task_id>")
    @handler_route(task, required_args=["task_id"])
    def get_task(task_id: str):
        """Get single task detail."""
        pass
    
    @app.route("/tasks/<task_id>/turns")
    @handler_route(turns, required_args=["task_id"])
    def get_turns(task_id: str):
        """Get turns for a task."""
        pass
    
    @app.route("/tasks/<task_id>/patch")
    @handler_route(patch, required_args=["task_id"])
    def get_patch(task_id: str):
        """Extract git patch. Query params: turn_id, raw (bool), output"""
        pass
    
    @app.route("/tasks/<task_id>/archive", methods=["POST"])
    @handler_route(archive, required_args=["task_id"])
    def archive_task(task_id: str):
        """Archive a task."""
        pass
    
    @app.route("/tasks/<task_id>/create-pr", methods=["POST"])
    @handler_route(create_pr, required_args=["task_id", "turn_id"])
    def create_pr_for_task(task_id: str):
        """Create PR for a task. Body params: turn_id, dry_run (bool)"""
        pass
    
    # Prompt endpoint
    @app.route("/prompt", methods=["POST"])
    @handler_route(prompt, required_args=["prompt_text"])
    def send_prompt():
        """Send prompt to create new task. 
        Body params: prompt_text, env_id, branch, best_of (int)
        """
        pass
    
    # Ping endpoint
    @app.route("/ping")
    @handler_route(ping, required_args=["url"])
    def ping_url():
        """Ping a URL. Query param: url"""
        pass
    
    # Poll endpoint
    @app.route("/poll", methods=["POST"])
    def poll_urls():
        """Poll multiple URLs.
        Body: {"urls": [...], "out": "output.json"}
        """
        try:
            data = request.get_json() or {}
            urls = data.get("urls", [])
            out = data.get("out", "poll.json")
            
            if not urls:
                return jsonify({"error": "No URLs provided"}), 400
            
            # Create temp file with URLs
            import tempfile
            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
                f.write("\n".join(urls))
                urls_file = f.name
            
            try:
                args = Namespace(urls_file=urls_file, out=out)
                session = get_session()
                result = poll.handle(args, session)
                return jsonify({"success": True, "data": result})
            finally:
                os.unlink(urls_file)
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }), 500
    
    # YOLO endpoint
    @app.route("/yolo", methods=["POST"])
    @handler_route(yolo)
    def yolo_mode():
        """YOLO mode - auto process tasks.
        Body params: verbose, limit, repo, no_confirm, dry_run, output_dir
        """
        pass
    
    # Dedup PRs endpoint
    @app.route("/dedup-prs", methods=["POST"])
    @handler_route(dedup_prs)
    def dedup_prs_endpoint():
        """Find and close duplicate PRs.
        Body params: repo, dry_run
        """
        pass
    
    # Run integration endpoint
    @app.route("/run", methods=["POST"])
    @handler_route(run)
    def run_integration():
        """Run integration.
        Body params: dry_run, yolo, output_dir
        """
        pass
    
    return app


def run_app(
    host: str = "127.0.0.1",
    port: int = 5000,
    debug: bool = False,
    env_path: str | None = None
):
    """Run the Flask application.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        debug: Enable debug mode
        env_path: Path to .env file
    """
    app = create_app(env_path)
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_app(debug=True)
