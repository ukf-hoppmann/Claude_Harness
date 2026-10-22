# STORY-044 — Formatprüfung für den Notes-Ordner

## State

- Ziel/Status: Formatprüfung für notes/ im Dateimodus (Stop-Hook, Meldung mit Datei und Zeile). In Arbeit, Klärung läuft; keine Spec.
- Nächster Schritt: Owner entscheidet Wortlaut der Kriterien 1 bis 3, Umfang und Zeitpunkt der Prüfung; danach Spec schreiben.
- Offen:
  - Kriterien 1 bis 3 auf den Neubau (Decoder, tests/fixtures/mirror-v2, ohne counters.md)
  - Umfang (Dokumente der Notes) und Zeitpunkt (Stop-Hook, ganzer Ordner)
  - Korrekturen aus STORY-043 aufnehmen (Status due, Großbuchstaben in new-Namen)
- Beschlossen:
  - Story gestartet, STORY-043 bestätigt (2026-10-22)
- Verweise: Viewer-Decoder decode.py und syntax.py (plugins/notes/infrastructure/mirror), Fixtures tests/fixtures/mirror-v2; STORY-043 Notes; EPIC-010

State confirmed after entry 2026-10-22 — Ausgangslage: Maßstab der Prüfung ist der Decoder des Neubaus (c19bf872cb42)

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
