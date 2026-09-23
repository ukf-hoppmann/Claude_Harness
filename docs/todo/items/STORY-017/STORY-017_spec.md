# STORY-017 — Spec: Aufbau des Backlogs

## Ziel

Ein Backlog-Standard, an dem sich jeder neue Eintrag ohne Rückfrage
orientieren kann und der die AI nur so viel lesen lässt, wie die Aufgabe
erfordert.

## Struktur

```
docs/todo/                  ← später konfigurierbar (EPIC-001)
 ├─ TODO.md                 ← Hauptliste, Standard-Arbeitsgrundlage
 └─ items/
     └─ <ID>/               ← nur bei Bedarf, Name = exakte ID
         ├─ <ID>_notes.md   ← Besprechungen, Entscheidungen, datiert
         └─ <ID>_spec.md    ← technische Zusammenfassung
```

## Eintragsformat

Übernommen aus Agent_Harness-Format v2:

- IDs: `EPIC-NNN`, `STORY-NNN`, `TASK-NNN`; stabil, ändern sich nie.
- Pflichtfelder: `Type`, `Status`, `Created`, `Area`, `Priority`,
  `Dependencies`, `Goal`, `Completion criteria`.
- Story/Task zusätzlich `Parent` (oder `None`), bei gesetztem Parent
  `Required for parent` (`Yes`/`No`).
- `Resolution` genau dann, wenn Status `Completed` oder `Rejected`.

Neu in Claude_Harness (optional):

- `Summary`: nicht-technische Kurzfassung für den Projekteigner. Pflicht,
  sobald das Item `Notes` hat.
- `Notes`, `Spec`: relativer Pfad ab `TODO.md`; nur wenn die Datei existiert.
  Vorerst ein Pfad, später kommagetrennt mehrere.

## Regeln

- Hierarchie: Story → Epic; Task → Story oder Epic; Epic ohne Parent.
- Parent- und Dependency-Graph sind zyklenfrei.
- Status: `Open` → `In progress` → `Awaiting confirmation` → `Completed`
  bzw. `Rejected`. `Completed` und `Rejected` nur durch ausdrückliche
  Entscheidung des Projekteigners.
- Parent nicht `Awaiting confirmation`/`Completed`, solange ein required
  Child offen ist; ein Reject des Parents reißt Children nicht mit.
- Statuswechsel ändern nur das Feld `Status`, nicht die Position im Dokument.

## Item-Dateien

- Notes: eine mitwachsende Datei, Einträge mit Datum und den Abschnitten
  Besprochen / Beschlossen / Offen.
- Spec: was und warum, Rahmenbedingungen, Schnittstellen, betroffene Dateien,
  Abnahmekriterien. Keine Schrittfolge; die entsteht im Plan Mode.
- Weitere Dateien nur per Themen-Suffix (`<ID>_spec_<thema>.md`).

## Lesereihenfolge für die AI

1. Standard: nur `TODO.md`.
2. Besprechung oder Entscheidung zu einem Item: zusätzlich dessen Notes.
3. Umsetzungsplanung oder Nachfrage: zusätzlich dessen Spec.

## Nicht übernommen

- Jede Kompatibilität zu Agent_Harness-Formaten. Dies ist Claude_Harness
  Backlog-Format Version 1.
- Kopplung an einen Python-Renderer, der Regeln in `CLAUDE.md` einbaut.

## Betroffene Dateien

- `docs/todo/TODO.md` (Formatbeschreibung und Einträge)
- später (`STORY-020`): `todo`-Skill im Plugin, Hook-Skript zur Formatprüfung

## Abnahmekriterien

- Die Formatbeschreibung in `TODO.md` deckt alle Punkte dieser Spec ab.
- Mindestens ein Item nutzt `Summary`, `Notes` und `Spec` korrekt.
- Ein neuer Eintrag lässt sich allein anhand der Formatbeschreibung anlegen.
