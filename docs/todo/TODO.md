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

- `STORY-044` **Formatprüfung für den Notes-Ordner**
  - Uid: 452b2474-a5e3-428c-b8cf-6a43fa6f62a5.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-10-16.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: `STORY-043`.
  - Goal: Eine Prüfung findet Formatfehler in den Dateien unter `notes/`
    (Dateimodus), bevor der ToDo-Viewer sie liest. Der Viewer bricht bei
    einem einzigen Formatfehler den ganzen Sync ab (400 `note_format`,
    Backlog und Notes), deshalb muss der Fehler schon beim Schreiben
    auffallen.
  - Completion criteria: 1. Ein Prüfskript (Stop-Hook wie
    `check_backlog.py`, nur bei `files` und nur nach Änderungen unter
    `notes/`) meldet Datei und Zeile bei: unbekannter Kopfzeile, ungültigem
    Status oder Zeitpunkt, Dateiname und Label verschieden, ungültiger
    Auslöser- oder Link-Zeile, falschem Zeilenaufbau in `topics.md` und
    `counters.md`. 2. Die Prüfung verwendet dieselben Beispiele wie der
    Viewer: die Golden-Files unter `backend/tests/golden/notes/` des
    ToDo-Viewers liegen als Testvorlagen im Harness und werden fehlerfrei
    gelesen; je ein Fehlerfall pro Meldung ist getestet. 3. Weicht das
    Format des Viewers von der Prüfung ab, ist der Unterschied in den Notes
    der Story festgehalten (damit erledigt sich der offene Punkt Harness
    gegen das Notes-Format aus STORY-047 des Viewers). 4. Techdocs
    beschreiben die Prüfung.
  - Summary: Ein Tippfehler in einer Notes-Datei würde sonst den ganzen
    Abgleich mit dem ToDo-Viewer blockieren. Die Prüfung meldet ihn sofort
    mit Datei und Zeile.

- `STORY-046` **Doppelt vergebene IDs bei paralleler Arbeit in Cloud und lokal vermeiden**
  - Uid: 6d64c87c-b4c2-48bf-8c2e-2563ec768a95.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-10-16.
  - Area: Governance.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Legen die Cloud (Dateimodus, nächste freie Nummer) und der lokale
    Viewer (Datenbank vergibt die ID) unabhängig voneinander ein Item
    gleichen Typs an, geht dabei kein Item verloren. Für Notes löst das
    schon das Verfahren mit `new-<kurzname>.md`, für Backlog-Items gibt es
    keines.
  - Completion criteria: 1. Geprüft und in den Notes festgehalten ist, wie
    der Viewer zwei unabhängig angelegte Items mit gleicher ID beim Sync
    behandelt (laut seiner Doku ein Konflikt `both_new`, bei dem nur eine
    Seite übernommen wird). 2. Die Entscheidung steht in den Notes: Regel im
    Skill (z. B. während einer Cloud-Sitzung lokal keine neuen Items
    gleichen Typs anlegen) oder Erweiterung des Viewers (vorläufige IDs für
    Items wie bei den Notes), jeweils mit Begründung. 3. Umgesetzt ist die
    gewählte Lösung: bei einer Regel im todo-Skill und in den Techdocs
    beschrieben; bei einer Viewer-Erweiterung ein Item im Backlog des
    ToDo-Viewers angelegt (mit Freigabe des Besitzers) und der Skill
    verweist darauf.
  - Summary: Verhindert, dass ein in der Cloud angelegter Eintrag beim
    Abgleich mit dem ToDo-Viewer verloren geht, wenn lokal gleichzeitig ein
    Eintrag mit derselben Nummer entsteht.

