# TASK-023 — Spec: Kopf-Befehle im API-Helfer

Grundlage: STORY-051_spec.md (Schnittstelle zum ToDo-Viewer, Umstellung).
Der ToDo-Viewer hat die Erweiterung seit v0.8.14 (dort TASK-044); maßgeblich
ist seine `docs/techdocs/interfaces.md`, Abschnitt Backlog/Notes.
Voraussetzung ist zusätzlich die Viewer-Version mit den englischen
Überschriften (`## State`, `- Decided:`, `State confirmed after entry …`,
Beschluss vom 2026-10-21).

## Schnittstelle des Viewers (Stand v0.8.14)

- `GET /backlog/items/{ref}/notes/state` → `content`, `stamp`, `state`
  (`current`/`stale`/`missing`), `checksum`, `last_entry`, `version` (des
  Kopfs), `hints`.
- `PUT …/notes/state` mit `content`, `version`: ersetzt und stempelt.
- `POST …/notes/state/confirm` mit `version`: nur der Stempel zieht nach.
- `GET …/notes/entries` optional `last` → `{position, day, topic, text}`.
- `POST …/notes` optional `state` (neuer Kopf) und `state_version`, wenn es
  schon einen Kopf gibt; Antwort mit `notes_state` und `hints`.
- `show`/`list` tragen `notes_state`; `index` hat die Spalte `Notes`.
- Hinweise `hints: [{code, message}]`: `notes_state_stale`,
  `notes_state_long`, `notes_history_rewritten`; nie eine Ablehnung.
- Fehler: `notes_not_found`, `notes_state_missing`, `notes_without_entries`.
- Eine Stempelzeile im gesendeten Text zählt nicht; den Stempel setzt nur der
  Server. Ohne Protokolleintrag gibt es keinen Stempel.

## Umfang

- `plugin/scripts/backlog_api.py` neue Befehle:
  - `state <ID>`: Kopf, Zustand, Stempel und Version lesen, ohne Protokoll.
  - `put-state <ID> <version>`: Kopf ersetzen (Text von stdin).
  - `confirm-state <ID> <version>`: Kopf unverändert bestätigen.
  - `entries <ID> [--last N]`: die letzten N Protokolleinträge.
  - `note <ID>`: optionale Felder `state` und `state_version` durchreichen.
  - Bei allen schreibenden Notes-Befehlen (`note`, `put-doc` auf Notes,
    `put-state`, `confirm-state`) die `hints` des Servers sichtbar ausgeben
    (stderr, eine Zeile je Hinweis), zusätzlich zur JSON-Ausgabe.
- Fähigkeitsprüfung: Der Viewer meldet keine Version (`/core/health` liefert
  nur `status`). Unterstützung erkennen am Feld `notes_state` in `show` bzw.
  an einer 404 auf `…/notes/state`; ohne Unterstützung klare Meldung, alte
  Befehle unverändert.
- Session-State (`state.py`): Items merken, deren Notes in der Session über
  den Helfer geändert wurden, und aktive Items (auf `In progress` gesetzt
  oder Spec per `doc` gelesen), für TASK-024.
- `plugin/skills/todo/api.md`: Befehle, Hinweise und Spalte `Notes`
  beschreiben; Lesereihenfolge "zuerst `state`, Protokoll mit `entries` oder
  `doc` nur bei Bedarf".
- Testvektoren der Prüfsumme: Kopie von
  `ToDo_viewer/tests/fixtures/notes-state/checksum.json` in die Tests des
  Harness (mit Herkunftsangabe), genutzt von TASK-022.

## Abnahme

- Unit-Tests gegen einen Test-Server (wie die vorhandenen Tests des
  Helfers): alle Befehle, Versionen, Hinweise, Fähigkeitsprüfung,
  Session-State.
- Manuell gegen den laufenden Viewer geprüft (state, put-state,
  confirm-state, note mit state).
