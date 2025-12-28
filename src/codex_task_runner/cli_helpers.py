"""CLI helper utilities for `codex_task_runner`.

Currently contains MediaWiki publish helper used by CLI subcommands and scripts.
"""
from __future__ import annotations

import requests
from pathlib import Path
from typing import Optional


def publish_to_wiki(username: str, password: str, title: str = "MCP Integration", docpath: Optional[Path] = None, api: str = "http://localhost:8080/api.php") -> dict:
    """Publish a document to a MediaWiki instance using the API.

    Returns the JSON response from the edit API call.
    Raises requests.HTTPError for HTTP-level errors.
    """
    if docpath is None:
        docpath = Path(__file__).resolve().parents[3] / 'docs' / 'MCP_INTEGRATION.md'
    else:
        docpath = Path(docpath)

    if not docpath.exists():
        raise FileNotFoundError(f"Document not found: {docpath}")

    content = docpath.read_text(encoding='utf-8')

    session = requests.Session()

    # 1) Get login token
    r = session.get(api, params={'action': 'query', 'meta': 'tokens', 'type': 'login', 'format': 'json'})
    r.raise_for_status()
    login_token = r.json()['query']['tokens']['logintoken']

    # 2) Log in
    r = session.post(api, data={'action': 'login', 'lgname': username, 'lgpassword': password, 'lgtoken': login_token, 'format': 'json'})
    r.raise_for_status()
    login_result = r.json()
    if login_result.get('login', {}).get('result') not in ('Success', 'NeedToken'):
        raise RuntimeError(f'Login failed: {login_result}')

    # 3) Get CSRF token
    r = session.get(api, params={'action': 'query', 'meta': 'tokens', 'format': 'json'})
    r.raise_for_status()
    csrf_token = r.json()['query']['tokens']['csrftoken']

    # 4) Edit/create page
    r = session.post(api, data={
        'action': 'edit',
        'title': title,
        'text': content,
        'token': csrf_token,
        'format': 'json'
    })
    r.raise_for_status()
    return r.json()


def md_to_wiki(md: str) -> str:
    """Convert a subset of Markdown to MediaWiki wikitext.

    This implements a small, pragmatic converter used by the project docs.
    """
    import re

    out = []
    in_code = False
    for line in md.splitlines():
        if line.startswith('```'):
            if not in_code:
                in_code = True
                out.append('<pre>')
            else:
                in_code = False
                out.append('</pre>')
            continue
        if in_code:
            out.append(line)
            continue

        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            hashes, title = m.groups()
            level = len(hashes)
            if level == 1:
                out.append('== ' + title.strip() + ' ==')
            else:
                out.append('=' * (level + 1) + ' ' + title.strip() + ' ' + '=' * (level + 1))
            continue

        if re.match(r'^\s*[-\*]\s+', line):
            out.append(re.sub(r'^\s*[-\*]\s+', '* ', line))
            continue

        # Inline code: `code` -> <code>code</code>
        line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)

        out.append(line)

    return '\n'.join(out)


def convert_md_to_wikitext(src: Optional[Path] = None, dest: Optional[Path] = None) -> Path:
    """Convert a Markdown file to a .wiki file.

    If `src` is None, uses `docs/MCP_SESSION_AND_APP.md` relative to the project root.
    Returns the path to the written `.wiki` file.
    """
    if src is None:
        src = Path(__file__).resolve().parents[3] / 'docs' / 'MCP_SESSION_AND_APP.md'
    src = Path(src)
    if not src.exists():
        raise FileNotFoundError(f'Source markdown not found: {src}')

    md = src.read_text(encoding='utf-8')
    wiki = md_to_wiki(md)

    if dest is None:
        dest = src.with_name(src.stem + '.wiki')
    dest = Path(dest)
    dest.write_text(wiki, encoding='utf-8')
    return dest


def compute_coverage(qmldir_path: Optional[Path] = None, react_glob_patterns: Optional[list] = None) -> dict:
    """Compute mapping of React fake UI components to QML registered components.

    Returns a dict with keys: react_names (set), qml_names (set), matched (list of tuples), missing (list)
    """
    import glob
    import os

    if react_glob_patterns is None:
        react_glob_patterns = ['frontend/src/fakemui/**/*.jsx', 'frontend/src/fakemui/**/*.js']

    react_files = []
    for p in react_glob_patterns:
        react_files.extend(glob.glob(p, recursive=True))

    react_names = set(os.path.splitext(os.path.basename(p))[0] for p in react_files)

    if qmldir_path is None:
        qmldir_path = Path(__file__).resolve().parents[3] / 'src' / 'codex_task_runner' / 'ui' / 'qml' / 'fakemui' / 'qmldir'
    else:
        qmldir_path = Path(qmldir_path)

    if not qmldir_path.exists():
        raise FileNotFoundError(f'qmldir not found: {qmldir_path}')

    qml = qmldir_path.read_text(encoding='utf-8')
    qml_names = set()
    for line in qml.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        qml_names.add(parts[0])

    matched = []
    missing = []
    for rn in sorted(react_names):
        cname = 'C' + rn if not rn.startswith('C') else rn
        if cname in qml_names:
            matched.append((rn, cname))
        else:
            missing.append(rn)

    return {
        'react_names': react_names,
        'qml_names': qml_names,
        'matched': matched,
        'missing': missing,
    }


def poll_codex_urls(env_path: str = '.env', urls_path: str = 'urls.txt', out_path: str = 'run_poll.json') -> Path:
    """Poll a list of URLs using the codex cloud session and save results to JSON.

    Uses `codex_task_runner.codex_cloud.session_from_env`, `poll_urls`, and `save_results`.
    Returns the path to the saved JSON file.
    """
    from codex_task_runner.codex_cloud import session_from_env, poll_urls, save_results
    from pathlib import Path

    sess = session_from_env(env_path)
    p = Path(urls_path)
    if not p.exists():
        raise FileNotFoundError(f'urls file not found: {urls_path}')
    urls = [l.strip() for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]
    if not urls:
        raise RuntimeError('no urls to poll')

    results = {"main": None, "polls": []}
    results["main"] = poll_urls(sess, [urls[0]])[0]
    if len(urls) > 1:
        results["polls"] = poll_urls(sess, urls[1:])

    save_results(out_path, results)
    return Path(out_path)


def run_codex_to_github(env_path: str = '.env', dry_run: bool = True, limit: int = 20) -> int:
    """Run fetch from Codex Cloud and process tasks locally.

    Returns the number of processed tasks (0 on failure).
    """
    from codex_task_runner.codex_cloud import session_from_env, get_tasks_list
    from codex_task_runner.runner import make_config, process_tasks

    sess = session_from_env(env_path)
    tasks = get_tasks_list(sess, limit=limit)
    if not tasks:
        return 0
    cfg = make_config(require_checks=False, method="merge", keep_branch=False, admin=False, auto=False, dry_run=dry_run, output_dir=None)
    process_tasks(cfg, tasks)
    return len(tasks)
