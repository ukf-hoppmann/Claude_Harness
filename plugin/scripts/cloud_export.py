"""Copy the plugin into a project so that Claude Code cloud sessions can use it.

A cloud session loads the repository but not the plugin. The copy puts what the plugin provides into
places the cloud does load: skills below .claude/skills, scripts and templates below
.claude-harness/runtime, hooks in .claude/settings.json. Only plugin/ is ever copied.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

# Where the copy lives inside a project (relative to the project root). A copy is a build product of the
# plugin; the names are fixed so that update and removal find it again.
SKILLS_DIR = PurePosixPath(".claude/skills")
RUNTIME_DIR = PurePosixPath(".claude-harness/runtime")
SETTINGS_FILE = PurePosixPath(".claude/settings.json")
# Prefix of every exported skill: it avoids clashes with built-in skills such as init.
SKILL_PREFIX = "harness-"
# Skills that stay with the local plugin: init and update manage the copy, worktree has no cloud counterpart.
LOCAL_ONLY_SKILLS = ("init", "update", "worktree")

# A hook command that contains this belongs to the copy; update and removal recognize their own entries by it.
MANAGED_MARK = RUNTIME_DIR.as_posix() + "/scripts/"
# The copy's hooks run only in cloud sessions (CLAUDE_CODE_REMOTE=true); locally the plugin's own hooks apply.
# "||" instead of a trailing "|| true" keeps the exit code of the script, which blocking hooks depend on.
CLOUD_GUARD = '[ "$CLAUDE_CODE_REMOTE" != "true" ] || '

_PLUGIN_ROOT = "${CLAUDE_PLUGIN_ROOT}"
_PROJECT_RUNTIME = "${CLAUDE_PROJECT_DIR:-.}/" + RUNTIME_DIR.as_posix()
_FRONT_NAME = re.compile(r"^(name:[ \t]*)(\S+)", re.MULTILINE)
_SKILL_REF = re.compile(r"claude-harness:([a-z][a-z-]*)")


class ExportError(Exception):
    """The copy cannot be made or changed; nothing has been written."""


def rewrite_skill_text(text: str, exported: frozenset[str]) -> str:
    """Turn the text of a plugin skill file into the text of its project copy."""
    text = _prefix_skill_name(text)
    text = _SKILL_REF.sub(lambda m: SKILL_PREFIX + m.group(1) if m.group(1) in exported else m.group(0), text)
    return text.replace(_PLUGIN_ROOT, RUNTIME_DIR.as_posix())


def _prefix_skill_name(text: str) -> str:
    """Prefix the name in the frontmatter, nothing else."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end < 0:
        return text
    front = _FRONT_NAME.sub(lambda m: m.group(1) + SKILL_PREFIX + m.group(2), text[:end], count=1)
    return front + text[end:]


def exported_skill_names(plugin_root: Path) -> list[str]:
    """Names of the plugin skills that are copied, sorted."""
    skills = plugin_root / "skills"
    return sorted(
        path.name
        for path in skills.iterdir()
        if (path / "SKILL.md").is_file() and path.name not in LOCAL_ONLY_SKILLS
    )


def skill_files(plugin_root: Path) -> dict[str, bytes]:
    """Project path (posix, relative to the project root) -> content, for every file of every exported skill."""
    names = exported_skill_names(plugin_root)
    exported = frozenset(names)
    files: dict[str, bytes] = {}
    for name in names:
        base = plugin_root / "skills" / name
        for path in sorted(p for p in base.rglob("*") if p.is_file() and not _is_noise(p.relative_to(base))):
            target = SKILLS_DIR / (SKILL_PREFIX + name) / path.relative_to(base).as_posix()
            data = path.read_bytes()
            if path.suffix == ".md":
                data = rewrite_skill_text(data.decode("utf-8"), exported).encode("utf-8")
            files[target.as_posix()] = data
    return files


def _is_noise(relative: Path) -> bool:
    """Files that are no part of a skill: caches and hidden files such as .DS_Store."""
    return any(part == "__pycache__" or part.startswith(".") for part in relative.parts)


def hook_entries(plugin_hooks: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """The plugin's hook groups (content of hooks.json) as groups for the project's .claude/settings.json."""
    entries: dict[str, list[dict[str, Any]]] = {}
    for event, groups in plugin_hooks["hooks"].items():
        entries[event] = [_project_group(group) for group in groups]
    return entries


def _project_group(group: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(group)
    for hook in result["hooks"]:
        command = hook["command"].replace(_PLUGIN_ROOT, _PROJECT_RUNTIME)
        hook["command"] = CLOUD_GUARD + command
    return result


def parse_settings(text: str) -> dict[str, Any]:
    """The content of .claude/settings.json; an empty file counts as no settings."""
    if not text.strip():
        return {}
    try:
        data = json.loads(text)
    except ValueError as error:
        raise ExportError(f"{SETTINGS_FILE} is not valid JSON: {error}") from error
    if not isinstance(data, dict):
        raise ExportError(f"{SETTINGS_FILE} does not contain a JSON object")
    return data


def dump_settings(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def merge_hooks(settings: dict[str, Any], entries: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Settings with the copy's hooks in place of any earlier copy; foreign hooks and other keys stay."""
    result = copy.deepcopy(settings)
    hooks = _foreign_hooks(result.get("hooks", {}))
    for event, groups in entries.items():
        hooks.setdefault(event, []).extend(copy.deepcopy(groups))
    result["hooks"] = hooks
    return result


def remove_hooks(settings: dict[str, Any]) -> dict[str, Any]:
    """Settings without the copy's hooks; a hooks key that stays empty is dropped."""
    result = copy.deepcopy(settings)
    if "hooks" not in result:
        return result
    hooks = _foreign_hooks(result["hooks"])
    if hooks:
        result["hooks"] = hooks
    else:
        del result["hooks"]
    return result


def _foreign_hooks(hooks: Any) -> dict[str, list[Any]]:
    """The hooks that do not belong to the copy, in their original order."""
    if not isinstance(hooks, dict):
        raise ExportError(f"hooks in {SETTINGS_FILE} is not an object")
    kept: dict[str, list[Any]] = {}
    for event, groups in hooks.items():
        remaining = [group for group in (_without_managed(g) for g in groups) if group is not None]
        if remaining:
            kept[event] = remaining
    return kept


def _without_managed(group: Any) -> Any:
    """The group without the copy's hooks, or None when nothing else is left in it."""
    if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
        return group
    foreign = [h for h in group["hooks"] if not _is_managed(h)]
    if not foreign:
        return None
    return {**group, "hooks": foreign}


def _is_managed(hook: Any) -> bool:
    return isinstance(hook, dict) and MANAGED_MARK in str(hook.get("command", ""))
