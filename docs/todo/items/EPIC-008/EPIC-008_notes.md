# EPIC-008 — Notizen

## 2026-09-28 — Übergabe aus dem ToDo-Viewer und Grundsatzentscheidungen

### Discussed

- Übergabe aus dem ToDo-Viewer (dort `EPIC-001`, Spec
  `EPIC-001_spec_harness.md`): Agenten sollen Backlogs über die HTTP-API
  pflegen. Zusammengefasst in [EPIC-008_spec.md](EPIC-008_spec.md).
- „backlog format version 2“ im Viewer ist die Kennung des alten
  Agent_Harness (LLM_Tests, my_story_game), keine neue Version des
  Claude_Harness-Formats. Das Harness bleibt bei Version 1.

### Decided

- Das bisherige Datei-Modul bleibt; die API ist ein wählbares Backend in
  `config.toml`. Standard ist `api`, `files` ist der Rückfall.
- Server nicht erreichbar: Hinweis an den Projektverantwortlichen und fragen,
  wie weiter (meist wird der Server gestartet, selten auf Dateien
  ausgewichen).
- Im API-Modus gibt es keine Backlog-Checks mehr; der Check gehört zum
  Datei-Modus.
- `format.md` ist maßgeblich, der Viewer setzt es um. Regeländerungen erst in
  `format.md`, dann in `backlog.py` und im Viewer. Übernommen aus dem Viewer:
  leeres Epic darf `Rejected` werden; Verweise auf unbekannte IDs sind
  Fehler. `backlog.py` meldet weiterhin auch Altlasten.
- Worktrees: Backlog-Änderungen im API-Modus landen im Haupt-Checkout; der
  Agent committet sie dort separat (`Backlog: …`).
- Löschen in den Papierkorb ist bei klarem Auftrag ohne Rückfrage erlaubt;
  endgültiges Löschen (Purge) nur durch den Projektverantwortlichen.
- Notes können über die API gelesen (`GET …/documents/<ID>_notes.md`) und
  ganz ersetzt werden (`PUT`); die Regel „Notes und Specs dürfen überarbeitet
  werden“ gilt daher auch im API-Modus.
- `TASK-015` bleibt für den Datei-Modus.

### Open

- Agent_Harness aus LLM_Tests und my_story_game entfernen und deren Backlogs
  migrieren; danach prüft der Viewer fest auf die Claude_Harness-Kennung.
  Läuft in einer eigenen Session.
