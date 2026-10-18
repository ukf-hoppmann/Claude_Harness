# Spec: Skill notes

## Was und warum

Der Skill ist der einzige Ort, an dem Claude die Regeln für Notes lernt. Er
wird nur geladen, wenn es um Merken, Erinnern oder Fälliges geht (Ladestufe
Skill, Architekturregel 9).

## Aufbau

- `plugin/skills/notes/SKILL.md`: Beschreibung in einem Satz ohne Regeln
  (wann laden). Abschnitte: Vor dem Start (Config lesen, Modul `notes` an;
  Texte in `[docs].language`; Server nicht erreichbar: nachfragen, kein
  Ausweichen), Erkennung, Befugnisse, Lesereihenfolge, Zeitangaben, Fälligkeit,
  Sprint-Merker, Umwandlung, Privatsphäre.
- `plugin/skills/notes/api.md`: Befehle des Helfers (aus STORY-039), Fehler,
  Beispiele.
- Inhalt der Regeln: siehe Spec von EPIC-009, Punkte 2 bis 11. Nicht
  verändern, nur ausformulieren.

## Hinweise zur Formulierung

- Englisch, knapp, keine Wiederholung der Regeln des todo-Skills; wo beide
  gelten, kurz auf `claude-harness:todo` verweisen.
- Beispiele für Erkennung: "merke für den nächsten Sprint" (Note im
  Sprint-Topic), "erinnere mich in 10 Minuten" (Wecker), "erinnere mich
  in drei Wochen an X" (Note mit Zeitpunkt), "prüfe die Performance, wenn die
  DB voll wird" (Note ohne Auslöser, Wiedervorlage).
- Zeitauflösung: Claude nennt den festen Zeitpunkt mit Datum und Uhrzeit zur
  Bestätigung; mehrdeutige Angaben ("früh", "abends") immer klären.
- Der Skill sagt ausdrücklich: Claude prüft keine Fälligkeit und meldet sie
  nicht von selbst.

## Abnahme

Siehe Abnahmekriterien der Story; zusätzlich Lesen des Skills aus Sicht eines
Modells, das den Rest des Harness nicht kennt: Jede Regel ist ohne
Rückfrage anwendbar.
