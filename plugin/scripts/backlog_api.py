"""Work on a backlog through the ToDo-Viewer's HTTP API (todo.backend = "api").

Usage: backlog_api.py [--project <name>] <command> [arguments]; see USAGE.
The backlog comes from the harness config of the session's project, never from a path argument.
"""
from __future__ import annotations

import sys
from typing import Any
from urllib.parse import quote

from viewer_api import (
    EXIT_USAGE, Api, ApiError, Target, find_project, print_json, print_projects, register_project, split_target,
    stdin_json, target_for, version_arg,
)

USAGE = """usage: backlog_api.py [--project <name> | --source <name>] <command> [arguments]
  --project <name>                        a registered subproject; default: the root project
  --source <name>                         another project's backlog by its exact name from 'sources'
                                          (only with the owner's explicit approval, see skill todo)
  health                                  server reachable?
  sources                                 the names of all projects the viewer knows, with their folders
  register                                register this backlog as a viewer project (only after the owner's yes)
  index                                   one line per item: ID | Type | Status | Area | Title | Parent
  show <ID>                               item as JSON, with its version (archived items too)
  areas                                   the areas in use, one per line
  create                                  stdin: JSON fields (type, title, area, goal, completion_criteria, ...)
  update <ID> <version>                   stdin: JSON {"fields": {...}, "resolution": ...}
  move <ID> <version> <parent|-> [--position N]   new parent ('-' = no parent) and position among siblings
  reopen <ID>                             reopen the item and its closed ancestors (In progress)
  note <ID>                               stdin: JSON {"topic", "discussed", "decided", "open", "summary"}
  doc <ID> <name>                         print a notes/spec document: 'version: <v>', blank line, content
  put-doc <ID> <name> <version|new> [--summary TEXT]   stdin: the complete new document text
  retype <ID> <version> <type>            change the type (Epic|Story|Task); the item gets a new ID
  delete <ID> <version> [--cascade]       move to the trash (with --cascade including descendants)
  trash                                   backlog items in the trash as JSON
  restore <ID>                            restore an item (with the descendants deleted with it) from the trash"""

BACKLOG_KINDS = ("epic", "story", "task")
NO_PARENT = ("", "-", None)


def _item(identifier: str, suffix: str = "") -> str:
    return f"/backlog/items/{quote(identifier)}{suffix}"


def _flag(value: Any) -> Any:
    """required_for_parent as the server wants it: the backlog format's Yes/No become true/false."""
    return {"yes": True, "no": False}.get(value.lower(), value) if isinstance(value, str) else value


def item_fields(target: Target, fields: dict[str, Any]) -> dict[str, Any]:
    """Fields as the server takes them: parent and dependencies by uid instead of label."""
    out = dict(fields)
    if "parent" in out:
        out["parent"] = None if out["parent"] in NO_PARENT else target.resolve(out["parent"])
    if "dependencies" in out:
        out["dependencies"] = [target.resolve(label) for label in out["dependencies"] or []]
    if "required_for_parent" in out:
        out["required_for_parent"] = _flag(out["required_for_parent"])
    return out


def _options(command: str, args: list[str]) -> tuple[list[str], dict[str, str | bool]]:
    """Positional arguments and the command's options (flags or options with a value)."""
    allowed = {"put-doc": {"--summary": False}, "delete": {"--cascade": True}, "move": {"--position": False}}
    flags = allowed.get(command, {})
    positional: list[str] = []
    options: dict[str, str | bool] = {}
    rest = iter(args)
    for arg in rest:
        if arg not in flags:
            positional.append(arg)
        elif flags[arg]:
            options[arg] = True
        else:
            value = next(rest, None)
            if value is None:
                raise ApiError(f"{arg} needs a value", EXIT_USAGE)
            options[arg] = value
    return positional, options


ARITY = {"health": 0, "sources": 0, "register": 0, "index": 0, "show": 1, "areas": 0, "create": 0, "update": 2,
         "move": 3, "reopen": 1, "note": 1, "doc": 2, "put-doc": 3, "retype": 3, "delete": 2, "trash": 0,
         "restore": 1}
# Position of the <version> argument per command.
VERSION_AT = {"update": 1, "move": 1, "put-doc": 2, "retype": 1, "delete": 1}


