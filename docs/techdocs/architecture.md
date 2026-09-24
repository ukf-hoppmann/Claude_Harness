# Architektur

Beschreibt den aktuellen Stand. Der Verlauf steht in den Tagesberichten
(`docs/daily/`), die Begründungen in den Backlog-Notizen.

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
| Suite `development`, Teil `architecture` | Skill, Scope-Tabelle, Lese-Merker, Hook vor Änderungen | `plugin/skills/architecture/`, `plugin/scripts/architecture.py`, `mark_architecture_read.py`, `check_architecture.py` |
| Befehl `init` | Richtet den Harness in einem Projekt ein | `plugin/skills/init/` |
| Vorlagen | Config, Backlog, Tagesbericht, Systemdoku, Architekturregeln | `plugin/templates/` |
| Sitzungszustand | Pfade für Merker pro Session | `plugin/scripts/state.py` |

## Module und Ladestufen

Wo jedes Modul liegt und warum. Die Regel dahinter steht in
`docs/development/architecture.md`, Abschnitt 7. Immer im Kontext sind nur
die Skill-Beschreibungen (je ein Satz) und eine Startzeile pro Modul.

| Modul | Hook (prüft, kostet nichts, solange alles stimmt) | Skill (lädt beim Thema) | Skript | Warum so |
|---|---|---|---|---|
| `todo` | Formatprüfung am Ende eines Turns, nur nach Backlog-Änderungen | Backlog-Regeln; Formatdetails in `format.md`, nur beim Anlegen oder bei Fehlern | `backlog.py` (Prüfung, Übersicht) | Das Format lässt sich prüfen und darf nicht kaputtgehen; die Arbeitsregeln betreffen nur Backlog-Arbeit |
| `daily` | Erinnerung bei neuen Commits auf dem Hauptzweig | Berichtsregeln | `daily.py` (offene Commits, Bestätigen) | Das Fehlen eines Berichts ist erkennbar; Schreiben ist nur nach Commits Thema; die Git-Auswertung ist stures Abarbeiten |
| `techdocs` | Erinnerung, wenn Code, aber keine Doku geändert wurde | Doku-Regeln | – | Vergessene Doku ist erkennbar; die Regeln braucht es nur bei dokumentationsrelevanten Änderungen |
| `development` / `architecture` | Blockiert Plan, Spec und Code-Änderungen, bis die Regeln gelesen sind | Umgang mit Architekturregeln | – | Die Regeln gelten für jede Code-Änderung und dürfen nicht übergangen werden; Bereichsregeln als Scopes nur für passende Pfade |
| `init` | – | Einrichtungsablauf, nur vom Nutzer aufrufbar | – | Wird einmal pro Projekt gebraucht |

Unterordner-`CLAUDE.md` nutzt der Harness nicht; bereichsbezogene Regeln
sind Architektur-Scopes. Die Root-`CLAUDE.md` schreibt das Plugin nie.

## Ablauf

1. **SessionStart:** `session_start.py` lädt die Config und schreibt eine
   Kurzfassung in den Kontext (aktive Module, Dokumentsprache, Orte der
   Dokumente, fehlende Dateien, Backlog-Fehler).
2. **PreToolUse (Write/Edit/MultiEdit/NotebookEdit/ExitPlanMode):**
   `check_architecture.py` lehnt das Vorlegen eines Plans, das Schreiben einer
   Backlog-Spec und die Änderung einer Projektdatei ab, bis die
   Architekturregeln (bei Projektdateien auch passende Scope-Dateien) in der
   Session vollständig gelesen wurden.
3. **PostToolUse (Read):** `mark_architecture_read.py` merkt sich vollständig
   gelesene Regel- und Scope-Dateien.
4. **PostToolUse (Write/Edit/MultiEdit):** `mark_backlog_dirty.py` merkt sich
   Änderungen im Backlog-Ordner; `mark_techdocs.py` merkt sich, ob
   Projektdateien oder Systemdoku geändert wurden.
5. **Stop:** Die Prüf-Hooks laufen nacheinander. Melden sie etwas, beenden sie
   sich mit Exit-Code 2; Claude Code gibt die Meldung an Claude zurück, das
   daraufhin weiterarbeitet.
   - `check_backlog.py`: prüft den Backlog nach Änderungen daran.
   - `check_daily.py`: erinnert an den Tagesbericht, wenn neue Commits auf dem
     Hauptzweig noch nicht erfasst sind. Commits, die nur Daily- oder
     Backlog-Ordner ändern, zählen nicht; der Backlog dokumentiert sich selbst.
   - `check_techdocs.py`: erinnert einmal pro Session, wenn Projektdateien,
     aber keine Systemdoku geändert wurden.

## Zustand und Ablage

| Zustand | Ort | Lebensdauer |
|---|---|---|
| Projektkonfiguration | `.claude-harness/config.toml` | im Repo versioniert |
| Merker pro Session (Backlog geändert, Hinweise gemeldet, Doku-Erinnerung, gelesene Architekturregeln) | `$CLAUDE_PLUGIN_DATA`, sonst `<tmp>/claude-harness/` | pro Session |
| Bestätigter Stand des Tagesberichts | `.git/claude-harness/daily-ack` | pro Klon, nie committet |
| Backlog, Tagesberichte, Systemdoku, Regeln der Suite `development` | unter `docs.root` (Standard `docs/`) bzw. `README.md` | im Repo versioniert |

## Wichtige Entscheidungen

| Entscheidung | Kurzbegründung | Referenz |
|---|---|---|
| Plugin mit Skills und Hooks statt gerenderter Regeln in `CLAUDE.md` | Regeln kosten nur Tokens, wenn sie gebraucht werden | `EPIC-007` |
| Ein Plugin mit Modulschaltern in der Config | Einfache Installation; Module prüfen ihren Schalter selbst | `EPIC-001` |
| Tagesbericht nur im Haupt-Checkout nach dem Merge | Vermeidet Merge-Konflikte bei parallelen Worktrees | `STORY-013` |
| Systemdoku im selben Change wie der Code | Doku und Code bleiben in jedem Stand konsistent | `STORY-012` |
| Gestufte Ablage: Hook → Scope → Skill → Skript → Root-`CLAUDE.md` | Nur das Nötigste ist immer im Kontext; Pflichtregeln prüft ein Hook | `STORY-019` |
| Architekturregeln als Teil der Suite `development`, englisch, Scopes als Tabelle in der Regeldatei, Lesen per Hook erzwungen | Regeln werden zuverlässig gelesen; Spezielles nur, wo es gilt | `STORY-023` |
| Nur Python-Standardbibliothek | Keine Installationsschritte in Zielprojekten | `STORY-018` |
