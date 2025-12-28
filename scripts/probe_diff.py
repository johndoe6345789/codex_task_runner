#!/usr/bin/env python3
"""Probe for diff/patch endpoints."""
from codex_task_runner.codex.codex_session import session_from_env
import json

session = session_from_env('.env')

# Get a task with turns
resp = session.get('https://chatgpt.com/backend-api/wham/tasks/list?limit=1&task_filter=current')
if resp.ok:
    data = resp.json()
    if data.get('items'):
        task_id = data['items'][0]['id']
        print(f'Task ID: {task_id}')
        
        # Get task detail - check for diffs
        r = session.get(f'https://chatgpt.com/backend-api/wham/tasks/{task_id}')
        if r.ok:
            task_data = r.json()
            print(f'Task detail keys: {list(task_data.keys())}')
            # Check if diff data is embedded
            for key in ['diffs', 'patch', 'changes', 'diff', 'code_changes']:
                if key in task_data:
                    print(f'Found {key}: {str(task_data[key])[:200]}')
        
        # Get turns
        r = session.get(f'https://chatgpt.com/backend-api/wham/tasks/{task_id}/turns')
        if r.ok:
            turns_data = r.json()
            current_turn = turns_data.get('current_turn_id')
            print(f'Current turn: {current_turn}')
            
            # Check turn_mapping for diff data
            if 'turn_mapping' in turns_data and current_turn in turns_data['turn_mapping']:
                turn = turns_data['turn_mapping'][current_turn].get('turn', {})
                print(f'Turn keys: {list(turn.keys())}')
                for key in ['diffs', 'patch', 'changes', 'diff', 'code_changes', 'content']:
                    if key in turn:
                        val = str(turn[key])
                        print(f'Turn {key}: {val[:300]}...' if len(val) > 300 else f'Turn {key}: {val}')
            
            # Probe for diff endpoints
            base = f'https://chatgpt.com/backend-api/wham/tasks/{task_id}'
            
            for endpoint in ['/diff', '/patch', '/changes', f'/turns/{current_turn}/diff', f'/turns/{current_turn}/patch', f'/turns/{current_turn}/changes', f'/turns/{current_turn}/code']:
                r = session.get(f'{base}{endpoint}')
                print(f'GET {endpoint}: {r.status_code}')
                if r.ok and r.text:
                    print(f'  Preview: {r.text[:300]}')
