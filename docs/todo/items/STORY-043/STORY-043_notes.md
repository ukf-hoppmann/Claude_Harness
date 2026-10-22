# STORY-043 — Notes und Topics im Dateimodus führen

## State

- Ziel/Status: Notes und Topics im Dateimodus führen (Regeln, Index-Helfer, Config). In Arbeit; Klärung abgeschlossen, Spec auf aktuellem Stand.
- Nächster Schritt: Umsetzungsplan vorlegen und vom Owner freigeben lassen.
- Offen:
  - nichts
- Beschlossen:
  - Story gestartet, STORY-042 und STORY-047 bestätigt (2026-10-22)
  - Dateiformat Version 2 des Viewer-Neubaus gilt, alte Fassung verworfen (2026-10-22)
  - alarms.md nicht in dieser Story (2026-10-22)
  - Kriterien 2 und 4 und das Ziel auf Version 2 umgestellt (2026-10-22)
  - Keine Tasks, eine Sitzung (2026-10-22)
- Verweise: Spec STORY-043_spec.md; Viewer-Techdoc docs/techdocs/interfaces.md (Dateiformat Version 2); EPIC-010; STORY-044 und STORY-045 für Formatprüfung und Ablauf

State confirmed after entry 2026-10-22 — Kriterien auf Version 2 umgestellt, Spec geschrieben (07f07953de9e)

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
