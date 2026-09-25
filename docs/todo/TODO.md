# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `EPIC-004` **Entwicklungsprozess & Prinzipien**
  - Type: Epic.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Verbindlich festlegen, wie in einem Projekt entwickelt wird:
    projektweite Architektur-Definitionen, Heuristik zur Task-Zerlegung,
    Change-Ablauf (Workspace, Ablauf, Cleanup), TDD-Ritual und einheitliche
    Testebenen (Unit/Integration/System), damit Qualität nicht vom Zufall
    abhängt.
  - Completion criteria: Architektur-Definitionen, Zerlegungs-Heuristik,
    Change-Ablauf und Testkommando sind dokumentiert und werden bei
    mindestens einem Change sichtbar angewendet.
  - Summary: Legt fest, wie entwickelt wird: Architekturregeln, Zerlegung,
    Change-Ablauf im Worktree, Tests und Versionierung. Ein eigenes
    Prinzipien-Dokument gehört nicht mehr dazu.
  - Notes: `items/EPIC-004/EPIC-004_notes.md`.

- `STORY-029` **SemVer-Versionierung klären und ggf. automatisieren**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: In progress.
  - Created: 2026-09-25.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Klären, ob und wie Versionierung nach SemVer (Major/Minor/Patch)
    automatisiert werden soll – etwa die Einstufung einer Änderung und das
    Anheben der Version in den Paketmetadaten – und das Vereinbarte
    umsetzen, damit Versionen nachvollziehbar und
    konsistent steigen.
  - Completion criteria: Die Entscheidung (ob, was und wie weit
    automatisiert wird) ist mit dem Owner geklärt und in den Notizen
    festgehalten; das Vereinbarte ist umgesetzt und an mindestens einer
    Änderung angewendet.
  - Summary: Klären, ob Claude bei Änderungen die Versionsnummer nach SemVer
    selbst einstufen und hochzählen soll, und das dann umsetzen.
  - Notes: `items/STORY-029/STORY-029_notes.md`.
  - Spec: `items/STORY-029/STORY-029_spec.md`.

