"""Copy the plugin into a project so that Claude Code cloud sessions can use it.

A cloud session loads the repository but not the plugin. The copy puts what the plugin provides into
places the cloud does load: skills below .claude/skills, scripts and templates below
.claude-harness/runtime, hooks in .claude/settings.json. Only plugin/ is ever copied.
"""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

# Where the copy lives inside a project (relative to the project root). A copy is a build product of the
# plugin; the names are fixed so that update and removal find it again.
SKILLS_DIR = PurePosixPath(".claude/skills")
RUNTIME_DIR = PurePosixPath(".claude-harness/runtime")
# Prefix of every exported skill: it avoids clashes with built-in skills such as init.
SKILL_PREFIX = "harness-"
# Skills that stay with the local plugin: init and update manage the copy, worktree has no cloud counterpart.
LOCAL_ONLY_SKILLS = ("init", "update", "worktree")

_PLUGIN_ROOT = "${CLAUDE_PLUGIN_ROOT}"
_FRONT_NAME = re.compile(r"^(name:[ \t]*)(\S+)", re.MULTILINE)
_SKILL_REF = re.compile(r"claude-harness:([a-z][a-z-]*)")


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
