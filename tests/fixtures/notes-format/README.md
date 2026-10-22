# Beispiele für die Formatprüfung der Notes

Kopie aus `tests/fixtures/mirror-v2` des ToDo-Viewers (Format Version 2), nur der Teil `notes/`:

- `valid/notes`: gültige Notes, Topics und ein Dokument; die Prüfung findet nichts.
- `invalid/<code>/`: je Fehlercode eine Kopie mit genau einem Fehler; `expected.json` nennt `code`, `file` und `line`.

Bei einer Änderung des Formats im Viewer werden die Dateien dort neu kopiert (Muster wie `notes-state`).
