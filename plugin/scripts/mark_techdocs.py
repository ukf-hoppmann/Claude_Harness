from __future__ import annotations

import json
import sys

from harness_config import ConfigError, load_config, project_root
from state import techdocs_marker
from techdocs import classify


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
    if config is None or not config.enabled("techdocs"):
        return 0

    kind = classify(root, config, file_path)
    if kind:
        marker = techdocs_marker(session_id, kind)
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch()
    return 0


if __name__ == "__main__":
    sys.exit(main())
