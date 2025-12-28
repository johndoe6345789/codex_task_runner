#!/usr/bin/env python3
import sys
import requests
from pathlib import Path

API = 'http://localhost:8080/api.php'

def fail(msg):
    print(msg)
    sys.exit(1)

def main():
    if len(sys.argv) < 3:
        fail('Usage: publish_to_wiki.py USERNAME PASSWORD [PAGE_TITLE]')

    username = sys.argv[1]
    password = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else 'MCP Integration'
    docpath = Path(__file__).resolve().parents[1] / 'docs' / 'MCP_INTEGRATION.md'
    if not docpath.exists():
        fail(f'Document not found: {docpath}')

    content = docpath.read_text()

    session = requests.Session()

    # 1) Get login token
    r = session.get(API, params={'action': 'query', 'meta': 'tokens', 'type': 'login', 'format': 'json'})
    r.raise_for_status()
    login_token = r.json()['query']['tokens']['logintoken']

    # 2) Log in
    r = session.post(API, data={'action': 'login', 'lgname': username, 'lgpassword': password, 'lgtoken': login_token, 'format': 'json'})
    r.raise_for_status()
    login_result = r.json()
    if login_result.get('login', {}).get('result') not in ('Success', 'NeedToken'):
        fail(f'Login failed: {login_result}')

    # 3) Get CSRF token
    r = session.get(API, params={'action': 'query', 'meta': 'tokens', 'format': 'json'})
    r.raise_for_status()
    csrf_token = r.json()['query']['tokens']['csrftoken']

    # 4) Edit/create page
    r = session.post(API, data={
        'action': 'edit',
        'title': title,
        'text': content,
        'token': csrf_token,
        'format': 'json'
    })
    r.raise_for_status()
    res = r.json()
    print('Edit result:')
    print(res)

if __name__ == '__main__':
    main()
