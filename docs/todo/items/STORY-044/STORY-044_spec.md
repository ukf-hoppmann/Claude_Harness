# STORY-044 — Spec: Formatprüfung für den Notes-Ordner

## Ziel

Bei `[todo].backend = files` prüft der Harness den Ordner `notes/` im Backlog-Ordner auf Formatfehler, bevor der ToDo-Viewer ihn liest. Der Viewer bricht bei einem einzigen Fehler den ganzen Sync ab (Backlog und Notes); der Fehler soll deshalb am Turn-Ende auffallen, mit Datei, Zeile und Fehlercode. Maßstab ist der Decoder des Neubaus (Format Version 2: `server/src/viewer/plugins/notes/infrastructure/mirror/decode.py` und `syntax.py` im ToDo-Viewer) und seine Beispiele (`tests/fixtures/mirror-v2/`). Das Format selbst bleibt Sache des Viewers; der Harness bildet nur ab, was der Viewer ablehnt.

## Verhalten

### Was geprüft wird

Die Prüfung liest den ganzen Ordner `notes/` (dateiübergreifende Fehler brauchen ihn) und meldet je Datei den ersten Fehler, wie der Decoder, dazu die dateiübergreifenden Fehler. Fehlercodes sind die des Viewers.

- **Dateien:** Gelesen werden `NOTE-<n>.md`, `new-<Kurzname>.md` (Muster `new-[A-Za-z0-9-]+`, der Kurzname selbst muss `a-z`, `0-9`, `-` sein, sonst `invalid_placeholder`), `topics.md` und die Dokumente `<Note>_notes.md`, `<Note>_spec.md`, `<Note>_spec_<Thema>.md`. Andere Dateien liest der Viewer nicht; sie ergeben einen Hinweis (kein Fehler), damit ein Tippfehler im Dateinamen auffällt. `counters.md` gibt es in Version 2 nicht und wird ignoriert (kein Hinweis, kein Fehler).
- **Notes:**
  - Erste Zeile `# NEW` bei `new-…`, sonst `# <Label>` wie der Dateiname, sonst `file_label_mismatch` (Zeile 1).
  - Kopf bis zur ersten Leerzeile. `Uid`, `Summary`, `Status`, `Topic`, `Review`, `Mode`, `Created`, `Updated`, `Archived`, `Deleted` sind die einzigen Kopfzeilen (`unknown_field` sonst); eine Zeile ohne Doppelpunkt, eine Kopfzeile zweimal, eine Listenzeile ohne Abschnitt (`Triggers:`/`Links:`) und `Triggers:`/`Links:` mit Text in derselben Zeile sind `invalid_value`.
  - Pflicht: `Summary` und `Status` (`missing_field`), `Uid` bei einer Note mit Label (`missing_field`); eine neue Note hat keine `Uid` (`invalid_value`).
  - `Status` aus `waiting`, `snoozed`, `done`, `dropped`, `promoted`; `due` ist abgeleitet und steht nie in einer Datei (`invalid_value`). `Mode` `any` oder `all`, `Archived` `true` oder `false`; Zeitpunkte (`Review`, `Created`, `Updated`, `Deleted`) UTC mit `Z`, sonst `invalid_value`.
  - `Triggers:` kennt nur `- event <Ziel> <Status> [fired …] [already_met]` (Status aus `In progress`, `Awaiting confirmation`, `Completed`, `Rejected`) und `- topic_due`; `time` und jede andere Art sind `unknown_trigger`, eine kaputte `event`-Zeile oder Marke ist `invalid_value`. `Links:` kennt `- reference <Ziel>` und `- origin <Ziel>`, sonst `invalid_value`. Ziele werden nicht auf Existenz geprüft.
- **topics.md:** Zeilenmuster `<Einrückung>- TOPIC-<n> | <Name> | <Angaben>` oder `- NEW | …`; Einrückung ein Vielfaches von zwei Leerzeichen und höchstens eine Ebene tiefer als die vorige Zeile; Name nicht leer; Angaben nur `uid=`, `due=`, `created=`, `archived=`, `deleted=` (`unknown_field` sonst) mit gültigen Zeitpunkten; ein Topic mit Label braucht `uid=` (`missing_field`).
- **Dateiübergreifend:** doppelte `Uid` (`duplicate_uid`), doppeltes Label (`duplicate_label`), doppelter Platzhalter (`invalid_placeholder`), jeweils bei Notes und Topics.
- **Ordner:** Git-Merge-Marker (eine Zeile `<<<<<<<` und eine Zeile `>>>>>>>` am Zeilenanfang in derselben Datei: `merge_markers`, Zeile des Anfangsmarkers) und nicht lesbare oder nicht UTF-8 kodierte Dateien (`unreadable`, Zeile 1).
- **Dokumente:** nur der Dateiname gilt; gehört kein `NOTE-…`/`new-…` dazu, ist das ein Hinweis (der Viewer ignoriert es), kein Fehler.

