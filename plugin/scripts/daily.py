"""Git state for daily development reports.

Usage: daily.py pending | ack

`pending` prints today's report path and the commits on the main branch that
are not yet acknowledged; `ack` acknowledges everything up to HEAD.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath

from harness_config import ConfigError, HarnessConfig, load_config, project_root


@dataclass(frozen=True)
class Commit:
    sha: str
    short: str
    when: str
    subject: str


def _git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, check=False
        )
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def main_branch(root: Path) -> str | None:
    remote_head = _git(root, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD")
    if remote_head:
        return remote_head.removeprefix("origin/")
    for name in ("main", "master"):
        if _git(root, "rev-parse", "--verify", "--quiet", f"refs/heads/{name}") is not None:
            return name
    return None


def is_main_checkout(root: Path) -> bool:
    """True for the primary working tree, False for linked worktrees."""
    git_dir = _git(root, "rev-parse", "--absolute-git-dir")
    common_dir = _git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    return git_dir is not None and git_dir == common_dir


def unavailable_reason(root: Path) -> str | None:
    """Why reports cannot be written here, or None when this is the right place."""
    if not is_main_checkout(root):
        return "not the main checkout (reports are written only there, after merging)"
    branch = main_branch(root)
    if branch is None:
        return "no main branch found"
    if _git(root, "branch", "--show-current") != branch:
        return f"the main branch '{branch}' is not checked out"
    return None


def head(root: Path) -> str | None:
    return _git(root, "rev-parse", "HEAD")


def _ack_file(root: Path) -> Path | None:
    # Inside the git directory so that hooks and the CLI share it and it is never committed.
    common_dir = _git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    return Path(common_dir) / "claude-harness" / "daily-ack" if common_dir else None


def load_ack(root: Path) -> str | None:
    path = _ack_file(root)
    if path is None:
        return None
    try:
        return path.read_text().strip() or None
    except OSError:
        return None


def save_ack(root: Path, sha: str) -> None:
    path = _ack_file(root)
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(sha)


def _changed_files(root: Path, sha: str) -> list[str]:
    parents = (_git(root, "rev-list", "--parents", "-n", "1", sha) or "").split()[1:]
    if len(parents) > 1:
        out = _git(root, "diff", "--name-only", parents[0], sha)
    else:
        out = _git(root, "diff-tree", "-r", "--root", "--no-commit-id", "--name-only", sha)
    return [line for line in (out or "").splitlines() if line]


def _counts(files: list[str], ignored: tuple[PurePosixPath, ...]) -> bool:
    """A commit counts unless it only touches the daily report or backlog folders."""
    return any(not any(PurePosixPath(f).is_relative_to(p) for p in ignored) for f in files)


def pending_commits(root: Path, config: HarnessConfig) -> list[Commit]:
    """Unacknowledged commits on HEAD, oldest first.

    Without a usable acknowledged state, HEAD becomes the silent starting point
    so that old history never triggers a report.
    """
    current = head(root)
    if current is None:
        return []
    base = load_ack(root)
    if base is None or _git(root, "merge-base", "--is-ancestor", base, current) is None:
        save_ack(root, current)
        return []
    log = _git(
        root, "log", "--reverse", "--date=format:%Y-%m-%d %H:%M",
        "--format=%H%x1f%h%x1f%ad%x1f%s", f"{base}..{current}",
    )
    commits = []
    for line in (log or "").splitlines():
        sha, short, when, subject = line.split("\x1f", 3)
        # The backlog documents itself, so backlog-only commits never need a report.
        if _counts(_changed_files(root, sha), (config.daily_path, config.todo_path)):
            commits.append(Commit(sha, short, when, subject))
    return commits


def report_path(config: HarnessConfig, day: date) -> PurePosixPath:
    return config.daily_path / f"{day.isoformat()}_daily.md"


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] not in ("pending", "ack"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    root = project_root()
    try:
        config = load_config(root)
    except ConfigError as exc:
        print(f"Invalid configuration: {exc}", file=sys.stderr)
        return 1
    if config is None or not config.enabled("daily"):
        print("Module 'daily' is not enabled in .claude-harness/config.toml.", file=sys.stderr)
        return 1
    reason = unavailable_reason(root)
    if reason:
        print(f"Daily reports unavailable here: {reason}.", file=sys.stderr)
        return 1

    if argv[0] == "ack":
        current = head(root)
        if current is None:
            print("No commit to acknowledge.", file=sys.stderr)
            return 1
        save_ack(root, current)
        print(f"Acknowledged up to {current[:7]}.")
        return 0

    path = report_path(config, date.today())
    state = "exists" if (root / path).is_file() else "new"
    lines = [f"Report: {path} ({state})", f"Language: {config.language}"]
    commits = pending_commits(root, config)
    if commits:
        lines.append("Pending commits (oldest first):")
        lines += [f"- {c.short} {c.when} {c.subject}" for c in commits]
    else:
        lines.append("No pending commits.")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
