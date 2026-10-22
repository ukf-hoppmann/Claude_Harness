# STORY-045 — Ablauf zwischen Cloud, Git und lokalem Viewer festlegen

## State

- Ziel/Status: Ablauf zwischen Cloud-Sitzung, Git und lokalem Viewer festlegen und im Skill todo beschreiben. In Arbeit; Klärung weitgehend abgeschlossen, Spec folgt.
- Nächster Schritt: Spec schreiben, dann Umsetzungsplan zur Freigabe vorlegen.
- Offen:
  - Spec und Umsetzungsplan
- Beschlossen:
  - Story gestartet, STORY-044 bestätigt (2026-10-22)
  - Rückweg nach main per Pull Request auf GitHub, lokales Merge als Alternative (2026-10-22)
  - Durchspielung am echten Backlog mit Backup und unschädlicher Änderung (2026-10-22)
  - Regeln in einer neuen Unterdatei sync-flow.md des Skills todo, SKILL.md und notes.md verweisen und werden berichtigt (2026-10-22)
- Verweise: Viewer-Doku operations.md (Auto-Sync, Notes im Sync), neubau-server.md (Sync), docs/handover/neubau-cloud.md; STORY-042, STORY-043, STORY-046; EPIC-010

State confirmed after entry 2026-10-22 — Durchspielung, Cloud-Seite (nachgestellt) (51df1a11fa77)

## 2026-10-16 — Befund aus den Cloud-Tests: Branches und Zuordnung

### Discussed

- Eine Cloud-Sitzung arbeitet auf einem Sitzungs-Branch claude/<name> ohne Upstream (Test 2, 2026-10-16). Änderungen an docs/todo erreichen main erst nach einem Merge (Pull Request oder lokal); erst dann kann der lokale Viewer sie lesen. Ein Repository ist nur dann beschreibbar, wenn es der Sitzung zugeordnet ist.

### Open