### Ausgabe

Eine Meldung je Fund: `notes/<Datei>:<Zeile>: <Code>: <Text>` (Pfad relativ zum Backlog-Ordner), Text Englisch. Fehler blockieren, Hinweise erscheinen einmal je Sitzung.

### Aufruf und Hook

- `notes_files.py <Backlog-Ordner> --check` gibt die Funde aus (ein Fund je Zeile, Fehler vor Hinweisen) und beendet mit 1 bei Fehlern, sonst 0; ohne Ordner `notes/` ist die Ausgabe leer. Das Gegenstück zu `backlog.py` ohne Option.
- `mark_backlog_dirty.py` merkt sich zusätzlich, dass in der Session eine Datei unter `<todo.path>/notes/` geändert wurde (eigene Marke je Projekt in `state.py`).
- `check_backlog.py` prüft am Turn-Ende bei dieser Marke den Notes-Ordner (nur Backend `files`, nur Modul `todo`) und blockiert mit den Fehlern; das Projekt bleibt markiert, bis keine Fehler mehr da sind. Die Meldung nennt die Regeldatei `notes-files.md` des Skills `todo`. Ohne Änderung unter `notes/` wird der Ordner nicht geprüft.
- Sitzungsstart prüft den Notes-Ordner nicht.

### Berichtigung aus STORY-043

- `plugin/skills/todo/notes-files.md`: die Statusliste nennt `due` nicht mehr als schreibbar; der Hinweis, vor dem Abschluss `notes_files.py --check` zu laufen (der Hook tut es ohnehin), kommt dazu.
- `plugin/scripts/notes_files.py`: Notes `new-<Name>.md` mit Großbuchstaben im Namen werden im Index angezeigt (Muster des Viewers); die Prüfung meldet sie als `invalid_placeholder`.

### Nicht Teil dieser Story

- Wecker (`alarms.md`), das Backlog selbst (prüft `backlog.py`), Ablauf zwischen Cloud, Git und Viewer (STORY-045).
- Prüfung von Verweisen (Ziele von Links, Triggern und Topics) auf Existenz; das ist beim Viewer ein Sync-Schritt.
- Ein Abgleich mit der Datenbank.

## Schnittstellen und Dokumentation

- Neu: `plugin/scripts/notes_format.py` (reine Funktionen: Fund, Prüfung eines Ordners; Standardbibliothek, Syntax nach `syntax.py` des Viewers). Geändert: `notes_files.py` (`--check`, Muster), `mark_backlog_dirty.py`, `check_backlog.py`, `state.py` (Marke), Skill `todo` (`notes-files.md`).
- Techdocs: `interfaces.md` (`notes_files.py --check`, Hook-Zeilen von `mark_backlog_dirty.py` und `check_backlog.py`), `architecture.md` (Komponente Notes). Der Fehlercode-Katalog steht in `interfaces.md`.
- `cloud_export.py` kopiert den Skripteordner; nichts zu tun.

## Tests

- Beispiele des Viewers als Fixtures unter `tests/fixtures/notes-format/` (aus `tests/fixtures/mirror-v2` des ToDo-Viewers): `valid/notes` (fehlerfrei gelesen) und die Notes-Fehlerfälle `unknown_trigger` und `file_label_mismatch` mit `expected.json` (Code, Datei, Zeile).
- Je Fehlercode und je Meldung ein Test mit einem kleinen Ordner im Temp-Verzeichnis (unbekannte Kopfzeile, doppelte Kopfzeile, fehlendes Summary, Status `due`, Uid bei neuer Note, kaputtes Datum, kaputte Trigger- und Link-Zeile, Topic-Zeile falsch, Einrückung, doppelte Uid, doppeltes Label, doppelter Platzhalter, Merge-Marker, nicht lesbar), dazu Hinweise (unbekannte Datei, Dokument ohne Note).
- Hook: `check_backlog.py` blockiert nach einer Änderung unter `notes/` bei einem Fehler, ist bei Backend `api` still, prüft ohne Änderung unter `notes/` nicht und lässt die Marke stehen, bis der Fehler behoben ist (Muster der vorhandenen Hook-Tests in `tests/implementation/integration/test_hooks.py`).
- `notes_files.py`: `--check`, Exit-Codes, `new-`-Datei mit Großbuchstaben im Index.
