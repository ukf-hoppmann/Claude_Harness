from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

CONFIG_RELATIVE_PATH = PurePosixPath(".claude-harness/config.toml")
CONFIG_VERSION = 1
KNOWN_MODULES = ("todo",)
DEFAULT_TODO_PATH = PurePosixPath("docs/todo")

_TOP_LEVEL_KEYS = {"version", "modules", "todo"}
_TODO_KEYS = {"path"}


class ConfigError(ValueError):
    """Raised when the project configuration violates the config schema."""


@dataclass(frozen=True)
class HarnessConfig:
    modules: dict[str, bool]
    todo_path: PurePosixPath

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

    todo_path = DEFAULT_TODO_PATH
    raw_todo = data.get("todo", {})
    if not isinstance(raw_todo, dict):
        errors.append("[todo] must be a table")
    else:
        unknown_todo = sorted(set(raw_todo) - _TODO_KEYS)
        if unknown_todo:
            errors.append(f"unknown keys in [todo]: {', '.join(unknown_todo)}")
        if "path" in raw_todo:
            try:
                todo_path = _relative_path(raw_todo["path"])
            except ConfigError as exc:
                errors.append(f"todo.path {exc}")

    if errors:
        raise ConfigError(
            f"{CONFIG_RELATIVE_PATH}: " + "; ".join(errors)
        )
    return HarnessConfig(modules=modules, todo_path=todo_path)


def _relative_path(value: Any) -> PurePosixPath:
    if not isinstance(value, str) or not value.strip():
        raise ConfigError("must be a non-empty string")
    path = PurePosixPath(value.strip())
    if path.is_absolute():
        raise ConfigError("must be relative to the project root")
    if ".." in path.parts:
        raise ConfigError("must not contain '..'")
    return path
