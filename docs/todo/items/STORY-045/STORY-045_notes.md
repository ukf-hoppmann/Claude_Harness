# STORY-045 — Ablauf zwischen Cloud, Git und lokalem Viewer festlegen

## State

- Goal/Status: Ablauf zwischen Cloud, Git und lokalem Viewer im Skill todo beschrieben und am echten Backlog durchgespielt. Umgesetzt, wartet auf Bestätigung.
- Next step: Owner bestätigt; danach STORY-046 (doppelte IDs) und das Epic EPIC-010 prüfen.
- Open:
  - Konflikt-, Merge-Marker- und Formatfehler-Fall nur nach Doku beschrieben, nicht erprobt
  - Sync-Status im Helfer backlog_api.py als möglicher Befehl, kein Item
- Decided:
  - Story gestartet, STORY-044 bestätigt (2026-10-22)
  - Rückweg nach main per Pull Request auf GitHub, lokales Merge als Alternative (2026-10-22)
  - Durchspielung am echten Backlog mit unschädlicher Änderung (2026-10-22)
  - Regeln in sync-flow.md im Skill todo, notes.md und SKILL.md berichtigt, README und Techdocs ergänzt (2026-10-22)
  - Durchspielung erfolgreich: Sync etwa 16 Sekunden nach dem Merge, Eintrag und Probe-Note mit Label in der Datenbank (2026-10-22)
- References: Spec STORY-045_spec.md; Viewer-Doku operations.md, neubau-server.md; STORY-042, STORY-043, STORY-046; EPIC-010

State confirmed after entry 2026-10-22 — Umsetzung und Durchspielung am echten Backlog (054f51975f3e)

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

## 2026-10-22 — Umsetzung und Durchspielung am echten Backlog

### Discussed

- Plan vom Owner freigegeben. Umgesetzt im Worktree story-045-sync-flow und in main gemergt: neue Unterdatei plugin/skills/todo/sync-flow.md (Voraussetzungen, Hinweg, Cloud-Seite, Rückweg, Pause des Auto-Syncs, Notes im Repository); notes.md (Schritt 3 und 5) und SKILL.md (Committing backlog changes) berichtigt: mit Spiegel schreibt der Viewer notes/ in den Backlog-Ordner, die Dateien werden als 'Backlog: …' committet, die KI schreibt sie im API-Modus nicht von Hand, die Notes sind dann nicht privat. README und Techdocs (architecture.md) beschreiben den Ablauf. Tests: 579 grün (neu: sync-flow.md landet in der Cloud-Kopie, die drei Skill-Dateien verweisen darauf, notes.md nennt den Spiegel).
- Durchspielung am echten Backlog (Kriterium 6), Cloud-Seite von Hand nachgestellt: Ausgangslage Viewer erreichbar, Projekt Claude_Harness mit Spiegel docs/todo, Auto-Sync an, Richtung beide, Sync-Status in_sync ohne Konflikte, Hauptcheckout sauber. Cloud-Seite im Worktree-Branch von main mit CLAUDE_CODE_REMOTE=true und den Hooks von Hand aufgerufen: Notes-Eintrag an die Notes von STORY-045 angehängt und die Note new-ablauf-probe.md angelegt; der Stop-Hook blockierte zuerst wegen des veralteten Kopfs der Notes (wie vorgesehen), nach backlog.py --confirm-state war er frei, notes_files.py --check ohne Fund, der Sitzungsstart zeigte 'backend files: cloud session' und 'Notes: docs/todo/notes/ as files'.
- Rückweg: Der Branch wurde in main gemergt (stellvertretend für den Pull Request, ohne Push). Der Viewer meldete danach 'mirror_changed' mit to_database 2 und war etwa 16 Sekunden nach dem Merge wieder 'in_sync' (Merge 15:56:19, letzter Sync 15:56:35 Ortszeit), ohne Konflikt. Über die API stand der Eintrag in den Notes von STORY-045 (position 3), die Probe-Note hatte das Label NOTE-004, und die Datei im Hauptcheckout hieß nun NOTE-004.md (new-ablauf-probe.md war weg; beides zunächst uncommittet, bis 'Backlog: …' committet wird, wie sync-flow.md es beschreibt). Die Probe-Note wurde als done beendet (ohne Rückfrage erlaubt) und stand wenige Sekunden später im Spiegel mit Archived: true.
- Abweichungen und Beobachtungen: (1) Ein echter Pull Request und ein Push waren nicht möglich (die KI pusht nicht); das lokale Merge stand stellvertretend. (2) Konflikt, Merge-Marker und note_format-Abbruch wurden nicht künstlich erzeugt; sie sind nach der Doku des Viewers beschrieben, nicht selbst erprobt. (3) Der Sync-Status des Viewers ist lesbar über GET /api/core/sync/<Projekt-uid>/status (Zustände in_sync, mirror_changed, paused mit reason; Zähler to_database, to_files, conflicts); mit dem Projektnamen statt der uid antwortet er irreführend 'paused / not_configured'. Der Helfer backlog_api.py hat dafür keinen Befehl; sync-flow.md sagt deshalb nur, dass der Besitzer im Zweifel nachfragt. (4) Die Probe-Note bleibt als erledigte Note in der Datenbank (nur der Besitzer löscht endgültig).

### Decided

- Kriterien 1 bis 7 sind erfüllt; Status Awaiting confirmation, Bestätigung durch den Owner offen.

### Open

- Ein Befehl für den Sync-Status im Helfer backlog_api.py (Zustand, Konflikte, letzter Sync) würde die Frage 'ist der Viewer durch?' beantwortbar machen; kein eigenes Item angelegt.
- Konflikt-, Merge-Marker- und Formatfehler-Fall sind nicht durchgespielt.
