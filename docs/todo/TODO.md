# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `EPIC-010` **Weg von der Claude-Code-App: Harness und ToDo-Viewer über claude.ai nutzen**
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
  - Notes: `items/EPIC-010/EPIC-010_notes.md`.

- `STORY-042` **Backlog-Backend je Umgebung umschalten**
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-10-16.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Das Backend des Backlogs (`api` oder `files`) lässt sich je
    Umgebung wählen, ohne die eingecheckte `.claude-harness/config.toml` zu
    ändern: lokal bleibt `api`, in einer Cloud-Session gilt `files`. Eine
    Umgebungsvariable überschreibt `[todo].backend`.
  - Completion criteria: 1. Die Umgebungsvariable
    `CLAUDE_HARNESS_TODO_BACKEND` (Werte `api`, `files`) überschreibt
    `[todo].backend` bei der Config-Auswertung; ein ungültiger Wert wird wie
    ein Config-Fehler gemeldet. 2. Sitzungsstart, Backlog-Hooks und Hinweise
    der Skills folgen dem wirksamen Backend. 3. Techdocs (Konfiguration) und
    der todo-Skill beschreiben die Variable. 4. Tests decken beide Backends
    und den Fehlerfall ab. 5. Ob die Cloud zusätzlich automatisch erkannt
    wird (z. B. über `CLAUDE_CODE_REMOTE`), ist geprüft; die Entscheidung
    steht in den Notes.
  - Summary: Lokal arbeitet der Harness weiter über die API des
    ToDo-Viewers, in der Cloud automatisch über die Markdown-Dateien. Die
    gemeinsame Config bleibt dafür unverändert.
  - Notes: `items/STORY-042/STORY-042_notes.md`.

- `STORY-043` **Notes und Topics im Dateimodus führen**
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-10-16.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: `STORY-042`.
  - Goal: Notes und Topics lassen sich im Dateimodus (`backend = files`, z.
    B. in einer Cloud-Session) über den Ordner `notes/` im Backlog-Ordner
    führen, im Format des ToDo-Viewers (dessen Techdoc `interfaces.md`,
    Abschnitt Dateiformat: Notes-Ordner). Der Viewer liest sie beim Sync in
    seine Datenbank.
  - Completion criteria: 1. Notes sind auch bei `files` aktiv
    (Config-Auswertung und Sitzungsstart-Zeile). 2. Der todo-Skill enthält
    eine Regeldatei für das Dateiformat und die Befugnis: Notes anlegen als
    `new-<kurzname>.md` mit erster Zeile `# NEW`, neue Topics als `Topic:
    new:<Name>` bzw. `NEW`-Zeile in `topics.md`, Zeiten in UTC mit `Z`;
    Labels, `counters.md` und der Auslöser-Zustand `fired` gehören dem
    Viewer und werden nicht von Hand gesetzt. 3. Ein Index-Helfer für
    `notes/` (Gegenstück zu `backlog.py --index`) listet Label, Status,
    Review, Topic und Summary, ohne alle Dateien zu lesen. 4. Fälligkeit
    ohne Viewer ist geregelt: nur auf Nachfrage werden Review-Datum und
    Zeit-Auslöser mit dem heutigen Datum verglichen. 5. Die Regeln für `api`
    und `files` sind getrennt; die Aussage, Notes seien privat und nie im
    Repository, gilt nur für `api`, und die Dateivariante weist darauf hin,
    dass die Notes dann im Repository (GitHub) liegen. 6. Techdocs und
    README beschreiben Notes im Dateimodus; Tests decken den Helfer ab.
  - Summary: Auch in der Cloud lassen sich Erinnerungen und Notizen führen:
    als Markdown-Dateien im Repository, die der ToDo-Viewer später in seine
    Datenbank übernimmt.

- `STORY-044` **Formatprüfung für den Notes-Ordner**
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

- `STORY-045` **Ablauf zwischen Cloud, Git und lokalem Viewer festlegen**
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

- `STORY-046` **Doppelt vergebene IDs bei paralleler Arbeit in Cloud und lokal vermeiden**
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

- `STORY-047` **Harness ohne Plugin in Cloud-Sessions verfügbar machen**
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: In progress.
  - Created: 2026-10-16.
  - Area: Architektur.
  - Priority: Important.
  - Dependencies: None.
  - Goal: In einer Cloud-Session eines Fremdprojekts (z. B. ezf-ui) wird das
    Plugin nicht geladen. Trotzdem stehen dort Regeln, Hooks und Skripte des
    Harness bereit, sodass Backlog (Dateimodus), Notes, Daily Reports,
    Techdocs und die übrigen Module wie lokal gelten.
  - Completion criteria: 1. Geprüft und in den Notes belegt (Doku und
    Probelauf): was eine Cloud-Session aus dem Repository des Zielprojekts
    lädt (z. B. CLAUDE.md, .claude/skills, Hooks in .claude/settings.json)
    und was nicht, welche Python-Version die VM hat (der Harness braucht
    3.11+), und wie die Pfadvariablen `CLAUDE_PLUGIN_ROOT` und
    `CLAUDE_PLUGIN_DATA` dort zu ersetzen sind. 2. Die Entscheidung, wie der
    Harness ins Zielprojekt kommt (z. B. erzeugte Kopie unter `.claude/`,
    Submodul, Setup-Script des Environments), steht mit Begründung und
    Aufwand für Aktualisierungen in den Notes. 3. Umgesetzt: Ein Befehl
    richtet ein Projekt für die Cloud ein, und Skills, Hooks und Skripte
    laufen dort ohne Plugin. 4. Module, die in der Cloud nicht funktionieren
    (z. B. worktree), sind benannt und abgeschaltet oder angepasst. 5.
    Techdocs und README beschreiben Einrichtung und Aktualisierung. 6. Ein
    Probelauf in einer Cloud-Sitzung zeigt, dass Sitzungsstart-Hinweis,
    Backlog im Dateimodus und mindestens ein Hook dort wirken.
  - Summary: Lokal wird der Harness als Plugin geladen. In der Cloud fehlt
    dieser Weg; hier steht, was die Doku dazu sagt und welche Wege es gibt,
    die Regeln und Skripte trotzdem dorthin zu bringen.
  - Notes: `items/STORY-047/STORY-047_notes.md`.
