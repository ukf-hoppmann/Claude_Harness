# STORY-024 — Notizen

## 2026-09-24 — Zuschnitt der Tasks

### Discussed

- Ein eigenes Verify-Skript mit Testebenen würde vorhandene Build-Werkzeuge
  (`make test`, `npm test`) nachbauen.
- Die ganze Suite muss nicht nach jeder Änderung laufen. Der Testumfang
  richtet sich nach dem Risiko der Änderung (z. B. Persistenz ja, triviale
  Rechnung nein). Der alte Harness ist hier teils übers Ziel hinausgeschossen.
- TDD überschneidet sich mit der Decomposition-Skill („Testable alone“,
  „Integrable alone“): Die legt fest, *dass* jeder Abschnitt einen Test hat,
  nicht *wann* der Test vor dem Code entsteht.

### Decided

- STORY-015 (Verifikations-Nachweis-Format) ist abgelehnt.
- TDD wird integriert, soweit sinnvoll.

### Open

- Zuschnitt von TASK-005 und TASK-006 (Testumfang nach Kontext statt
  „alle Ebenen“).

## 2026-09-24 — Umbenennung der Task-IDs

### Decided

- Einmalige Ausnahme von der Regel „IDs ändern sich nie“ (`format.md`),
  vom Projektverantwortlichen erteilt: Tasks mit `STORY-`-ID heißen jetzt
  STORY-006 → TASK-002, STORY-007 → TASK-003, STORY-008 → TASK-004,
  STORY-010 → TASK-005, STORY-011 → TASK-006. Alle Verweise wurden
  angepasst. Das archivierte STORY-015 behält seine ID.

## 2026-09-24 — TDD (TASK-005)

### Decided

- TDD kommt als Abschnitt „Test first“ in die Skill
  `claude-harness:decomposition`: Bugfix und neues Verhalten mit klarer
  Schnittstelle → Test zuerst; Refactoring → Tests unverändert grün;
  Konfiguration, Doku, Prototypen, UI-Feinschliff → kein Test zuerst.
- Keine Dokumentation zu den Tests oder zum Rot-Grün-Zyklus. Der Test selbst
  ist das Ergebnis.

## 2026-09-24 — Testumfang (TASK-006)

### Discussed

- Der Agent testet meist schon, was betroffen sein kann. Schwächen:
  indirekt betroffene Tests übersehen, teure Suiten still weglassen, nach
  dem letzten kleinen Fix nicht erneut testen, rote Tests vorschnell als
  „schon vorher kaputt“ abtun.

### Decided

- Diese Punkte stehen als Abschnitt „Running tests“ in der Skill
  `claude-harness:decomposition`. Kein eigenes Verify-Skript.

### Open

- Ob TASK-006 darauf reduziert oder abgelehnt wird (Konfigurationseintrag
  für Testbefehle erst, wenn ein Projekt ihn braucht).

## 2026-09-24 — Abschluss

### Decided

- Ziel und Abschlusskriterium auf „Test zuerst und Testumfang“ angepasst
  (Verify-Kommando entfällt, Nachweis abgelehnt); vom
  Projektverantwortlichen als erledigt bestätigt.
