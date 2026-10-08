# STORY-040 — Skill notes: Regeln für Notes und Topics

## 2026-10-06 — Planung

### Discussed

- Abgrenzung Note, Backlog-Eintrag und Wecker; der Zeitaspekt ist der Marker.

### Decided

- Claude prüft und meldet Fälliges nicht von selbst; er liest es nur auf Zuruf.
- Mehrdeutige Zeitangaben wie früh werden immer geklärt.

### Open

- api.md folgt dem Helfer aus STORY-039.

## 2026-10-08 — Umsetzung

### Discussed

- SKILL.md und api.md geschrieben, Befehle stimmen mit notes_api.py überein.

### Decided

- Zeitauflösung mit lokaler Zeitzone als ISO 8601 mit Offset; mehrdeutige Angaben werden erfragt.

### Open

- Die Probe mit echten Notes (Erkennung, Anlegen, Bestätigung des Zeitpunkts, Lesen über den Index) steht aus, solange nichts in den Viewer geschrieben wurde. Nach der Abnahme von STORY-039 sinnvoll.

## 2026-10-08 — Probe mit echter Note

### Discussed

- NOTE-001 gegen den laufenden Viewer: anlegen, Zeitauslöser (lokale Zeit mit Offset), Link auf STORY-040, Index und --linked-item, Auslöser in der Vergangenheit (Status due, Grund trigger, im Fälligkeits-Index), Zurückstellen mit neuem Auslöser ersetzt die alten, Notizen-Eintrag, version_conflict mit alter Version, Erledigen (Archiv).

### Decided

- Probe bestanden; die Testnote NOTE-001 ist erledigt und archiviert.

### Open

- Topics und Sprint-Ablauf (topic_due) wurden nicht gegen den echten Server geprüft.

## 2026-10-08 — Probe mit Test-Topic

### Discussed

- TOPIC-001 mit Termin, NOTE-002 darin mit Auslöser topic_due; Termin in die Vergangenheit gesetzt: Note wird due mit Grund topic_due, auch im Topic-Index (Due: yes); neuer Termin (topic-update) und snooze mit neuem topic_due-Auslöser: Note snoozed, Topic nicht mehr fällig; Löschen eines Topics mit Inhalt ohne --cascade: 409 topic_has_content, mit --cascade in den Papierkorb samt Note.

### Decided

- Sprint-Ablauf aus dem Skill (erst Topic-Termin setzen, dann jede Note mit neuem topic_due zurückstellen) funktioniert gegen den echten Server.
