# TASK-025 — Spec: Nachfrage bei Notes an eine Story mit Kind in Arbeit

Grundlage: STORY-051_spec.md (Prüfidee A, Regel zum Ort).

## Umfang

- API-Modus, `backlog_api.py`: Bei `note` und bei `put-doc` auf die Notes
  einer Story (oder eines Epics) die Kinder prüfen (`show`); ist eines
  `In progress`, nach dem Schreiben einen Hinweis ausgeben: "TASK-x ist in
  Arbeit – gehört das dorthin? Ausnahmen sind erlaubt." Der Eintrag wird immer
  geschrieben.
- Files-Modus, `check_backlog.py`: gleicher Hinweis für in der Session
  geänderte Story-Notes; Hinweis, kein Fehler.
- Keine Prüfung bei Tasks.
- Doku: ein Satz in `api.md` bzw. `format.md`.

## Abnahme

- Unit-Tests: Story mit Kind in Arbeit (Hinweis), ohne (kein Hinweis), Task
  (kein Hinweis); Eintrag wird nie abgelehnt.
