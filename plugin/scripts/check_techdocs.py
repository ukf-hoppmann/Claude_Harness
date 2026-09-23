from __future__ import annotations

import json
import sys

from harness_config import ConfigError, load_config, project_root
from state import techdocs_marker


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        return 0
    session_id = hook_input.get("session_id")
    if not session_id or hook_input.get("stop_hook_active"):
        return 0
    if not techdocs_marker(session_id, "project").exists():
        return 0
    if techdocs_marker(session_id, "docs").exists() or techdocs_marker(session_id, "reminded").exists():
        return 0

    root = project_root(hook_input)
    try:
        config = load_config(root)
    except ConfigError:
        return 0
    if config is None or not config.enabled("techdocs"):
        return 0

    reminded = techdocs_marker(session_id, "reminded")
    reminded.parent.mkdir(parents=True, exist_ok=True)
    reminded.touch()
    print(
        "Claude_Harness techdocs: project files changed in this session, but no technical "
        f"documentation (README.md, {config.techdocs_path}/). Load skill claude-harness:techdocs "
        "and check whether a document must be updated; if not, state briefly why. "
        "(Shown once per session.)",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
