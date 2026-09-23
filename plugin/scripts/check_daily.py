from __future__ import annotations

import json
import sys
from pathlib import Path

from daily import head, pending_commits, unavailable_reason
from harness_config import ConfigError, load_config, project_root
from state import daily_reminded_file

DAILY_SCRIPT = Path(__file__).resolve().parent / "daily.py"


def _load_reminded(session_id: str) -> set[str]:
    try:
        return set(json.loads(daily_reminded_file(session_id).read_text()))
    except (OSError, ValueError):
        return set()


def _save_reminded(session_id: str, heads: set[str]) -> None:
    path = daily_reminded_file(session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted(heads)))


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        return 0
    session_id = hook_input.get("session_id")
    if not session_id or hook_input.get("stop_hook_active"):
        return 0

    root = project_root(hook_input)
    try:
        config = load_config(root)
    except ConfigError:
        return 0
    if config is None or not config.enabled("daily") or unavailable_reason(root):
        return 0

    commits = pending_commits(root, config)
    current = head(root)
    if not commits or current is None:
        return 0
    reminded = _load_reminded(session_id)
    if current in reminded:
        return 0
    _save_reminded(session_id, reminded | {current})

    print(
        f"Claude_Harness daily: {len(commits)} commit(s) on the main branch are not yet "
        "recorded in the daily report. Load skill claude-harness:daily and follow it "
        f'(start with: python3 "{DAILY_SCRIPT}" pending).',
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
