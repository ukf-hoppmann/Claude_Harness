---
name: decomposition
description: Rules for splitting work into small, separately testable steps (development suite). Use when planning how to implement a change, presenting an implementation plan, or considering whether a backlog item should get child tasks.
---

# Decomposition

## Before you start

Read `.claude-harness/config.toml` in the project root. The rules apply only
if `[modules].development` is `true` and `[development].decomposition` is not
`false`; otherwise say so and stop.

## Why

Small steps with their own test fail early and cheaply instead of late and
expensively. A step that carries everything it needs can be implemented
without the planning session's context, even by a simpler model.

## Two levels

Work is split at two levels of very different size. Do not mix them.

### Backlog: child tasks (coarse)

Propose child tasks for a story only if all three hold:

1. Each task delivers a result the project owner can use or check on its own.
2. Each task can be finished in a session of its own.
3. The story does not fit sensibly into one implementation plan.

The layers of one feature are never backlog tasks; they are sections of the
plan. Create items only as the `todo` skill allows (owner approval).

### Plan: sections (fine)

An implementation plan consists of sections. A section is cut right when all
of these hold:

- **One job.** It can be described without "and also".
- **Testable alone.** It has its own test or an observable check: a command
  and its expected result.
- **Integrable alone.** After it, the project builds and all tests pass. No
  broken intermediate state.
- **Self-contained.** It names its goal, the files or symbols it touches, its
  interface to neighbouring sections, what it must not touch, its test, and
  when to stop and ask instead of guessing.
- **Decided.** It contains no open decision. Interfaces between sections
  (data formats, signatures, names) are fixed in the plan, not in a section.

Order sections by their dependencies: each section uses only sections that
are already implemented and tested. There is no fixed direction such as
bottom-up.

The last section is always **integration**: check the whole flow against the
original goal.

Do not split, or merge sections, when:

- the task has one job and one test (a bug fix, a config change): one
  section;
- a section would not be testable alone: merge it into the neighbour whose
  test covers it;
- the change is mechanical and the same across many files (a rename): one
  section;
- splitting would leave a state that does not build or fails tests.

Example: a button triggers processing whose result is stored, reloaded, and
shown. Sections: 1. persist, 2. load, 3. backend processing, 4. API
endpoint, 5. frontend button awaiting the response, 6. integration.

## Dimension checklist

While splitting, go through these dimensions for the task:

persistence · loading/state · domain logic · interfaces (API, CLI, file
formats, hooks) · UI · configuration · security · error handling ·
migration/operations · tests · documentation

- Assign every touched dimension to a section, or give it one of its own.
- Tests and documentation normally belong to the section that makes the
  change, not to a section of their own.
- End the plan with one line that records the result, e.g. "Dimensions:
  persistence §1, loading §2, domain logic §3, interfaces §4, UI §5, tests
  per section, docs §6; not touched: security, migration."

## Where the plan lives

The sections belong in the implementation plan (plan mode or chat). A
backlog spec stays without a step sequence.
