# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `EPIC-008` **Backlog über die API des ToDo-Viewers**
  - Type: Epic.
  - Status: Open.
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

- `STORY-031` **Backlog-Format an den ToDo-Viewer angleichen**
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-28.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: None.
  - Goal: `format.md` und `backlog.py` kennen das Feld `Deleted` (Papierkorb),
    akzeptieren nur `No entries.` als Leer-Markierung, erlauben das Ablehnen
    eines Epics ohne Pflichtkind und melden Verweise auf unbekannte IDs.
  - Completion criteria: `Deleted`-Einträge in `archive.md` werden von der
    Archiv-Statusregel und den Parent-Regeln ausgenommen und im Index
    markiert; `Keine Einträge.` wird als Fehler gemeldet; ein leeres Epic mit
    `Rejected` ist kein Fehler; `Parent`/`Dependencies` auf unbekannte IDs
    sind Fehler; `format.md` beschreibt `Deleted` und das Wiederherstellen;
    Tests in `tests/test_backlog.py` decken alle Punkte ab.

- `STORY-032` **Backend-Einstellung für den Backlog**
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-28.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: `config.toml` bekommt `[todo].backend` (`api` oder `files`, Standard
    `api`) und `[todo].api_url` (Standard `http://localhost:5411/api/v2`).
  - Completion criteria: Die Werte werden geladen und validiert; fehlende
    Schlüssel ergeben die Standardwerte, bestehende Configs laufen ohne
    Migration weiter; `docs/techdocs/configuration.md` beschreibt beide
    Schlüssel; Tests decken Standard, gültige und ungültige Werte ab.

- `STORY-033` **API-Helfer für den Backlog**
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-28.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `STORY-032`.
  - Goal: Ein Skript im Plugin kapselt die Aufrufe der Viewer-API
    (Erreichbarkeit, Quelle zum Backlog-Ordner finden oder anlegen, Index,
    Item lesen, anlegen, ändern, löschen, Notes und Specs lesen und schreiben,
    Papierkorb ohne endgültiges Löschen), damit der Agent keine
    JSON-Aufrufe von Hand bauen muss.
  - Completion criteria: Das Skript nutzt nur die Standardbibliothek, liest
    `api_url` aus der Config, gibt Antworten und Fehler (inkl.
    `version_conflict`) verständlich aus und endet bei nicht erreichbarem
    Server mit eigenem Exit-Code; Tests laufen gegen einen lokalen Testserver;
    `docs/techdocs/interfaces.md` beschreibt die Befehle.

- `STORY-034` **todo-Skill für den API-Modus**
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-28.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: `STORY-033`.
  - Goal: `SKILL.md` und `format.md` beschreiben die Arbeit im API-Modus
    über den Helfer und im Datei-Modus wie bisher; die Entscheidungsbefugnis
    bleibt im Skill. Löschen in den Papierkorb ist bei klarem Auftrag ohne
    Rückfrage erlaubt, endgültiges Löschen nur durch den
    Projektverantwortlichen.
  - Completion criteria: Der Skill nennt je Modus Lesen, Anlegen, Ändern,
    Notes/Specs und Löschen; bei nicht erreichbarem Server gibt der Agent
    einen Hinweis und fragt, ob der Server gestartet, auf Dateien
    ausgewichen oder abgebrochen wird; Konflikte (409) werden neu gelesen und
    geprüft, nicht blind wiederholt.

- `STORY-035` **Hooks und Sitzungsstart je Backend**
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-28.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: `STORY-032`.
  - Goal: Der Backlog-Check läuft nur im Datei-Modus; der Hinweis beim
    Sitzungsstart nennt im API-Modus die API statt `TODO.md`.
  - Completion criteria: Im API-Modus markiert `mark_backlog_dirty.py` nichts
    und `check_backlog.py` prüft nichts; `session_start.py` meldet je Modus
    den passenden Hinweis; Tests decken beide Modi ab.

- `STORY-036` **Backlog-Änderungen im API-Modus committen**
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-28.
  - Area: Governance.
  - Priority: Normal.
  - Dependencies: `STORY-034`.
  - Goal: Der Worktree-Skill regelt, dass Backlog-Änderungen im API-Modus im
    Haupt-Checkout landen und dort vom Agenten mit eigenem Commit
    (`Backlog: …`) festgehalten werden; im Datei-Modus bleibt die Regel
    „im selben Branch“.
  - Completion criteria: `worktree`- und `todo`-Skill beschreiben beide Modi
    widerspruchsfrei; ein Merge des Worktrees kollidiert nicht mit
    Backlog-Änderungen im Haupt-Checkout.

- `TASK-015` **Einzelitem-Abruf in backlog.py für archive.md**
  - Type: Task.
  - Parent: None.
  - Status: Open.
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
