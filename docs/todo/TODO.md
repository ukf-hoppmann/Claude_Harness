# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 2. The rules are defined in
`docs/techdocs/interfaces.md` of the ToDo Viewer.

## Work items

- `EPIC-010` **Weg von der Claude-Code-App: Harness und ToDo-Viewer über claude.ai nutzen**
  - Uid: 0bb9fc23-a57b-4616-b5b1-3cf7f0d8b9e9.
  - Type: Epic.
  - Status: Open.
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

- `EPIC-008` **Backlog über die API des ToDo-Viewers**
  - Uid: 6da1ed5f-d947-48b4-b198-8bd2e96ef709.
  - Type: Epic.
  - Status: In progress.
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

- `STORY-051` **todo-Skill: Ort und Inhalt der Diskussionsprotokolle (Notes) festlegen**
  - Uid: 3b18df8f-3832-4a6b-a090-51a845d0cabd.
  - Type: Story.
  - Parent: None.
  - Status: Open.
  - Created: 2026-10-19.
  - Area: Dokumentation.
  - Priority: Urgent.
  - Dependencies: None.
  - Goal: Der todo-Skill legt Ort, Inhalt, Zeitpunkt und Aufbau der
    Item-Notes fest: Kopf mit dem geltenden Stand, darunter das Protokoll;
    die Spec wird fortlaufend geschrieben. Der Harness stellt mechanisch
    sicher, dass der Kopf nach jeder Änderung der Notes geprüft wird.
  - Completion criteria: Die beschlossenen Regeln stehen im todo-Skill und
    in format.md; die Prüfsumme des Kopfs wird in API- und Files-Modus
    gesetzt und geprüft; der Hook am Turn-Ende und der Reminder B sind
    umgesetzt und getestet; die Schnittstelle zum ToDo-Viewer ist
    beschrieben und dort umgesetzt.
  - Summary: Claude schreibt Besprechungen bisher teils ins falsche Item, zu
    knapp, und lange Notes sind unübersichtlich. Künftig regelt der Harness,
    wo und wie protokolliert wird; jede Notes-Datei bekommt oben eine
    Übersicht über den aktuellen Stand, deren Aktualität der Harness prüft.

- `TASK-024` **Hooks für aktuellen Notes-Kopf und Protokoll-Reminder**
  - Uid: 93bf2558-2beb-4088-9d63-c4e980a0fac4.
  - Type: Task.
  - Parent: `STORY-051`.
  - Required for parent: Yes.
  - Status: In progress.
  - Created: 2026-10-20.
  - Area: Entwicklung.
  - Priority: Urgent.
  - Dependencies: `TASK-022`, `TASK-023`.
  - Goal: Ein Hook am Turn-Ende blockiert, solange Notes, die in der Session
    geändert wurden, einen veralteten Kopf haben, bis der Kopf angepasst
    oder bestätigt ist (API- und Files-Modus). Ein Reminder (Prüfidee B)
    erinnert, wenn ein aktives Item seit mehreren Turns keinen Notes-Eintrag
    bekam.
  - Completion criteria: Beide Hooks sind umgesetzt, in der
    Plugin-Konfiguration registriert, in der Doku beschrieben und getestet
    (Unit-Tests; Endlosschleife ausgeschlossen, weil Bestätigen den Hook
    auflöst).
  - Summary: Ein Hook sorgt dafür, dass die Übersicht nach jeder Änderung
    der Notes geprüft wird, und erinnert ans Protokollieren.
