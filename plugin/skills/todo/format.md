# Claude_Harness backlog format, version 1

The backlog lives in the folder configured as `[todo].path` in
`.claude-harness/config.toml` (default `docs/todo`):

```
<todo path>/
 ├─ TODO.md          active items (Open, In progress, Awaiting confirmation)
 ├─ archive.md       Completed and Rejected items
 └─ items/<ID>/      optional notes and spec per item
```

Both files contain exactly one `## Work items` section. An empty section
contains the line `No entries.`. `TODO.md` and `archive.md` form one backlog:
identifiers are unique across both, and references may cross between them.
Position and ordering do not determine status or hierarchy.

## Language

Field names, types, statuses, priorities, and section headings are English so
the format is usable without knowing the project's working language. Content
(titles, goals, criteria, summaries, notes, specs) is written in the project's
working language.

## Entry syntax

```markdown
- `STORY-001` **Concise title**
  - Type: Story.
  - Parent: `EPIC-001`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: YYYY-MM-DD.
  - Area: Project area.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Describe the result. Continuation lines are indented
    by four spaces.
  - Completion criteria: State how the result is verified.
```

Identifiers use the pattern `PREFIX-NNN` (`EPIC-001`, `STORY-001`,
`TASK-001`), counted per type. They never change — not when an item changes
type, status, priority, parent, or scope. References are written in backticks;
several references are comma-separated; no reference is `None`.

## Status model

- `Open`: Accepted backlog work that has not started.
- `In progress`: Work whose implementation or investigation has begun.
- `Awaiting confirmation`: Implementation and verification are complete, but
  project-owner confirmation is still pending.
- `Completed`: Explicitly confirmed as complete by the project owner.
- `Rejected`: Explicitly rejected by the project owner.

Passing tests, commits, merges, silence, and agent assessment do not constitute
completion confirmation.

## Work-item types

- `Epic`: A larger outcome containing multiple independently verifiable
  results.
- `Story`: An independently deliverable and observable result for a user,
  operator, or consuming system.
- `Task`: Supporting work that does not by itself deliver an independent
  stakeholder-visible result.

An epic has no parent. A story may belong to one epic. A task may belong to one
story or directly to one epic when it enables multiple stories. Stories and
tasks may also be standalone (`Parent: None`).

`Parent` records outcome membership. `Dependencies` record prerequisites or
execution ordering. These relationships are independent. Neither graph may
contain cycles.

## Required fields

Every entry contains `Type`, `Status`, `Created`, `Area`, `Priority`,
`Dependencies`, `Goal`, and `Completion criteria`.

A story or task additionally contains `Parent`. A parented story or task
contains `Required for parent` (`Yes` or `No`). Optional children never block
their parent.

A completed or rejected entry contains `Resolution`, recording the explicit
project-owner decision; active entries never contain it. Missing historical
evidence remains visible and is never invented.

Priorities are `Urgent`, `Important`, and `Prospective`.

Areas are free text. An existing area is reused whenever it plausibly fits; a
new area is introduced only when no existing one fits.

## Parent lifecycle

- An epic needs at least one required child before it leaves `Open`.
- A parent cannot be `Awaiting confirmation` while a required child is `Open`
  or `In progress`, and cannot be `Completed` until every required child is
  `Completed`.
- A completed parent receives no new required child unless the project owner
  reopens it first.
- Rejecting a parent never silently closes its children; active children are
  reparented or get their own decision first.

## Optional fields

- `Summary`: Short, non-technical summary for the project owner. Required as
  soon as the item has `Notes`.
- `Notes`: Path to the item's notes file, relative to the backlog folder.
- `Spec`: Path to the item's spec file, relative to the backlog folder.

`Notes` and `Spec` appear only when the file exists. For now they contain
exactly one path; multiple comma-separated paths are allowed.

## Item files

Items that need discussion or planning get a folder `items/<ID>/` whose name is
exactly the item ID. Small items need no folder. The folder does not depend on
the parent, so reparenting never moves files.

- `<ID>_notes.md`: Discussions and decisions. One file that grows over time;
  entries are dated (`## YYYY-MM-DD — Topic`) and use the headings
  `### Discussed`, `### Decided`, and `### Open`.
- `<ID>_spec.md`: Technical summary (what and why, constraints, interfaces,
  affected files, acceptance criteria). It is the basis for planning an
  implementation but contains no step-by-step plan itself.

Additional files are created only when needed, with a topic suffix such as
`<ID>_spec_<topic>.md`; the first file is never renamed. Notes and specs may be
revised when plans change, but changes of direction are recorded in the notes
instead of being silently overwritten.

Daily development reports do not belong in the backlog folder.

## Archive

Once an item is `Completed` or `Rejected` and has its `Resolution`, it moves
unchanged from `TODO.md` to `archive.md`. Its item folder stays in `items/`.
References to archived IDs remain valid. `archive.md` never contains active
items.

## Change authority

The agent may change without asking:

- notes and spec files: add, revise, or restructure whatever is relevant;
- the `Summary`, `Notes`, and `Spec` fields;
- status transitions `Open` → `In progress`, `In progress` →
  `Awaiting confirmation`, and back to `In progress`;
- wording fixes that do not change meaning;
- moving confirmed or rejected items to `archive.md`.

The agent proposes and waits for project-owner approval before:

- creating or deleting items;
- changing the meaning of `Goal` or `Completion criteria`, or changing
  `Parent`, `Required for parent`, `Dependencies`, or `Priority`;
- setting `Completed` or `Rejected`, or reopening a closed item.

Reopening a closed item requires a recorded reason.

## Proposing new items

Propose an item only for concrete, relevant project work that was discussed
but intentionally not done now. Check the backlog and archive for equivalent
work first. Questions, discarded alternatives, temporary debugging steps, and
vague ideas without a next action are not items. A proposal states title,
type, goal, completion criteria, area, and priority.

Never copy credentials, personal data, or unnecessary conversation quotes into
the backlog.
