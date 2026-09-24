"""Classify edited files for the techdocs module."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from harness_config import README, HarnessConfig, project_relative

_TEST_NAME = re.compile(r"^test_|_test\.|\.test\.")


def _is_test(path: PurePosixPath) -> bool:
    return any(part in ("test", "tests") for part in path.parts[:-1]) or bool(
        _TEST_NAME.search(path.name)
    )


def classify(root: Path, config: HarnessConfig, file_path: str) -> str | None:
    """Return 'docs', 'project', or None for files that do not matter."""
    rel = project_relative(root, file_path)
    if rel is None:
        return None
    if rel == README or rel.is_relative_to(config.techdocs_path):
        return "docs"
    if config.is_harness_file(rel) or _is_test(rel):
        return None
    return "project"


def document_paths(config: HarnessConfig) -> list[PurePosixPath]:
    return [README] + [config.techdocs_path / f"{kind}.md" for kind in config.techdocs]
