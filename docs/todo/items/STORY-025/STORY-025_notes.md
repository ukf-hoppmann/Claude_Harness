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

## 2026-09-24 — Autonomie und Pfad zum Harness-Repo

### Discussed

- Eine eigene Autonomie-Regel wäre überflüssig: Eine regelkonforme Lösung,
  die das gewünschte Ergebnis nicht verändert, wählt die AI ohnehin; das ist
  kein Konflikt, sondern Umsetzung.
- Die Übergabe an eine Session im Harness-Projekt braucht dessen Pfad. Ein
  Rechnername als Schlüssel ist auf macOS unzuverlässig (`hostname` wechselt
  mit dem Netz).

### Decided

- Keine Autonomie-Regel. Stattdessen ein Satz, was als Konflikt gilt: eine
  Regel müsste gebrochen oder geändert werden, oder das Ergebnis ändert sich
  für den Projektverantwortlichen.
- Der Pfad steht in der Projekt-Config als Liste `[harness].repo`. Die AI
  nimmt den ersten Pfad, der auf dem Rechner existiert und wirklich das
  Harness-Repo ist; passt keiner, gibt es einen fertigen Text zum Mitnehmen.
  `init` schlägt den Pfad vor und ergänzt ihn auf weiteren Rechnern.

## 2026-09-24 — Spec freigegeben

### Decided

- Spec `STORY-025_spec.md` freigegeben: neuer Skill `conflicts`, Skript
  `harness_repo.py`, Config `[harness].repo`, Anpassung von Skill
  `architecture`, Vorlage und `architecture.md` dieses Repos.
- Kein Hinweis-Hook bei direkten Änderungen an Regeldateien:
  Regeländerungen folgen ohnehin einer Entscheidung im Chat.
- Goal und Completion criteria an die breitere Auslegung angepasst.

### Open

- Keine.

## 2026-09-24 — Umsetzung

### Discussed

- Umgesetzt nach Spec: Skill `conflicts`, Skript `harness_repo.py`,
  `[harness].repo` (Validierung, Doku, Tests), Verweise in Skill
  `architecture` und Vorlage, `init`, Config-Vorlage, Systemdoku, README.
  `harness.repo` in der Config dieses Repos gesetzt. 95 Tests grün.
- `architecture.md` dieses Repos, Abschnitt „Changing these rules“, an die
  neue Vorlage angepasst (mit der Spec freigegeben).
- Test mit `claude -p` in einem Wegwerfprojekt:
  1. Architekturkonflikt (`open()` außerhalb von `src/repository/`): Die
     Session hielt an, nannte Regel und Abschnitt, bot Ausnahme,
     regelkonforme Umsetzung und Regeländerung an und änderte nichts.
  2. Harness-Konflikt (Architekturregeln auf Deutsch, in allen Projekten):
     Die Session erkannte die Harness-Vorgabe, bot einmalige Ausnahme oder
     Harness-Änderung an. Nach der Wahl „Harness-Änderung“ fand sie über
     `harness_repo.py` das Repo (nicht existierender erster Eintrag
     übersprungen) und gab einen fertigen Befehl
     `cd <repo> && claude "…"` mit eigenständigem englischem Auftrag aus.

### Decided

- Die Completion criteria sind erfüllt; die Story wartet auf Bestätigung.
