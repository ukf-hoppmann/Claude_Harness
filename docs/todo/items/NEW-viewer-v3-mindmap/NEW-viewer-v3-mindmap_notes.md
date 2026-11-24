# NEW-viewer-v3-mindmap — Harness auf Format Version 3 und die Mindmap umstellen

## State

- Goal/Status: Vier Aufträge des Owners geordnet, Umsetzung noch nicht begonnen (2026-11-24)
- Next step: Owner entscheidet die offenen Fragen, danach Schritt 1 (Format Version 3) in einem Worktree (2026-11-24)
- Open: keine (2026-11-24)
- Decided: docs/todo und docs/todo_v1 bleiben Version 2 (Viewer-Spiegel stellt um); Memos-Umbenennung steht seit v0.14.0 auf main, in den Aufträgen memos_* meint die vorhandenen memos_*-Dateien; Release dieser Story wird 0.15.0 am Ende nach Bestätigung; keine Cloud-Kopie in diesem Repo, nur Hinweis auf update (2026-11-24)
- Decided: Reihenfolge Format 3, dann API-Regel, dann Dateimodus-Mindmap, ein gemeinsames Release (2026-11-24)
- References: Aufträge TASK-072 (Prompt 1 und 2), TASK-078, TASK-082 des ToDo-Viewers (2026-11-24)

State confirmed after entry 2026-11-24 — Reihenfolge der vier Aufträge (fa5fc5674f7c)

## 2026-11-24 — Reihenfolge der vier Aufträge

### Discussed

- Auftrag A, TASK-072 Prompt 2 (Format Version 3 ohne Area): ändert Skripte, Check, Vorlagen, `format.md`, `api.md`, `SKILL.md`, README, Tests. Alle anderen Aufträge bauen darauf auf.
- Auftrag B, TASK-078 (API-Modus, Regel „Item dem Themenbaum zuordnen“): ein Absatz in `SKILL.md`, Abschnitt Working rules. Überschneidet sich mit A, weil A einen Satz zur Mindmap in `SKILL.md`/`api.md` ergänzt und die Area-Regel streicht. B baut diesen Satz aus. Vermerk „Dateimodus noch offen“.
- Auftrag C, TASK-082 (Mindmap im Dateimodus): Abschnitt „Mindmap“ in `format.md` und `SKILL.md`, `backlog.py`/Hooks kennen `mindmap/`, Test mit Viewer-Fixture. Setzt die Check-Änderungen aus A voraus und entfernt den Vermerk aus B.
- Auftrag D, TASK-072 Prompt 1 (Themenbaum aus den Items erzeugen): ändert den Harness nicht. Läuft lokal im Projekt mit laufendem Viewer und MCP-Server `todo-viewer`; in dieser Cloud-Sitzung nicht ausführbar. Er ordnet die Items den Knoten zu, nachdem der Viewer Area entfernt hat.

### Recommendation

1. A zuerst (Grundlage, größte Änderung, bricht die Schnittstelle).
2. B danach (kleiner Text, setzt den Mindmap-Satz aus A voraus).
3. C danach (nutzt die Check-Änderungen aus A, ersetzt den Vermerk aus B).
4. Ein gemeinsames Release nach C (semver: eine Änderung, ein Schritt; bei 0.x inkompatibel = minor, also 0.14.0). Cloud-Kopie neu erzeugen, Projekte müssen `update` ausführen.
5. D außerhalb des Harness, lokal durch den Owner, unabhängig von 1 bis 4; sinnvoll nach A, damit Skill und Viewer denselben Stand haben.
6. Umsetzung je Auftrag als eigener Plan und eigener Worktree-Abschnitt, Tests nach jedem Schritt.

### Open

- Das eigene Backlog `docs/todo` und `docs/todo_v1` (Version 2 mit Area) umstellen oder lassen?
- Die Aufträge nennen „Memos“; im Repo heißt es `notes_api.py`, `notes-api.md`, `notes.md`. Gemeint sind die Notes?
- Version erhöhen (0.14.0) und Release-Commit mit Tag machen oder dem Owner überlassen?
- Cloud-Kopie: Dieses Repo hat keinen `[cloud]`-Abschnitt. Nichts erzeugen und nur im Bericht auf `update` hinweisen?
