from __future__ import annotations

import json
import sys
from pathlib import Path

from architecture import mark_read, rules_path, scopes_dir
from harness_config import ConfigError, load_config, project_root, project_relative


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        return 0
    tool_input = hook_input.get("tool_input") or {}
    file_path = tool_input.get("file_path")
    session_id = hook_input.get("session_id")
    if not file_path or not session_id:
        return 0

    root = project_root(hook_input)
    try:
        config = load_config(root)
    except ConfigError:
        return 0
    if config is None or not config.part_enabled("architecture"):
        return 0

    rel = project_relative(root, file_path)
    if rel is None or (rel != rules_path(config) and rel.parent != scopes_dir(config)):
        return 0
    if not _complete_read(root / rel, tool_input):
        return 0
    mark_read(session_id, rel)
    return 0


def _complete_read(path: Path, tool_input: dict) -> bool:
    """Only a read from the first line that covers the whole file counts."""
    offset = tool_input.get("offset")
    if offset not in (None, 0, 1):
        return False
    limit = tool_input.get("limit")
    if limit is None:
        return True
    try:
        lines = len(path.read_text(encoding="utf-8").splitlines())
    except OSError:
        return False
    return limit >= lines


if __name__ == "__main__":
    sys.exit(main())
