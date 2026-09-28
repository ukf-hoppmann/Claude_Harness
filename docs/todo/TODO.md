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
  - Status: In progress.
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

- `EPIC-008` **Backlog über die API des ToDo-Viewers**
  - Type: Epic.
  - Status: Awaiting confirmation.
  - Created: 2026-09-28.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Agenten pflegen Backlogs standardmäßig über die HTTP-API des
    ToDo-Viewers statt die Markdown-Dateien direkt zu schreiben; der direkte
    Dateizugriff bleibt als wählbarer Modus und als Rückfall erhalten. Das
    Backlog-Format in `format.md` ist verbindlich, der Viewer setzt es um.
  - Completion criteria: Alle Pflicht-Stories sind abgeschlossen; ein Projekt
    mit Standard-Config arbeitet über die API, ein Projekt mit
    `backend = "files"` wie bisher; ist der Server nicht erreichbar, weist der
    Agent darauf hin und fragt, wie er vorgehen soll.
  - Summary: Der Backlog wird künftig über den ToDo-Viewer gepflegt. Der
    Server prüft Format und Regeln und vergibt IDs; direkter Dateizugriff
    bleibt als Rückfall.
  - Notes: `items/EPIC-008/EPIC-008_notes.md`.
  - Spec: `items/EPIC-008/EPIC-008_spec.md`.

- `TASK-016` **Backlog-Ziel aus der Config statt aus einem Pfadparameter**
  - Type: Task.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Awaiting confirmation.
  - Created: 2026-09-28.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: `backlog_api.py` ermittelt den Backlog-Ordner selbst aus der
    Harness-Config (Root-Projekt oder `--project <Name>` für Teilprojekte)
    statt aus einem frei angegebenen Pfad; beim Anlegen einer Quelle im
    ToDo-Viewer wird der Projektname mitgegeben.
  - Completion criteria: Der Helfer nimmt keinen Ordner mehr entgegen;
    unbekannte Projekte, abgeschaltetes Modul `todo` und fehlende `TODO.md`
    enden mit Fehler, ohne eine Quelle anzulegen; neue Quellen tragen den
    Projektnamen (Teilprojekt) bzw. den Repo-Namen (Root); Tests decken
    Root, Teilprojekt, Worktree und die Fehlerfälle ab; `api.md` und
    `docs/techdocs/interfaces.md` beschreiben den neuen Aufruf.
