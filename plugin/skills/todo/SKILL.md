---
name: todo
description: Rules for the project backlog (TODO.md, archive.md, per-item notes and specs). Use when reading, discussing, creating, updating, or archiving backlog items — epics, stories, tasks, their status, notes, or specs.
---

# Project backlog

## Before you start

1. Read `.claude-harness/config.toml` in the project root. If `[modules].todo`
   is not `true`, these rules do not apply — say so and stop.
2. The backlog folder is `[todo].path` (default `docs/todo`).
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
- `archive.md`: only when an archived item is referenced.

## Working rules

- Refer to items as `Type ID`, e.g. `Story STORY-017`.
- You may change without asking: notes and specs (add and revise whatever is
  relevant), `Summary`/`Notes`/`Spec` fields, status up to
  `Awaiting confirmation` and back, wording fixes, archiving closed items.
- Ask first before: creating or deleting items; changing the meaning of
  `Goal`/`Completion criteria`; changing `Parent`, `Required for parent`,
  `Dependencies`, or `Priority`; setting `Completed`/`Rejected`; reopening.
- Only the project owner confirms `Completed` or `Rejected`. Record it in
  `Resolution`, then move the item unchanged to `archive.md`.
- When an item gets notes, create `items/<ID>/<ID>_notes.md`, add the `Notes`
  path, and write a plain-language `Summary` (required with `Notes`).
- Record decisions in the item's notes as they happen, dated, under
  `Discussed` / `Decided` / `Open`.
- Reuse existing areas before inventing new ones. New IDs take the next free
  number of their type.

Field syntax, lifecycle rules, and details: [format.md](format.md). Read it
when creating items or when the backlog check reports an error.

The backlog is checked automatically at the end of a turn in which files in
the backlog folder changed. Fix every reported error.
