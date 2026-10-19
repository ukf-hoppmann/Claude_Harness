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
