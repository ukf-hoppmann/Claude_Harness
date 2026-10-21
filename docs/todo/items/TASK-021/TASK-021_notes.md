# TASK-021 — Notes-Regeln und Format im todo-Skill

## Stand

- Goal/Status: Regeln und Format der Notes im todo-Skill beschrieben; umgesetzt, wartet auf Bestätigung.
- Next step: Owner bestätigt; danach TASK-022, TASK-023, TASK-025.
- Open: nichts
- Decided:
  - Format der Notes in format.md (Abschnitt Notes) mit Beispiel und echter Prüfsumme; Prüfsummen-Beschreibung gegen die 8 Testvektoren des ToDo-Viewers geprüft (2026-10-21)
  - SKILL.md nennt noch keine Befehle für Kopf und Bestätigung; die kommen mit TASK-022 und TASK-023 (2026-10-21)
- References: Spec TASK-021_spec.md; Story STORY-051

Stand bestätigt nach Eintrag 2026-10-21 — Umsetzung (591fca3b79ec)

## 2026-10-21 — Umsetzung

### Discussed

- Plan vom Owner freigegeben; Umsetzung im Worktree TASK-021.
- format.md: Item files verweist auf den neuen Unterabschnitt Notes (Kopf ## State mit festen englischen Markern, Regeln für den Kopf, Stempelzeile, Zustände missing/stale/current, kanonische Form und Prüfsumme, Protokoll nur anhängen, alte Notes bekommen den Kopf beim nächsten Bearbeiten); Spec als immer aktueller Stand.
- SKILL.md: Lesereihenfolge (Kopf und Spec vor dem Protokoll); Regeln Where/What/When/Head; Spec aktuell halten, Plan nicht im Backlog.
- decomposition/SKILL.md: Plan wird nicht im Backlog gespeichert.
- Prüfsumme der Beschreibung gegen tests/fixtures/notes-state/checksum.json des Viewers nachgerechnet: 8 von 8 gleich. Das Beispiel in format.md hat eine echte Prüfsumme (1ddbc455ee9d).
- Techdocs: Das Notes-Format steht dort nicht; interfaces.md ändert sich erst mit TASK-023.
- Tests: 441 OK.

### Decided

- Befehle für Kopf und Bestätigung bleiben aus SKILL.md heraus, bis TASK-022 und TASK-023 sie bauen, damit dieses Repo (nutzt sein eigenes Plugin) nicht auf fehlende Befehle verweist.
