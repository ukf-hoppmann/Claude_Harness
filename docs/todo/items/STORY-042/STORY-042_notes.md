# STORY-042 — Backlog-Backend je Umgebung umschalten

## 2026-10-16 — Cloud-Erkennung ist dokumentiert

### Discussed

- Die Doku der Cloud-Umgebungen (geprüft 2026-10-16) sagt: Die Session-VM trägt CLAUDE_CODE_REMOTE=true, lokal ist die Variable nie true.

### Open

- Vorschlag für Kriterium 5: Die Cloud wird automatisch über CLAUDE_CODE_REMOTE=true erkannt (dann Dateimodus), und CLAUDE_HARNESS_TODO_BACKEND bleibt als Übersteuerung. Das ändert die Abnahmekriterien; der Besitzer entscheidet.

## 2026-10-16 — Entscheidung: Cloud-Erkennung über CLAUDE_CODE_REMOTE

### Discussed

- Mit dem Beschluss für Weg A (STORY-047) nutzen die in der Cloud eingecheckten Hooks ohnehin CLAUDE_CODE_REMOTE=true als Wächter.

### Decided

- Der Besitzer entscheidet am 2026-10-16: Die Cloud wird automatisch über CLAUDE_CODE_REMOTE=true erkannt und arbeitet dann im Dateimodus. Rangfolge: CLAUDE_HARNESS_TODO_BACKEND vor der Cloud-Erkennung vor [todo].backend. Kriterium 5 der Story ist entsprechend umgeschrieben.

### Open

- Umsetzung steht aus; STORY-047 läuft zuerst und ist unabhängig davon baubar.
