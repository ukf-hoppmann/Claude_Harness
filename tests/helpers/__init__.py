from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "plugin" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

HEADER = "# Backlog\n\n## Work items\n\n"


def item(identifier: str, title: str = "Title", **fields: str) -> str:
    defaults = {
        "Type": "Story",
        "Parent": "None",
        "Status": "Open",
        "Created": "2026-09-23",
        "Area": "Test",
        "Priority": "Important",
        "Dependencies": "None",
        "Goal": "Goal.",
        "Completion criteria": "Criteria.",
    }
    defaults.update({k.replace("_", " "): v for k, v in fields.items()})
    if defaults.get("Type") == "Epic":
        defaults.pop("Parent", None)
    lines = [f"- `{identifier}` **{title}**"]
    for name, value in defaults.items():
        if value is None:
            continue
        lines.append(f"  - {name}: {value}")
    return "\n".join(lines) + "\n\n"


def write_backlog(todo_dir: Path, todo_items: list[str], archive_items: list[str] | None = None) -> None:
    todo_dir.mkdir(parents=True, exist_ok=True)
    (todo_dir / "TODO.md").write_text(HEADER + ("".join(todo_items) or "No entries.\n"))
    if archive_items is not None:
        (todo_dir / "archive.md").write_text(HEADER + ("".join(archive_items) or "No entries.\n"))
