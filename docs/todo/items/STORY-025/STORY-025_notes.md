# STORY-025 — Notes

## 2026-09-24 — Auslegung und Grundhaltung

### Discussed

- Erste Auslegung (zu eng): nur die Regeldateien der Suite `development` und
  ein Hook-Hinweis bei direkten Änderungen daran. Der Projektverantwortliche
  meint etwas Breiteres:
  1. Eine Architektur wird gestaltet, die nicht zur dokumentierten passt.
  2. Der Projektverantwortliche möchte etwas, das der Harness (das Plugin
     selbst) nicht erlaubt oder anders festlegt.

### Decided

- Bei einem Konflikt handelt die AI nicht selbst. Sie macht den
  Projektverantwortlichen darauf aufmerksam, erklärt kurz den Konflikt und
  schlägt, wenn möglich, Lösungen vor.
- Regeln sind Leitlinien. Wünscht der Projektverantwortliche nach der
  Benennung des Konflikts eine Ausnahme, folgt die AI dem. Es gibt keine
  Unterscheidung zwischen Einzelausnahme und Regeländerung als Pflicht.
- Eine einmalige Ausnahme wird nicht eigens dokumentiert, höchstens im
  Tagesbericht.
- Soll eine Harness-Vorgabe dauerhaft anders werden, schlägt die AI das vor;
  nach Rücksprache wird es als Backlog-Notiz im Harness aufgenommen.

## 2026-09-24 — Plugin-Vorgaben, Festhalten, Autonomie

### Discussed

- Plugin-Vorgaben (Skills, Hooks unter `plugin/`) lassen sich in einem
  anderen Projekt nicht ändern; mechanische Sperren durch Hooks kann die AI
  nicht umgehen.
- Wunsch nach einer Harness-Änderung aus einem anderen Projekt: Die AI dort
  kennt den Harness-Backlog nicht. Idee des Projektverantwortlichen: die
  Aufgabe an einen neuen Chat im Projekt Claude_Harness delegieren, der den
  Backlog ergänzt (saubere Trennung).

### Decided

- Einmalige Ausnahmen werden nicht festgehalten, auch wenn sie im Code
  sichtbar bleiben; meist ändert der Projektverantwortliche die Regel ohnehin.
  Probleme mit dem Harness spricht die AI an.
- Die AI erhält eine kleine Autonomie (Umfang noch festzulegen).

### Open

- Umfang der Autonomie.
- Wie die Übergabe an eine Session im Harness-Projekt technisch geht und
  woher der Pfad zum Harness-Repo kommt.
- Goal und Completion criteria an die breitere Auslegung anpassen
  (Freigabe nötig).
