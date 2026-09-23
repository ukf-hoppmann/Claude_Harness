# STORY-017 — Notes

## 2026-09-23 — Grundstruktur des Backlogs

### Besprochen

- Vorlage war das Backlog-Format v2 aus Agent_Harness. Claude_Harness löst
  Agent_Harness ab; übernommen werden nur die guten Konzepte, die alten Regeln
  sind nicht bindend.
- Wunsch: Besprechungen und Entscheidungen zu einem Item festhalten, als
  Gedächtnisstütze für die AI, ohne die Hauptliste aufzublähen.
- Erwogen: Notizen direkt in `TODO.md`. Verworfen, weil die Liste dadurch
  schwer lesbar wird und bei jeder Aufgabe unnötig Tokens kostet.
- Erwogen: eine datierte Notizdatei pro Besprechung. Verworfen zugunsten einer
  mitwachsenden Datei pro Item, weil Items irgendwann abgeschlossen sind und
  dann nichts mehr wächst.
- Erwogen: eine Datei „Plan“ mit Umsetzungsschritten. Verworfen, weil das den
  Plan Mode doppelt. Stattdessen eine Spec als technische Grundlage, aus der
  der Plan Mode einen Plan erzeugt.

### Beschlossen

- Übernommen aus v2: Epic/Story/Task, Pflichtfelder, Statusmodell,
  Bestätigung nur durch den Projekteigner, Trennung von `Parent` und
  `Dependencies`, `Required for parent`, kein Kaskaden-Reject.
- Ablage unter `docs/todo/`; später über die Projektkonfiguration einstellbar
  (`EPIC-001`), bis dahin fester Standard.
- Pro Item bei Bedarf ein Ordner `items/<ID>/` mit `<ID>_notes.md` und
  `<ID>_spec.md`. Kleine Aufgaben brauchen keinen Ordner.
- Vorerst je eine Notes- und eine Spec-Datei; erweiterbar per Themen-Suffix,
  ohne die erste Datei umzubenennen.
- Neue optionale Felder in `TODO.md`: `Summary` (für den Projekteigner, nicht
  technisch), `Notes` und `Spec` (relativer Pfad, nur wenn vorhanden). Die
  Kurzfassung steht nur in `TODO.md`, nicht in Notes oder Spec.
- Notes und Spec dürfen überarbeitet werden; Richtungswechsel werden in den
  Notes festgehalten.
- Lesereihenfolge: standardmäßig nur `TODO.md`; Notes bei Besprechung oder
  Entscheidung; Spec bei Umsetzungsplanung oder Nachfrage.
- Daily-Reports gehören nicht in diesen Ordner.

- Nachtrag: `Summary` ist Pflicht, sobald ein Item `Notes` hat; sonst
  optional.
- Nachtrag: Keine Kompatibilität zu Agent_Harness-Formaten. Claude_Harness
  startet neu; dies ist Backlog-Format Version 1.
- Nachtrag: Skill und Hook für die Backlog-Regeln werden als `STORY-020` unter
  `EPIC-007` umgesetzt.

### Offen

- Automatische Formatprüfung: als Hook-Skript im Plugin, analog zu
  `backlog.py` aus Agent_Harness, inklusive der neuen Felder und der
  Summary-Pflicht (`STORY-020`).
- Nach `STORY-020` wird die Formatbeschreibung im Kopf von `TODO.md` auf einen
  Verweis auf den `todo`-Skill gekürzt.
