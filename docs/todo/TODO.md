# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `TASK-017` **update-Skill: Backlog-Backend (api/files) umstellen**
  - Type: Task.
  - Parent: None.
  - Status: Open.
  - Created: 2026-09-28.
  - Area: Konfiguration.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: `/claude-harness:update` kann in einem bestehenden Projekt das
    Backlog-Backend umstellen: Ist das `todo`-Modul aktiv, zeigt der Skill
    das aktuelle `[todo].backend` (fehlt es, gilt die Voreinstellung `api`)
    und `api_url`, fragt, ob das Projekt über die ToDo-Viewer-API (`api`)
    oder direkt auf den Dateien (`files`) arbeiten soll, und trägt die Wahl
    nach Freigabe ein. Das geschieht auch dann, wenn die Config-Version
    schon aktuell ist; heute hört der Skill in diesem Fall ohne Änderung
    auf.
  - Completion criteria: Bei aktueller Config-Version und aktivem
    `todo`-Modul bietet `update` den Wechsel des Backends an und schreibt
    nach Freigabe nur `backend` (und bei `api` gegebenenfalls `api_url`) in
    `[todo]`; Kommentare, Reihenfolge und alle anderen Werte bleiben
    unverändert. Wer nichts ändern will, bekommt eine unveränderte Datei.
    Beim Wechsel auf `api` prüft der Skill mit `backlog_api.py health`, ob
    der Server erreichbar ist, und meldet das Ergebnis. Das Ergebnis besteht
    die Config-Validierung. README/techdocs beschreiben das neue Verhalten.
  - Summary: Mit `/claude-harness:update` soll man in einem Projekt, das den
    Harness schon nutzt, einfach zwischen den beiden Backlog-Varianten
    wechseln können: über die ToDo-Viewer-API oder direkt auf den Dateien.
    Bisher prüft `update` nur die Config-Version und ändert sonst nichts.
