from __future__ import annotations

import json
import sys

from architecture import read_files, required_files
from harness_config import ConfigError, load_config, project_root, project_relative


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        return 0
    tool_input = hook_input.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
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
    if rel is None or config.is_harness_file(rel):
        return 0
    done = read_files(session_id)
    missing = [p.as_posix() for p in required_files(root, config, rel) if p.as_posix() not in done]
    if not missing:
        return 0

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Claude_Harness architecture: before changing {rel}, read the binding "
                f"architecture rules in full with the Read tool: {', '.join(missing)}. "
                "Load skill claude-harness:architecture if not loaded yet, check your plan "
                "against the rules, then retry."
            ),
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
