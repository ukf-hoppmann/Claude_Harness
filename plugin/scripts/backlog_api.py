"""Work on a backlog through the ToDo-Viewer's HTTP API (todo.backend = "api").

Usage: backlog_api.py [--project <name>] <command> [arguments]; see USAGE.
The backlog comes from the harness config of the session's project, never from a path argument.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode

from backlog import TODO_FILE
from harness_config import CONFIG_RELATIVE_PATH, ROOT_PROJECT, ConfigError, project_root
from projects import Project, load_projects
from worktree import WorktreeError, in_main_checkout

USAGE = """usage: backlog_api.py [--project <name>] <command> [arguments]
  --project <name>                        a registered subproject; default: the root project
  health                                  server reachable?
  index                                   one line per item: ID | Type | Status | Title | Parent
  show <ID>                               item as JSON, with its version (archived items too)
  create                                  stdin: JSON fields (type, title, area, goal, completion_criteria, ...)
  update <ID> <version>                   stdin: JSON {"fields": {...}, "resolution": ...}
  note <ID>                               stdin: JSON {"topic", "discussed", "decided", "open", "summary"}
  doc <ID> <name>                         print a notes/spec document: 'version: <v>', blank line, content
  put-doc <ID> <name> <version|new> [--summary TEXT]   stdin: the complete new document text
  delete <ID> <version> [--cascade]       move to the trash (with --cascade including descendants)
  trash                                   items in the trash as JSON
  restore <ID> <version>                  restore an item from the trash"""
EXIT_ERROR, EXIT_USAGE, EXIT_UNREACHABLE = 1, 2, 3
TIMEOUT_SECONDS = 15
CONFLICT_HINT = "read the item again and check the change before retrying; never retry blindly"


class ApiError(Exception):
    def __init__(self, message: str, exit_code: int = EXIT_ERROR):
        super().__init__(message)
        self.exit_code = exit_code


class Api:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def call(self, method: str, path: str, body: Any = None, query: dict[str, str] | None = None) -> Any:
        url = self.base_url + path + (f"?{urlencode(query)}" if query else "")
        data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
        request = urllib.request.Request(url, data=data, method=method)
        if data is not None:
            request.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                return json.loads(response.read() or b"null")
        except urllib.error.HTTPError as exc:
            raise ApiError(_http_error(exc)) from exc
        except (urllib.error.URLError, OSError) as exc:
            reason = getattr(exc, "reason", exc)
            raise ApiError(
                f"ToDo-Viewer API not reachable at {self.base_url} ({reason}). Tell the user and ask "
                "whether to start the server, work on the files instead, or stop.",
                EXIT_UNREACHABLE,
            ) from exc


def _http_error(exc: urllib.error.HTTPError) -> str:
    raw = exc.read().decode(errors="replace")
    try:
        body = json.loads(raw)
    except ValueError:
        return f"HTTP {exc.code}: {raw.strip() or exc.reason}"
    if not isinstance(body, dict) or "code" not in body:
        return f"HTTP {exc.code}: {json.dumps(body, ensure_ascii=False)}"
    message = f"HTTP {exc.code} {body['code']}: {body.get('message', '')}"
    if body.get("details"):
        message += f"\ndetails: {json.dumps(body['details'], ensure_ascii=False)}"
    if body["code"] == "version_conflict":
        message += f"\n{CONFLICT_HINT}"
    return message


def find_project(name: str) -> Project:
    """The session's project with that name; its config decides the backlog and the API URL."""
    root = project_root({"cwd": os.getcwd()})
    try:
        projects = load_projects(root)
    except ConfigError as exc:
        raise ApiError(str(exc), EXIT_USAGE) from exc
    if projects is None:
        raise ApiError(f"no {CONFIG_RELATIVE_PATH} in {root}; the harness is not set up here", EXIT_USAGE)
    project = projects.get(name)
    if project is None:
        known = ", ".join(p.name for p in projects.projects)
        raise ApiError(f"unknown project {name!r} (known: {known})", EXIT_USAGE)
    if not project.config.enabled("todo"):
        raise ApiError(f"module todo is off in project {project.name}", EXIT_USAGE)
    return project


def source_folder(project: Project) -> Path:
    """The project's backlog folder in the main checkout: the server writes there, never into a worktree."""
    folder = project.root / project.config.todo_path
    if not (folder / TODO_FILE).is_file():
        raise ApiError(
            f"{folder / TODO_FILE} does not exist; the backlog must be created first (skill claude-harness:todo)",
            EXIT_USAGE,
        )
    try:
        return in_main_checkout(folder)
    except (WorktreeError, OSError):
        # Not in a Git repository: the folder is its own source.
        return folder.resolve()


