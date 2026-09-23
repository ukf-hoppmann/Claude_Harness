---
name: todo
description: Rules for the project backlog (TODO.md, archive.md, per-item notes and specs). Use when reading, discussing, creating, updating, or archiving backlog items — epics, stories, tasks, their status, notes, or specs.
---

# Project backlog

## Before you start

1. Read `.claude-harness/config.toml` in the project root. If `[modules].todo`
   is not `true`, these rules do not apply — say so and stop.
2. The backlog folder is `[todo].path` below `[docs].root` (default
   `docs/todo`). Write backlog texts in `[docs].language`; field names stay
   English.
3. If `TODO.md` is missing there, tell the user and ask for permission before
   creating anything. The backlog may just live elsewhere — look for it and
   ask. Only after approval, create `TODO.md` and `archive.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/todo/`.

## Reading order

Read only what the task needs:

- By default: `TODO.md` only.
- Discussing or deciding something about an item: also its `Notes`.
- Planning its implementation or asked about its spec: also its `Spec`.
  The spec is the input for a plan; do not write step-by-step plans into it.
- Overview across `TODO.md` and `archive.md` (e.g. to place new work): run
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py" <backlog folder> --index`
  instead of reading the files.
- `archive.md`: only when a specific archived item is needed in full.

## Working rules

- Refer to items as `Type ID`, e.g. `Story STORY-017`.
- You may change without asking: notes and specs (add and revise whatever is
  relevant), `Summary`/`Notes`/`Spec` fields, status up to
  `Awaiting confirmation` and back, wording fixes, archiving closed items.
- Ask first before: creating or deleting items; changing the meaning of
  `Goal`/`Completion criteria`; changing `Parent`, `Required for parent`,
  `Dependencies`, or `Priority`; setting `Completed`/`Rejected`; reopening.
- When you start work on an item, set it to `In progress`. When its
  completion criteria are met and verified, set it to `Awaiting confirmation`
  yourself and tell the owner — do not ask whether to do so.
- Only the project owner confirms `Completed` or `Rejected`. Record it in
  `Resolution`, then move the item unchanged to `archive.md`.
- When an item gets notes, create `items/<ID>/<ID>_notes.md`, add the `Notes`
  path, and write a plain-language `Summary` (required with `Notes`).
- Record decisions in the item's notes as they happen, dated, under
  `Discussed` / `Decided` / `Open`.
- When all required children of a parent are `Completed`, check the parent's
  own completion criteria: if met, set it to `Awaiting confirmation` and tell
  the owner; otherwise say what is missing. A parent is only completed or
  rejected once every child is closed or reparented.
- New work goes under an existing epic or story whenever one fits — including
  archived ones. Prefer proposing to reopen a closed parent (owner approval,
  reason recorded in its notes) over creating a new epic or story.
- Reuse existing areas before inventing new ones. New IDs take the next free
  number of their type.

Field syntax, lifecycle rules, and details: [format.md](format.md). Read it
when creating items or when the backlog check reports an error.

The backlog is checked automatically at the end of a turn in which files in
the backlog folder changed. Fix every reported error.
