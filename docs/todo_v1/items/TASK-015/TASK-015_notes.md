# TASK-015 — Einzelitem-Abruf in backlog.py für archive.md

## 2026-09-28 — Zweistufiges Laden auch für archive.md

### Discussed

- Heute wird für archivierte Items im Files-Modus die ganze archive.md gelesen, was viele Tokens kostet.
- Im API-Modus gibt es index und show bereits; die API liefert im Index aber keine Area.

### Decided

- Prinzip: erst flache Liste (index/--index), dann gezielt einzelne Items; archive.md nie ganz lesen.
- backlog.py bekommt --show <ID> [<ID> ...] für ein oder mehrere Items aus TODO.md oder archive.md, Ausgabe als Markdown-Block mit Quelldatei.
- Die flache Liste bekommt die Spalte Area (backlog.py --index und backlog_api.py index).

### Open

- Die ToDo-Viewer-API liefert Area im Index noch nicht; backlog_api.py zeigt sie, sobald die API sie mitliefert.

## 2026-09-28 — Area im API-Index geklärt

### Decided

- Der ToDo-Viewer liefert area jetzt im Index (dort TASK-001); backlog_api.py index zeigt die Spalte ohne weitere Änderung. Der offene Punkt vom 2026-09-28 ist damit erledigt.
