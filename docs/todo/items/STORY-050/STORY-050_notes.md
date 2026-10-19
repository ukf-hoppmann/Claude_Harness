# STORY-050 — Skills auf den MCP-Server des ToDo-Viewers umstellen

## 2026-10-19 — Herkunft und Entwurf

### Discussed

- Abgespalten aus STORY-049, als die Story auf die HTTP-API neu ausgerichtet wurde. Prüfergebnisse und offene Fragen zur MCP-Schnittstelle stehen in den Notizen von STORY-049.

### Decided

- Einbindung über .mcp.json im Plugin mit fester Adresse http://localhost:5411/mcp.
- Ein PreToolUse-Hook setzt das eigene Projekt ein (updatedInput) und fragt bei fremdem Projekt nach; zuerst prüfen, ob updatedInput bei MCP-Tools aus Plugins greift. Rückfall: workspace_use_project im Viewer.
- Session-Start meldet Projekt und Erreichbarkeit (GET /api/core/health); fehlen die Tools, fragt Claude nach (Server starten, Helfer, Dateien, abbrechen).
- Berechtigungen: Lese-Tools über init/update freigeben, Schreib-Tools folgen dem Berechtigungsmodus. Bisher gab es keine Regeln; die Helfer liefen als Bash-Befehle.
- Hängt vom Umbau im ToDo-Viewer ab: dort STORY-092 (projektübergreifend, daher nicht als Dependency eintragbar).
