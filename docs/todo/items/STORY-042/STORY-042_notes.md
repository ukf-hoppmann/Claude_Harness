# STORY-042 — Backlog-Backend je Umgebung umschalten

## 2026-10-16 — Cloud-Erkennung ist dokumentiert

### Discussed

- Die Doku der Cloud-Umgebungen (geprüft 2026-10-16) sagt: Die Session-VM trägt CLAUDE_CODE_REMOTE=true, lokal ist die Variable nie true.

### Open

- Vorschlag für Kriterium 5: Die Cloud wird automatisch über CLAUDE_CODE_REMOTE=true erkannt (dann Dateimodus), und CLAUDE_HARNESS_TODO_BACKEND bleibt als Übersteuerung. Das ändert die Abnahmekriterien; der Besitzer entscheidet.
