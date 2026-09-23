# STORY-017 — Notes

## 2026-09-23 — Grundstruktur des Backlogs

### Discussed

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

### Decided

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

### Open

- Automatische Formatprüfung: als Hook-Skript im Plugin, analog zu
  `backlog.py` aus Agent_Harness, inklusive der neuen Felder und der
  Summary-Pflicht (`STORY-020`).
- ~~Nach `STORY-020` wird die Formatbeschreibung im Kopf von `TODO.md` auf
  einen Verweis auf den `todo`-Skill gekürzt.~~ Erledigt am 2026-09-23.

## 2026-09-23 — Archiv, Änderungsrechte, Sprache, Areas

### Discussed

- Erledigte Einträge in `TODO.md` würden die Datei dauerhaft wachsen lassen und
  bei jeder Session mitgelesen werden.
- Im Agent_Harness brauchte jede Backlog-Änderung eine Freigabe. Das ist für
  Kleinigkeiten zu schwerfällig.
- Der Kopf von `TODO.md` war englisch, die Einträge deutsch.

### Decided

- `Completed`/`Rejected` wandern nach `archive.md`; Item-Ordner bleiben in
  `items/`.
- Die AI ändert Kleinigkeiten selbstständig, insbesondere Notes und Specs:
  Sie ergänzt und ändert dort selbstständig, was relevant ist. Neue Items,
  inhaltliche Änderungen an Ziel/Kriterien/Beziehungen/Priorität sowie
  `Completed`/`Rejected` brauchen weiter die Freigabe des Projekteigners.
- Alle Keys (Feldnamen, Status, Typen, Prioritäten, Überschriften) sind
  englisch, damit auch Nicht-Deutschsprachige das Format nutzen können. Die
  Inhalte führt der Projekteigner auf Deutsch.
- Prioritäten heißen daher `Urgent`, `Important`, `Prospective`.
- Areas bleiben frei wählbar. Die AI verwendet plausible Kategorien und nutzt
  bestehende wieder, bevor sie neue anlegt.

### Open

- ~~Nummerierung und Reihenfolge der Einträge in `TODO.md`.~~ Entschieden am
  2026-09-23: bleibt wie bisher (siehe unten).

## 2026-09-23 — Nummerierung, Umzug der Regeln ins Plugin

### Discussed

- Vorschlag, die Einträge in `TODO.md` nach Epic zu gruppieren.

### Decided

- Nummerierung und Reihenfolge bleiben wie bisher. Beim Umhängen einer Story
  in ein anderes Epic bleiben ID, Ordner `items/<ID>/` und Pfade gleich, weil
  die Ordner flach nach ID liegen.
- Die Formatregeln stehen jetzt in `plugin/skills/todo/format.md`; der Kopf
  von `TODO.md` und `archive.md` verweist nur noch darauf.
- `Notes`/`Spec`-Pfade sind relativ zum Backlog-Ordner (gleichbedeutend mit
  relativ zu `TODO.md`).
- Fehlt `TODO.md` am konfigurierten Pfad, fragt die AI nach, statt eine neue
  anzulegen — die Datei kann auch nur woanders liegen.
