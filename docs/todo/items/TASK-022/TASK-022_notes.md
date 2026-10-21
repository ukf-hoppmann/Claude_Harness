# TASK-022 — Kopf-Prüfsumme im Files-Modus

## Stand

- Goal/Status: Kopf-Prüfsumme im Files-Modus umgesetzt; wartet auf Bestätigung.
- Next step: Owner bestätigt; danach TASK-025.
- Open: nichts
- Decided:
  - Neues Modul notes_head.py (Zerlegen, Prüfsumme, Zustand, Bestätigen, Hinweise) mit den Testvektoren des ToDo-Viewers (2026-10-21)
  - backlog.py --confirm-state <ID> setzt nur die Stempelzeile (2026-10-21)
  - Prüfung am Turn-Ende blockiert bei stale/missing für in der Session geänderte Notes; langer Kopf und umgeschriebenes Protokoll als einmalige Hinweise (2026-10-21)
  - Protokollvergleich normalisiert Zeilenenden und Leerzeilen am Eintragsende (2026-10-21)
- References: Spec TASK-022_spec.md; Story STORY-051; tests/fixtures/notes-state/checksum.json

Stand bestätigt nach Eintrag 2026-10-21 — Umsetzung (3a78e5fbe0b1)

## 2026-10-21 — Umsetzung

### Discussed

- Plan vom Owner freigegeben; Umsetzung im Worktree TASK-022 in vier Abschnitten, Tests jeweils vorweg.
- notes_head.py: split, canonical, checksum, state_of, last_entry, confirmed, decided_count, history_rewritten. Testvektoren nach tests/fixtures/notes-state/checksum.json kopiert; alle 8 und das Beispiel aus format.md stimmen.
- backlog.py --confirm-state <ID>: liest und schreibt mit newline='' (Zeilenenden bleiben), Exit 1 ohne Notes, ohne Kopf oder ohne Eintrag, Exit 2 bei falschem Aufruf.
- mark_backlog_dirty.py merkt sich geänderte Notes-Dateien (state.read_changed_notes/write_changed_notes); check_backlog.py prüft deren Kopf.
- Abweichung vom Plan: Hinweise (langer Kopf, umgeschriebenes Protokoll) laufen über den vorhandenen Mechanismus 'einmal pro Session'; dabei hält der Stop-Hook den Turn einmal an, sonst sieht die KI sie nicht.
- history_rewritten vergleicht normalisiert (Zeilenenden, Leerzeichen am Zeilenende, Leerzeilen am Eintragsende), weil Anhängen meist eine Leerzeile an den vorherigen Eintrag hängt. Der ToDo-Viewer vergleicht exakt; dort könnte put-doc mit angehängtem Eintrag fälschlich notes_history_rewritten melden.
- decided_count zählt verschachtelte Punkte mit, wie der ToDo-Viewer.
- Doku: interfaces.md (backlog.py, Hooks), format.md (Bestätigen im Files-Modus). cloud_export kopiert den ganzen scripts-Ordner, nichts zu tun.
- Tests: 468 OK.
