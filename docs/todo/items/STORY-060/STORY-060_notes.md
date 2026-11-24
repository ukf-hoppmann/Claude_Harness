# STORY-060 — Notes heißen Memos: Harness an den umbenannten Viewer anpassen

## State

- Goal/Status: Harness auf Memo und Hint des Viewers umgestellt; Code, Skill, Tests und Techdocs im Branch, alle Tests grün (2026-11-12)
- Next step: Commit, Merge nach main, Release 0.14.0, Daily-Report, dann Bestätigung durch den Owner (2026-11-12)
- Open: Cloud-Kopie anderer Projekte neu exportieren; alte NOTE-Verweise in Texten bleiben (2026-11-12)
- Decided: Name Hint übernommen, kein MCP-Wechsel, alter Ordner notes/ entfernt (2026-11-12)
- References: ToDo_viewer/docs/handover/memo-umstellung.md

State confirmed after entry 2026-11-12 — Umstellung auf Memos: Umfang und Entscheidungen (b9ac43cf5670)

## 2026-11-12 — Umstellung auf Memos: Umfang und Entscheidungen

### Discussed

- Grundlage: ToDo_viewer/docs/handover/memo-umstellung.md. Der Viewer kennt /api/notes nicht mehr, nur /api/memos; Spiegelordner memos/, Labels MEMO-nnn.
- Umbenannt: notes_api.py, notes_files.py, notes_format.py, die Skill-Dateien notes*.md und die Tests samt Fixtures zu memos*. Befehle: notices -> hints, notes-of-item -> memos-of-item, note-entry -> memo-entry.
- Fixtures memos-format sind Kopien aus dem Viewer (tests/fixtures/mirror-v2).
- Unverändert, weil sie die Item-Notizen betreffen: backlog_api.py, backlog.py, check_notes_state.py, mark_notes_state.py, remind_notes.py, notes_head.py, notes_hint.py, mark_active_item.py. Die Harness-eigenen notices (backlog.py, check_backlog.py) sind etwas anderes als der Hint des Viewers und bleiben.

### Decided

- Übernommen wird der Name Hint wie vom Viewer; eine spätere Umbenennung (Vorschlag Advisory) folgt dem Viewer.
- Kein Wechsel auf MCP: der Harness bleibt bei den HTTP-Helfern.
- Alter Ordner docs/todo/notes/ wird im Branch entfernt; die Memos liegen jetzt in docs/todo/memos/.

### Open

- Verweise NOTE-nnn in alten Backlog-Texten und Daily-Reports bleiben stehen, auch im Viewer.
- Eine Kopie des Harness im Projekt (.claude-harness/runtime) gibt es hier nicht; für andere Projekte mit Cloud-Kopie muss cloud_export.py neu laufen.
