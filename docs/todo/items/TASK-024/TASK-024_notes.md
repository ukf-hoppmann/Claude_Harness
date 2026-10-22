# TASK-024 — Hooks für aktuellen Notes-Kopf und Protokoll-Reminder

## State

- Goal/Status: Hooks für aktuellen Notes-Kopf (API-Modus) und Protokoll-Reminder (beide Modi). Umgesetzt, bestätigt (Completed), im echten Lauf belegt.
- Next step: Keiner; ältere Merker in state.py haben dieselbe Schwäche ohne Sperre (kein Item).
- Open:
  - Ältere Merker in state.py (dirty-Marke, geänderte Notes, Hinweise) ohne Sperre
- Decided:
  - Weg A: PostToolUse-Hook auf Bash legt die Merker ab, kein Netzwerk im Hook (2026-10-22)
  - Helfer meldet Zustand und aktives Item als [harness]-Zeilen, legt nichts mehr ab (2026-10-22)
  - Reminder über UserPromptSubmit, nie blockierend; Files-Modus über Lesen der Spec und Ändern der Notes-Datei (2026-10-22)
  - Echter Lauf bestanden; Merker-Datei wird gesperrt und atomar ersetzt, weil Hooks paralleler Aufrufe gleichzeitig laufen (2026-10-22)
- References: Spec TASK-024_spec.md; STORY-051 (Spec, Notes); TASK-022, TASK-023; Architekturregel 2

State confirmed after entry 2026-10-22 — Echter Hook-Lauf in einer frisch gestarteten Session (41b8349e6a9b)

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

## 2026-10-22 — Umsetzung

### Discussed

- Plan vom Owner freigegeben; Umsetzung im Worktree task-024-notes-hooks in sieben Commits, Tests jeweils vorweg (636 Tests grün, vorher 580).
- Helfer backlog_api.py: legt keine Merker mehr ab; druckt nach jedem erfolgreichen Schreiben von Notes (note, put-state, confirm-state, put-doc auf Notes) '[harness] notes-state <ID> <current|stale|missing>' (Zustand aus der Antwort, sonst aus den Hinweisen) und '[harness] active <ID>' bei update auf In progress, reopen und beim Lesen der Spec; nichts bei --source. Die bisherigen Tests der Merker sind ersetzt, vier Tests, die leeres stderr verlangten, ignorieren jetzt diese Zeilen.
- state.py: neuer Merker-Speicher notes-marks-<Session>.json (Projekt und ID → Zustand des Kopfs, Zähler); add_item/read_items/items_file entfallen.
- Neue Hooks: mark_notes_state.py (PostToolUse Bash, liest Befehl und Antwort, kein Netzwerk), check_notes_state.py (Stop, blockiert bei stale oder missing, beachtet stop_hook_active, nur Backend api), remind_notes.py (UserPromptSubmit, nach 5, 10, 15 … Prompts ohne Notes-Eintrag, nie blockierend, beide Backends), mark_active_item.py (PostToolUse Read, Files-Modus: Lesen der Spec macht aktiv); mark_backlog_dirty.py setzt den Zähler beim Ändern der Notes-Datei zurück. Alle in hooks.json registriert; die Cloud-Kopie übernimmt sie (Tests der Kopie grün).
- Abweichung vom Plan: Das Zurücksetzen des Zählers geschieht bei jedem Notes-Schreibvorgang des Helfers (auch put-state/confirm-state), weil die Meldung des Helfers Eintrag und Kopf nicht unterscheidet; das ist großzügiger als 'nur ein Eintrag'. Der Reminder-Text wurde nach dem Handlauf klarer formuliert.
- Handlauf gegen den echten Viewer mit nachgestellter Hook-Eingabe: doc der Spec → '[harness] active TASK-024'; fünf Prompts → Erinnerung erst beim fünften; confirm-state gegen den echten Viewer → '[harness] notes-state TASK-024 current', der Stop-Hook gibt frei, der Zähler beginnt neu; ein gemeldetes stale blockiert, current gibt frei. Echte Antworten des Viewers tragen 'state' (put-state/confirm-state) bzw. 'notes_state' (note); beides wird gelesen.
- Doku: interfaces.md (Hook-Tabelle, Zeilen des Helfers), architecture.md (Notes-Zeilen, Merker), Skill todo (api.md, SKILL.md: Bedeutung von Blockade und Erinnerung).

### Decided

