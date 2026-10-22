# TASK-024 — Spec: Hooks für aktuellen Notes-Kopf und Protokoll-Reminder

Grundlage: STORY-051_spec.md (Absicherung des Kopfs). Nutzt die Funktionen aus TASK-022 (`notes_head.py`, Files-Modus) und die Kopf-Befehle aus TASK-023 (`backlog_api.py`). Entscheidung vom 2026-10-22 (Weg A, Notes dieses Items): Die Hooks fragen den Viewer nie ab (Architekturregel 2); ein PostToolUse-Hook liest Befehl und Antwort des Helfers und legt die Merker selbst ab.

## Umfang

### Meldungen des Helfers (`backlog_api.py`)

- Nach jedem erfolgreichen Schreiben von Notes (`note`, `put-state`, `confirm-state`, `put-doc` auf `<ID>_notes.md`) druckt der Helfer auf stderr eine Zeile `[harness] notes-state <ID> <current|stale|missing>`. Der Zustand kommt aus `notes_state` der Antwort; fehlt das Feld (`put-doc`), aus den Hinweisen der Antwort (`notes_state_stale` → `stale`, ohne diesen Hinweis `current`).
- Setzt ein Aufruf ein Item auf `In progress` (`update`, `reopen`) oder liest er dessen Spec (`doc <ID> <ID>_spec.md`), druckt der Helfer `[harness] active <ID>`.
- Der Helfer legt keine Merker mehr im Session-State ab (`_remember_in`, `add_item`/`read_items` in `state.py` und der Test `test_session_remembers_changed_notes_and_active_items` entfallen). `CLAUDE_CODE_SESSION_ID` braucht er nicht mehr.
- Mit `--source` (anderes Projekt) druckt er die Zeilen nicht.

### Merker setzen (PostToolUse auf `Bash`)

- Neues Skript `mark_notes_state.py`. Es wertet nur Aufrufe von `backlog_api.py` aus (Befehlstext, mit `--project <Name>` das Projekt, sonst das Root-Projekt) und liest die `[harness]`-Zeilen aus `tool_response.stdout`/`stderr`. Es nutzt `session_id` der Hook-Eingabe und schreibt über `state.py` in den Datenordner der Hooks; kein Netzwerk.
- Merker je Projekt und Item: Zustand des Kopfs (`current`/`stale`/`missing`), Item aktiv, Zähler „Turns seit dem letzten Notes-Eintrag“. Ein Notes-Eintrag (`notes-state`-Zeile) setzt den Zähler des Items auf 0, `active` legt den Zähler mit 0 an, wenn er fehlt.
- Läuft nur bei Modul `todo` und wirksamem Backend `api`; sonst sofort Exit 0. Ein fehlgeschlagener Helfer-Aufruf löst PostToolUse nicht aus; es entsteht kein Merker.

### Stop-Hook Kopf (API-Modus)

- Neues Skript `check_notes_state.py`: blockiert das Turn-Ende (Exit 2), solange ein in der Session geänderter Eintrag den Zustand `stale` oder `missing` hat; Meldung wie im Files-Modus: Kopf ansehen, anpassen (`put-state`) oder bestätigen (`confirm-state`), mit Verweis auf `format.md`, Abschnitt Notes. Kein Merker für `current`. Kennt der Viewer keine Köpfe oder ist er nicht erreichbar, schlägt der Helfer fehl und es entsteht kein Merker: es wird nicht blockiert.
- `stop_hook_active` wird beachtet (nicht blockieren, wenn der Hook schon weiterläuft). Endlosschleife ausgeschlossen: Bestätigen oder Ersetzen setzt den Zustand auf `current`.
- Nur Modul `todo` und Backend `api` (der Files-Modus läuft über `check_backlog.py`).

### Reminder B (beide Modi, nie blockierend)

- Neues Skript `remind_notes.py` auf `UserPromptSubmit`: Jeder Prompt zählt für jedes aktive Item den Zähler um 1 hoch. Bei 5, 10, 15, … gibt der Hook auf stdout (als Kontext, Exit 0) eine kurze Erinnerung aus: „Aktives Item TASK-x: seit 5 Turns kein Notes-Eintrag. Gab es Klärungen, Entscheidungen oder verworfene Optionen? Dann jetzt ins Protokoll (Skill todo).“ Höchstens eine Meldung je Item und 5 Turns.
- Aktiv ist ein Item, das in der Session auf `In progress` gesetzt oder dessen Spec gelesen wurde.
- Files-Modus: Der Merker kommt aus Dateizugriffen: Lesen von `items/<ID>/<ID>_spec.md` macht das Item aktiv, Ändern von `items/<ID>/<ID>_notes.md` ist der Notes-Eintrag (Zähler 0). Dafür liest ein kleiner Hook `mark_active_item.py` auf `Read` die Spec; `mark_backlog_dirty.py` setzt beim Ändern der Notes-Datei den Zähler zurück.
- Nur Modul `todo`; in beiden Backends je nach Merker.

### Registrierung und Doku

- `plugin/hooks/hooks.json`: PostToolUse `Bash` → `mark_notes_state.py`; PostToolUse `Read` → `mark_active_item.py`; Stop → `check_notes_state.py`; UserPromptSubmit → `remind_notes.py`.
- Techdocs: `interfaces.md` (Hook-Tabelle, Zeilen `[harness]` des Helfers), `architecture.md` (Komponente, Ladestufen-Tabelle). Skill `todo` (`api.md`: die `[harness]`-Zeilen; `SKILL.md`: was Blockade und Erinnerung bedeuten).

## Abnahme

- Unit-/Integrationstests: Helfer druckt die Zeilen (alle vier Notes-Schreibbefehle, `update`/`reopen`/Spec lesen, nicht bei `--source`); `mark_notes_state.py` legt Merker aus Befehl und Antwort ab (richtiges Projekt, ignoriert fremde Befehle und fehlerhafte Antworten); `check_notes_state.py` blockiert bei `stale`/`missing` nur für in der Session geänderte Notes, nicht bei `current`, nicht ohne Merker, nicht bei `stop_hook_active`, nicht bei Backend `files`; Reminder nach 5 Turns, nicht davor, nie blockierend, einmal je 5 Turns, zurückgesetzt durch einen Notes-Eintrag; Files-Modus über Dateizugriffe.
- Handlauf in einer echten Session: Nach dem Neuladen des Plugins blockiert das Turn-Ende bei einer Notes-Änderung mit veraltetem Kopf und gibt nach `confirm-state` frei (Prüfung ausstehend, braucht neue Session mit den neuen Hooks).
