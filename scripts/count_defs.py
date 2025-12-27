#!/usr/bin/env python3
"""Count top-level definitions in Python files."""

import ast
from pathlib import Path

def count_top_level_defs(filepath: Path) -> int:
    try:
        content = filepath.read_text()
        tree = ast.parse(content)
        count = 0
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                count += 1
        return count
    except Exception:
        return 0

def main():
    src = Path(__file__).parent.parent / "src" / "codex_task_runner"
    results = []
    
    for py_file in src.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue
        if py_file.name == "__init__.py":
            continue
        if py_file.name == "module_class.py":
            continue
            
        count = count_top_level_defs(py_file)
        if count >= 2:
            rel = py_file.relative_to(src.parent.parent)
            results.append((count, str(rel)))
    
    results.sort(key=lambda x: (-x[0], x[1]))
    
    print("**Files With Multiple Things**\n")
    for count, path in results:
        print(f"- **{count}:** [{path}]({path}) — {count} top-level `def`/`class`")

if __name__ == "__main__":
    main()
