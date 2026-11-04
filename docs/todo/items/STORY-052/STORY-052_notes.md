# STORY-052 — Branch-Stand beim Start einer Cloud-Session mit origin abgleichen

## State

- Goal/Status: Cloud-Session gleicht beim Start den Branch mit origin ab oder meldet die Abweichung. Spec steht, Umsetzung offen.
- Next step: Umsetzung planen (Skill decomposition) und im Worktree umsetzen.
- Open:
  - Ursache in ezf-ui belegen: Rebase/Force-Push oder alter Cache (2026-11-04)
- Decided:
  - Logik in cloud_sync.py, Aufruf zu Beginn von session_start.py (2026-11-04)
  - Abschaltbar über cloud.sync, Standard true (2026-11-04)
  - Nie überschreiben, reset --hard nur auf Rückfrage, kein --unshallow (2026-11-04)
  - Ausnahme von Architekturregel 2 und 5 für Cloud-Sessions freigegeben (2026-11-04)
- References: STORY-052_spec.md; EPIC-010; STORY-047

State confirmed after entry 2026-11-04 — Anlass, Ort der Lösung und Architektur-Ausnahme (66160be8069a)

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
