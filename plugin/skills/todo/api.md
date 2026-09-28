# Backlog through the ToDo-Viewer API

Used when `[todo].backend` is `api` (the default). The ToDo-Viewer server
checks the format and the parent rules, assigns IDs, writes notes entries in
the format, and detects concurrent changes through version tokens. It does
not know which changes the project owner approved: the change authority in
[SKILL.md](SKILL.md) still applies.

## Calling the helper

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog_api.py" <backlog folder> <command> [arguments]
```

The helper finds the ToDo-Viewer source of the backlog folder (and registers
it if missing) and reads the URL from `[todo].api_url`. Inside a worktree it
uses the same folder in the main checkout. JSON input goes to stdin; use a
quoted heredoc so the shell leaves the text alone:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog_api.py" docs/todo update STORY-017 3f9a... <<'EOF'
{"fields": {"status": "In progress"}}
EOF
```

| Command | Use |
|---|---|
| `health` | Is the server reachable? |
| `index` | Overview: `ID \| Type \| Status \| Title \| Parent` |
| `show <ID>` | One item as JSON with its `version`, archived items included |
| `create` | New item. stdin: `type`, `title`, `area`, `goal`, `completion_criteria`, optional `parent`, `required_for_parent` (`"Yes"`/`"No"`), `priority`, `dependencies` (list of IDs), `summary`. Prints the item with its new ID |
| `update <ID> <version>` | stdin: `{"fields": {...}}` with any of `title`, `status`, `parent`, `required_for_parent`, `priority`, `dependencies`, `area`, `goal`, `completion_criteria`, `summary`; add `"resolution": "..."` when setting `Completed` or `Rejected` |
| `note <ID>` | Append a dated notes entry. stdin: `{"topic": "...", "discussed": [...], "decided": [...], "open": [...]}`; add `"summary"` if the item has none yet |
| `doc <ID> <name>` | Print a notes or spec document: `version: <v>`, a blank line, the text. Names: `<ID>_notes.md`, `<ID>_spec.md`, `<ID>_spec_<topic>.md` |
| `put-doc <ID> <name> <version\|new> [--summary TEXT]` | Replace a document with the complete text from stdin, or create it with `new` (first notes need `--summary` if the item has none) |
| `delete <ID> <version> [--cascade]` | Move to the trash; an item with children needs `--cascade` (the server answers `has_children` first) |
| `trash` | Items in the trash |
| `restore <ID> <version>` | Restore from the trash |

The date of a notes entry is set by the server. To revise notes or a spec,
read it with `doc`, change the text, and write it back with `put-doc` and the
version you read.

## Errors

- Exit 1: the server refused; stderr shows `HTTP <status> <code>: <message>`
  and `details`.
  - `version_conflict`: someone changed the item or document since you read
    it. Read it again, check whether your change still fits, then decide —
    never repeat the call blindly.
  - A rule violation names the blocking items in `details.items`. Resolve it
    as [format.md](format.md) describes, or ask the owner.
- Exit 2: wrong call or invalid JSON on stdin.
- Exit 3: server not reachable; see step 4 in [SKILL.md](SKILL.md). The
  server usually runs permanently in a container; after changes to the
  ToDo-Viewer it must be rebuilt (`./todo.sh update` there).
