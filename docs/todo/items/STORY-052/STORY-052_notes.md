# STORY-052 — Branch-Stand beim Start einer Cloud-Session mit origin abgleichen

## State

- Goal/Status: Cloud-Session gleicht beim Start den Branch mit origin ab oder meldet die Abweichung. Umgesetzt und released (v0.12.8, nicht gepusht); Kriterien 1 bis 6 erfüllt, Kriterium 7 offen.
- Next step: Harness pushen, in ezf-ui /claude-harness:update ausführen und committen, dann eine Cloud-Session starten und die Zeile prüfen.
- Open:
  - Kriterium 7: Lauf in einer echten Cloud-Session (2026-11-04)
  - Ursache in ezf-ui belegen: Rebase/Force-Push oder alter Cache (2026-11-04)
- Decided:
  - Logik in cloud_sync.py, Aufruf zu Beginn von session_start.py (2026-11-04)
  - Abschaltbar über cloud.sync, Standard true (2026-11-04)
  - Nie überschreiben, reset --hard nur auf Rückfrage, kein --unshallow (2026-11-04)
  - Ausnahme von Architekturregel 2 und 5 für Cloud-Sessions freigegeben (2026-11-04)
  - Release als Patch v0.12.8 (2026-11-04)
- References: STORY-052_spec.md; EPIC-010; STORY-047; Merge 5968aba; docs/daily/2026-11-04_daily.md

State confirmed after entry 2026-11-04 — Umgesetzt und released (v0.12.8) (cf94fedb7d64)

## 2026-11-04 — Anlass, Ort der Lösung und Architektur-Ausnahme

### Discussed

- Anlass: Cloud-Session von ezf-ui startete auf gecachtem Shallow Clone vom 2026-11-02, origin 86 Commits weiter, kein gemeinsamer Vorfahr. Der Session-Start der Kopie gleicht den Branch nicht ab.
- Ort: eigener Hook in hooks.json (läuft parallel zu session_start.py, Reihenfolge nicht gesichert) gegen Aufruf als erster Schritt in session_start.py (Reihenfolge gesichert). Setup-Skript der Cloud-Umgebung verworfen: pro Projekt von Hand, nicht im Plugin.
- Konflikt: git fetch verletzt Architekturregel 2 (kein Netz), git merge --ff-only Regel 5 (nicht ins Projekt schreiben).

### Decided

- Abgleich in plugin/scripts/cloud_sync.py, aufgerufen zu Beginn von session_start.py, nur in Cloud-Sessions beim Start.
- Abschaltbar über cloud.sync (Standard true).
- Nie überschreiben; git reset --hard nur nach Rückfrage beim Nutzer; kein --unshallow.
- Der Besitzer gibt die auf Cloud-Sessions begrenzte Ausnahme von Regel 2 und 5 frei; sie wird in architecture.md festgehalten.

### Open

- Ursache in ezf-ui belegen (Rebase/Force-Push oder alter Cache): Commit-Texte beider Stände vergleichen.

## 2026-11-04 — Umgesetzt und released (v0.12.8)

### Discussed

- Umsetzung im Worktree in vier Abschnitten: Architektur-Ausnahme (6afacad), cloud.sync (76278f1), cloud_sync.py mit Tests gegen ein lokales Bare-Repo (dda7deb), Einbindung in session_start.py samt Techdocs und README (a7da016), Ende-zu-Ende-Test des exportierten SessionStart-Befehls (4db25ec). Merge 5968aba, Release v0.12.8 (6c8b9f1), nicht gepusht.
- Abweichung vom Plan: Patch statt Minor, weil die SemVer-Regeln eine neue Einstellung und Teilfunktion einer bestehenden Funktion als Patch einstufen.
- Detail: Nach einem Abgleich liest der Session-Start Config und Dokumente neu, damit seine Zeilen den neuen Stand zeigen. Git läuft in einer eigenen Prozessgruppe, damit ein Zeitlimit auch ssh oder https-Helfer beendet.

### Decided

- Kriterien 1 bis 6 erfüllt und mit Tests belegt (Suite 667 Tests OK, dazu 2 Ende-zu-Ende-Tests).

### Open

- Kriterium 7: Lauf in einer echten Cloud-Session; braucht Push des Harness und /claude-harness:update in ezf-ui.
