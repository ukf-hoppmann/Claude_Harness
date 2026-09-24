"""Classify edited files for the techdocs module."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from harness_config import CONFIG_RELATIVE_PATH, HarnessConfig

README = PurePosixPath("README.md")
_TEST_NAME = re.compile(r"^test_|_test\.|\.test\.")


def _is_test(path: PurePosixPath) -> bool:
    return any(part in ("test", "tests") for part in path.parts[:-1]) or bool(
        _TEST_NAME.search(path.name)
    )


def classify(root: Path, config: HarnessConfig, file_path: str) -> str | None:
    """Return 'docs', 'project', or None for files that do not matter."""
    target = Path(file_path)
    if not target.is_absolute():
        target = root / target
    try:
        rel = PurePosixPath(target.resolve().relative_to(root.resolve()).as_posix())
    except ValueError:
        return None
    if rel == README or rel.is_relative_to(config.techdocs_path):
        return "docs"
    if rel.is_relative_to(config.todo_path) or rel.is_relative_to(config.daily_path):
        return None
    harness_dirs = (".git", CONFIG_RELATIVE_PATH.parts[0])
    if (rel.parts and rel.parts[0] in harness_dirs) or _is_test(rel):
        return None
    return "project"


def document_paths(config: HarnessConfig) -> list[PurePosixPath]:
    return [README] + [config.techdocs_path / f"{kind}.md" for kind in config.techdocs]
