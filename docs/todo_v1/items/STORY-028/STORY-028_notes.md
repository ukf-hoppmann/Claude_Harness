# STORY-028 – Notizen

## Summary
Pfade und Verweise auf Configs/DBs/Services gehören in eine Config statt
hartkodiert in den Code, außer sie sind bewusst und erkennbar fix.

## Discussed (2026-09-25)
- Entstanden aus der Diskussion zu STORY-016 (Secrets): Owner will
  grundsätzlich auch Pfade nicht fest im Code, da sich die meisten
  (Configs, DBs) zwischen Umgebungen ändern können. Seltene Ausnahme:
  bewusst fixe Pfade/URLs.
- Getrennt von STORY-016 gehalten, da anderer Grund (Maintainability statt
  Security) und andere Ausnahmeregel.
- Priorität als `Normal` gesetzt (neuer neutraler Standardwert; Owner hat
  dafür `Planned` in `Normal` umbenannt und das Backlog-Format entsprechend
  angepasst, Commit `4834f24`).

## Decided (2026-09-25)
- Regel als Abschnitt "8. Paths and configuration values" in
  `docs/development/architecture.md` aufgenommen (bindend, vom
  Architecture-Hook vor jeder Code-Änderung gelesen).
- Status auf `Awaiting confirmation` gesetzt, da die Regel vollständig
  dokumentiert ist.
