"""Git state for daily development reports.

Usage: daily.py pending | ack [--project <name>]

`pending` prints today's report path and the commits on the main branch that
are not yet acknowledged; `ack` acknowledges everything up to HEAD. With
subprojects, --project selects the project (default: root).
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath

from harness_config import ROOT_PROJECT, ConfigError, HarnessConfig, project_root
from projects import Project, ProjectSet, load_projects


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


def _prefix(project: Project) -> str | None:
    """The project folder relative to the Git root, '' at the Git root, e.g. 'Plugins/A/'."""
    return _git(project.root, "rev-parse", "--show-prefix")


def _ack_file(project: Project) -> Path | None:
    # Inside the git directory so that hooks and the CLI share it and it is never committed.
    # Keyed by the folder, so a subproject shares its state whether the session starts there or above.
    common_dir = _git(project.root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    prefix = _prefix(project)
    if not common_dir or prefix is None:
        return None
    name = "daily-ack" if not prefix else "daily-ack-" + prefix.rstrip("/").replace("/", "_")
    return Path(common_dir) / "claude-harness" / name


def load_ack(project: Project) -> str | None:
    path = _ack_file(project)
    if path is None:
        return None
    try:
        return path.read_text().strip() or None
    except OSError:
        return None


def save_ack(project: Project, sha: str) -> None:
    path = _ack_file(project)
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(sha)


def _changed_files(root: Path, sha: str) -> list[str]:
    """Files a commit changed, relative to the Git root."""
    parents = (_git(root, "rev-list", "--parents", "-n", "1", sha) or "").split()[1:]
    if len(parents) > 1:
        out = _git(root, "diff", "--name-only", parents[0], sha)
    else:
        out = _git(root, "diff-tree", "-r", "--root", "--no-commit-id", "--name-only", sha)
    return [line for line in (out or "").splitlines() if line]


def _counts(files: list[PurePosixPath], ignored: tuple[PurePosixPath, ...]) -> bool:
    """A commit counts unless it only touches the daily report or backlog folders."""
    return any(not any(f.is_relative_to(p) for p in ignored) for f in files)


def _project_files(files: list[str], prefix: str, excluded: tuple[PurePosixPath, ...]) -> list[PurePosixPath]:
    """Files inside the project, relative to it; files in excluded subproject folders are dropped."""
    inside = [PurePosixPath(f[len(prefix):]) for f in files if f.startswith(prefix)]
    return [f for f in inside if not any(f.is_relative_to(e) for e in excluded)]


def pending_commits(projects: ProjectSet, project: Project) -> list[Commit]:
    """Unacknowledged commits on HEAD that change files of project, oldest first.

    Without a usable acknowledged state, HEAD becomes the silent starting point
    so that old history never triggers a report.
    """
    root = project.root
    current = head(root)
    prefix = _prefix(project)
    if current is None or prefix is None:
        return []
    base = load_ack(project)
    if base is None or _git(root, "merge-base", "--is-ancestor", base, current) is None:
        save_ack(project, current)
        return []
    log = _git(
        root, "log", "--reverse", "--date=format:%Y-%m-%d %H:%M",
        "--format=%H%x1f%h%x1f%ad%x1f%s", f"{base}..{current}",
    )
    # The root project does not report changes that belong to a subproject.
    excluded = tuple(path for _, path in projects.registry) if project.name == ROOT_PROJECT else ()
    config = project.config
    commits = []
    for line in (log or "").splitlines():
        sha, short, when, subject = line.split("\x1f", 3)
        files = _project_files(_changed_files(root, sha), prefix, excluded)
        # The backlog documents itself, so backlog-only commits never need a report.
        if _counts(files, (config.daily_path, config.todo_path)):
            commits.append(Commit(sha, short, when, subject))
    return commits


def report_path(config: HarnessConfig, day: date) -> PurePosixPath:
    return config.daily_path / f"{day.isoformat()}_daily.md"


def main(argv: list[str]) -> int:
    name = None
    if len(argv) == 3 and argv[1] == "--project":
        argv, name = argv[:1], argv[2]
    if len(argv) != 1 or argv[0] not in ("pending", "ack"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    root = project_root()
    try:
        projects = load_projects(root)
    except ConfigError as exc:
        print(f"Invalid configuration: {exc}", file=sys.stderr)
        return 1
    project = _select(projects, name)
    if project is None:
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
        save_ack(project, current)
        print(f"Acknowledged up to {current[:7]}.")
        return 0

    config = project.config
    path = report_path(config, date.today())
    state = "exists" if (project.root / path).is_file() else "new"
    lines = [f"Report: {project.path / path} ({state})", f"Language: {config.language}"]
    commits = pending_commits(projects, project)
    if commits:
        lines.append("Pending commits (oldest first):")
        lines += [f"- {c.short} {c.when} {c.subject}" for c in commits]
    else:
        lines.append("No pending commits.")
    print("\n".join(lines))
    return 0


def _select(projects: ProjectSet | None, name: str | None) -> Project | None:
    """The project to work on, or None after printing why there is none."""
    with_daily = [p.name for p in projects.projects if p.config.enabled("daily")] if projects else []
    project = projects.get(name or ROOT_PROJECT) if projects else None
    if project is not None and project.config.enabled("daily"):
        return project
    if name is not None:
        print(
            f"Project {name!r} is unknown, unusable, or has no daily reports "
            f"(projects with daily reports: {', '.join(with_daily) or 'none'}).",
            file=sys.stderr,
        )
    elif with_daily:
        options = ", ".join(f"--project {n}" for n in with_daily)
        print(f"Module 'daily' is not enabled for the root project; choose one of: {options}.", file=sys.stderr)
    else:
        print("Module 'daily' is not enabled in .claude-harness/config.toml.", file=sys.stderr)
    return None


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