- `STORY-043` **Notes und Topics im Dateimodus führen**
  - Uid: 6e490502-1f99-4cba-8eb0-6985f5929ba7.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: In progress.
  - Created: 2026-10-16.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: `STORY-042`.
  - Goal: Notes und Topics lassen sich im Dateimodus (`backend = files`, z.
    B. in einer Cloud-Session) über den Ordner `notes/` im Backlog-Ordner
    führen, im Format des ToDo-Viewers (dessen Techdoc `interfaces.md`,
    Abschnitt Dateiformat Version 2: Notes und Topics). Der Viewer liest sie
    beim Sync in seine Datenbank.
  - Completion criteria: 1. Notes sind auch bei `files` aktiv
    (Config-Auswertung und Sitzungsstart-Zeile). 2. Der todo-Skill enthält
    eine Regeldatei für das Dateiformat (Version 2) und die Befugnis: Notes
    anlegen als `new-<kurzname>.md` mit erster Zeile `# NEW`, neue Topics
    als `Topic: new:<Name>` bzw. `NEW`-Zeile in `topics.md`, Zeiten in UTC
    mit `Z`; Labels, `Uid` und der Auslöser-Zustand `fired` gehören dem
    Viewer und werden nicht von Hand gesetzt; es gibt nur die Auslöser
    `event` und `topic_due`, eine `time`-Zeile ist ein Formatfehler. 3. Ein
    Index-Helfer für `notes/` (Gegenstück zu `backlog.py --index`) listet
    Label, Status, Review, Topic und Summary, ohne alle Dateien zu lesen. 4.
    Fälligkeit ohne Viewer ist geregelt: nur auf Nachfrage werden `Review`
    und das Datum des Topics mit dem heutigen Datum verglichen; Zeitpunkte
    sind Sache der Wecker und kommen hier nicht vor. 5. Die Regeln für `api`
    und `files` sind getrennt; die Aussage, Notes seien privat und nie im
    Repository, gilt nur für `api`, und die Dateivariante weist darauf hin,
    dass die Notes dann im Repository (GitHub) liegen. 6. Techdocs und
    README beschreiben Notes im Dateimodus; Tests decken den Helfer ab.
  - Summary: Auch in der Cloud lassen sich Erinnerungen und Notizen führen:
    als Markdown-Dateien im Repository, die der ToDo-Viewer später in seine
    Datenbank übernimmt.

- `STORY-045` **Ablauf zwischen Cloud, Git und lokalem Viewer festlegen**
  - Uid: dfc1d2ff-773e-4c7f-87d6-d312bf19de67.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-10-16.
  - Area: Governance.
  - Priority: Normal.
  - Dependencies: `STORY-042`, `STORY-043`.
  - Goal: Der todo-Skill beschreibt, wie Backlog und Notes zwischen einer
    Cloud-Sitzung (Dateien im Repository) und dem lokalen ToDo-Viewer
    (Datenbank) wandern, und widerspricht dabei nicht den Regeln des
    API-Modus.
  - Completion criteria: 1. Der Skill beschreibt den Ablauf vor der
    Cloud-Sitzung: Viewer-Sync, dann den Backlog-Ordner samt `notes/`
    committen und pushen. 2. Er beschreibt die Cloud-Seite im Dateimodus:
    Änderungen an Backlog und Notes gehören zur Änderung und liegen im
    Branch der Sitzung. 3. Er beschreibt den Rückweg: Branch mergen, lokal
    holen, Viewer-Sync (Auto-Sync oder Dialog), Konflikte im Dialog
    entscheiden; bei Merge-Markern in einer Datei pausiert der Auto-Sync,
    und die Marker sind zuerst zu lösen. 4. Er nennt die Voraussetzung im
    Viewer (Spiegel-Ordner ist der Backlog-Ordner des Repositorys, Auto-Sync
    an). 5. Die Regeln des API-Modus sind abgeglichen: Bei aktivem Spiegel
    werden auch die Dateien unter `notes/` committet (bisher steht dort,
    dass nichts committet wird), `TODO.md` und `archive.md` bleiben für die
    KI lokal unangetastet. 6. Der Ablauf ist einmal von Anfang bis Ende
    durchgespielt (die Cloud-Seite darf von Hand nachgestellt sein, solange
    keine Cloud-Umgebung zur Verfügung steht); das Ergebnis steht in den
    Notes. 7. Techdocs und README beschreiben den Ablauf.
  - Summary: Klare Schritte, wie der Stand zwischen Cloud und dem lokalen
    ToDo-Viewer hin und her wandert, damit nichts verloren geht und lokal
    weiter nur die API genutzt wird.

- `EPIC-008` **Backlog über die API des ToDo-Viewers**
  - Uid: 6da1ed5f-d947-48b4-b198-8bd2e96ef709.
  - Type: Epic.
  - Status: In progress.
  - Created: 2026-09-28.
  - Area: Konfiguration.
  - Priority: Important.
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
  - Required for parent: No.
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
  - Status: Open.
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
