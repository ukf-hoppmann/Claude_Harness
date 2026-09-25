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
    Entwicklungsprinzipien, projektweite Architektur-Definitionen, Heuristik
    zur Task-Zerlegung, Change-Ablauf (Workspace, Ablauf, Cleanup), TDD-Ritual
    und einheitliche Testebenen (Unit/Integration/System), damit Qualität
    nicht vom Zufall abhängt.
  - Completion criteria: Prinzipien, Architektur-Definitionen,
    Zerlegungs-Heuristik, Change-Ablauf und Testkommando sind dokumentiert und
    werden bei mindestens einem Change sichtbar angewendet.

- `STORY-009` **Entwicklungsprinzipien-Dokument**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Projektbezogene Entwicklungsprinzipien (z. B. keine unnötigen
    Abstraktionen, keine spekulativen Features) explizit und
    projekt-konfigurierbar festhalten statt nur implizit im Systemverhalten
    zu belassen.
  - Completion criteria: Ein kurzes, prüfbares Prinzipien-Dokument liegt vor.

- `STORY-028` **Keine hartkodierten Pfade/Config-Werte im Code**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-25.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Eine Regel festlegen, dass Pfade und Verweise auf Configs,
    Datenbanken o. Ä. nicht fest im Code stehen, sondern über eine Config
    änderbar sind, da sie sich zwischen Umgebungen typischerweise
    unterscheiden. Fälle, in denen ein Pfad/eine URL bewusst fix im Code
    stehen soll, bleiben als benannte Ausnahme möglich.
  - Completion criteria: Die Regel ist als bindende Architekturregel
    dokumentiert und deckt ab: Pfade/Config-Verweise gehören in eine Config
    statt in den Code, mit einer klar benannten Ausnahme für bewusst fixe
    Werte.