- Der Ablauf muss den Merge des claude/*-Branches nach main vor dem Viewer-Sync enthalten. Welcher Weg (Pull Request auf GitHub oder lokales Merge) Standard wird, entscheidet der Besitzer.

## 2026-10-22 — Ausgangslage: Befunde zum Ablauf und offene Entscheidungen

### Discussed

- STORY-044 ist bestätigt (Completed); STORY-045 gestartet (In progress). Bisher steht in den Notes nur der Befund vom 2026-10-16 (Cloud-Sitzung arbeitet auf einem Branch claude/<name>, Änderungen erreichen main erst nach einem Merge). Keine Spec.
- Belege aus der Viewer-Doku (operations.md, neubau-server.md, interfaces.md): Der Viewer synchronisiert den Spiegel-Ordner (bei diesem Projekt docs/todo) mit der Datenbank. Mit Auto-Sync ('Ein, Sync automatisch') prüft er alle 30 Sekunden und überträgt Konfliktfreies in beide Richtungen; eine Änderung wird erst übernommen, wenn sie bei zwei Prüfungen gleich war. Konflikte (both_changed, both_created, deleted_in_files, deleted_in_database) und Löschungen bleiben offen bis zur Entscheidung im Sync-Dialog (database, files oder defer). Der Auto-Sync pausiert, wenn der Ordner fehlt, nicht lesbar ist, Git-Merge-Marker enthält oder ein Git-Lock liegt (git_operation); die nächste gute Prüfung setzt fort. Vor einem Sync, der Notes in die Datenbank schreibt, entsteht ein Backup. Die Notes liegen im Unterordner notes/ des Spiegel-Ordners, 'git add/pull dieses Ordners trägt Notes zwischen Rechnern und in die Cloud'.
- Praxisbeleg: Die Übergabe des Viewers für seine Cloud-Sitzung (docs/handover/neubau-cloud.md) lief schon so: Branch neubau/epic-007 von main, Backlog direkt in den Dateien, pushen nach jedem Item, nicht nach main mergen; lokal übernimmt der Sync die Änderungen nach dem Pull.
- Widerspruch in den Regeln des Harness (Kriterium 5): notes.md (Schritt 3 und 5) sagt für api, die Notes lägen nur in der Datenbank, es gebe keine Dateien und nichts werde committet, und sie seien privat. Mit aktivem Spiegel stimmt das nicht: Der Viewer schreibt notes/ in den Backlog-Ordner (in diesem Repository liegt docs/todo/notes im Git). SKILL.md ('Committing backlog changes') nennt für api nur, den Backlog-Ordner im Hauptcheckout 'Backlog: …' zu committen, ohne notes/ zu erwähnen.
- Neue Frage für die Spec: In der Cloud neu angelegte Backlog-Einträge brauchen Platzhalter (NEW-<name>, format.md), damit lokal keine doppelten IDs entstehen; die Lösung für doppelte IDs ist STORY-046, der Ablauf verweist darauf.

### Open

- Standardweg zurück nach main: Pull Request auf GitHub oder lokales Merge des claude/<name>-Branches (aus dem Eintrag vom 2026-10-16, Entscheidung des Besitzers).
- Wie der Ablauf einmal durchgespielt wird (Kriterium 6): mit einem Wegwerf-Projekt im Viewer, gegen das echte Projekt Claude_Harness oder nur mit der Vorschau (GET preview, ändert nichts).
- Wo die Regeln stehen: Vorschlag eine neue Unterdatei sync-flow.md des Skills todo (Ablauf Cloud, Git, Viewer), SKILL.md und notes.md verweisen kurz darauf und werden berichtigt.

## 2026-10-22 — Entscheidung: Rückweg per Pull Request, Durchspielung am echten Backlog

### Discussed

- Frage 1, Rückweg nach main: Der Cloud-Branch claude/<Name> kommt per Pull Request auf GitHub nach main (A), oder der Branch wird lokal geholt und gemergt (B). Für A: Der Merge ist auf GitHub sichtbar und prüfbar, die Cloud-Sitzung endet ohnehin dort. Für B: kein PR nötig, aber der Merge liegt nur lokal.
- Frage 2, Durchspielung (Kriterium 6): Testprojekt im Viewer (keine echten Daten, aber ein zusätzliches Viewer-Projekt), echtes Backlog von Claude_Harness (echte Daten, vor dem Sync ein Backup des Viewers) oder nur die Vorschau (ändert nichts, endet vor dem Sync). Die Cloud-Seite wird in beiden ersten Fällen von Hand nachgestellt: Branch, Änderung an den Dateien unter docs/todo, Merge in main; ein Push oder ein echter Pull Request entfällt, weil die KI nicht pusht.

### Decided

- Standardweg zurück ist der Pull Request auf GitHub, danach lokal git pull und Viewer-Sync; das lokale Merge steht als Alternative im Skill (Owner, 2026-10-22).
- Der Ablauf wird am echten Backlog von Claude_Harness durchgespielt, mit Backup des Viewers vorher und einer unschädlichen Änderung (ein angehängter Notes-Eintrag) auf einem Branch; Ergebnis in diese Notes (Owner, 2026-10-22).

### Open

- Spec schreiben: neue Unterdatei sync-flow.md im Skill todo, Berichtigung von notes.md und SKILL.md (Kriterium 5), README und Techdocs. Umsetzungsplan danach zur Freigabe.

## 2026-10-22 — Durchspielung, Cloud-Seite (nachgestellt)

### Discussed

- Probe der Cloud-Seite: Dieser Eintrag und die Note new-ablauf-probe.md wurden in einem Branch (worktree-story-045-probe) direkt in den Dateien geschrieben, wie es eine Cloud-Sitzung mit Backend files täte. Er soll nach dem Merge in main und dem Auto-Sync des Viewers über die API in diesen Notes stehen.
