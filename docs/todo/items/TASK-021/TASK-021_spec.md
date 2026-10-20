# TASK-021 — Spec: Notes-Regeln und Format im todo-Skill

Grundlage: STORY-051_spec.md (Abschnitte Rollen der Dokumente, Wo und wie
protokolliert wird, Aufbau der Notes-Datei, Absicherung des Kopfs). Dieser
Task ändert nur Texte; Code kommt in TASK-022 bis TASK-025.

## Umfang

- `plugin/skills/todo/SKILL.md`, Working rules:
  - Ort, Inhalt, Zeitpunkt des Protokollierens (Regeln 1–3).
  - Rollen: Notes = Weg zur Entscheidung, Spec = immer aktueller Stand,
    fortlaufend aktualisiert; Umsetzungsplan entsteht beim Start, wird nicht
    gespeichert.
  - Nach jeder Änderung der Notes Kopf anpassen oder bewusst bestätigen;
    Stempel nie von Hand schreiben.
  - Lesereihenfolge: zuerst Kopf und Spec, Protokoll nur bei Bedarf.
- `plugin/skills/todo/format.md`, Item files:
  - Aufbau der Notes-Datei (Titel, `## Stand` mit fester Reihenfolge,
    Stempelzeile, Protokoll) mit Beispiel.
  - Regeln für den Kopf (ein Punkt pro Zeile mit Datum, nur Geltendes,
    Technisches als Verweis auf die Spec, Hinweis ab 15 Beschlüssen).
  - Protokoll nur anhängen; erledigte Open-Punkte ausdrücklich schließen.
  - Definition der Prüfsumme (gemeinsamer Vertrag mit dem ToDo-Viewer):
    SHA-256 über das Protokoll in kanonischer Form, erste 12 Hex-Zeichen;
    kanonische Form exakt beschreiben (ab erster Zeile `## YYYY-MM-DD — `,
    LF, ohne Leerzeichen am Zeilenende, genau ein abschließender
    Zeilenumbruch).
  - Zustände des Kopfs: `current`, `stale`, `missing`.
  - Spec-Beschreibung: "immer der aktuelle Stand" ergänzen.
- `plugin/skills/todo/api.md`: nur ein Satz, dass Kopf-Befehle mit TASK-023
  kommen; die Befehle selbst beschreibt TASK-023.
- `plugin/skills/decomposition/SKILL.md` "Where the plan lives": prüfen, ob
  ein Satz nötig ist (Plan wird nicht im Backlog gespeichert).
- Sprache der Skills: Englisch, wie die vorhandenen Texte.

## Nicht in diesem Task

Helfer, Prüfung, Hooks, ToDo-Viewer.

## Abnahme

- Texte decken alle Beschlüsse der Story-Spec zu Regeln und Format ab.
- Kanonische Form der Prüfsumme ist so beschrieben, dass zwei unabhängige
  Umsetzungen dasselbe Ergebnis liefern.
- Bestehende Tests laufen (`python3 -m unittest discover -s tests/implementation -t tests`).
- techdocs/semver nach den Regeln des Projekts behandelt.
