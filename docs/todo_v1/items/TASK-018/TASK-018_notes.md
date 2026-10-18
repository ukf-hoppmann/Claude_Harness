# TASK-018 — todo-Skill: Lücken beim Wiedereröffnen und bei geschlossenen Parents

## 2026-09-28 — Anlass

### Discussed

- Beim Anlegen von STORY-037 hat der Server ein optionales Kind unter dem abgeschlossenen EPIC-004 abgelehnt (HTTP 409 children_still_active). format.md:124 schließt nur neue Pflicht-Kinder aus.
- Der Agent hat die Story daraufhin ohne Parent angelegt und erst danach gefragt, ob er EPIC-004 wieder öffnen soll. SKILL.md verlangt, das Wiedereröffnen vorzuschlagen, sagt aber nicht, dass die Frage vor dem Anlegen kommt.
- Das Wiedereröffnen läuft über update mit status Open. api.md erwähnt das nicht.

### Open

- Wird format.md an den Server angepasst oder der Server an format.md?

## 2026-09-29 — Entscheidung: format.md folgt dem Server

### Discussed

- Der ToDo-Viewer hat mit seiner STORY-017 nachgezogen: Unter einem geschlossenen Parent (Completed/Rejected) darf kein aktives Item stehen (Anlegen, Umhängen, Wiederöffnen eines Kindes, Wiederherstellen aus dem Papierkorb). Der Server antwortet dann mit 409 parent_closed; details.items nennt die geschlossenen Vorfahren von oben nach unten. children_still_active gilt nur noch beim Schließen eines Parents mit aktiven Kindern.
- Wiedereröffnen läuft über update mit einem Status ohne Endstatus (z. B. In progress), auch für archivierte Items; Resolution entfällt dabei.

### Decided

- format.md wird an den Server angepasst, nicht umgekehrt.
- api.md beschreibt das Wiedereröffnen und den Fehler parent_closed.
- SKILL.md: Die Frage nach dem Wiedereröffnen kommt vor dem Anlegen; bei parent_closed fragt der Agent in einer Rückfrage nach allen genannten Vorfahren und legt das Item nie ohne Parent an.