- Kriterien erfüllt (beide Hooks umgesetzt, registriert, dokumentiert, getestet; Endlosschleife ausgeschlossen); Status Awaiting confirmation. Kein Release: STORY-051 hält das Harness-Release bis zum Ende der Story.

### Open

- Die neuen Hooks greifen erst nach einem Neuladen des Plugins; der Lauf mit den echten Hooks (Block am Turn-Ende, Erinnerung als Kontext, Form der Bash-Antwort in tool_response) ist in einer neuen Session zu prüfen. Die Form von tool_response (stdout/stderr) stammt aus der Doku von Claude Code, nicht aus einem echten Lauf.
- Das Zurücksetzen des Zählers auch bei put-state und confirm-state ist eine Vereinfachung; ein feinerer Unterschied bräuchte eine zweite Zeile des Helfers.

## 2026-10-22 — Hook-Test

### Discussed

- Testeintrag des echten Hook-Laufs (STORY-051); darf ignoriert werden.

## 2026-10-22 — Echter Hook-Lauf in einer frisch gestarteten Session

### Discussed

- Der Owner wollte die offenen Läufe als Test sehen. In einer neuen lokalen Session (Plugin v0.12.6 geladen) lief der Test: Spec von TASK-024 lesen, einen Testeintrag in diese Notes schreiben (Eintrag 'Hook-Test' im Protokoll, bleibt stehen), Turn ohne Bestätigung beenden, dann bestätigen, danach fünf Prompts.
- Beobachtet, wie erwartet: nach 'note' druckte der Helfer '[harness] notes-state TASK-024 stale', der Merker 'stale' lag im Datenordner der Hooks; der Stop-Hook blockierte mit 'Claude_Harness notes check: the head of these notes is not current …' und nannte TASK-024; nach 'confirm-state' meldete der Helfer 'current' und der Hook gab frei. Fünf Prompts nach dem Aktivieren: kein Hinweis bei den Prompts 1 bis 4, bei Prompt 5 'Claude_Harness reminder: no notes entry yet for the active items TASK-024 (5 turns), TASK-025 (5 turns). …' als Kontext.
- Echte Eingabe von PostToolUse (mit einem Debug-Dump aufgezeichnet, danach wieder entfernt): tool_response hat stdout, stderr, interrupted, isImage, noOutputExpected; stderr ist immer leer, die stderr-Zeilen des Helfers stehen in stdout. Das Lesen beider Felder hat das abgedeckt. Dazu kommen session_id, cwd, prompt_id, permission_mode, tool_use_id und duration_ms.
- Befund: Im ersten Durchlauf fehlte der Merker 'aktiv' nach 'doc' (und die Merker-Datei war nach dem 'note' ohne 'turns'). Ursache: Claude Code führt die Hooks paralleler Bash-Aufrufe gleichzeitig aus, und das Lesen, Ändern und Schreiben der Merker-Datei war nicht gesperrt; ein gleichzeitiger Schreibvorgang überschrieb den anderen. In einem Nachstellversuch mit gleichzeitigen Hook-Prozessen wurde die Datei sogar halb geschrieben (ungültiges JSON, das als leer gelesen wird).
- Behebung (ed809ae): state.edit_notes_marks sperrt (fcntl.flock) und ersetzt die Datei atomar (temporäre Datei, os.replace); mark_notes_state.py, mark_active_item.py, remind_notes.py und mark_backlog_dirty.py nutzen es. Tests: Unit-Test mit zwölf parallelen Prozessen, Hook-Test mit zwölf parallelen Aufrufen; der Nachstellversuch verlor danach in 60 Läufen keinen Merker (vorher Fehler in jedem Lauf mit beschädigter Datei). 642 Tests grün. Die gleiche Schwäche haben die älteren Merker der Backlog-Prüfung (dirty, geänderte Notes) in state.py; sie sind hier nicht angefasst.

### Decided

- Die Hooks sind in einer echten Session belegt: Merker, Stop-Block, Freigabe und Reminder nach fünf Prompts. Der Fund mit den parallelen Aufrufen ist behoben.

### Open

- Die älteren Merker in state.py (dirty-Marke des Backlogs, geänderte Notes, Hinweise gemeldet) lesen und schreiben ebenfalls ohne Sperre; bei parallelen Aufrufen kann dort ein Eintrag verloren gehen. Ein eigenes Item wurde nicht angelegt.
- Die Testsession läuft noch (idle) und kann archiviert werden; sie hat nichts geändert außer dem Testeintrag in diesen Notes.
