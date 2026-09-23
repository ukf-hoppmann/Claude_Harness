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


def dirty_marker(session_id: str) -> Path:
    safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", session_id)
    return state_dir() / f"backlog-dirty-{safe_id}"
