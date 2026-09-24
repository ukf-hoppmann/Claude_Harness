from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path


def state_dir() -> Path:
    data_dir = os.environ.get("CLAUDE_PLUGIN_DATA")
    if data_dir:
        return Path(data_dir)
    return Path(tempfile.gettempdir()) / "claude-harness"


def _safe(session_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "_", session_id)


def dirty_marker(session_id: str) -> Path:
    return state_dir() / f"backlog-dirty-{_safe(session_id)}"


def delivered_notices_file(session_id: str) -> Path:
    return state_dir() / f"backlog-notices-{_safe(session_id)}.json"


def daily_reminded_file(session_id: str) -> Path:
    return state_dir() / f"daily-reminded-{_safe(session_id)}.json"


def techdocs_marker(session_id: str, kind: str) -> Path:
    """kind: 'project' (project files changed), 'docs' (docs changed), 'reminded'."""
    return state_dir() / f"techdocs-{kind}-{_safe(session_id)}"


def architecture_read_file(session_id: str) -> Path:
    return state_dir() / f"architecture-read-{_safe(session_id)}.json"
