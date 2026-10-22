# TASK-024 — Hooks für aktuellen Notes-Kopf und Protokoll-Reminder

## State

- Goal/Status: Hooks für aktuellen Notes-Kopf (API-Modus) und Protokoll-Reminder (beide Modi). In Arbeit; Weg A gewählt, Spec wird angepasst.
- Next step: Spec anpassen, Umsetzungsplan zur Freigabe vorlegen.
- Open:
  - Plan zur Freigabe
  - Erkennung des aktiven Items im Files-Modus (Vorschlag: Lesen der Spec)
- Decided:
  - Weg A: PostToolUse-Hook auf Bash legt die Merker ab, kein Netzwerk im Hook (2026-10-22)
  - Der Helfer meldet Zustand und aktives Item über stderr-Zeilen und legt keine Merker mehr ab (Vorschlag, 2026-10-22)
- References: Spec TASK-024_spec.md; STORY-051 (Spec, Notes); TASK-022, TASK-023; Architekturregel 2

State confirmed after entry 2026-10-22 — Entscheidung: Merker über einen PostToolUse-Hook (Weg A) (c04300909d93)

## 2026-10-22 — Entscheidung: Merker über einen PostToolUse-Hook (Weg A)

### Discussed

- Ausgangslage: TASK-022 und TASK-023 sind Completed; TASK-024 war nicht begonnen. Der Besitzer hat gefragt, was fehlt, und danach Weg A gewählt.
- Befund 1, Architektur: Die Spec ließ den Stop-Hook im API-Modus den Zustand 'beim Viewer abfragen'. Architekturregel 2 verbietet Hooks das Netzwerk (Skill conflicts: Konflikt benannt).
- Befund 2, Übergabe der Merker: Der Helfer backlog_api.py legt die Merker (Notes geändert, aktives Item) mit CLAUDE_CODE_SESSION_ID im Session-State ab. Die Session-ID ist dieselbe wie die session_id der Hooks (an den Dateinamen im Datenordner der Hooks geprüft). Aber der Helfer läuft über Bash ohne CLAUDE_PLUGIN_DATA und schreibt deshalb nach $TMPDIR/claude-harness/, während die Hooks aus ~/.claude/plugins/data/claude-harness-claude-harness-dev/ lesen. Die Hooks sehen die Merker nie.
- Option A: PostToolUse-Hook auf Bash liest Befehl und Antwort von backlog_api.py und legt die Merker selbst ab (richtiger Datenordner, richtige session_id, kein Netzwerk). Option B: Datenordner im Helfer ableiten (zerbrechlich, hängt am Installationspfad des Plugins). Option C: Ausnahme von Regel 2 für eine Viewer-Abfrage im Hook (verworfen: Regel gilt, und ein hängender Viewer würde das Turn-Ende verzögern).
- Doku (Hooks-Referenz von Claude Code): PostToolUse läuft nur nach erfolgreichen Tool-Aufrufen; ein fehlgeschlagener Helfer-Aufruf (Exit-Code ungleich 0) löst ihn nicht aus, das passt, weil dann nichts geschrieben wurde. Die Eingabe enthält session_id, tool_name, tool_input.command; die Antwort von Bash hat stdout, stderr, interrupted, isImage. Stop-Hooks bekommen stop_hook_active.
- Weil Befehl und Antwort allein nicht immer den Zustand verraten (put-doc auf Notes druckt nur 'saved', ein Befehl mit Eingabe aus einer Datei zeigt den Inhalt nicht im Befehl), druckt der Helfer nach jedem Schreiben von Notes eine maschinenlesbare Zeile auf stderr, die der Hook liest. Das ersetzt das Ablegen der Merker im Helfer.

### Decided

- Weg A: Ein PostToolUse-Hook auf Bash liest Befehl und Antwort von backlog_api.py und legt die Merker selbst ab; kein Netzwerk im Hook (Besitzer, 2026-10-22).
- Umsetzung (Vorschlag, mit dem Plan zu bestätigen): Der Helfer druckt Zeilen '[harness] notes-state <ID> <current|stale|missing>' und '[harness] active <ID>' und legt keine Merker mehr ab; Reminder B läuft über UserPromptSubmit (nie blockierend, Hinweis als Kontext), der Stop-Hook blockiert nur bei veraltetem oder fehlendem Kopf.

### Open

- Plan zur Freigabe vorlegen.
- Wie im Files-Modus 'aktiv' erkannt wird: Vorschlag Lesen von items/<ID>/<ID>_spec.md; der Notes-Eintrag (Zurücksetzen) ist dort das Ändern von <ID>_notes.md.
