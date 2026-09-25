# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `EPIC-007` **Plugin-Architektur**
  - Type: Epic.
  - Status: In progress.
  - Created: 2026-09-23.
  - Area: Architektur.
  - Priority: Urgent.
  - Dependencies: None.
  - Goal: Claude_Harness als Claude-Code-Plugin aufbauen, in dem die Module
    als Skills und die harten Regeln als Hooks umgesetzt sind, sodass Regeln
    gestuft geladen werden und bei unbeteiligten Aufgaben kaum Tokens kosten.
  - Completion criteria: Das Plugin ist in diesem Repo aktiv, mindestens ein
    Modul läuft als Skill mit zugehörigem Hook, und die Root-`CLAUDE.md`
    enthält nur Verweise statt Regeltexten.
  - Summary: Der Harness wird ein Zusatzpaket für Claude Code. Regeln werden
    nur dann geladen, wenn sie zur aktuellen Aufgabe passen; Pflichtregeln
    prüft ein Skript automatisch.
  - Notes: `items/EPIC-007/EPIC-007_notes.md`.

- `STORY-030` **Harness-Konfiguration aktualisieren**
  - Type: Story.
  - Parent: `EPIC-007`.
  - Required for parent: No.
  - Status: In progress.
  - Created: 2026-09-25.
  - Area: Architektur.
  - Priority: Normal.
  - Dependencies: `STORY-021`.
  - Goal: Ein `update`-Schritt (Skill) als Pendant zum `init`-Skill: Ein
    Projekt, das den Harness schon nutzt, kann prüfen, ob seine
    `.claude-harness/config.toml` dem aktuellen Schema entspricht, und
    fehlende Ergänzungen (i. d. R. neue Module oder Schema-Migrationen) nach
    Freigabe eintragen, ohne Bestehendes zu überschreiben. Dazu gehört ein
    Versionierungsmechanismus fürs Config-Schema: `CONFIG_VERSION` in
    `harness_config.py` wird um eine Migrationsliste je Versionsschritt
    erweitert, statt auf SemVer umzustellen.
  - Completion criteria: Der Aufruf des Update-Schritts auf ein Projekt mit
    veralteter Config wendet die fehlenden Migrationen an (mit Rückfragen nur
    bei neuen, wirklich zu entscheidenden Werten) und schreibt die Config auf
    die aktuelle Version; auf eine bereits aktuelle Config wird gemeldet, dass
    nichts zu tun ist; das Ergebnis besteht die bestehende Config-Validierung.
  - Summary: Ein neuer Befehl soll bestehende Harness-Configs in anderen
    Projekten automatisch auf den neuesten Stand bringen, ähnlich wie der
    Einrichtungs-Befehl das für neue Projekte tut.
  - Notes: `items/STORY-030/STORY-030_notes.md`.
