# EPIC-004 – Notizen

## Summary
Legt fest, wie entwickelt wird: Architekturregeln, Zerlegung, Change-Ablauf
im Worktree, Tests und Versionierung. Ein eigenes Prinzipien-Dokument gehört
nicht mehr dazu.

## 2026-09-25 — STORY-009 verworfen

### Discussed
- STORY-009 (Entwicklungsprinzipien-Dokument) mit Agent_Harness
  (`rules/core/development.md`) verglichen. Die genannten Prinzipien (keine
  unnötigen Abstraktionen, keine spekulativen Features, kommentarsparsam,
  fremde Arbeit erhalten) sind natives Verhalten von Claude. Ein Dokument
  dazu würde nur Tokens kosten.
- Projektspezifische Regeln landen ohnehin als Abschnitte in
  `docs/development/architecture.md` (siehe Secrets, Pfade).

### Decided
- Der Owner hat STORY-009 verworfen. Goal und Completion criteria von
  EPIC-004 sind angepasst: „Entwicklungsprinzipien“ wurde gestrichen.
- Neues Pflicht-Kind STORY-029 (SemVer-Versionierung) angelegt.

## 2026-09-25 — Abschluss

### Decided
- STORY-009 steht jetzt auf `Required for parent: No`. Das folgt aus der
  Owner-Entscheidung vom selben Tag, Goal und Completion criteria ohne
  Prinzipien-Dokument zu fassen. Das Feld war dabei stehen geblieben und
  hätte den Abschluss blockiert.
- Der Owner hat den Abschluss von STORY-029 und EPIC-004 vorab erlaubt,
  sobald sie fertig sind. Die Kriterien des Epics wurden im Change zu
  STORY-029 angewendet: Architekturregeln gelesen, Plan in Abschnitten mit
  Tests zuerst, Worktree-Ablauf, volle Testsuite. Danach folgt der erste
  Release-Tag `v0.1.0`.

## 2026-09-28 — Wiedereröffnet für STORY-037

### Discussed

- STORY-037 (Testkonventionen) gehört fachlich zu diesem Epic; die Testebenen aus EPIC-004 wurden nie umgesetzt. Der ToDo-Viewer nimmt unter einem abgeschlossenen Parent kein aktives Kind an.

### Decided

- Auf Wunsch des Owners wieder auf In progress gesetzt und STORY-037 als optionales Kind (Required for parent: No) eingehängt.
- Das Epic kann wieder abgeschlossen werden, sobald STORY-037 geschlossen ist.

## 2026-09-29 — Alle Kinder abgeschlossen

### Discussed

- Mit STORY-037 sind alle Kinder abgeschlossen oder abgelehnt. Abschlusskriterien geprüft: Architektur-Definitionen (STORY-023), Zerlegungs-Heuristik (STORY-004/005), Change-Ablauf (STORY-022) und Testkommando (STORY-037, tests/README.md) sind dokumentiert und wurden beim Change zu STORY-037 sichtbar angewendet (Plan mit Abschnitten, Worktree, Test zuerst, Release v0.7.0).
- Das Ziel nennt die Testebenen Unit/Integration/System. Umgesetzt sind Unit und Integration als Implementierungstests sowie Funktionalitätstests des Owners; eine eigene Ebene System gibt es nicht. Die Abschlusskriterien verlangen sie nicht.

### Decided

- Epic auf Awaiting confirmation gesetzt.

### Open

- Owner bestätigt das Epic oder fordert eine eigene Ebene System nach.
