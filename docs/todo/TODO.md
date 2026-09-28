# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `TASK-015` **Einzelitem-Abruf in backlog.py für archive.md**
  - Type: Task.
  - Parent: None.
  - Status: Awaiting confirmation.
  - Created: 2026-09-27.
  - Area: Dokumentation.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: `backlog.py` bekommt einen Modus, der ein einzelnes Item per ID aus
    `TODO.md` oder `archive.md` ausgibt, ohne die jeweilige Datei komplett
    einzulesen. Die Leseregel in `plugin/skills/todo/format.md` ("Read an
    archived item in full") wird darauf umgestellt, diesen Modus statt eines
    Volllesens von `archive.md` zu nutzen.
  - Completion criteria: `backlog.py <backlog-ordner> --show <ID>` (oder
    vergleichbare Option) gibt genau den Eintrag mit ID, Feldern und
    Freitext-Feldern (Goal, Completion criteria, Resolution) aus; Tests in
    `tests/test_backlog.py` decken den neuen Modus ab (gefundene ID, fehlende
    ID); `format.md` und `SKILL.md` verweisen auf den neuen Modus statt auf
    Volllesen von `archive.md`; `docs/techdocs/interfaces.md` beschreibt die
    neue Option.
  - Notes: `items/TASK-015/TASK-015_notes.md`.
  - Summary: Das Archiv soll nicht mehr als ganze Datei geladen werden. Erst
    kommt eine kurze Liste aller Einträge, danach werden nur die Einträge
    geöffnet, die gerade gebraucht werden.
