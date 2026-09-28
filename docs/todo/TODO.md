# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `TASK-017` **update-Skill: Projekt-Config mit dem aktuellen Harness-Stand abgleichen**
  - Type: Task.
  - Parent: None.
  - Status: Open.
  - Created: 2026-09-28.
  - Area: Konfiguration.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: `/claude-harness:update` gleicht die `.claude-harness/config.toml`
    des Projekts mit dem aktuellen Stand des Harness ab, also mit der
    Config-Vorlage (`plugin/templates/config.toml`) und den bekannten
    Schlüsseln in `harness_config.py`. Er trägt fehlende Abschnitte,
    Optionen, Module und die erklärenden Kommentare der Vorlage nach, damit
    die Config dem aktuellen Stand entspricht. Das gilt auch, wenn die
    Config-Version schon aktuell ist; der Abgleich hängt nicht mehr allein
    an `version` und `MIGRATIONS`. Neue Werte mit festem Standard setzt der
    Skill ohne Rückfrage. Nach Werten, die wirklich zu entscheiden sind,
    fragt er wie `init`, z. B. nach neuen Modulen oder danach, ob der
    Backlog über die API (`api`) oder direkt auf den Dateien (`files`)
    läuft.
  - Completion criteria: Auf ein Projekt, dessen Config Abschnitte,
    Optionen, Module oder Kommentare der aktuellen Vorlage nicht enthält,
    zeigt `update` die konkreten Ergänzungen und schreibt sie erst nach
    Freigabe. Bestehende Werte, eigene Kommentare und die Reihenfolge
    bleiben erhalten. Rückfragen gibt es nur für zu entscheidende Werte,
    darunter das Backlog-Backend, wenn `todo` aktiv ist. Beim Backend `api`
    prüft der Skill mit `backlog_api.py health`, ob der Server erreichbar
    ist, und meldet das Ergebnis. Auf eine vollständige Config meldet
    `update`, dass nichts zu tun ist, und ändert die Datei nicht. Das
    Ergebnis besteht die Config-Validierung. Die Config dieses Repos ist
    damit auf den aktuellen Stand gebracht. README/techdocs beschreiben das
    neue Verhalten.
  - Summary: `/claude-harness:update` soll die Einstellungen eines Projekts
    mit dem aktuellen Stand des Harness vergleichen und alles nachtragen,
    was fehlt: neue Optionen, Module und Erklärungen. Nur wo es wirklich
    etwas zu entscheiden gibt, zum Beispiel ob der Backlog über die
    ToDo-Viewer-API läuft, fragt es nach. Bisher prüft `update` nur die
    Versionsnummer der Config und ändert sonst nichts.
  - Notes: `items/TASK-017/TASK-017_notes.md`.

- `STORY-037` **Testkonventionen: Ablage, Gliederung, Test-Arten**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Status: Open.
  - Created: 2026-09-28.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Verbindlich festlegen, wo und wie Tests in einem Projekt liegen:
    alle Tests in einem Testordner (keine Inline-Tests), mit fester
    Gliederung, getrennt nach Implementierungstests (vom Agenten für die
    eigene Absicherung gebaut) und Funktionalitätstests (für den
    Projekt-Owner, um fachliche Funktionen wie Filter oder größere Abläufe
    gezielt selbst zu prüfen).
  - Completion criteria: Die Regeln zu Testordner, Gliederung, Benennung und
    den beiden Test-Arten stehen im Plugin (Suite development) und sind für
    Projekte mit anderer Sprache oder anderem Test-Framework anwendbar. Der
    Owner kann Funktionalitätstests getrennt von den Implementierungstests
    aufrufen und findet sie über ihren Funktionsnamen. Dieses Repo ist nach
    den Regeln gegliedert und die Tests laufen weiter durch.
  - Summary: Legt fest, dass alle Tests in einem Ordner liegen und wie er
    gegliedert ist. Unterscheidet Tests, die der Agent für sich baut, von
    Tests, mit denen der Owner Funktionen selbst prüft.
  - Notes: `items/STORY-037/STORY-037_notes.md`.
  - Required for parent: Yes.

- `EPIC-004` **Entwicklungsprozess & Prinzipien**
  - Type: Epic.
  - Status: In progress.
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