def run(project_name: str, source_name: str | None, command: str, args: list[str]) -> None:
    positional, options = _options(command, args)
    if command not in ARITY or len(positional) != ARITY[command]:
        raise ApiError(USAGE, EXIT_USAGE)
    # A wrong version is a wrong call: refuse it before anything reaches the server.
    at = VERSION_AT.get(command)
    if at is not None and not (command == "put-doc" and positional[at] == "new"):
        version_arg(positional[at])
    project = find_project(project_name)
    api = Api(project.config.todo_api_url)
    if command == "health":
        print_json(api.call("GET", "/core/health"))
        return
    if command == "sources":
        print_projects(api)
        return
    if command == "register":
        if source_name is not None:
            raise ApiError("register works only on the session's own backlog", EXIT_USAGE)
        record = register_project(api, project)
        print(f"registered as viewer project {record['name']!r} (uid {record['uid']})")
        return
    target = target_for(api, project, source_name)
    _run(target, command, positional, options)


def _run(target: Target, command: str, positional: list[str], options: dict[str, str | bool]) -> None:
    api, project = target.api, target.uid
    if command == "index":
        print(api.call("GET", "/backlog/index", query={"projects": project})["text"])
    elif command == "show":
        print_json(api.call("GET", _item(positional[0]), query={"project": project}))
    elif command == "areas":
        print("\n".join(api.call("GET", "/backlog/areas", query={"project": project})["areas"]))
    elif command == "create":
        fields = stdin_json()
        item_type = fields.pop("type", None)
        body = {"project": project, "type": item_type, "fields": item_fields(target, fields)}
        print_json(api.call("POST", "/backlog/items", body))
    elif command == "update":
        identifier, version = positional[0], version_arg(positional[1])
        data = stdin_json()
        body: dict[str, Any] = {"project": project, "version": version,
                                "fields": item_fields(target, data.get("fields") or {})}
        if "resolution" in data:
            body["resolution"] = data["resolution"]
        print_json(api.call("PUT", _item(identifier), body))
    elif command == "move":
        identifier, version, parent = positional[0], version_arg(positional[1]), positional[2]
        body = {"project": project, "version": version,
                "parent": None if parent in NO_PARENT else target.resolve(parent)}
        if "--position" in options:
            body["position"] = version_arg(str(options["--position"]))
        print_json(api.call("POST", _item(identifier, "/move"), body))
    elif command == "reopen":
        print_json(api.call("POST", _item(positional[0], "/reopen"), {"project": project}))
    elif command == "note":
        print_json(api.call("POST", _item(positional[0], "/notes"), {**stdin_json(), "project": project}))
    elif command == "doc":
        identifier, name = positional
        document = api.call("GET", _item(identifier, f"/documents/{quote(name)}"), query={"project": project})
        sys.stdout.write(f"version: {document['version']}\n\n{document['content']}")
    elif command == "put-doc":
        identifier, name, version = positional
        body = {"project": project, "content": sys.stdin.read(),
                "version": None if version == "new" else version_arg(version)}
        if "--summary" in options:
            body["summary"] = options["--summary"]
        document = api.call("PUT", _item(identifier, f"/documents/{quote(name)}"), body)
        print(f"{document['name']}: saved, version {document['version']}")
    elif command == "retype":
        identifier, version, new_type = positional
        body = {"project": project, "version": version_arg(version), "type": new_type}
        print_json(api.call("POST", _item(identifier, "/retype"), body))
    elif command == "delete":
        identifier, version = positional
        query = {"version": str(version_arg(version)), **({"cascade": "true"} if options.get("--cascade") else {})}
        print_json(api.call("DELETE", f"/workspace/elements/{quote(target.resolve(identifier))}", query=query))
    elif command == "trash":
        elements = api.call("GET", "/workspace/trash", query={"projects": project})
        print_json([e for e in elements if e.get("kind") in BACKLOG_KINDS])
    elif command == "restore":
        print_json(api.call("POST", "/workspace/trash/restore", {"uids": [target.resolve(positional[0])]}))


def main(argv: list[str]) -> int:
    args = argv[1:]
    try:
        project_name, source_name, args = split_target(args)
        if not args:
            print(USAGE, file=sys.stderr)
            return EXIT_USAGE
        run(project_name, source_name, args[0], args[1:])
    except ApiError as exc:
        print(exc if exc.exit_code == EXIT_USAGE and str(exc) == USAGE else f"error: {exc}", file=sys.stderr)
        return exc.exit_code
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
