from __future__ import annotations

import json
import sys

from architecture import load_scopes, reset_read, rules_path
from backlog import TODO_FILE, validate_backlog
from techdocs import document_paths
from harness_config import CONFIG_RELATIVE_PATH, ConfigError, load_config, project_root

MAX_REPORTED = 5


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        hook_input = {}
    root = project_root(hook_input)
    session_id = hook_input.get("session_id")
    if session_id and hook_input.get("source") in ("compact", "clear"):
        # Rules read earlier may no longer be in context.
        reset_read(session_id)

    try:
        config = load_config(root)
    except ConfigError as exc:
        print(f"Claude_Harness: invalid configuration — {exc}. Tell the user; do not guess values.")
        return 0
    if config is None:
        print(
            f"Claude_Harness: plugin active but no {CONFIG_RELATIVE_PATH} in this project. "
            "Set it up with /claude-harness:init if the user wants the harness here."
        )
        return 0

    states = ", ".join(
        f"{name}={'on' if enabled else 'off'}" for name, enabled in sorted(config.modules.items())
    ) or "none"
    lines = [
        f"Claude_Harness: modules {states}.",
        f"Document language: {config.language} (write all harness documents in it).",
    ]

    if config.enabled("todo"):
        todo_dir = root / config.todo_path
        if not (todo_dir / TODO_FILE).is_file():
            lines.append(
                f"Backlog: {config.todo_path}/{TODO_FILE} does not exist. When the backlog "
                "becomes relevant, tell the user and ask for permission before creating it — "
                "it may just be located elsewhere."
            )
        else:
            lines.append(
                f"Backlog: {config.todo_path}/{TODO_FILE}; rules in skill claude-harness:todo "
                "(load it only when working with the backlog)."
            )
            report = validate_backlog(todo_dir)
            problems = report.errors + report.notices
            if problems:
                lines.append(f"Backlog check found {len(report.errors)} errors, {len(report.notices)} notices:")
                lines += [f"- {p}" for p in problems[:MAX_REPORTED]]
                if len(problems) > MAX_REPORTED:
                    lines.append(f"- … {len(problems) - MAX_REPORTED} more")

    if config.enabled("daily"):
        lines.append(
            f"Daily reports: {config.daily_path}/; rules in skill claude-harness:daily "
            "(load it when reminded or asked about daily reports)."
        )

    if config.enabled("techdocs"):
        lines.append(
            f"Technical docs: README.md and {config.techdocs_path}/; rules in skill "
            "claude-harness:techdocs (load it when changing documented behavior, interfaces, "
            "configuration, or architecture, or when reminded)."
        )
        missing = [str(p) for p in document_paths(config) if not (root / p).is_file()]
        if missing:
            lines.append(
                f"Missing technical docs: {', '.join(missing)}. Propose creating them from the "
                "templates when relevant; create only after approval."
            )

    if config.part_enabled("architecture"):
        rules = rules_path(config)
        if not (root / rules).is_file():
            lines.append(
                f"Architecture rules: {rules} does not exist. Propose creating it from the "
                "template when architecture becomes relevant; create only after approval."
            )
        else:
            lines.append(
                f"Architecture rules: {rules} (binding; read it before planning, designing, or changing code); "
                "rules in skill claude-harness:architecture."
            )
            _, scope_errors = load_scopes(root, config)
            if scope_errors:
                lines.append(f"Architecture scope table has {len(scope_errors)} errors:")
                lines += [f"- {e}" for e in scope_errors[:MAX_REPORTED]]
                if len(scope_errors) > MAX_REPORTED:
                    lines.append(f"- … {len(scope_errors) - MAX_REPORTED} more")

    if config.part_enabled("decomposition"):
        lines.append(
            "Decomposition: rules in skill claude-harness:decomposition (load it when planning "
            "an implementation or splitting backlog items)."
        )

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
