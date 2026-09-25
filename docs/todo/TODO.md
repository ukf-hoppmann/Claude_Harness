# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `EPIC-001` **Konfigurierbarer Harness (Policy)**
  - Type: Epic.
  - Status: In progress.
  - Created: 2026-09-23.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Eine projekteigene Konfigurationsdatei für das Claude_Harness-Plugin
    definieren, die nur echte Projektwerte enthält (Pfade, Sprache, aktive
    Module) und von Skills und Hooks gelesen wird. Weitere Felder bringt jedes
    Modul selbst mit. Genehmigungen und Rechte bleiben bei den nativen
    Claude-Code-Einstellungen.
  - Completion criteria: Das Konfigurationsschema ist validiert und
    dokumentiert und wird von den Hooks mehrerer Module tatsächlich gelesen und
    angewendet.
  - Summary: Jedes Projekt bekommt eine kleine Einstellungsdatei, in der steht,
    wo Dinge liegen, wie getestet wird und welche Harness-Teile an sind.
  - Notes: `items/EPIC-001/EPIC-001_notes.md`.

- `STORY-027` **Harness pro Teilprojekt**
  - Type: Story.
  - Parent: `EPIC-001`.
  - Required for parent: Yes.
  - Status: In progress.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Ein Repository kann mehrere Teilprojekte mit je eigener
    Harness-Konfiguration, Doku, Backlog und Architekturregeln enthalten
    (z. B. Plugin-Core im Root, jedes Plugin in seinem Ordner). Startet die
    Session im Teilprojekt, liegt im Repo-Root keine Harness-Datei. Beim
    Start im Root legt eine optionale, minimale Registry fest, welche
    Konfiguration für welche Datei gilt. Hooks, Daily Reports und der
    Worktree-Workflow arbeiten korrekt, wenn Teilprojekt-Root und Git-Root
    verschieden sind.
  - Completion criteria: In einem Test-Repo mit Root-Projekt und zwei
    Plugin-Teilprojekten gilt beim Bearbeiten einer Datei nachweislich die
    Konfiguration ihres Teilprojekts, sowohl beim Start im Teilprojekt als
    auch beim Start im Root mit Registry. Ein Daily Report im Teilprojekt
    enthält nur dessen Änderungen. Tests decken beides ab.
  - Summary: Der Harness soll in einem gemeinsamen Repo nur für einzelne
    Teile gelten können, z. B. für ein einzelnes Plugin, mit eigener Doku und
    eigenen Regeln, ohne dass Kollegen im Repo-Root etwas davon sehen.
  - Notes: `items/STORY-027/STORY-027_notes.md`.
  - Spec: `items/STORY-027/STORY-027_spec.md`.

- `TASK-008` **Architekturregeln pro Projekt**
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Awaiting confirmation.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-007`.
  - Goal: Die Architektur-Hooks verlangen die Regeln des Projekts, zu dem die
    geänderte Datei, die Spec oder der Plan gehört.
  - Completion criteria: Tests zeigen: Eine Änderung im Teilprojekt verlangt
    dessen Regeln, eine Änderung im Core die Root-Regeln. Ein Plan verlangt
    die Regeln jedes darin genannten Projekts.

- `TASK-009` **Geerbte Architekturregeln**
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-008`.
  - Goal: Ein Projekt kann in `## Inherited rules` seiner `architecture.md`
    Regeln eines anderen Projekts übernehmen (Hauptdatei oder einzelne
    Scopes). Der Hook verlangt sie zusätzlich.
  - Completion criteria: Tests zeigen: Erbt ein Teilprojekt `root:
    architecture.md`, verlangt eine Änderung dort beide Regeldateien.
    Fehlerhafte Einträge meldet der Session-Start. Template und Skill
    `architecture` sind angepasst.

- `TASK-010` **Backlog und techdocs pro Projekt**
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-007`.
  - Goal: Backlog-Prüfung und techdocs-Erinnerung arbeiten pro Projekt.
  - Completion criteria: Tests zeigen: Eine Änderung im Backlog eines
    Teilprojekts prüft nur dieses Backlog. Die techdocs-Erinnerung erscheint
    pro Projekt, dessen Code geändert wurde.

- `TASK-011` **Daily Reports pro Projekt**
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-007`.
  - Goal: Jedes Projekt hat eigene Daily Reports mit eigenem
    Bestätigungsstand. Ein Commit zählt nur für das Projekt, dessen Dateien er
    ändert, auch wenn das Git-Root über dem Projekt liegt.
  - Completion criteria: Tests zeigen: Ein Commit nur in einem Teilprojekt
    erscheint nur in dessen Daily. Ein reiner Backlog-Commit zählt nirgends.
    Beim Start im Teilprojekt mit Git-Root darüber zählen Commits außerhalb
    nicht. `daily.py --project` funktioniert.

- `TASK-012` **Skills, init und Worktree für Teilprojekte**
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-007`.
  - Goal: Die Skills beschreiben die Arbeit mit mehreren Projekten, `init`
    kann Teilprojekte anlegen, und der Worktree übernimmt gitignorierte
    Teilprojekt-Dateien nachweislich.
  - Completion criteria: Skill-Texte und `init` sind angepasst und in einem
    Test-Repo einmal durchgespielt. Ein Test zeigt, dass `worktree.py start`
    eine gitignorierte Teilprojekt-Konfiguration spiegelt.

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

- `TASK-013` **Worktree-Ablauf: Merge und Hook-Pfade korrigieren**
  - Type: Task.
  - Parent: `STORY-022`.
  - Required for parent: Yes.
  - Status: Awaiting confirmation.
  - Created: 2026-09-25.
  - Area: Governance.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Der Worktree-Ablauf funktioniert in einer isolierten
    Worktree-Session von Claude Code ohne Umweg, und die Hooks bewerten
    Dateien im Worktree so, als lägen sie im Projekt. Der Merge in den
    Haupt-Checkout läuft nach dem Verlassen des Worktrees, danach werden
    Worktree und Branch entfernt. Dateipfade unter
    `.claude/worktrees/<Name>/` werden relativ zu diesem Worktree bewertet.
  - Completion criteria: Der Skill `worktree` beschreibt einen Abschluss,
    den Claude Code nicht blockiert, und ein realer Change ist so
    durchgelaufen. Tests zeigen: Eine Doku-Änderung im Worktree zählt für
    den techdocs-Hook als Doku, und der Architektur-Hook verlangt für eine
    Datei im Worktree dieselben Regeln wie im Haupt-Checkout.

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
