# STORY-043 — Spec: Notes und Topics im Dateimodus

## Ziel

Bei `[todo].backend = files` (wirksames Backend, auch durch die Cloud-Erkennung aus STORY-042) lassen sich Notes und Topics über den Ordner `notes/` im Backlog-Ordner führen. Der ToDo-Viewer liest ihn beim Sync in seine Datenbank. Maßgeblich ist das Dateiformat Version 2 aus der Viewer-Techdoc (`interfaces.md`, Abschnitt „Dateiformat Version 2“, Unterabschnitt „Notes und Topics“). Wecker (`alarms.md`) gehören nicht dazu.

## Verhalten

### Wann Notes aktiv sind

- `notes_enabled()` gilt bei jedem Backend, solange `[modules].todo` an ist. Es gibt keinen neuen Schalter.
- Der Sitzungsstart nennt Notes je Backend: bei `api` wie bisher die API des Viewers, bei `files` den Ordner `<todo.path>/notes/` und den Verweis auf die Regeln (Skill `todo`, Datei für den Dateimodus). Es wird nichts abgefragt und kein Ordner angelegt.
- `notes_api.py` und `alarms_api.py` bleiben an `api` gebunden; im Dateimodus melden sie, dass sie dort nicht gelten.

### Regeln im Skill `todo`

- `notes.md` bleibt die Regel für `api`; ihr erster Schritt verweist im Dateimodus auf die neue Datei `notes-files.md`.
- `notes-files.md` enthält: Ablage und Dateiformat (Verweis auf die Viewer-Techdoc, nur die für das Anlegen nötigen Zeilen), die Befugnis und den Datenschutzhinweis.
- Anlegen: `notes/new-<kurzname>.md`, erste Zeile `# NEW`, danach die Kopfzeilen des Formats (`Summary`, `Status`, `Topic`, `Review`, `Mode`, `Triggers`, `Links`), leere Zeile, Langtext. Dokumente einer Note heißen `new-<kurzname>_notes.md` usw. Neue Topics: `Topic: new:<Name>` in der Note und eine `- NEW | <Name> | …`-Zeile in `topics.md`.
- Zeiten stehen in UTC mit `Z`. Die KI rechnet relative Angaben in einen festen Zeitpunkt um und nennt ihn mit Wochentag in der Antwort.
- Nur Auslöser `event` und `topic_due`; Zeit-Erinnerungen sind Wecker (nicht im Dateimodus, die KI sagt das). Eine `time`-Zeile ist ein Formatfehler.
- Nicht von Hand setzen oder ändern: Labels, `Uid`, `Created`/`Updated`, den Auslöser-Zustand `fired`, `counters.md` (gibt es in Version 2 nicht). Vorhandene Dateien mit Label darf die KI inhaltlich ändern (Summary, Review, Langtext, Dokumente), ohne Kopf und Uid anzufassen.
- Befugnis wie in `notes.md` (ohne Rückfrage anlegen und ändern, `dropped` und Löschen nur nach Rückfrage), soweit sie sich in Dateien ausdrücken lässt; `promote`, `demote` und `move` gibt es nur über den Viewer.
- Datenschutz: Im Dateimodus liegen die Notes im Repository (bei Cloud-Nutzung in GitHub). Die KI weist beim ersten Anlegen darauf hin; die Aussage „Notes sind privat“ in `notes.md` gilt nur für `api`.
- Lesereihenfolge wie bei `api`: zuerst der Index, dann nur passende Notes.

### Index-Helfer

- Neues Skript `plugin/scripts/notes_files.py <Backlog-Ordner> --index [--due] [--today YYYY-MM-DD]`.
- `--index` listet je Note eine Zeile `Datei | Status | Review | Topic | Summary` aus den Kopfzeilen, ohne Langtext und Dokumente. Topics werden mit Namen aus `topics.md` aufgelöst, eine unbekannte Topic-Angabe bleibt, wie sie steht. Notes im Papierkorb (`Deleted:` gesetzt) und archivierte stehen nicht im Index.
- `--due` zeigt nur Notes mit Status `waiting`, `due` oder `snoozed`, deren `Review` vor oder am heutigen Tag liegt oder deren Topic ein `due` am heutigen Tag oder davor hat; dazu steht der Grund. `--today` ersetzt das Tagesdatum (für Tests). Es gibt keine Auslöser-Auswertung (`event` braucht den Viewer).
- Fehlt `notes/`, ist die Ausgabe leer und der Exit-Code 0. Eine Datei, die sich nicht lesen lässt, wird in der Ausgabe gemeldet; der Helfer prüft das Format nicht vollständig (das ist Aufgabe von STORY-044).
- Nur Standardbibliothek, ein Eintrag je Zeile, deterministische Reihenfolge nach Dateiname.

### Nicht Teil dieser Story

- Wecker im Dateimodus (`alarms.md`).
- Vollständige Formatprüfung und Hook für `notes/` (STORY-044).
- Ablauf zwischen Cloud, Git und Viewer (STORY-045).
- Ein Abgleich mit der Datenbank; der Viewer bleibt für Labels, Uid und Fälligkeit mit Auslösern zuständig.

## Schnittstellen und Dokumentation

- Neu: `notes_files.py` mit den Optionen oben; geändert: `harness_config.py` (`notes_enabled`), `session_start.py`, Skill `todo` (`SKILL.md`-Abschnitt Notes, `notes.md`, neue Datei `notes-files.md`).
- Techdocs `interfaces.md` (neuer Helfer, Sitzungsstart), `configuration.md` (Hinweis bei `modules.todo` und `todo.backend`) und README beschreiben Notes im Dateimodus.
- `cloud_export.py` kopiert den ganzen Skill- und Skriptordner; für die Kopie ist nichts zu tun, aber ein Test prüft, dass `notes_files.py` und `notes-files.md` mitgehen.

## Tests

- Unit: Parser und Index von `notes_files.py` (Kopfzeilen, Topics auflösen, Papierkorb/Archiv, `new-`-Dateien, fehlender Ordner, `--due` mit Review, Topic-Datum und `--today`).
- Config und Sitzungsstart: `notes_enabled()` je Backend (die bisherigen Erwartungen `False` für `files` ändern sich), Zeile je Backend, Cloud-Fall.
- Der Helfer wird einmal gegen die Beispieldatei der Viewer-Techdoc geprüft (als Fixture im Testordner).
