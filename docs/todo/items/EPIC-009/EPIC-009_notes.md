# EPIC-009 — Notes und Topics: Erinnerungen neben dem Backlog

## 2026-10-06 — Umfang und Entscheidungen mit dem Besitzer

### Discussed

- Quelle ist der Prompt `docs/notes-harness-prompt.md` im ToDo-Viewer-Repo; der Viewer baut die Technik (dort EPIC-005), der Harness die Regeln.
- Konflikt mit Architekturregel 2 (Hooks ohne Netzwerk): entfällt, weil kein automatischer Trigger kommt.
- Kurzfristige Erinnerungen (Minuten bis Stunden) sind keine Notes, sondern Wecker innerhalb der Session; längerfristige sind Notes.

### Decided

- Kein automatischer Hinweis auf Fälliges, weder per Hook noch beim Session-Start. Der Besitzer sieht die Markierung im Viewer oder fordert Claude auf, nach Fälligem zu sehen.
- Claude prüft Fälligkeiten nie; das ist allein Sache des Viewers.
- Befugnisse: anlegen, ändern, Links setzen, zurückstellen, erledigen frei; verwerfen und befördern nur nach Rückfrage; endgültig löschen nie.
- Erkennung: eindeutige Notes legt Claude an, bei Zweifel fragt er; der Zeitaspekt ist der Marker (Wecker oder Note).
- Relative Zeitangaben löst Claude auf und nennt den Zeitpunkt zur Bestätigung; bei Unklarheit (z. B. früh: 6 Uhr oder 9 Uhr) fragt er nach. Keine feste Uhrzeit in der Config.
- Prüf-Datum: der Standard (30 Tage) des Viewers gilt; Claude ändert ihn nur auf ausdrücklichen Wunsch. Kein Config-Schlüssel dafür.
- Sprint-Merker: läuft der Termin eines Topics ab, fragt Claude nach dem nächsten Termin und setzt ihn nach Bestätigung.
- Config: nur `[modules].notes`; Session-Start: eine statische Zeile; sonst kein Hook.
- Notes kommen nicht in den Tagesbericht; die Techdocs verweisen für das Notes-Modell auf die Viewer-Doku.
- Notes sind privat, solange sie nur in der Datenbank liegen; der Skill hält das ausdrücklich fest.

### Open

- Genaue API-Befehle, Felder und Index-Format: kommen mit der API des Viewers; STORY-039 und STORY-040 beginnen erst danach.
- STORY-038 (Config und Session-Start) hängt nicht von der API ab und kann sofort umgesetzt werden.
- Wie der Viewer Notes dem Projekt zuordnet: wie beim Backlog über die Config des Projekts (Quelle aus `todo.path`); Details legt der Viewer fest.
