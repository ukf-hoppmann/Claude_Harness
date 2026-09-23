from __future__ import annotations

import json
import sys
from pathlib import Path

from harness_config import ConfigError, load_config, project_root
from state import dirty_marker


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        return 0
    file_path = (hook_input.get("tool_input") or {}).get("file_path")
    session_id = hook_input.get("session_id")
    if not file_path or not session_id:
        return 0

    root = project_root(hook_input)
    try:
        config = load_config(root)
    except ConfigError:
        return 0
    if config is None or not config.enabled("todo"):
        return 0

    todo_dir = (root / config.todo_path).resolve()
    target = Path(file_path)
    if not target.is_absolute():
        target = root / target
    if target.resolve().is_relative_to(todo_dir):
        marker = dirty_marker(session_id)
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch()
    return 0


if __name__ == "__main__":
    sys.exit(main())
