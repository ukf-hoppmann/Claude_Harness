# EPIC-008 — Spec: Backlog über die API des ToDo-Viewers

## Ausgangslage

Der ToDo-Viewer (`/Users/hoppmann/Documents/GitHub/ToDo_viewer`) bietet eine
HTTP-API unter `http://localhost:5411/api/v2`. Maßgeblich für die API sind dort
`docs/techdocs/interfaces.md` (Abschnitt „Nutzung durch Agenten“) und
`web/src/api/openapi.json`. Der Server prüft Format und Parent-Regeln, vergibt
IDs, schreibt Notes-Einträge im Format und erkennt konkurrierende Änderungen
über Versions-Tokens. Er kennt keine Freigaben des Projektverantwortlichen und
committet nicht.

## API in Kürze

- Erreichbarkeit: `GET /health` → `{status: "ok", api: "2"}`. Der Container
  läuft dauerhaft, nur an `127.0.0.1:5411`; nach Änderungen am Viewer muss er
  mit `./todo.sh update` neu gebaut werden.
- Quelle: In `GET /sources` den Eintrag suchen, dessen `path` der
  Backlog-Ordner ist; fehlt er, `POST /sources` mit `{path}`. Jeder Backlog
  (auch je Teilprojekt) ist eine eigene Quelle.
- Überblick: `GET /index?source_id=…` ersetzt `backlog.py --index`.
- Item (auch archiviert): `GET /items/{source_id}/{id}`, liefert `version`.
- Anlegen: `POST /items`; die ID vergibt der Server.
- Ändern: `PATCH /items/{source_id}/{id}` mit `{version, fields}`. Bei 409
  `version_conflict` neu lesen und die Änderung prüfen, nicht blind
  wiederholen. `Completed`/`Rejected` brauchen `resolution`; der Server
  archiviert und holt beim Zurücksetzen zurück.
- Notes anhängen: `POST /items/{source_id}/{id}/notes` mit
  `{topic, discussed, decided, open, summary?}`; Datum setzt der Server; der
  erste Eintrag legt die Datei an und verlangt eine Summary.
- Notes/Specs lesen und ersetzen: `GET`/`PUT
  /items/{source_id}/{id}/documents/{name}` mit `{content, version}`
  (`version: null` = neu). Namen: `<ID>_notes.md`, `<ID>_spec.md`,
  `<ID>_spec_<thema>.md`.
- Löschen: `DELETE /items/{source_id}/{id}?version=…` legt in den Papierkorb
  (bei Kindern 409 `has_children`, mit `cascade=true` samt Nachfahren);
  `GET /trash`, `POST /trash/{source_id}/{id}/restore`; `DELETE /trash/…`
  löscht endgültig samt `items/<ID>/`.

## Formaterweiterungen des Viewers

- Feld `Deleted: <YYYY-MM-DD>.` für Items im Papierkorb. Sie liegen in
  `archive.md`, auch mit nicht abgeschlossenem Status, und zählen für die
  Parent-Regeln nicht.
- Leer-Markierung ist nur `No entries.`; die Format-Kennung steht englisch in
  `TODO.md`.
- Der Viewer bricht lange Feldwerte bei 76 Zeichen mit vier Leerzeichen
  Einzug um, schreibt IDs und Pfade in Backticks, fügt neue Felder am Ende
  eines Eintrags ein und setzt zurückgeholte Einträge ans Ende von `TODO.md`.
  Neue Notes-Dateien beginnen mit `# <ID> — <Titel>`.

## Regelunterschiede Viewer ↔ `backlog.py`

- Der Viewer lehnt nur neue Verstöße ab; `backlog.py` meldet alle.
- Ein Epic ohne Pflichtkind darf im Viewer `Rejected` werden.
- Nur im Viewer: unbekannte Verweise, Verweis-Schutz beim Löschen.

## Randbedingungen aus den Architekturregeln

- Hooks nutzen kein Netzwerk (Regel 2): Der Sitzungsstart prüft die
  Erreichbarkeit nicht, er nennt nur das Backend. Die Prüfung macht das
  API-Hilfsskript, das der Skill aufruft.
- Neue Config-Schlüssel werden in `harness_config.py` validiert, in
  `docs/techdocs/configuration.md` dokumentiert und in `tests/test_config.py`
  getestet (Regel 4).
- Die API-URL steht in der Config; der Standardwert ist eine benannte
  Konstante (Regel 8).
- Skill-Texte und Hook-Meldungen bleiben englisch (Regel 6).

## Betroffene Dateien im Harness

- `plugin/skills/todo/SKILL.md`, `plugin/skills/todo/format.md`
- `plugin/scripts/backlog.py`, `harness_config.py`, `session_start.py`,
  `mark_backlog_dirty.py`, `check_backlog.py`, neues API-Hilfsskript
- `plugin/skills/worktree/SKILL.md`, `plugin/templates/todo/`
- `docs/techdocs/configuration.md`, `docs/techdocs/interfaces.md`
