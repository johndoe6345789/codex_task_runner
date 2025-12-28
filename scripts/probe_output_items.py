#!/usr/bin/env python3
"""Examine turn output_items for diff/code data."""
from codex_task_runner.codex.codex_session import session_from_env
import json

session = session_from_env('.env')

resp = session.get('https://chatgpt.com/backend-api/wham/tasks/list?limit=1&task_filter=current')
data = resp.json()
task_id = data['items'][0]['id']
print(f'Task: {task_id}')

# Get turns
r = session.get(f'https://chatgpt.com/backend-api/wham/tasks/{task_id}/turns')
turns_data = r.json()
current_turn = turns_data.get('current_turn_id')

# Look at turn structure
turn_info = turns_data['turn_mapping'][current_turn]['turn']
print(f'output_items type: {type(turn_info.get("output_items"))}')
output_items = turn_info.get('output_items', [])
print(f'output_items count: {len(output_items)}')

for i, item in enumerate(output_items[:10]):
    item_type = item.get('type', 'unknown')
    print(f'\nItem {i}: type={item_type}')
    print(f'  keys: {list(item.keys())}')
    if item_type == 'code' or 'diff' in str(item.keys()).lower():
        print(f'  Full item: {json.dumps(item, indent=2)[:1000]}')
    elif 'content' in item:
        content = item.get('content', '')
        if isinstance(content, str) and len(content) > 0:
            print(f'  content: {content[:200]}')

# Also check if there's branch info we can use to get diff from GitHub
print(f'\nBranch: {turn_info.get("branch")}')
print(f'Base commit: {turn_info.get("base_commit_sha")}')
