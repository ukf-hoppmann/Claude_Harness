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

- `STORY-026` **Abschnitte an Subagenten übergeben**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: No.
  - Status: Open.
  - Created: 2026-09-24.
  - Area: Entwicklung.
  - Priority: Prospective.
  - Dependencies: `STORY-004`.
  - Goal: Prüfen, ob und wie Plan-Abschnitte an einen Subagenten mit
    günstigerem Modell übergeben werden: eigener Agent im Plugin, Auftrag aus
    dem Abschnitts-Vertrag samt nötiger Architekturregeln, Rückmeldung in
    festem Format, Kontrolle jedes Abschnitts durch die Hauptsession,
    Verhalten der Hooks im Subagenten und eine Schwelle, ab wann sich die
    Übergabe lohnt.
  - Completion criteria: Es ist entschieden, ob Abschnitte übergeben werden.
    Falls ja, wurde mindestens ein Abschnitt eines realen Features von einem
    Subagenten ohne Rückfrage korrekt umgesetzt und von der Hauptsession
    geprüft.

- `STORY-022` **Change-Workflow im Worktree**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: In progress.
  - Created: 2026-09-24.
  - Area: Governance.
  - Priority: Urgent.
  - Dependencies: None.
  - Goal: Changes mit freigegebenem Plan laufen in einem eigenen Worktree,
    der vom aktuell ausgecheckten Branch abzweigt. Nach Abschluss committet
    die AI, merged selbstständig in diesen Ausgangsbranch zurück und löscht
    den Worktree. Changes ohne Plan laufen lokal. So kann parallel gearbeitet
    werden, ohne dass fremde Worktrees angefasst werden.
  - Completion criteria: Der Ablauf ist als Teilbereich der Suite
    `development` umgesetzt (Schalter, Session-Start-Hinweis, Skill) und
    getestet. Ein realer Change mit Plan ist vom Ausgangsbranch über Worktree,
    Merge-Commit und Löschen des Worktrees ohne Rückfrage durchgelaufen;
    Worktrees anderer Sessions blieben unberührt.
  - Summary: Größere Änderungen macht die AI in einer eigenen Arbeitskopie
    und führt sie danach selbst in den Branch zurück, von dem sie gestartet
    ist. Die früheren Tasks TASK-001 bis TASK-004 sind in der Spec
    aufgegangen.
  - Notes: `items/STORY-022/STORY-022_notes.md`.
  - Spec: `items/STORY-022/STORY-022_spec.md`.

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

- `STORY-016` **Umgang mit Secrets/Credentials**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Sicherheit.
  - Priority: Prospective.
  - Dependencies: None.
  - Goal: Eine Regel festlegen, wie mit erkennbaren Zugangsdaten in
    Kommandozeilen-Output, Logs oder Dateien umgegangen wird (z. B. nie in
    Klartext in Dateien schreiben, vor dem Committen prüfen).
  - Completion criteria: Die Regel ist dokumentiert und deckt mindestens die
    Fälle Logging, Dateien und Git-Commits ab.
