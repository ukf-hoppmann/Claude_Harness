from __future__ import annotations

import json
import sys

from backlog import validate_backlog
from harness_config import ConfigError, load_config, project_root
from state import delivered_notices_file, dirty_marker


def _load_delivered(session_id: str) -> set[str]:
    try:
        return set(json.loads(delivered_notices_file(session_id).read_text()))
    except (OSError, ValueError):
        return set()


def _save_delivered(session_id: str, notices: set[str]) -> None:
    path = delivered_notices_file(session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted(notices)))


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
    delivered = _load_delivered(session_id)
    new_notices = [n for n in report.notices if n not in delivered]

    if report.ok:
        marker.unlink(missing_ok=True)
    if not report.errors and not new_notices:
        return 0
    # With errors the marker stays so the backlog is checked again at the next stop.
    if hook_input.get("stop_hook_active"):
        return 0

    lines = [f"Claude_Harness backlog check after your edits in {config.todo_path}:"]
    if report.errors:
        lines.append("Fix these errors:")
        lines += [f"- {e}" for e in report.errors]
    if new_notices:
        lines.append("Handle these notices (each is shown once per session):")
        lines += [f"- {n}" for n in new_notices]
        _save_delivered(session_id, delivered | set(new_notices))
    print("\n".join(lines), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
