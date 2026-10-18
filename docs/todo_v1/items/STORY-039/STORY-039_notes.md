# STORY-039 — API-Helfer für Notes und Topics

## 2026-10-06 — Planung

### Discussed

- Der gemeinsame HTTP-Client wird aus backlog_api.py herausgelöst, damit es keine Kopie gibt.

### Decided

- Umsetzung erst, wenn der Viewer seine Notes-API beschrieben hat.

### Open

- Befehlsnamen, Felder und Index-Format folgen der API des Viewers.

## 2026-10-08 — Umsetzung

### Discussed

- API des Viewers (interfaces.md) gelesen; Helfer gegen den laufenden Server nur lesend geprüft.

### Decided

- Gemeinsamer Client viewer_api.py; notes_api.py ohne endgültiges Löschen und ohne Schreiben der Settings.
- notices braucht in der API immer ein Label (Note oder Item); der Helfer fragt daher je Note oder Item ab.

### Open

- Schreibende Aufrufe sind nur gegen einen Stub getestet, nicht gegen den echten Server.
