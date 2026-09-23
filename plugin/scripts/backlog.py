from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path, PurePosixPath

TODO_FILE = "TODO.md"
ARCHIVE_FILE = "archive.md"

ITEM_TYPES = {"Epic", "Story", "Task"}
STATUSES = {"Open", "In progress", "Awaiting confirmation", "Completed", "Rejected"}
CLOSED_STATUSES = {"Completed", "Rejected"}
READY_CHILD_STATUSES = {"Awaiting confirmation", "Completed"}
PRIORITIES = {"Urgent", "Important", "Prospective"}
REQUIRED_FIELDS = {
    "Type",
    "Status",
    "Created",
    "Area",
    "Priority",
    "Dependencies",
    "Goal",
    "Completion criteria",
}
KNOWN_FIELDS = REQUIRED_FIELDS | {
    "Parent",
    "Required for parent",
    "Resolution",
    "Summary",
    "Notes",
    "Spec",
}

_ID = r"[A-Z][A-Z0-9_-]*-[0-9]{3,}"
_ITEM_HEADER = re.compile(rf"^- `(?P<identifier>{_ID})` \*\*(?P<title>[^*\r\n].*?)\*\*$")
_FIELD = re.compile(r"^  - (?P<name>[^:\r\n]+):(?P<value>.*)$")
_REFERENCE = re.compile(rf"`({_ID})`")
_PATH_REFERENCE = re.compile(r"`([^`]+)`")
_EMPTY_MARKERS = {"No entries.", "Keine Einträge."}


@dataclass(frozen=True)
class BacklogItem:
    identifier: str
    title: str
    source: str
    item_type: str
    status: str
    created: date
    area: str
    priority: str
    dependencies: tuple[str, ...]
    parent: str | None
    required_for_parent: bool | None
    resolution: str | None
    notes: tuple[str, ...]
    specs: tuple[str, ...]


@dataclass
class BacklogReport:
    items: list[BacklogItem] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    notices: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_backlog(todo_dir: Path) -> BacklogReport:
    """Validate TODO.md and archive.md in todo_dir as one backlog."""
    report = BacklogReport()
    todo_file = todo_dir / TODO_FILE
    if not todo_file.is_file():
        report.errors.append(f"{TODO_FILE} not found in {todo_dir}")
        return report

    seen_ids: dict[str, str] = {}
    files = [todo_file]
    archive_file = todo_dir / ARCHIVE_FILE
    if archive_file.is_file():
        files.append(archive_file)

    for path in files:
        for identifier, title, fields, line in _parse_file(path, report):
            location = f"{path.name}:{line}"
            if identifier in seen_ids:
                report.errors.append(
                    f"{identifier} is defined twice ({seen_ids[identifier]} and {location})"
                )
                continue
            seen_ids[identifier] = location
            item = _build_item(identifier, title, path.name, fields, todo_dir, report)
            if item is not None:
                report.items.append(item)

    _validate_placement(report)
    _validate_relationships(report, set(seen_ids))
    _validate_lifecycle(report)
    return report


