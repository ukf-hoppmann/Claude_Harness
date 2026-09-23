# Architektur

Beschreibt den aktuellen Stand. Der Verlauf steht in den Tagesberichten
(`docs/development/daily/`), die Begründungen in den Backlog-Notizen.

## Überblick

Claude_Harness ist ein Claude-Code-Plugin. Regeln, die nur bei bestimmten
Aufgaben gelten, liegen als Skills vor; Claude Code lädt dauerhaft nur ihre
einzeilige Beschreibung und den Inhalt erst beim passenden Thema. Regeln, die
nicht vergessen werden dürfen, prüfen Hooks: Python-Skripte, die Claude Code
bei Ereignissen aufruft und die keine Tokens kosten, solange sie nichts melden.
Jedes Modul prüft selbst, ob es in der Projektkonfiguration eingeschaltet ist.

## Komponenten

| Komponente | Aufgabe | Ort |
|---|---|---|
| Plugin-Manifest | Name, Version, Beschreibung des Plugins | `plugin/.claude-plugin/plugin.json` |
| Marketplace | Macht das Plugin lokal installierbar | `.claude-plugin/marketplace.json` |
| Hook-Registrierung | Verknüpft Ereignisse mit Skripten | `plugin/hooks/hooks.json` |
| Config-Lader | Liest und validiert `.claude-harness/config.toml` | `plugin/scripts/harness_config.py` |
| Session-Start | Meldet aktive Module, Sprache, fehlende Dateien und Backlog-Fehler | `plugin/scripts/session_start.py` |
| Modul `todo` | Skill mit Backlog-Regeln, Formatprüfung, Prüf-Hooks | `plugin/skills/todo/`, `plugin/scripts/backlog.py`, `mark_backlog_dirty.py`, `check_backlog.py` |
| Modul `daily` | Skill, Git-Auswertung, Erinnerungs-Hook | `plugin/skills/daily/`, `plugin/scripts/daily.py`, `check_daily.py` |
| Modul `techdocs` | Skill, Dateiklassifikation, Erinnerungs-Hooks | `plugin/skills/techdocs/`, `plugin/scripts/techdocs.py`, `mark_techdocs.py`, `check_techdocs.py` |
| Befehl `init` | Richtet den Harness in einem Projekt ein | `plugin/skills/init/` |
| Vorlagen | Config, Backlog, Tagesbericht, Systemdoku | `plugin/templates/` |
| Sitzungszustand | Pfade für Merker pro Session | `plugin/scripts/state.py` |

## Ablauf

1. **SessionStart:** `session_start.py` lädt die Config und schreibt eine
   Kurzfassung in den Kontext (aktive Module, Dokumentsprache, Orte der
   Dokumente, fehlende Dateien, Backlog-Fehler).
2. **PostToolUse (Write/Edit/MultiEdit):** `mark_backlog_dirty.py` merkt sich
   Änderungen im Backlog-Ordner; `mark_techdocs.py` merkt sich, ob
   Projektdateien oder Systemdoku geändert wurden.
3. **Stop:** Die Prüf-Hooks laufen nacheinander. Melden sie etwas, beenden sie
   sich mit Exit-Code 2; Claude Code gibt die Meldung an Claude zurück, das
   daraufhin weiterarbeitet.
   - `check_backlog.py`: prüft den Backlog nach Änderungen daran.
   - `check_daily.py`: erinnert an den Tagesbericht, wenn neue Commits auf dem
     Hauptzweig noch nicht erfasst sind.
   - `check_techdocs.py`: erinnert einmal pro Session, wenn Projektdateien,
     aber keine Systemdoku geändert wurden.

## Zustand und Ablage

| Zustand | Ort | Lebensdauer |
|---|---|---|
| Projektkonfiguration | `.claude-harness/config.toml` | im Repo versioniert |
| Merker pro Session (Backlog geändert, Hinweise gemeldet, Doku-Erinnerung) | `$CLAUDE_PLUGIN_DATA`, sonst `<tmp>/claude-harness/` | pro Session |
| Bestätigter Stand des Tagesberichts | `.git/claude-harness/daily-ack` | pro Klon, nie committet |
| Backlog, Tagesberichte, Systemdoku | unter `docs.root` (Standard `docs/`) bzw. `README.md` | im Repo versioniert |

## Wichtige Entscheidungen

| Entscheidung | Kurzbegründung | Referenz |
|---|---|---|
| Plugin mit Skills und Hooks statt gerenderter Regeln in `CLAUDE.md` | Regeln kosten nur Tokens, wenn sie gebraucht werden | `EPIC-007` |
| Ein Plugin mit Modulschaltern in der Config | Einfache Installation; Module prüfen ihren Schalter selbst | `EPIC-001` |
| Tagesbericht nur im Haupt-Checkout nach dem Merge | Vermeidet Merge-Konflikte bei parallelen Worktrees | `STORY-013` |
| Systemdoku im selben Change wie der Code | Doku und Code bleiben in jedem Stand konsistent | `STORY-012` |
| Nur Python-Standardbibliothek | Keine Installationsschritte in Zielprojekten | `STORY-018` |
