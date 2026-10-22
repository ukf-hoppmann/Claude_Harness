# STORY-043 — Notes und Topics im Dateimodus führen

## State

- Goal/Status: Notes und Topics im Dateimodus führen. Umgesetzt und getestet, wartet auf Bestätigung.
- Next step: Owner bestätigt; danach STORY-044 (Formatprüfung) oder STORY-045 (Ablauf).
- Open:
  - Sync mit dem echten Viewer nicht geprüft (new-Dateien, topics.md, Deleted)
- Decided:
  - Story gestartet, STORY-042 und STORY-047 bestätigt (2026-10-22)
  - Dateiformat Version 2 des Viewer-Neubaus gilt, alte Fassung verworfen (2026-10-22)
  - alarms.md nicht in dieser Story (2026-10-22)
  - Kriterien 2 und 4 und das Ziel auf Version 2 umgestellt (2026-10-22)
  - Keine Tasks, eine Sitzung (2026-10-22)
  - Umgesetzt: notes_enabled bei jedem Backend, viewer_notes_enabled für die API-Helfer, notes_files.py, notes-files.md, Doku (2026-10-22)
- References: Spec STORY-043_spec.md; Viewer-Techdoc docs/techdocs/interfaces.md (Dateiformat Version 2); EPIC-010; STORY-044 und STORY-045 für Formatprüfung und Ablauf

State confirmed after entry 2026-10-22 — Umsetzung (977fe1df9f84)

## 2026-10-22 — Ausgangslage: Dateiformat und Umfang prüfen

### Discussed

- STORY-042 und STORY-047 sind bestätigt; STORY-043 gestartet (In progress). Es gibt noch keine Notes und keine Spec.
- Ist-Stand im Harness: notes_enabled() ist nur bei Backend api wahr; notes.md und alarms.md gelten ausdrücklich nur für api. In der Cloud (files) sind Notes also aus, session_start schweigt dazu. Für Notes im Dateimodus gibt es weder Regeln noch einen Index-Helfer.
- Das Dateiformat steht in der Techdoc des ToDo-Viewers (interfaces.md). Dort gibt es zwei Fassungen: das Notes-Format des alten Viewers (Abschnitt 'Dateiformat: Notes-Ordner', mit counters.md und Zeit-Auslösern an Notes) und Version 2 des Neubaus (Uid im Kopf, keine counters.md, Zeit-Auslöser entfallen und werden Wecker in alarms.md; nur event und topic_due bleiben; eine time-Zeile ist dort ein Fehler unknown_trigger).
- Die Abschlusskriterien 2 und 4 der Story stammen vom 2026-10-16 und beschreiben die alte Fassung (counters.md, Zeit-Auslöser, Fälligkeit über Review-Datum und Zeit-Auslöser). Der Harness spricht inzwischen mit dem Neubau (Felder uid und notes_state in den API-Antworten), also gilt wohl Version 2.

### Open

- Welche Fassung des Dateiformats gilt für die Regeln: Version 2 (Neubau) oder die alte? Folge für Kriterien 2 und 4.
- Gehört die Datei alarms.md (Wecker im Dateimodus) in diese Story oder in eine eigene?
- Zerlegung: Passt die Story in eine Sitzung, oder braucht sie Tasks (Regeln und Format, Index-Helfer, Config und Sitzungsstart, Doku)?

## 2026-10-22 — Entscheidung: Format Version 2, Wecker ausgeklammert

### Discussed

- Frage 1, Formatfassung: Version 2 des Neubaus (passt zum Viewer, mit dem der Harness jetzt spricht; keine counters.md, keine Zeit-Auslöser an Notes) gegen die alte Fassung (wie in den Kriterien vom 16.10.).
- Frage 2, Wecker: alarms.md in diese Story aufnehmen oder getrennt führen. Dafür spricht der Zusammenhang mit Fälligkeit; dagegen wächst die Story über Notes und Topics (ihren Titel) hinaus.

### Decided