def _parse_file(path: Path, report: BacklogReport) -> list[tuple[str, str, dict[str, str], int]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    sections = [i for i, line in enumerate(lines) if line == "## Work items"]
    if len(sections) != 1:
        report.errors.append(f"{path.name} requires exactly one '## Work items' section")
        return []

    raw: list[tuple[str, str, dict[str, str], int]] = []
    current: tuple[str, str, dict[str, str], int] | None = None
    field_name: str | None = None

    for index in range(sections[0] + 1, len(lines)):
        line = lines[index]
        number = index + 1
        header = _ITEM_HEADER.fullmatch(line)
        if header:
            current = (header.group("identifier"), header.group("title").strip(), {}, number)
            raw.append(current)
            field_name = None
            continue
        if not line.strip():
            continue
        if current is None and line.strip() in _EMPTY_MARKERS:
            continue
        match = _FIELD.fullmatch(line)
        if match:
            if current is None:
                report.errors.append(f"{path.name}:{number} field outside an item")
                continue
            fields = current[2]
            field_name = match.group("name").strip()
            value = match.group("value").strip()
            if field_name in fields:
                report.errors.append(f"{current[0]} contains duplicate field: {field_name}")
            elif not value:
                report.errors.append(f"{current[0]} has an empty field: {field_name}")
            else:
                fields[field_name] = value
            continue
        if line.startswith("    ") and current is not None and field_name in current[2]:
            current[2][field_name] = f"{current[2][field_name]} {line.strip()}"
            continue
        report.errors.append(f"{path.name}:{number} invalid backlog content: {line}")
    return raw


def _build_item(
    identifier: str,
    title: str,
    source: str,
    fields: dict[str, str],
    todo_dir: Path,
    report: BacklogReport,
) -> BacklogItem | None:
    errors: list[str] = []

    missing = sorted(REQUIRED_FIELDS - fields.keys())
    if missing:
        report.errors.append(f"{identifier} is missing required fields: {', '.join(missing)}")
        return None

    unknown = sorted(fields.keys() - KNOWN_FIELDS)
    if unknown:
        errors.append(f"{identifier} has unknown fields: {', '.join(unknown)}")

    item_type = _scalar(fields["Type"])
    if item_type not in ITEM_TYPES:
        errors.append(f"{identifier} Type must be Epic, Story, or Task: {item_type}")
    status = _scalar(fields["Status"])
    if status not in STATUSES:
        errors.append(f"{identifier} has unsupported Status: {status}")
    priority = _scalar(fields["Priority"])
    if priority not in PRIORITIES:
        errors.append(
            f"{identifier} Priority must be one of {', '.join(sorted(PRIORITIES))}: {priority}"
        )
    created = date.min
    try:
        created = date.fromisoformat(_scalar(fields["Created"]))
    except ValueError:
        errors.append(f"{identifier} Created must use YYYY-MM-DD")

    dependencies = _references(identifier, "Dependencies", fields["Dependencies"], errors)

    parent: str | None = None
    required_for_parent: bool | None = None
    if item_type == "Epic":
        for name in ("Parent", "Required for parent"):
            if name in fields:
                errors.append(f"{identifier} Epic must not contain {name}")
    elif item_type in ITEM_TYPES:
        if "Parent" not in fields:
            errors.append(f"{identifier} is missing required field: Parent")
        else:
            parents = _references(identifier, "Parent", fields["Parent"], errors)
            if len(parents) > 1:
                errors.append(f"{identifier} Parent must be one identifier or None")
            parent = parents[0] if parents else None
        required_value = fields.get("Required for parent")
        if parent is not None:
            if required_value is None:
                errors.append(f"{identifier} is missing required field: Required for parent")
            elif _scalar(required_value) not in {"Yes", "No"}:
                errors.append(f"{identifier} Required for parent must be Yes or No")
            else:
                required_for_parent = _scalar(required_value) == "Yes"
        elif required_value is not None:
            errors.append(f"{identifier} without a Parent must not contain Required for parent")

    resolution = fields.get("Resolution")
    if status in CLOSED_STATUSES and resolution is None:
        errors.append(f"{identifier} with Status {status} requires Resolution")
    if status not in CLOSED_STATUSES and resolution is not None:
        errors.append(f"{identifier} with active Status {status} must not contain Resolution")

    notes = _paths(identifier, "Notes", fields.get("Notes"), todo_dir, errors)
    specs = _paths(identifier, "Spec", fields.get("Spec"), todo_dir, errors)
    if "Notes" in fields and "Summary" not in fields:
        errors.append(f"{identifier} has Notes and therefore requires Summary")

    if errors:
        report.errors.extend(errors)
        return None
    return BacklogItem(
        identifier=identifier,
        title=title,
        source=source,
        item_type=item_type,
        status=status,
        created=created,
        area=_scalar(fields["Area"]),
        priority=priority,
        dependencies=dependencies,
        parent=parent,
        required_for_parent=required_for_parent,
        resolution=resolution,
        notes=notes,
        specs=specs,
    )


def _validate_placement(report: BacklogReport) -> None:
    for item in report.items:
        if item.source == ARCHIVE_FILE and item.status not in CLOSED_STATUSES:
            report.errors.append(
                f"{item.identifier} in {ARCHIVE_FILE} must be Completed or Rejected, is {item.status}"
            )
        if item.source == TODO_FILE and item.status in CLOSED_STATUSES:
            report.notices.append(
                f"{item.identifier} is {item.status}; move it to {ARCHIVE_FILE}"
            )


def _validate_relationships(report: BacklogReport, known_ids: set[str]) -> None:
    by_id = {item.identifier: item for item in report.items}
    for item in report.items:
        if item.parent is not None:
            if item.parent not in known_ids:
                report.errors.append(f"{item.identifier} references missing parent: {item.parent}")
            elif item.parent in by_id:
                parent = by_id[item.parent]
                allowed = {"Epic"} if item.item_type == "Story" else {"Epic", "Story"}
                if parent.item_type not in allowed:
                    report.errors.append(
                        f"{item.identifier} {item.item_type} cannot use "
                        f"{parent.item_type} {parent.identifier} as Parent"
                    )
        for dependency in item.dependencies:
            if dependency == item.identifier:
                report.errors.append(f"{item.identifier} must not depend on itself")
            elif dependency not in known_ids:
                report.errors.append(
                    f"{item.identifier} references missing dependency: {dependency}"
                )

    parent_edges = {
        item.identifier: (item.parent,) if item.parent in by_id else ()
        for item in report.items
    }
    dependency_edges = {
        item.identifier: tuple(d for d in item.dependencies if d in by_id and d != item.identifier)
        for item in report.items
    }
    _reject_cycles(parent_edges, "parent", report)
    _reject_cycles(dependency_edges, "dependency", report)


def _validate_lifecycle(report: BacklogReport) -> None:
    children: dict[str, list[BacklogItem]] = {item.identifier: [] for item in report.items}
    for item in report.items:
        if item.parent in children:
            children[item.parent].append(item)

    for item in report.items:
        kids = children[item.identifier]
        required = [child for child in kids if child.required_for_parent]
        if item.item_type == "Epic" and item.status not in {"Open", "Rejected"} and not required:
            report.errors.append(
                f"{item.identifier} Epic with Status {item.status} requires at least one required child"
            )
        if item.status == "Awaiting confirmation":
            unready = [c.identifier for c in required if c.status not in READY_CHILD_STATUSES]
            if unready:
                report.errors.append(
                    f"{item.identifier} cannot be Awaiting confirmation while required "
                    f"children are active: {', '.join(unready)}"
                )
        if item.status == "Completed":
            incomplete = [c.identifier for c in required if c.status != "Completed"]
            if incomplete:
                report.errors.append(
                    f"{item.identifier} cannot be Completed while required children "
                    f"are incomplete: {', '.join(incomplete)}"
                )
        if item.status == "Rejected":
            active = [c.identifier for c in kids if c.status not in CLOSED_STATUSES]
            if active:
                report.errors.append(
                    f"{item.identifier} is Rejected but has active children: {', '.join(active)}"
                )


def _reject_cycles(edges: dict[str, tuple[str, ...]], label: str, report: BacklogReport) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str, trail: tuple[str, ...]) -> bool:
        if identifier in visiting:
            report.errors.append(f"{label} cycle detected: {' -> '.join((*trail, identifier))}")
            return True
        if identifier in visited:
            return False
        visiting.add(identifier)
        for target in edges.get(identifier, ()):
            if visit(target, (*trail, identifier)):
                return True
        visiting.discard(identifier)
        visited.add(identifier)
        return False

    for identifier in edges:
        if identifier not in visited and visit(identifier, ()):
            return


