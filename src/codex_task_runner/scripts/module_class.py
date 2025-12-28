from __future__ import annotations

from codex_task_runner.scripts import (
    capture_task_creation,
    codex_cli,
    compute_coverage,
    convert_md_to_wikitext,
    count_defs,
    discover_create_task,
    discover_endpoints,
    poll_codex,
    probe_archive,
    probe_diff,
    probe_output_items,
    publish_to_wiki,
    run_codex_to_github,
    run_flask_server,
    run_tests,
    test_ui_screenshot,
)


class ScriptsModule:
    """Aggregates convenience script modules as attributes."""

    capture_task_creation = capture_task_creation
    codex_cli = codex_cli
    compute_coverage = compute_coverage
    convert_md_to_wikitext = convert_md_to_wikitext
    count_defs = count_defs
    discover_create_task = discover_create_task
    discover_endpoints = discover_endpoints
    poll_codex = poll_codex
    probe_archive = probe_archive
    probe_diff = probe_diff
    probe_output_items = probe_output_items
    publish_to_wiki = publish_to_wiki
    run_codex_to_github = run_codex_to_github
    run_flask_server = run_flask_server
    run_tests = run_tests
    test_ui_screenshot = test_ui_screenshot
