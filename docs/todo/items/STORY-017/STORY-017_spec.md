# STORY-017 — Spec: Aufbau des Backlogs

## Goal

Ein Backlog-Standard, an dem sich jeder neue Eintrag ohne Rückfrage
orientieren kann und der die AI nur so viel lesen lässt, wie die Aufgabe
erfordert.

## Structure

```
docs/todo/                  ← später konfigurierbar (EPIC-001)
 ├─ TODO.md                 ← aktive Einträge, Standard-Arbeitsgrundlage
 ├─ archive.md              ← Completed/Rejected, nur bei Bedarf gelesen
 └─ items/
     └─ <ID>/               ← nur bei Bedarf, Name = exakte ID
         ├─ <ID>_notes.md   ← Besprechungen, Entscheidungen, datiert
         └─ <ID>_spec.md    ← technische Zusammenfassung
```

## Entry format

Übernommen aus Agent_Harness-Format v2:

- IDs: `EPIC-NNN`, `STORY-NNN`, `TASK-NNN`; stabil, ändern sich nie.
- Pflichtfelder: `Type`, `Status`, `Created`, `Area`, `Priority`,
  `Dependencies`, `Goal`, `Completion criteria`.
- Story/Task zusätzlich `Parent` (oder `None`), bei gesetztem Parent
  `Required for parent` (`Yes`/`No`).
- Prioritäten: `Urgent`, `Important`, `Prospective`.
- Areas: frei wählbar; bestehende Areas werden wiederverwendet, neue nur, wenn
  keine plausibel passt.
- `Resolution` genau dann, wenn Status `Completed` oder `Rejected`.

Neu in Claude_Harness (optional):

- `Summary`: nicht-technische Kurzfassung für den Projekteigner. Pflicht,
  sobald das Item `Notes` hat.
- `Notes`, `Spec`: relativer Pfad ab `TODO.md`; nur wenn die Datei existiert.
  Vorerst ein Pfad, später kommagetrennt mehrere.

## Language

Feldnamen, Typen, Status, Prioritäten und Überschriften sind englisch, damit
das Format auch ohne Deutschkenntnisse nutzbar ist. Inhalte werden in der
Arbeitssprache des Projekts geführt (hier Deutsch).

## Rules

- Hierarchie: Story → Epic; Task → Story oder Epic; Epic ohne Parent.
- Parent- und Dependency-Graph sind zyklenfrei.
- Status: `Open` → `In progress` → `Awaiting confirmation` → `Completed`
  bzw. `Rejected`. `Completed` und `Rejected` nur durch ausdrückliche
  Entscheidung des Projekteigners.
- Parent nicht `Awaiting confirmation`/`Completed`, solange ein required
  Child offen ist; ein Reject des Parents reißt Children nicht mit.
- Statuswechsel ändern nur das Feld `Status`, nicht die Position im Dokument.

## Item files

- Notes: eine mitwachsende Datei, Einträge mit Datum und den Abschnitten
  `Discussed` / `Decided` / `Open`.
- Spec: was und warum, Rahmenbedingungen, Schnittstellen, betroffene Dateien,
  Abnahmekriterien. Keine Schrittfolge; die entsteht im Plan Mode.
- Weitere Dateien nur per Themen-Suffix (`<ID>_spec_<thema>.md`).

## Archive

- Ist ein Item `Completed` oder `Rejected` und hat seine `Resolution`, wandert
  es unverändert nach `archive.md`. Der Item-Ordner bleibt in `items/`.
- Verweise auf archivierte IDs bleiben gültig.

## Change authority

Die AI ändert selbstständig:

- Notes und Specs: ergänzen, überarbeiten, umstrukturieren, was relevant ist;
- die Felder `Summary`, `Notes`, `Spec`;
- Status `Open` → `In progress` → `Awaiting confirmation` und zurück zu
  `In progress`;
- sprachliche Korrekturen ohne Bedeutungsänderung;
- Verschieben bestätigter oder abgelehnter Items ins Archiv.

Die AI schlägt vor und wartet auf Freigabe:

- neue Items anlegen oder Items löschen;
- inhaltliche Änderungen an `Goal` oder `Completion criteria`; Änderungen an
  `Parent`, `Required for parent`, `Dependencies`, `Priority`;
- `Completed`, `Rejected`, Wiederöffnen.

## Reading order

1. Standard: nur `TODO.md`.
2. Besprechung oder Entscheidung zu einem Item: zusätzlich dessen Notes.
3. Umsetzungsplanung oder Nachfrage: zusätzlich dessen Spec.
4. `archive.md` nur, wenn ein archiviertes Item gebraucht wird.

## Not adopted

- Jede Kompatibilität zu Agent_Harness-Formaten. Dies ist Claude_Harness
  Backlog-Format Version 1.
- Kopplung an einen Python-Renderer, der Regeln in `CLAUDE.md` einbaut.

## Affected files

- `plugin/skills/todo/format.md` (vollständige Formatbeschreibung)
- `plugin/skills/todo/SKILL.md` (Arbeitsregeln für die AI)
- `plugin/templates/todo/` (Vorlagen für neue Projekte)
- `docs/todo/TODO.md`, `docs/todo/archive.md` (Kopf verweist auf den Skill)
- `plugin/scripts/backlog.py` (automatische Prüfung, `STORY-020`)

## Acceptance criteria

- Die Formatbeschreibung in `plugin/skills/todo/format.md` deckt alle Punkte
  dieser Spec ab.
- Mindestens ein Item nutzt `Summary`, `Notes` und `Spec` korrekt.
- Ein neuer Eintrag lässt sich allein anhand der Formatbeschreibung anlegen.
