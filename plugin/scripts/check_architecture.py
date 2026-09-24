from __future__ import annotations

import json
import re
import sys

from architecture import read_files, required_files, rules_path
from harness_config import ConfigError, load_config, project_root, project_relative

# Backlog specs are the input for implementation plans (<ID>_spec.md, <ID>_spec_<topic>.md).
_SPEC_NAME = re.compile(r"[A-Z]+-\d+_spec(_[^/]+)?\.md")


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        return 0
    tool_input = hook_input.get("tool_input") or {}
    session_id = hook_input.get("session_id")
    if not session_id:
        return 0

    root = project_root(hook_input)
    try:
        config = load_config(root)
    except ConfigError:
        return 0
    if config is None or not config.part_enabled("architecture"):
        return 0
    rules = rules_path(config)
    if not (root / rules).is_file():
        return 0
    done = read_files(session_id)

    if hook_input.get("tool_name") == "ExitPlanMode":
        if rules.as_posix() not in done:
            _deny(
                f"before presenting a plan, read the binding architecture rules in full with the "
                f"Read tool: {rules}, plus every scope listed there whose paths the plan touches. "
                "Check the plan against the rules, then present it again."
            )
        return 0

    file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not file_path:
        return 0
    rel = project_relative(root, file_path)
    if rel is None:
        return 0
    if rel.is_relative_to(config.todo_path) and _SPEC_NAME.fullmatch(rel.name):
        if rules.as_posix() not in done:
            _deny(
                f"a spec is the input for an implementation plan. Before writing {rel}, read the "
                f"binding architecture rules in full with the Read tool: {rules}, plus every scope "
                "listed there whose paths the spec touches. Align the spec with the rules, then retry."
            )
        return 0
    if config.is_harness_file(rel):
        return 0
    missing = [p.as_posix() for p in required_files(root, config, rel) if p.as_posix() not in done]
    if missing:
        _deny(
            f"before changing {rel}, read the binding architecture rules in full with the Read "
            f"tool: {', '.join(missing)}. Load skill claude-harness:architecture if not loaded "
            "yet, check your plan against the rules, then retry."
        )
    return 0


def _deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Claude_Harness architecture: {reason}",
        }
    }))


if __name__ == "__main__":
    sys.exit(main())