- Format Version 2 (Neubau) ist maßgeblich; die alte Fassung ist verworfen, weil der Harness bereits gegen den Neubau arbeitet und die alten Zeit-Auslöser dort entfallen (Owner, 2026-10-22).
- alarms.md bleibt außerhalb dieser Story; falls nötig kommt später ein eigenes Item (Owner, 2026-10-22).

### Open

- Kriterien 2 und 4 sowie der Verweis im Ziel müssen auf Version 2 umgestellt werden (counters.md und Zeit-Auslöser streichen, Uid und Wecker erwähnen); Wortlaut dem Owner vorlegen.
- Zerlegung: Vorschlag keine Tasks (eine Sitzung: Config und Sitzungsstart, Regeldatei, Index-Helfer mit Tests, Doku); wartet auf den Owner.

## 2026-10-22 — Kriterien auf Version 2 umgestellt, Spec geschrieben

### Discussed

- Vorschlag: Kriterium 2 ohne counters.md, mit Uid und der Regel, dass nur event und topic_due als Auslöser gelten; Kriterium 4 nur noch Review und Topic-Datum, Zeitpunkte sind Wecker. Das Ziel verweist auf Dateiformat Version 2.
- Zerlegung: Config und Sitzungsstart, Regeldatei, Index-Helfer mit Tests und Doku passen in eine Sitzung; Tasks würden nur Plan-Abschnitte abspalten.

### Decided

- Kriterien 2 und 4 und das Ziel sind wie vorgeschlagen geändert (Owner, 2026-10-22).
- Keine Tasks; die Story wird in einer Sitzung umgesetzt, die Abschnitte stehen im Plan (Owner, 2026-10-22).
- Spec STORY-043_spec.md geschrieben: Notes bei jedem Backend aktiv, neue Regeldatei notes-files.md, Index-Helfer notes_files.py (--index, --due, --today), Wecker, Formatprüfung und Ablauf ausgeklammert.

## 2026-10-22 — Umsetzung

### Discussed

- Plan vom Owner freigegeben; Umsetzung im Worktree story-043-notes-dateimodus in fünf Commits, Tests jeweils vorweg (520 Tests grün, vorher 468 plus neue).
- notes_enabled() gilt jetzt bei jedem Backend; neu viewer_notes_enabled() (nur api) schützt notes_api.py und alarms_api.py. Der Sitzungsstart nennt im Dateimodus 'Notes: <todo.path>/notes/ as files'.
- Abweichung vom Plan: Im Mehrprojekt-Test kommt der Skill todo jetzt zweimal vor (Backlog-Zeile und Notes-Zeile), weil Notes auch bei files aktiv sind; der Test erwartet das ausdrücklich.
- notes_files.py (--index, --due, --today) liest nur Kopfzeilen, löst Topics über topics.md auf, lässt Papierkorb und Archiv weg und wertet event-Auslöser nicht aus. Namen mit '|' bleiben mit Escape stehen, damit eine Zeile eine Zeile bleibt.
- Neue Regeldatei plugin/skills/todo/notes-files.md (Format Version 2, Befugnis, Datenschutzhinweis, Lesereihenfolge); notes.md verweist im Dateimodus dorthin. Techdocs (architecture, interfaces, configuration) und README angepasst; ein Test sichert, dass Helfer und Regeldatei in der Cloud-Kopie landen.
- Handlauf in einem Temp-Projekt mit CLAUDE_CODE_REMOTE=true: Sitzungsstart zeigt die Notes-Zeile, Index und --due liefern die Fixture, notes_api.py meldet weiter 'need api' (Exit 2). Nicht geprüft: eine echte Cloud-Sitzung und der Sync der Dateien mit dem Viewer.

### Decided

- Kriterien 1 bis 6 sind erfüllt; Status Awaiting confirmation, Bestätigung durch den Owner offen.

### Open

- Ob der Viewer-Sync die von der KI geschriebenen Dateien (new-<name>.md, topics.md) annimmt, ist nicht gegen einen echten Sync geprüft; die Formatprüfung ist STORY-044.
- Ein 'Deleted:'-Zeitpunkt, von der KI in eine Note geschrieben, ist im Format vorgesehen, aber ungetestet gegen den Viewer.
