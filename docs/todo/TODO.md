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

- `EPIC-011` **Hierarchische Architektur- und Schnittstellen-Doku für die AI**
  - Uid: 37382d27-0b2a-4d59-b52f-4401524a99b2.
  - Type: Epic.
  - Status: Awaiting confirmation.
  - Created: 2026-11-05.
  - Area: Architektur.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Projekte können ihre verbindlichen Regeln für die AI (development)
    als Baum führen: Architektur sagt, was wohin gehört und was Pflicht ist;
    eine Schnittstellen-Doku mit Katalog wiederverwendbarer Bausteine sagt,
    wie es geht. Der Harness stellt sicher, dass die AI die passenden
    Dokumente liest (Pflicht über Pfade und über Nutzung), dass Verweise
    gültig bleiben und dass bei Änderungen an öffentlichen APIs an die
    Pflege erinnert wird. Bestehende Projekte mit flachen Scopes
    funktionieren unverändert.
  - Completion criteria: 1. Scopes können in Unterordnern liegen
    (STORY-053).
    2. Scopes können Pflichtlektüre außerhalb der Architektur nennen, der
    Hook erzwingt sie (STORY-054).
    3. Tote relative Links in development- und techdocs-Dateien werden
    gemeldet (STORY-055).
    4. Änderungen an konfigurierten öffentlichen API-Dateien lösen eine
    Pflege-Erinnerung aus (STORY-056).
    5. Nutzung bestimmter Bezeichner erzwingt das Lesen der zugehörigen Doku
    (STORY-057).
    6. Vorlagen und Skills beschreiben den Aufbau; Projekte ohne die neuen
    Teile laufen unverändert (STORY-058).
  - Summary: Aus ezf-ui kam der Wunsch, Architektur und Schnittstellen nicht
    in großen Einzeldateien, sondern als Baum zu führen, und
    sicherzustellen, dass die AI die passenden Teile liest und vorhandene
    Bausteine wiederverwendet. Das Epic baut die nötigen Mechanismen in den
    Harness: Scopes in Unterordnern, Pflichtlektüre, Linkprüfung,
    Pflege-Erinnerung, Pflicht über Nutzung, Vorlagen und Skills.
