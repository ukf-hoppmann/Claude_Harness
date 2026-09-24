# STORY-019 — Notes

## 2026-09-24 — Ladestufen-Regel

### Discussed

- Die Regel ist eine Bauregel für den Harness (wohin gehört eine neue Regel),
  nicht eine Anweisung, wie zur Laufzeit geladen wird; das erledigt Claude
  Code selbst (Root-`CLAUDE.md`, Skill-Beschreibungen, SessionStart-Zeile).
  Deshalb gehört sie in `docs/development/architecture.md`, nicht in die
  Root-`CLAUDE.md`.
- Die Root-`CLAUDE.md` braucht keine Liste der Plugins: Skill-Beschreibungen
  und die Startzeile des Hooks sind ohnehin im Kontext.
- Unterordner-`CLAUDE.md` wird automatisch beim Arbeiten im Ordner geladen,
  aber das Lesen wird nicht geprüft und kann nach einer Komprimierung
  verschwinden. Architektur-Scopes decken denselben Zweck zentral und
  geprüft ab.

### Decided

- Regel als Abschnitt 7 „Load tiers“ in `docs/development/architecture.md`:
  fünf Fragen in fester Reihenfolge (Hook → Scope → Skill → Skript →
  Root-`CLAUDE.md`). Neuer Abschnitt am Ende, damit die Nummern der
  bestehenden Regeln stabil bleiben.
- Unterordner-`CLAUDE.md` nutzt der Harness vorerst nicht, weil Scopes das
  abdecken; bei Bedarf neu bewerten.
- Die Modul-Übersicht (welches Modul auf welcher Stufe und warum) steht als
  Übersicht für Menschen in `docs/techdocs/architecture.md`.
