# TASK-018 — todo-Skill: Lücken beim Wiedereröffnen und bei geschlossenen Parents

## 2026-09-28 — Anlass

### Discussed

- Beim Anlegen von STORY-037 hat der Server ein optionales Kind unter dem abgeschlossenen EPIC-004 abgelehnt (HTTP 409 children_still_active). format.md:124 schließt nur neue Pflicht-Kinder aus.
- Der Agent hat die Story daraufhin ohne Parent angelegt und erst danach gefragt, ob er EPIC-004 wieder öffnen soll. SKILL.md verlangt, das Wiedereröffnen vorzuschlagen, sagt aber nicht, dass die Frage vor dem Anlegen kommt.
- Das Wiedereröffnen läuft über update mit status Open. api.md erwähnt das nicht.

### Open

- Wird format.md an den Server angepasst oder der Server an format.md?
