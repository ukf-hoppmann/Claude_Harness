# STORY-045 — Spec: Ablauf zwischen Cloud, Git und lokalem Viewer

## Ziel

Der Skill `todo` beschreibt, wie Backlog und Notes zwischen einer Cloud-Sitzung (Dateien im Repository, Backend `files`) und dem lokalen ToDo-Viewer (Datenbank, Backend `api`) wandern, ohne dass die Regeln des API-Modus gebrochen werden. Der Ablauf ist einmal von Anfang bis Ende am echten Backlog durchgespielt; das Ergebnis steht in den Notes der Story.

## Verhalten (Inhalt der Regeln)

Die Regeln stehen in einer neuen Unterdatei `plugin/skills/todo/sync-flow.md` (Englisch, nur bei Bedarf geladen). `SKILL.md` und `notes.md` verweisen kurz darauf (Ladestufe 3 der Architektur: ein Thema, ein Skill; keine neue Hook-Logik).

### Voraussetzungen im Viewer

- Das Projekt ist im Viewer registriert, sein Spiegel-Ordner ist der Backlog-Ordner des Repositorys (`todo.path`, Hauptcheckout).
- Auto-Sync steht auf „Ein, Sync automatisch“ (Viewer: Einstellungen → Projekte → Einrichtung). Er prüft alle 30 Sekunden; eine Änderung wird erst übernommen, wenn sie bei zwei Prüfungen gleich war. Ohne Auto-Sync löst der Besitzer den Sync im Dialog aus.
- Der Backlog-Ordner samt `notes/` und `items/` ist im Repository eingecheckt (so liest ihn die Cloud).

### Hinweg (lokal, vor der Cloud-Sitzung)

1. Der Viewer-Sync ist durch (keine offenen Konflikte; Auto-Sync abwarten oder Sync im Dialog).
2. Den Backlog-Ordner samt `notes/` im Hauptcheckout als `Backlog: …` committen und `main` pushen. Das Pushen ist Sache des Besitzers; die KI pusht nicht.
3. Erst danach die Cloud-Sitzung starten, sonst arbeitet sie auf veralteten Dateien.

### In der Cloud (Backend `files`)

- Es gelten die Dateiregeln (`format.md`, `notes-files.md`); die KI bearbeitet `TODO.md`, `archive.md`, `items/` und `notes/` direkt, der Stop-Hook prüft sie.
- Neue Backlog-Einträge bekommen Platzhalter (`NEW-<Name>`), neue Notes `new-<Name>.md`; Labels und Uids vergibt der Viewer beim Sync. Doppelte IDs bei paralleler Arbeit sind Sache von STORY-046; bis dahin legt die KI in der Cloud nur Einträge mit Platzhalter an.
- Die Änderungen an Backlog und Notes gehören zur Änderung und liegen im Branch der Sitzung (`claude/<Name>`), nicht auf `main`.

### Rückweg

1. Der Branch kommt per Pull Request auf GitHub nach `main` (Standard, Entscheidung des Besitzers vom 2026-10-22). Alternative: lokal `git fetch` und Merge von `origin/claude/<Name>` nach `main`.
2. Lokal im Hauptcheckout: erst eigene Backlog-Änderungen, die die API geschrieben hat, als `Backlog: …` committen, dann `git pull`, damit der Pull nicht an unversionierten Dateien scheitert.
3. Der Viewer übernimmt die Dateien beim nächsten Auto-Sync oder im Sync-Dialog. Konflikte (`both_changed`, `both_created`, `deleted_in_files`, `deleted_in_database`) und Löschungen bleiben offen, bis der Besitzer im Dialog `database`, `files` oder `defer` entscheidet; die KI entscheidet sie nicht und löscht nichts in diesem Zusammenhang.
4. Enthält eine Datei Git-Merge-Marker (`<<<<<<<` und `>>>>>>>`), fehlt der Ordner oder liegt ein Git-Lock, pausiert der Auto-Sync. Dann zuerst die Marker lösen (die KI darf das auf Bitte des Besitzers, danach Dateien prüfen), den Git-Vorgang beenden, dann syncen. Ein Formatfehler in `notes/` bricht den Sync mit `note_format` samt Datei und Zeile ab, ohne etwas zu ändern.
5. Nach dem Sync tragen die Einträge Labels und Uids (aus Platzhaltern wurden Labels, Dateien wurden umbenannt); die KI liest den Stand wieder über die API.

