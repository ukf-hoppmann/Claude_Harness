from __future__ import annotations

import os
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

CONFIG_RELATIVE_PATH = PurePosixPath(".claude-harness/config.toml")
CONFIG_VERSION = 1
KNOWN_MODULES = ("todo", "daily", "techdocs")
DEFAULT_DOCS_ROOT = PurePosixPath("docs")
DEFAULT_LANGUAGE = "en"
DEFAULT_TODO_PATH = PurePosixPath("todo")
DEFAULT_DAILY_PATH = PurePosixPath("development/daily")
DEFAULT_TECHDOCS_PATH = PurePosixPath("techdocs")
TECHDOC_KINDS = ("architecture", "interfaces", "configuration", "operations")
DEFAULT_TECHDOCS = ("architecture", "interfaces", "configuration")

_TOP_LEVEL_KEYS = {"version", "docs", "modules", "todo", "daily", "techdocs"}
_DOCS_KEYS = {"root", "language"}
_PATH_KEYS = {"path"}
_LANGUAGE_PATTERN = re.compile(r"[a-z]{2}")


class ConfigError(ValueError):
    """Raised when the project configuration violates the config schema."""


@dataclass(frozen=True)
class HarnessConfig:
    modules: dict[str, bool]
    docs_root: PurePosixPath
    language: str
    # Module paths are resolved against docs_root, i.e. relative to the project root.
    todo_path: PurePosixPath
    daily_path: PurePosixPath
    techdocs_path: PurePosixPath
    techdocs: tuple[str, ...]

    def enabled(self, module: str) -> bool:
        return self.modules.get(module, False)


def project_root(hook_input: dict[str, Any] | None = None) -> Path:
    env_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_root:
        return Path(env_root)
    if hook_input and hook_input.get("cwd"):
        return Path(hook_input["cwd"])
    return Path.cwd()


def load_config(root: Path) -> HarnessConfig | None:
    """Return the parsed config, or None when the project has no config file."""
    path = root / CONFIG_RELATIVE_PATH
    if not path.is_file():
        return None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"{CONFIG_RELATIVE_PATH}: invalid TOML: {exc}") from exc
    return parse_config(data)


def parse_config(data: dict[str, Any]) -> HarnessConfig:
    errors: list[str] = []

    unknown = sorted(set(data) - _TOP_LEVEL_KEYS)
    if unknown:
        errors.append(f"unknown top-level keys: {', '.join(unknown)}")

    version = data.get("version")
    if version != CONFIG_VERSION:
        errors.append(f"version must be {CONFIG_VERSION}, got {version!r}")

    modules: dict[str, bool] = {}
    raw_modules = data.get("modules", {})
    if not isinstance(raw_modules, dict):
        errors.append("[modules] must be a table")
    else:
        for name, value in raw_modules.items():
            if name not in KNOWN_MODULES:
                errors.append(
                    f"unknown module '{name}' (known: {', '.join(KNOWN_MODULES)})"
                )
            elif not isinstance(value, bool):
                errors.append(f"modules.{name} must be true or false")
            else:
                modules[name] = value

    raw_docs = _table(data, "docs", _DOCS_KEYS, errors)
    docs_root = _path_value(raw_docs, "root", "docs", DEFAULT_DOCS_ROOT, errors)
    language = raw_docs.get("language", DEFAULT_LANGUAGE)
    if not isinstance(language, str) or not _LANGUAGE_PATTERN.fullmatch(language):
        errors.append(f"docs.language must be a two-letter ISO 639-1 code, got {language!r}")

    todo_path = _path_value(_table(data, "todo", _PATH_KEYS, errors), "path", "todo", DEFAULT_TODO_PATH, errors)
    daily_path = _path_value(_table(data, "daily", _PATH_KEYS, errors), "path", "daily", DEFAULT_DAILY_PATH, errors)
    raw_techdocs = _table(data, "techdocs", {"path", "documents"}, errors)
    techdocs_path = _path_value(raw_techdocs, "path", "techdocs", DEFAULT_TECHDOCS_PATH, errors)
    techdocs = _techdoc_kinds(raw_techdocs.get("documents", list(DEFAULT_TECHDOCS)), errors)

    if errors:
        raise ConfigError(
            f"{CONFIG_RELATIVE_PATH}: " + "; ".join(errors)
        )
    return HarnessConfig(
        modules=modules,
        docs_root=docs_root,
        language=language,
        todo_path=docs_root / todo_path,
        daily_path=docs_root / daily_path,
        techdocs_path=docs_root / techdocs_path,
        techdocs=techdocs,
    )


def _techdoc_kinds(value: Any, errors: list[str]) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        errors.append("techdocs.documents must be a list of strings")
        return DEFAULT_TECHDOCS
    unknown = [v for v in value if v not in TECHDOC_KINDS]
    if unknown:
        errors.append(
            f"unknown techdocs.documents: {', '.join(unknown)} (known: {', '.join(TECHDOC_KINDS)})"
        )
    if len(set(value)) != len(value):
        errors.append("techdocs.documents must not contain duplicates")
    return tuple(value)


def _table(data: dict[str, Any], name: str, keys: set[str], errors: list[str]) -> dict[str, Any]:
    raw = data.get(name, {})
    if not isinstance(raw, dict):
        errors.append(f"[{name}] must be a table")
        return {}
    unknown = sorted(set(raw) - keys)
    if unknown:
        errors.append(f"unknown keys in [{name}]: {', '.join(unknown)}")
    return raw


def _path_value(
    table: dict[str, Any], key: str, table_name: str, default: PurePosixPath, errors: list[str]
) -> PurePosixPath:
    if key not in table:
        return default
    try:
        return _relative_path(table[key])
    except ConfigError as exc:
        errors.append(f"{table_name}.{key} {exc}")
        return default


def _relative_path(value: Any) -> PurePosixPath:
    if not isinstance(value, str) or not value.strip():
        raise ConfigError("must be a non-empty string")
    path = PurePosixPath(value.strip())
    if path.is_absolute():
        raise ConfigError("must be a relative path")
    if ".." in path.parts:
        raise ConfigError("must not contain '..'")
    return path