def source_id(api: Api, folder: Path, project: Project) -> str:
    for source in api.call("GET", "/sources"):
        if Path(source["path"]).resolve() == folder:
            return source["id"]
    body = {"path": str(folder)}
    if project.name != ROOT_PROJECT:
        # Without a name the server uses the Git repository's, which subprojects share with the root.
        body["project"] = project.name
    source = api.call("POST", "/sources", body)
    print(f"registered backlog {folder} as ToDo-Viewer source {source['id']}", file=sys.stderr)
    return source["id"]


def _stdin_json() -> dict[str, Any]:
    try:
        data = json.loads(sys.stdin.read())
    except ValueError as exc:
        raise ApiError(f"stdin must be a JSON object: {exc}", EXIT_USAGE) from exc
    if not isinstance(data, dict):
        raise ApiError("stdin must be a JSON object", EXIT_USAGE)
    return data


def _print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _item(sid: str, identifier: str, suffix: str = "") -> str:
    return f"/items/{quote(sid)}/{quote(identifier)}{suffix}"


def run(project_name: str, command: str, args: list[str]) -> None:
    arity = {"health": 0, "index": 0, "show": 1, "create": 0, "update": 2, "note": 1, "doc": 2,
             "put-doc": 3, "delete": 2, "trash": 0, "restore": 2}
    options = {"put-doc": "--summary", "delete": "--cascade"}
    flag = options.get(command)
    positional = list(args)
    option_value: str | bool | None = None
    if flag == "--cascade" and flag in positional:
        positional.remove(flag)
        option_value = True
    elif flag == "--summary" and flag in positional:
        at = positional.index(flag)
        if at + 1 >= len(positional):
            raise ApiError("--summary needs a text", EXIT_USAGE)
        option_value = positional[at + 1]
        del positional[at:at + 2]
    if command not in arity or len(positional) != arity[command]:
        raise ApiError(USAGE, EXIT_USAGE)
    project = find_project(project_name)
    api = Api(project.config.todo_api_url)
    if command == "health":
        _print_json(api.call("GET", "/health"))
        return
    sid = source_id(api, source_folder(project), project)

    if command == "index":
        items = api.call("GET", "/index", query={"source_id": sid})["items"]
        print("ID | Type | Status | Title | Parent")
        for item in items:
            print(f"{item['id']} | {item['type']} | {item['status']} | {item['title']} | {item['parent'] or '-'}")
    elif command == "show":
        _print_json(api.call("GET", _item(sid, positional[0])))
    elif command == "create":
        _print_json(api.call("POST", "/items", {**_stdin_json(), "source_id": sid}))
    elif command == "update":
        identifier, version = positional
        body = _stdin_json()
        _print_json(api.call("PATCH", _item(sid, identifier), {"version": version, **body}))
    elif command == "note":
        _print_json(api.call("POST", _item(sid, positional[0], "/notes"), _stdin_json()))
    elif command == "doc":
        identifier, name = positional
        document = api.call("GET", _item(sid, identifier, f"/documents/{quote(name)}"))
        sys.stdout.write(f"version: {document['version']}\n\n{document['content']}")
    elif command == "put-doc":
        identifier, name, version = positional
        body: dict[str, Any] = {"content": sys.stdin.read(), "version": None if version == "new" else version}
        if option_value is not None:
            body["summary"] = option_value
        document = api.call("PUT", _item(sid, identifier, f"/documents/{quote(name)}"), body)
        print(f"{document['name']}: saved, version {document['version']}")
    elif command == "delete":
        identifier, version = positional
        query = {"version": version, **({"cascade": "true"} if option_value else {})}
        _print_json(api.call("DELETE", _item(sid, identifier), query=query))
    elif command == "trash":
        _print_json(api.call("GET", "/trash", query={"source_id": sid}))
    elif command == "restore":
        identifier, version = positional
        _print_json(api.call("POST", f"/trash/{quote(sid)}/{quote(identifier)}/restore", {"version": version}))


def main(argv: list[str]) -> int:
    args = argv[1:]
    project_name = ROOT_PROJECT
    if args[:1] == ["--project"] and len(args) >= 2:
        project_name, args = args[1], args[2:]
    if not args:
        print(USAGE, file=sys.stderr)
        return EXIT_USAGE
    try:
        run(project_name, args[0], args[1:])
    except ApiError as exc:
        print(exc if exc.exit_code == EXIT_USAGE and str(exc) == USAGE else f"error: {exc}", file=sys.stderr)
        return exc.exit_code
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
