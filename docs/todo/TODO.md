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

- `STORY-052` **Branch-Stand beim Start einer Cloud-Session mit origin abgleichen**
  - Uid: 3b72b84e-cf3a-43f0-b071-d6d79331e4f1.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: In progress.
  - Created: 2026-11-04.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Eine Cloud-Session eines Projekts mit cloud.export arbeitet nicht
    unbemerkt auf einem veralteten Branch-Stand. Beim Start holt der
    Session-Start den aktuellen Branch von origin, spult bei sauberem Stand
    vor und meldet sonst in einer Zeile, wie weit der Stand abweicht und
    welcher Befehl passt. Er überschreibt nie etwas.
  - Completion criteria: 1. Ein Skript plugin/scripts/cloud_sync.py holt
    beim Start einer Cloud-Session (CLAUDE_CODE_REMOTE=true, Quelle startup)
    nur den aktuellen Branch von origin, ohne --unshallow und mit Zeitlimit,
    und läuft als erster Schritt von session_start.py, damit dessen Hinweise
    den neuen Stand sehen. Lokal tut es nichts.
    2. Bei sauberem Arbeitsbaum und HEAD als Vorfahr von origin spult es per
    git merge --ff-only vor und meldet das in einer Zeile; bei gleichem
    Stand oder nur lokal vorausliegenden Commits schweigt es.
    3. Bei unsauberem Arbeitsbaum, beidseitigen Commits, fehlendem
    gemeinsamem Vorfahren (Shallow Clone, Force-Push) oder gescheitertem
    Fetch ändert es nichts und meldet eine Zeile mit Abweichung (Zahl der
    Commits oder Hash und Datum beider Stände) und passendem Befehl; git
    reset --hard nur nach Rückfrage beim Nutzer.
    4. Die Konfiguration cloud.sync (Boolean, Standard true) schaltet den
    Abgleich ab; geprüft in harness_config.py, dokumentiert in
    configuration.md, getestet in test_config.py.
    5. architecture.md enthält die freigegebene, auf Cloud-Sessions
    begrenzte Ausnahme von Regel 2 (Netz) und Regel 5 (Schreiben ins
    Projekt).
    6. Unit-Tests mit einem lokalen Bare-Repo als origin decken alle Fälle
    aus 2 und 3 ab, dazu Zeitlimit und lokale Session; Techdocs
    (interfaces.md, configuration.md) beschreiben das Verhalten.
    7. Ein Lauf in einer echten Cloud-Session eines Projekts mit
    aktualisierter Kopie zeigt den Abgleich oder die Meldung.
  - Summary: Cloud-Sessions starteten auf einem veralteten, gecachten
    Branch-Stand, ohne dass es jemand merkte. Künftig holt der Session-Start
    den Branch von origin, aktualisiert ihn, wenn das gefahrlos geht, und
    meldet sonst die Abweichung.

- `STORY-060` **Notes heißen Memos: Harness an den umbenannten Viewer anpassen**
  - Uid: b14b4a8c-5f7c-4c38-8f3e-fb90b681f663.
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: No.
  - Status: In progress.
  - Created: 2026-11-12.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Der Harness arbeitet mit Memos, Topics und Hints des ToDo-Viewers
    (ab 0.10.0) über die Routen /api/memos, im Dateimodus mit dem Ordner
    memos/. Der Begriff Note bezeichnet im Harness nur noch die Notiz zu
    einem Backlog-Item.
  - Completion criteria: 1. Der Helfer für Memos (memos_api.py) nutzt die
    Routen /api/memos/… und die neuen Feldnamen (memos, memo_count, hints,
    active_memos); notices heißt hints.
    2. Dateimodus (memos_files.py, memos_format.py): Ordner memos/, Dateien
    MEMO-…, Verweise memo:.
    3. Sitzungsstart, Konfiguration und der Hook für geänderte
    Backlog-Dateien sprechen von Memos und erkennen den Ordner memos/.
    4. Der todo-Skill (memos.md, memos-api.md, memos-files.md, SKILL.md,
    sync-flow.md, format.md, alarms.md) benutzt Memo und Hint; Item-Notizen
    sind klar abgegrenzt.
    5. Tests und Fixtures sind umbenannt und grün; Techdocs sind
    nachgezogen.
    6. Die Kopie des Harness im Projekt ist neu exportiert, falls vorhanden,
    und der alte Ordner docs/todo/notes/ ist entfernt.
  - Summary: Umstellung des Harness auf die Begriffe Memo und Hint des
    ToDo-Viewers ab 0.10.0.
