from __future__ import annotations

import json
import sys

from backlog import format_report, validate_backlog
from harness_config import ConfigError, load_config, project_root
from state import dirty_marker


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        return 0
    session_id = hook_input.get("session_id")
    if not session_id:
        return 0
    marker = dirty_marker(session_id)
    if not marker.exists():
        return 0

    root = project_root(hook_input)
    try:
        config = load_config(root)
    except ConfigError:
        return 0
    if config is None or not config.enabled("todo"):
        marker.unlink(missing_ok=True)
        return 0

    report = validate_backlog(root / config.todo_path)
    if report.ok:
        marker.unlink(missing_ok=True)
        return 0

    # The marker stays so the backlog is checked again at the next stop.
    if hook_input.get("stop_hook_active"):
        return 0
    print(
        "Claude_Harness backlog check failed after your edits in "
        f"{config.todo_path}. Fix these problems:\n{format_report(report)}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
