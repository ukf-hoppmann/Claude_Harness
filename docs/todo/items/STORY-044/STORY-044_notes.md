# STORY-044 — Formatprüfung für den Notes-Ordner

## State

- Goal/Status: Formatprüfung für notes/ im Dateimodus. Umgesetzt und getestet, wartet auf Bestätigung.
- Next step: Owner bestätigt; danach STORY-045 (Ablauf zwischen Cloud, Git und Viewer) oder STORY-046.
- Open:
  - Prüfung dupliziert die Regeln des Viewer-Decoders; bei Formatänderung Fixtures neu kopieren
  - Verweisziele werden nicht auf Existenz geprüft
- Decided:
  - Story gestartet, STORY-043 bestätigt (2026-10-22)
  - Maßstab ist der Decoder des Neubaus (Format Version 2) mit den Beispielen aus tests/fixtures/mirror-v2; counters.md entfällt (2026-10-22)
  - Umfang notes/ ohne Prüfung von Verweisen; Hook im vorhandenen check_backlog.py, nur nach Änderung unter notes/ (2026-10-22)
  - Korrekturen aus STORY-043 gehören hierher; keine Tasks (2026-10-22)
  - Umgesetzt: notes_format.py, notes_files.py --check, Marke und Stop-Hook, Skill-Regeln, Techdocs (2026-10-22)
- References: Spec STORY-044_spec.md; Viewer-Decoder decode.py und syntax.py, Fixtures tests/fixtures/mirror-v2; STORY-043 Notes; EPIC-010

State confirmed after entry 2026-10-22 — Umsetzung (f722b63e144c)

## 2026-10-22 — Ausgangslage: Maßstab der Prüfung ist der Decoder des Neubaus

### Discussed

- STORY-043 ist bestätigt (Completed); STORY-044 gestartet (In progress). Es gibt noch keine Notes und keine Spec.
- Die Kriterien vom 2026-10-16 verweisen auf die Golden-Files unter backend/tests/golden/notes/ des ToDo-Viewers und prüfen counters.md. Das ist der alte Viewer (src_old). Seit der Entscheidung in STORY-043 gilt Format Version 2 des Neubaus: counters.md entfällt dort, Zeit-Auslöser sind ein Fehler.
- Der Neubau hat einen eigenen Decoder (server/src/viewer/plugins/notes/infrastructure/mirror/decode.py, Syntax in syntax.py) und Golden-Files unter tests/fixtures/mirror-v2/: valid/ (ein vollständiges Projekt mit notes/) und invalid/<code>/ mit expected.json (code, file, line, reason). Nur zwei Fehlerfälle betreffen notes/: unknown_trigger (Zeit-Auslöser) und file_label_mismatch; die übrigen Fälle betreffen TODO.md.
- Fehler, die der Decoder meldet (Code): invalid_value (u. a. Kopfzeile ohne Doppelpunkt, Kopfzeile doppelt, Zeile ohne Abschnitt, Verknüpfung oder Auslöser ungültig, Status/Mode/Archived/Zeitpunkt ungültig, Status due steht nie in einer Datei, neue Note mit Uid, Topic-Zeile ohne passendes Muster, Einrückung), unknown_field (Kopfzeile, Topic-Angabe), missing_field (Summary, Status, Uid bei Note mit Label, Topic-Name, uid bei Topic mit Label), file_label_mismatch (erste Zeile passt nicht zum Dateinamen), invalid_placeholder (Kurzname nicht a-z, 0-9, -), unknown_trigger (time und alles außer event und topic_due), duplicate_uid, duplicate_label. Dazu prüft der Viewer ordnerweit Git-Merge-Marker (merge_markers) und unlesbare Dateien.
- Ein Fehler bricht im Viewer den ganzen Sync ab. Die Prüfung im Harness bildet also nur nach, was der Viewer ohnehin ablehnt; die Logik liegt dann doppelt vor. Gegen Abweichung helfen die geteilten Fixtures (wie bei den Prüfsummen-Testvektoren in tests/fixtures/notes-state).
- Aus STORY-043 zwei Korrekturen, die zu dieser Prüfung gehören: (1) notes-files.md führt den Status due als schreibbaren Wert auf; er steht nie in einer Datei (erlaubt: waiting, snoozed, done, dropped, promoted). (2) notes_files.py erkennt new-Dateien nur mit kleinem Kurznamen und übergeht so Dateien mit Großbuchstaben still; der Viewer meldet dafür invalid_placeholder.

### Open

- Kriterien 1 bis 3 auf den Neubau umstellen: Maßstab ist der Decoder von Format Version 2 und tests/fixtures/mirror-v2 statt der alten Golden-Files; counters.md fällt weg. Wortlaut dem Owner vorlegen.
- Umfang: nur der Ordner notes/ (Notes, topics.md) oder auch die Dokumente der Notes? Vorschlag: Dokumente nur auf Dateinamen und zugehörige Note (der Viewer liest ihren Text unverändert).
- Wann geprüft wird: Vorschlag Stop-Hook im bestehenden check_backlog.py, wenn in der Session eine Datei unter notes/ geändert wurde; dann wird der ganze Ordner geprüft (dateiübergreifende Fehler wie doppelte Uid brauchen ihn).
- Zerlegung und Korrekturen aus STORY-043 (due, Großbuchstaben) in diese Story aufnehmen.