### Berichtigung der Regeln des API-Modus

- `notes.md`: Die Aussage, Notes seien nur in der Datenbank, nie in Dateien und nie committet, gilt nur ohne Spiegel. Mit Spiegel schreibt der Viewer `notes/` in den Backlog-Ordner; die Dateien werden wie der Rest des Backlog-Ordners committet (`Backlog: …`), die KI schreibt sie nicht von Hand. Notes sind dann nicht mehr privat (Repository, bei Cloud-Nutzung GitHub); der Hinweis an den Besitzer steht an derselben Stelle wie bei `notes-files.md`.
- `SKILL.md`, Abschnitt „Committing backlog changes“: Im API-Modus gehört bei aktivem Spiegel auch `notes/` zu den Dateien, die im Hauptcheckout als `Backlog: …` committet werden. `TODO.md`, `archive.md` und `items/` bleiben für die KI im API-Modus unangetastet (unverändert).
- Wie die KI erkennt, ob ein Spiegel aktiv ist: der Helfer kennt das Viewer-Projekt (`mirror_folder`, über `sources`). Die KI committet `notes/`, wenn der Ordner im Backlog-Ordner existiert; gibt es ihn nicht, gibt es nichts zu committen.

## Durchspielung (Kriterium 6)

Am echten Backlog von Claude_Harness, Cloud-Seite von Hand nachgestellt (Entscheidung des Besitzers). Nur mit unschädlicher Änderung und Backup des Viewers vorher:

1. Ausgangslage prüfen: Viewer erreichbar, Spiegel dieses Repositorys, Auto-Sync an, keine offenen Konflikte, Backlog-Ordner sauber.
2. Cloud-Seite: Branch von `main`, Backend `files` (`CLAUDE_HARNESS_TODO_BACKEND=files`), dort einen Notes-Eintrag an `STORY-045` anhängen und eine neue Note `new-ablauf-probe.md` anlegen; Stop-Hook läuft; committen.
3. Rückweg: Branch nach `main` mergen (stellvertretend für den Pull Request), Auto-Sync abwarten.
4. Ergebnis prüfen: Der Notes-Eintrag steht über die API in `STORY-045`; die Probe-Note hat ein Label und die Datei heißt `NOTE-xxx.md`. Die Probe-Note wird danach als `dropped` beendet (nach Rückfrage; endgültiges Löschen ist Sache des Besitzers).
5. Ergebnis, Dauer und Auffälligkeiten (auch Abweichungen von dieser Spec) kommen in die Notes der Story. Konflikte oder Merge-Marker werden nicht künstlich erzeugt.

## Nicht Teil dieser Story

- Doppelte IDs bei paralleler Arbeit (STORY-046), Wecker, ein Pull Request über die GitHub-API oder `gh` (die Cloud-Seite endet am Branch).
- Änderungen am Viewer.

## Dokumentation und Tests

- Neu: `plugin/skills/todo/sync-flow.md`. Geändert: `notes.md`, `SKILL.md` (Abschnitte Notes und Committing backlog changes).
- README (Abschnitt Cloud-Sitzungen) und Techdocs (`architecture.md`: Zeile Notes und Backlog) beschreiben den Ablauf kurz und verweisen auf den Skill.
- Tests: Der Ablauf ist Regeltext ohne neuen Code; ein Test sichert, dass `sync-flow.md` in der Cloud-Kopie landet und `SKILL.md` und `notes.md` darauf verweisen. Die Durchspielung ist der Integrationsnachweis.
