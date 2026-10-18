# TASK-014 — Notizen

## 2026-09-25 — Regel für abgelehnte Pflicht-Kinder

### Discussed

- Auslöser: `STORY-022` konnte nicht abgeschlossen werden, weil
  `TASK-001` bis `TASK-003` als Pflicht-Tasks abgelehnt waren. Ihr Inhalt
  war in der Spec aufgegangen.
- Varianten:
  - streng mit Hinweis
  - „abgelehnt zählt nicht“
  - beim Ablehnen automatisch optional

  Nur der Owner kann unterscheiden, ob der Inhalt anderswo aufgegangen ist
  oder dem Parent wirklich ein Teil seines Ziels fehlt.

### Decided

- Eine Mischung aus streng und automatisch, vom Owner gewählt:
  - Beim Ablehnen einer Pflicht-Aufgabe fragt die AI im selben Schritt:
    `Required for parent: No`, Ziel und Kriterien des Parents anpassen oder
    den Parent ablehnen. Die Antwort kommt in die Notes des Parents
    (Skill `todo`, `format.md`).
  - Sicherheitsnetz, z. B. für Statusänderungen in der UI: Das Prüfskript
    blockiert `Awaiting confirmation` und `Completed` bei abgelehnten
    Pflicht-Kindern weiter. Die Meldung nennt jetzt den Status jedes
    Kindes und die Rückfrage. Sind alle Pflicht-Kinder geschlossen, aber
    einige abgelehnt, erscheint schon vorher ein Hinweis.
- `format.md` beschreibt die Regel für `Awaiting confirmation` jetzt wie das
  Skript: Alle Pflicht-Kinder müssen `Awaiting confirmation` oder
  `Completed` sein.
