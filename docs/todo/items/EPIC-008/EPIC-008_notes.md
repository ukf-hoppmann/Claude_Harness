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

## 2026-09-28 — Umsetzung

### Discussed

- Zwei Punkte der Übergabe stimmten nicht: `backlog.py` prüfte unbekannte
  Verweise schon und erlaubte das Ablehnen eines leeren Epics schon; nur
  `format.md` sagte es beim Epic noch anders.

### Decided

- `backlog_api.py` kapselt die API; JSON kommt über stdin, Dokumente als
  Rohtext. Endgültiges Löschen bietet das Skript bewusst nicht an. Exit 3
  heißt „Server nicht erreichbar“.
- Liegt der Backlog-Ordner in einem Worktree, nutzt das Skript denselben
  Ordner im Haupt-Checkout als Quelle (`worktree.in_main_checkout`); so
  entsteht keine zweite Quelle je Worktree.
- API-Befehle stehen in `plugin/skills/todo/api.md` und werden nur bei Bedarf
  gelesen; der Sitzungsstart prüft die Erreichbarkeit nicht (Hooks ohne
  Netzwerk).
- Der Index von `backlog.py` markiert gelöschte Einträge mit
  `(deleted <Datum>)`, statt sie auszublenden.
- Nachweis: 216 Tests grün; zusätzlich ein Durchlauf gegen den laufenden
  Viewer auf einem temporären Backlog (Anlegen, Ändern, Versionskonflikt,
  Regelverstoß, Notes anhängen und ersetzen, Spec, Löschen mit Kindern,
  Papierkorb, Wiederherstellen); `backlog.py` akzeptierte die vom Viewer
  geschriebenen Dateien in jedem Zustand. Quelle und Ordner wurden danach
  entfernt.

### Open

- Dieses Repo arbeitet nach dem Merge mit dem Standard `backend = "api"`.

## 2026-09-28 — Wiedereröffnet für TASK-016

### Discussed

- Der Helfer nahm den Backlog-Ordner als freien Parameter. Ein falscher, aber gültiger Backlog (z. B. Core statt Plugin in EZF-Backend) wäre ohne Fehler beschrieben worden. Falsche Pfade selbst sind harmlos: der Viewer legt keine `TODO.md` an, die Quelle bekommt nur einen Fehlerzustand.
- Eine Viewer-`source_id` in der Config wäre rechnerabhängig (pfadbasiert), die Config ist eingecheckt.

### Decided

- Vom Projektverantwortlichen freigegeben: EPIC-008 wieder öffnen, `TASK-016` darunter.
- Der Helfer liest den Backlog-Ordner aus der Config (Root oder `--project <Name>`), wie `daily.py`; beim Anlegen einer Quelle wird der Projektname mitgegeben.

## 2026-10-19 — Wiedereröffnung: Umstellung auf den MCP-Server des Viewers

### Discussed

- Der Neubau des ToDo-Viewers hat /api/v2 entfernt; backlog_api.py und notes_api.py laufen gegen 404. Die neue Schnittstelle bietet HTTP-Routen unter /api/<plugin>/… und einen MCP-Server unter /mcp (63 Tools, live geprüft).

### Decided

- EPIC-008 wird wieder geöffnet (Freigabe des Projektverantwortlichen). Eine neue Pflicht-Story stellt die Skills todo und notes auf die MCP-Tools des Viewers um; MCP ist für die lokale Arbeit besser geeignet als ein eigener HTTP-Helfer.

### Open

- Regel für fremde Projekte unter MCP (bisher --source mit Freigabe).
- Verhalten bei nicht erreichbarem Server ohne Exit-Code 3.
- Ob die Wecker (alarms_*) eigene Harness-Regeln brauchen.
