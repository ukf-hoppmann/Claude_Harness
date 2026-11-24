# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 2. The rules are defined in
`docs/techdocs/interfaces.md` of the ToDo Viewer.

## Work items

- `EPIC-008` **Backlog über die API des ToDo-Viewers**
  - Uid: 6da1ed5f-d947-48b4-b198-8bd2e96ef709.
  - Type: Epic.
  - Status: Open.
  - Created: 2026-09-28.
  - Area: Konfiguration.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Agenten pflegen Backlogs standardmäßig über die HTTP-API des
    ToDo-Viewers statt die Markdown-Dateien direkt zu schreiben; der direkte
    Dateizugriff bleibt als wählbarer Modus und als Rückfall erhalten. Das
    Backlog-Format in `format.md` ist verbindlich, der Viewer setzt es um.
  - Completion criteria: Alle Pflicht-Stories sind abgeschlossen; ein
    Projekt mit Standard-Config arbeitet über die API, ein Projekt mit
    `backend = "files"` wie bisher; ist der Server nicht erreichbar, weist
    der Agent darauf hin und fragt, wie er vorgehen soll.
  - Summary: Der Backlog wird künftig über den ToDo-Viewer gepflegt. Der
    Server prüft Format und Regeln und vergibt IDs; direkter Dateizugriff
    bleibt als Rückfall.

- `STORY-050` **Skills auf den MCP-Server des ToDo-Viewers umstellen**
  - Uid: 4846f8a8-2123-46a5-b63f-8fe463446f92.
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-10-19.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: `STORY-049`.
  - Goal: Claude arbeitet im API-Modus über die MCP-Tools des Viewers an
    Backlog, Notes und Weckern, sobald der MCP-Server im Viewer überarbeitet
    ist. Das Projekt gibt Claude dabei nicht selbst an: Ein PreToolUse-Hook
    des Harness setzt das eigene Projekt deterministisch ein und fragt bei
    einem fremden Projekt nach.
  - Completion criteria: Das Plugin bringt eine .mcp.json mit
    http://localhost:5411/mcp mit; ein PreToolUse-Hook setzt das eigene
    Projekt ein (aus Config und Hauptarbeitskopie) und fragt bei fremdem
    Projekt nach; der Session-Start meldet Projekt und Erreichbarkeit des
    Viewers; die Skills todo und notes beschreiben die Tools, die Helfer
    bleiben als Rückfall; Lese-Tools lassen sich über init/update in den
    Projekt-Settings freigeben; Lese-, Schreib- und Notizfluss sind über MCP
    gegen den laufenden Viewer geprüft.
  - Summary: Spätere Umstellung von den Helfer-Skripten auf die nativen
    MCP-Tools des Viewers. Sie wartet auf STORY-049 und auf den Umbau des
    MCP-Servers im ToDo-Viewer.

- `EPIC-010` **Weg von der Claude-Code-App: Harness und ToDo-Viewer über claude.ai nutzen**
  - Uid: 0bb9fc23-a57b-4616-b5b1-3cf7f0d8b9e9.
  - Type: Epic.
  - Status: In progress.
  - Created: 2026-10-14.
  - Area: Architektur.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Der Claude_Harness ist auch in Cloud-Sessions auf claude.ai/code
    nutzbar, z. B. bei der Arbeit an ezf-ui, ohne die
    Claude-Code-Desktop-App. Lokal arbeitet der Harness mit Backlog und
    Notes über die API des ToDo-Viewers, in der Cloud über die
    Markdown-Dateien im Repository. Beide Seiten bleiben über den Sync des
    ToDo-Viewers (Git und Spiegel-Ordner) im Gleichstand.
  - Completion criteria: 1. Geklärt und dokumentiert, wie Skill, Hooks und
    Skripte des Harness in einer Cloud-Session eines Fremdprojekts (z. B.
    ezf-ui) verfügbar sind; das Plugin selbst wird dort nicht geladen. 2.
    Lokal gilt die API, in der Cloud der Dateimodus für Backlog und Notes;
    die Umschaltung braucht keine Änderung der eingecheckten Config. 3. Der
    Abgleich zwischen den Cloud-Dateien und der lokalen Datenbank ist
    beschrieben und läuft ohne Verlust, auch bei gleichzeitiger Arbeit auf
    beiden Seiten und bei gleichen IDs. 4. Ein Fremdprojekt läuft in einer
    claude.ai-Session mit Harness, Backlog und Notes nachweislich durch, und
    der Stand ist danach lokal im Viewer.
  - Summary: Lokal bleibt die API des ToDo-Viewers, in der Cloud arbeitet
    der Harness mit den Markdown-Dateien im Repository; beide Seiten bleiben
    über den Sync im Gleichstand. Offen: wie der Harness dort ohne Plugin
    läuft.

- `NEW-viewer-v3-mindmap` **Harness auf Backlog-Format Version 3 und die Mindmap des Viewers umstellen**
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: No.
  - Status: Awaiting confirmation.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Der Harness folgt der Überarbeitung des ToDo-Viewers: Das Feld
    `Area` entfällt, das Dateiformat heißt Version 3 (Version 2 wird weiter
    gelesen, nur 3 geschrieben), und die Themen eines Items sind die Knoten
    der Mindmap. Im API-Modus ordnet die KI neue Items per MCP-Tools dem
    Themenbaum zu; im Dateimodus kennt der Skill die Dateien unter
    `mindmap/` und bearbeitet sie nach festen Regeln. Die Quellen sind vier
    Aufträge des Owners (TASK-072 Prompt 2, TASK-078, TASK-082 aus dem
    Viewer-Repository sowie TASK-072 Prompt 1 als Aufgabe außerhalb des
    Harness).
  - Completion criteria: 1. Format Version 3 ist umgesetzt (Skripte, Check, Hooks, Vorlagen,
    `format.md`, `api.md`, Skills, README, Tests): Version 2 und 3 werden
    gelesen, `Area` wird toleriert und nie geschrieben, `areas` und
    `area` in `create`/`update`/`promote` entfallen, die Index-Zeile hat
    keine Spalte Area.
    2. Der Skill `todo` enthält die Regel zum Zuordnen neuer Items zum
    Themenbaum für den API-Modus (Werkzeugnamen stimmen mit dem Viewer
    überein).
    3. Der Skill `todo` enthält den Abschnitt „Mindmap“ für den Dateimodus;
    `backlog.py` und die Hooks melden Dateien unter `mindmap/` nicht; die
    Regel zum Anlegen von Items im Dateimodus steht im Skill; der
    Vermerk „Dateimodus noch offen“ aus dem API-Auftrag ist entfernt.
    4. Alle Tests sind grün; `grep -rniw area` findet nur Toleranz,
    Tests dafür und andere Wortbedeutungen.
    5. Ein Release mit der Versionsnummer nach der semver-Regel ist
    vorbereitet; die Cloud-Kopie wird nicht von Hand geändert und der
    Owner ist über das nötige `update` der Projekte informiert.
  - Summary: Sammelauftrag für die Umstellung des Harness auf Format 3
    ohne Area und auf die Mindmap des Viewers. Reihenfolge: erst
    Format 3, dann API-Regel, dann Dateimodus-Mindmap, am Ende ein
    gemeinsames Release. Umgesetzt (A, B, C); wartet auf die Bestätigung
    des Owners, Release 0.15.0 vorbereitet.
