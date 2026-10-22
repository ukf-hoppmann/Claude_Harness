# TASK-023 — Kopf-Befehle im API-Helfer

## State

- Goal/Status: Helfer-Befehle für den Notes-Kopf; Code und Tests fertig, Doku fertig, manuelle Prüfung gegen den Viewer läuft.
- Next step: Merge in main, dann TASK-023 auf Awaiting confirmation.
- Open:
  - Stimmt CLAUDE_CODE_SESSION_ID mit der session_id der Hooks überein? Prüfung in TASK-024 (2026-10-22)
- Decided:
  - Merker (notes, active) in TASK-023, wie in der Spec (2026-10-22)
- References: Spec TASK-023_spec.md; STORY-051; TASK-024 nutzt die Merker

State confirmed after entry 2026-10-22 — Umsetzung: Kopf-Befehle im API-Helfer (6effe9f2ce8f)

## 2026-10-22 — Umsetzung: Kopf-Befehle im API-Helfer

### Discussed

- Schnittstelle gegen den laufenden Viewer v0.9.0 geprüft: GET/PUT notes/state, POST notes/state/confirm, GET notes/entries, hints in den Antworten.
- Merker im Session-State: Der Helfer liest CLAUDE_CODE_SESSION_ID aus der Umgebung und legt Items mit geänderten Notes und aktive Items ab; ob die ID mit der session_id der Hooks übereinstimmt, prüft TASK-024.

### Decided

- Merker bleiben in TASK-023, wie in der Spec; Owner hat den Plan freigegeben (2026-10-22).

### Open

- Stimmt CLAUDE_CODE_SESSION_ID mit der session_id der Hooks überein? Prüfung in TASK-024.