## 2026-10-22 — Entscheidung: Maßstab Neubau, Kriterien umgestellt, Spec geschrieben

### Discussed

- Vorschlag: Kriterien 1 bis 3 am Decoder von Format Version 2 und an tests/fixtures/mirror-v2 ausrichten, counters.md streichen; Umfang nur notes/ (Dokumente nur auf Dateiname und zugehörige Note); Prüfung am Turn-Ende im bestehenden check_backlog.py, wenn in der Session unter notes/ etwas geändert wurde, dann über den ganzen Ordner; die beiden Korrekturen aus STORY-043 (Status due, Großbuchstaben in new-Namen) gehören hierher; keine Tasks.
- Beim Lesen der Beispiele des Viewers: Der Decoder meldet je Datei den ersten Fehler; dateiübergreifende Fehler (doppelte Uid, doppeltes Label, doppelter Platzhalter) und Merge-Marker kommen vom Ordner. Ein Dokument ohne Note ignoriert der Viewer still, dateien mit unbekanntem Namen liest er nicht; beides wird im Harness ein Hinweis statt eines Fehlers, damit ein Tippfehler im Dateinamen auffällt.
- Entwurf der Umsetzung: neues Modul notes_format.py mit reinen Funktionen, notes_files.py bekommt --check (Gegenstück zu backlog.py ohne Option), mark_backlog_dirty.py merkt sich Änderungen unter notes/ in einer eigenen Marke, check_backlog.py prüft dann den Ordner.

### Decided

- Kriterien 1 bis 3 sind wie vorgeschlagen auf den Neubau umgestellt (Owner, 2026-10-22).
- Umfang: Ordner notes/ mit Notes, topics.md und Dokumentnamen; keine Prüfung von Verweisen auf Existenz (Owner, 2026-10-22).
- Die Korrekturen aus STORY-043 sind Teil dieser Story; keine Tasks, eine Sitzung (Owner, 2026-10-22).
- Spec STORY-044_spec.md geschrieben.

## 2026-10-22 — Umsetzung

### Discussed

- Plan vom Owner freigegeben; Umsetzung im Worktree story-044-notes-format in vier Commits, Tests jeweils vorweg (576 Tests grün, vorher 520).
- notes_format.py prüft den Ordner notes/ nach den Regeln des Viewer-Decoders (Format Version 2): je Datei der erste Fehler, dazu duplicate_uid, duplicate_label, doppelte Platzhalter, merge_markers und unreadable; Hinweise (nicht blockierend) für Dateien, die der Viewer nicht liest (ignored_file), und für Dokumente ohne Note (document_without_note). Fehlercodes sind die des Viewers. Die gültigen Beispiele und die beiden Notes-Fehlerfälle des Viewers liegen als Fixtures unter tests/fixtures/notes-format und stimmen mit expected.json (Code, Datei, Zeile) überein.
- Kein Unterschied zum Decoder gefunden, der den Kriterien widerspricht. Beobachtet beim Nachbauen: Der Decoder behandelt 'topic_due soon' und eine unvollständige event-Zeile als invalid_value (nicht unknown_trigger); nur time und fremde Arten sind unknown_trigger. Die Prüfung folgt dem.
- notes_files.py hat --check (Funde als notes/<Datei>:<Zeile>: <Code>: <Text>, Exit 1 bei Fehlern). Das Muster für new-Dateien ist das des Viewers (Großbuchstaben erlaubt), damit sie im Index erscheinen und die Prüfung invalid_placeholder meldet; notes-files.md nennt den Status due nicht mehr als schreibbar und beschreibt die Prüfung.
- Hook: mark_backlog_dirty.py merkt sich Änderungen unter notes/ in einer eigenen Marke (state.py), check_backlog.py prüft dann den ganzen Ordner, nur bei Backend files; die Marke bleibt bis zur Korrektur, Hinweise kommen einmal je Sitzung. Der Sitzungsstart prüft den Ordner nicht.
- Handlauf in einem Temp-Projekt mit den gültigen Beispielen: --check ohne Fund; nach einer 'time'-Zeile in NOTE-001.md blockiert der Hook mit 'notes/NOTE-001.md:15: unknown_trigger' (wie expected.json des Viewers), nach der Korrektur Exit 0. Nicht geprüft: ein echter Sync mit dem Viewer und eine Cloud-Sitzung.

### Decided

- Kriterien 1 bis 4 sind erfüllt; Status Awaiting confirmation, Bestätigung durch den Owner offen.

### Open

- Die Prüfung dupliziert die Regeln des Viewer-Decoders; ändert der Viewer das Format, müssen die Fixtures in tests/fixtures/notes-format neu kopiert und notes_format.py angepasst werden.
- Verweise (Ziele von Links, Triggern, Topics) werden nicht auf Existenz geprüft; der Viewer tut das beim Sync.
