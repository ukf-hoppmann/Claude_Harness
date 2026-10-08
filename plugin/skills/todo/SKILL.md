---
name: todo
description: Rules for the project backlog (via the ToDo-Viewer API, or TODO.md, archive.md, per-item notes and specs in files mode). Use when reading, discussing, creating, updating, or archiving backlog items — epics, stories, tasks, their status, notes, or specs.
---

# Project backlog

## Before you start

1. Read `.claude-harness/config.toml` of the project the work belongs to (with
   subprojects, the session start lists each project and its folder; paths
   below are relative to that folder). If `[modules].todo` is not `true`,
   these rules do not apply — say so and stop.
2. The backlog folder is `[todo].path` below `[docs].root` (default
   `docs/todo`). Write backlog texts in `[docs].language`; field names stay
   English.
3. `[todo].backend` decides how you work on it (default `api`):
   - `api`: only through the ToDo-Viewer's HTTP API, using
     `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog_api.py" [--project <name>] <command>`
     (`--project` for a subproject's backlog).
     Commands and inputs: [api.md](api.md); read it before the first call.
     **Never read, edit, create, or delete `TODO.md`, `archive.md`, or `items/`
     in this mode** — not even to look something up; the server owns them and
     may keep the backlog in its database instead. They are not required here.
   - `files`: edit the Markdown files directly as [format.md](format.md)
     describes.
4. API mode: if the helper exits with code 3 (server not reachable), tell the
   user and ask whether to start the server, work on the files this time, or
   stop. Do not fall back to the files on your own.
5. Files mode only (API mode needs no `TODO.md`): if `TODO.md` is missing, tell the user and ask for permission before
   creating anything. The backlog may just live elsewhere — look for it and
   ask. Only after approval, create `TODO.md` and `archive.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/todo/`.

## Reading order

Read only what the task needs:

- By default: the overview — API: `index`; files: `TODO.md`.
- Discussing or deciding something about an item: also its `Notes`.
- Planning its implementation or asked about its spec: also its `Spec`.
  The spec is the input for a plan; do not write step-by-step plans into it.
- Overview across `TODO.md` and `archive.md` (e.g. to place new work or to
  look for earlier work): API: `index`; files: run
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py" <backlog folder> --index`.
- A single item, archived ones included — API: `show <ID>`; files: the
  item in `TODO.md`, or `backlog.py <backlog folder> --show <ID> [<ID> ...]`.
  Pick the IDs from the overview. Never read `archive.md` in full.

## Working rules

- Refer to items as `Type ID`, e.g. `Story STORY-017`.
- You may change without asking: notes and specs (add and revise whatever is
  relevant), `Summary`/`Notes`/`Spec` fields, status up to
  `Awaiting confirmation` and back, wording fixes, archiving closed items.
- Moving an item to the trash (deleting) needs no extra confirmation when the
  user's request clearly asks for it; otherwise propose it first. Only the
  user removes items from the trash for good — never do that yourself.
- Ask first before: creating items; changing the meaning of
  `Goal`/`Completion criteria`; changing the type (API: `retype`, which also changes the ID); changing `Parent`, `Required for parent`,
  `Dependencies`, or `Priority`; setting `Completed`/`Rejected`; reopening.
- When you start work on an item, set it to `In progress`. When its
  completion criteria are met and verified, set it to `Awaiting confirmation`
  yourself and tell the owner — do not ask whether to do so.
- Only the project owner confirms `Completed` or `Rejected`. Record it in
  `Resolution`; the item then moves unchanged to `archive.md` (API: the
  server moves it).
- When an item gets notes, it needs a plain-language `Summary` (required with
  `Notes`). Files: create `items/<ID>/<ID>_notes.md` and add the `Notes`
  path; API: the first notes entry does both.
- Record decisions in the item's notes as they happen, dated, under
  `Discussed` / `Decided` / `Open`.
- Before rejecting a required child, ask in the same question whether it
  becomes `Required for parent: No` (then also adjust the parent's `Goal` and
  `Completion criteria` if they name the child's content) or whether the
  parent is rejected too; record the answer in the parent's notes.
- When all required children of a parent are `Completed`, check the parent's
  own completion criteria: if met, set it to `Awaiting confirmation` and tell
  the owner; otherwise say what is missing. A parent is only completed or
  rejected once every child is closed or reparented.
- New work goes under an existing epic or story whenever one fits — including
  archived ones. Prefer proposing to reopen a closed parent (owner approval,
  reason recorded in its notes) over creating a new epic or story.
- If the fitting parent is closed, ask whether to reopen it in the same
  question that proposes the new item, before creating anything. Without a
  yes, do not create the item without a parent; ask how to proceed.
- With subprojects, each project has its own backlog. New items go into the
  backlog of the project the work belongs to; if that is unclear, ask.
- Reuse existing areas before inventing new ones. Files: new IDs take the
  next free number of their type; API: the server assigns them.

## Notes

Reminders, open questions, observations, and ideas without a completion
definition are not backlog work; they are notes (skill `claude-harness:notes`,
when `[modules].notes` is on). Turning a note into an item and an item back
into a note runs through that skill. A backlog item's notes entries
(`<ID>_notes.md`) are not those notes; when unclear which is meant, ask.

## Committing backlog changes

- Files mode: backlog changes belong to the change they describe and are
  committed with it (in a worktree: in its branch).
- API mode: the server writes into the backlog folder of the main checkout,
  never into a worktree, and does not commit. Commit those files in the main
  checkout on their own (message `Backlog: …`) when the task is done. During
  a worktree change, do it after `ExitWorktree` and before the merge.

Field syntax, lifecycle rules, and details: [format.md](format.md). Read it
when creating items or when a check or the server reports a rule violation.

Files mode only: the backlog is checked automatically at the end of a turn in
which files in the backlog folder changed. Fix every reported error.
