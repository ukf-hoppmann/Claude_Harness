"""UserPromptSubmit hook: reminds to record the discussion of an active backlog item in its notes (todo module).

An item is active once the session set it `In progress` or read its spec (see mark_notes_state.py for the API backend and
mark_active_item.py for the files backend). Every prompt counts for the active items; one without a notes entry for 5
prompts gets a reminder, then another after every further 5. A notes entry restarts the count. The reminder only adds
context to the prompt; it never blocks.
"""

from __future__ import annotations

import json
import sys

from harness_config import ROOT_PROJECT, ConfigError, project_root
from projects import load_projects
from state import read_notes_marks, write_notes_marks

INTERVAL = 5


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        return 0
    session_id = hook_input.get("session_id") if isinstance(hook_input, dict) else None
    if not session_id:
        return 0
    marks = read_notes_marks(session_id)
    active = [key for key, mark in marks.items() if mark["turns"] is not None]
    if not active:
        return 0
    try:
        projects = load_projects(project_root(hook_input))
    except ConfigError:
        return 0
    due: list[str] = []
    for key in sorted(active):
        project, identifier = key
        known = projects.get(project) if projects else None
        if known is None or not known.config.enabled("todo"):
            del marks[key]
            continue
        marks[key]["turns"] = int(marks[key]["turns"]) + 1
        turns = marks[key]["turns"]
        if turns % INTERVAL == 0:
            due.append(f"{identifier}{'' if project == ROOT_PROJECT else f' ({project})'}: {turns} turns")
    try:
        write_notes_marks(session_id, marks)
    except OSError:
        pass
    if due:
        print(
            "Claude_Harness reminder: no notes entry for these active items since "
            + "; ".join(due)
            + ". If something was clarified, decided, or rejected, record it in the item's notes now "
            "(skill todo, record discussions in the notes). Ignore this if nothing of that happened."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
