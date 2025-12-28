#!/usr/bin/env python3
"""Probe for archive endpoint."""
from codex_task_runner.codex.codex_session import session_from_env

session = session_from_env('.env')

# Get a task ID first
resp = session.get('https://chatgpt.com/backend-api/wham/tasks/list?limit=1&task_filter=current')
print('List status:', resp.status_code)
if resp.ok:
    data = resp.json()
    if data.get('items'):
        task_id = data['items'][0]['id']
        print(f'Task ID: {task_id}')
        
        base = f'https://chatgpt.com/backend-api/wham/tasks/{task_id}'
        
        # Try POST to /archive (common pattern)
        r = session.post(f'{base}/archive', json={})
        print(f'POST /archive: {r.status_code}')
        if r.text:
            print(f'  Response: {r.text[:300]}')
        
        # Try PATCH to task with archived flag
        r = session.patch(base, json={'archived': True})
        print(f'PATCH archived=true: {r.status_code}')
        if r.text:
            print(f'  Response: {r.text[:300]}')
            
        # Try POST with status
        r = session.post(f'{base}/status', json={'status': 'archived'})
        print(f'POST /status: {r.status_code}')
        if r.text:
            print(f'  Response: {r.text[:300]}')
