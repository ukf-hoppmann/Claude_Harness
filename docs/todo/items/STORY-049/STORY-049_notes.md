# STORY-049 — todo- und notes-Skill auf den MCP-Server des ToDo-Viewers umstellen

## 2026-10-19 — Prüfung der MCP-Schnittstelle und offene Fragen

### Discussed

- Live gegen den laufenden Viewer geprüft: 17 Lese-Tools (core, workspace, backlog, notes, alarms) und 9 Fehlerfälle (version_conflict, not_found, validation_error, invalid_input, value_required, unbekanntes Tool) liefern die dokumentierten Antworten. Den Schreibablauf deckt der Systemtest des Viewers ab (test_harness_flow.py, grün).
- Unterschiede zum alten Helfer: parent und dependencies sind uids, required_for_parent ist ein Wahrheitswert, version ist eine Zahl, ein Label braucht immer die Projekt-uid. Das Schema von fields nennt keine Feldnamen; die muss der Skill beschreiben.
- Betroffen im Harness: backlog_api.py, notes_api.py, viewer_api.py, session_start.py, harness_config.py, config-Vorlage, Skills todo (SKILL.md, api.md, notes.md, notes-api.md, format.md), init, update, zwei Integrationstests, Techdocs.

### Open

- Einbindung: .mcp.json im Plugin (gilt für jedes Projekt mit dem Plugin) oder je Projekt, Adresse aus der Config?
- Projektgrenze: MCP sieht alle Projekte, der Helfer hat das technisch begrenzt. Reicht die Skill-Regel, oder soll ein Hook Aufrufe mit fremder Projekt-uid abfangen?
- Projekt-uid: soll der Session-Start sie ermitteln und ausgeben (Zuordnung über mirror_folder)?
- Server nicht erreichbar: Ohne Exit-Code 3 fehlen die Tools einfach. Wie soll Claude das erkennen und nachfragen?
- Alte Helfer: ganz entfernen oder als Rückfall (z. B. für Hooks) auf die neuen HTTP-Routen umstellen?
- Wecker (alarms_*) und Sync (core_sync_*): in den Skill aufnehmen oder vorerst weglassen?
- Berechtigungen: welche MCP-Tools ohne Rückfrage erlaubt sein sollen (Lese-Tools sind als readOnly markiert).

## 2026-10-19 — Entscheidungen zu den offenen Fragen

### Discussed

- Bisherige Berechtigungen: Weder Plugin noch Projekt noch Nutzer-Settings enthalten Regeln für die Helfer. Jeder Helfer-Aufruf war ein Bash-Befehl, über den der Berechtigungsmodus der Session entschied.
- Bisherige Projektzuordnung: viewer_api.py fand die Quelle über den Backlog-Ordner der Hauptarbeitskopie (auch aus einem Worktree) und registrierte sie, wenn sie fehlte. Unter MCP gibt es kein Tool zum Anlegen eines Projekts.

### Decided

- Einbindung: .mcp.json im Plugin mit der festen Adresse http://localhost:5411/mcp (Empfehlung angenommen).
- Fremde Projekte: wie bisher keine technische Sperre. Jede Session ändert nur ihr eigenes Projekt, auf ausdrückliche Aufforderung des Eigners aber auch fremde Backlogs. Die bisherige Freigaberegel im Skill gilt sinngemäß weiter (Projekt über workspace_list_projects statt sources).
- Alte Helfer bleiben als Rückfall und werden auf die neuen HTTP-Routen umgestellt.
- Wecker (alarms_*) kommen in den Skill; Sync (core_sync_*) nicht, er läuft automatisch.

### Open

- Projekt-uid im Session-Start ausgeben (Vorschlag liegt vor).
- Verhalten bei nicht erreichbarem Server (Vorschlag: Health-Check im Session-Start und Regel im Skill).
- Berechtigungen für die MCP-Tools (Vorschlag: Lese-Tools freigeben, Schreib-Tools folgen dem Berechtigungsmodus).

## 2026-10-19 — Neuausrichtung: erst die HTTP-API, MCP später

### Discussed

- MCP verlangt das Projekt bei jedem Aufruf; die API funktionierte gut, weil der Helfer das Projekt deterministisch aus Config und Hauptarbeitskopie nahm und Claude es nie angab.
- Eine falsche Projekt-uid legt per MCP kein Projekt an; backlog_index_lines liefert dann aber still eine leere Liste.

### Decided

- Die Story stellt nur die Helfer auf die neue HTTP-API um (Titel, Ziel und Abschlusskriterien angepasst). Die MCP-Anbindung ist STORY-050 und wartet auf den Umbau des MCP-Servers im ToDo-Viewer (dort STORY-092).
- Projekte im Viewer werden nur auf ausdrücklichen Befehl nach Rückfrage registriert; das stille Registrieren in viewer_api.py entfällt.
- Fremde Projekte: keine technische Sperre, nur auf Aufforderung des Eigners (Regel im Skill bleibt).
- Wecker kommen als Befehle und in den Skill; Sync nicht, er läuft automatisch.

## 2026-10-19 — Umsetzung im Worktree: Helfer auf der neuen API

### Discussed

- backlog_api.py, notes_api.py und das neue alarms_api.py sprechen die neuen Routen an; Live-Prüfung gegen den laufenden Viewer.

### Decided

- Der Health-Check im Session-Start entfällt: Hooks dürfen das Netzwerk nicht nutzen (Architekturregel 2); die Erreichbarkeit meldet weiter Exit 3 des Helfers.

## 2026-10-19 — Umgesetzt und geprüft (v0.11.0)

### Decided

- Gemerged als 40b1e25, Release v0.11.0. Alle Abschlusskriterien erfüllt: Befehle von backlog_api.py und notes_api.py laufen gegen den neuen Viewer, IDs in parent und dependencies, Exit 4 statt stillem Registrieren, register nur auf Befehl, Wecker über alarms_api.py, Config-Standard ohne /api/v2, Skills und Techdocs aktualisiert, Integrationstests grün, Lese-, Schreib- und Notizfluss live geprüft.

### Open

- Bestätigung durch den Projektverantwortlichen.