def _scalar(value: str) -> str:
    normalized = value.strip()
    if normalized.endswith("."):
        normalized = normalized[:-1].rstrip()
    return normalized


def _references(identifier: str, name: str, value: str, errors: list[str]) -> tuple[str, ...]:
    normalized = _scalar(value)
    if normalized == "None":
        return ()
    references = []
    for part in (p.strip() for p in normalized.split(",")):
        match = _REFERENCE.fullmatch(part)
        if match is None:
            errors.append(f"{identifier} {name} must contain backticked identifiers or None")
            return ()
        references.append(match.group(1))
    if len(set(references)) != len(references):
        errors.append(f"{identifier} contains duplicate {name} references")
    return tuple(references)


def _paths(
    identifier: str,
    name: str,
    value: str | None,
    todo_dir: Path,
    errors: list[str],
) -> tuple[str, ...]:
    if value is None:
        return ()
    paths = []
    for part in (p.strip() for p in _scalar(value).split(",")):
        match = _PATH_REFERENCE.fullmatch(part)
        if match is None:
            errors.append(f"{identifier} {name} must contain backticked relative paths")
            return ()
        relative = PurePosixPath(match.group(1))
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"{identifier} {name} path must stay inside the backlog folder: {relative}")
        elif not (todo_dir / relative).is_file():
            errors.append(f"{identifier} {name} file does not exist: {relative}")
        else:
            paths.append(str(relative))
    return tuple(paths)


def format_report(report: BacklogReport) -> str:
    lines = [f"error: {e}" for e in report.errors]
    lines += [f"notice: {n}" for n in report.notices]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: backlog.py <backlog-folder>", file=sys.stderr)
        return 2
    report = validate_backlog(Path(argv[1]))
    output = format_report(report)
    if output:
        print(output)
    print(f"{len(report.items)} valid items, {len(report.errors)} errors, {len(report.notices)} notices")
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
