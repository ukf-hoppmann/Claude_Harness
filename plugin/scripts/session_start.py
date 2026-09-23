from __future__ import annotations

import json
import sys

from backlog import TODO_FILE, validate_backlog
from harness_config import CONFIG_RELATIVE_PATH, ConfigError, load_config, project_root

MAX_REPORTED = 5


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        hook_input = {}
    root = project_root(hook_input)

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

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
