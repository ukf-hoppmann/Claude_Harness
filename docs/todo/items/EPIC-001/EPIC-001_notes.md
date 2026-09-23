# EPIC-001 — Notes

## 2026-09-23 — Konfiguration im Plugin-Modell

Grundlage ist die Plugin-Architektur aus `EPIC-007`.

### Besprochen

- Im Plugin-Modell entfällt das Rendern der Regeln in `CLAUDE.md`. Übrig
  bleiben echte Projektwerte, die Skills und Hooks nachschlagen.
- Varianten für Modul-Schalter (`STORY-003`):
  1. Ein Plugin pro Modul; abschalten = nicht installieren.
  2. Ein Plugin mit Schalterliste in der Projektkonfiguration.

### Beschlossen

- `STORY-003`: Variante 2 — ein Plugin, Schalterliste in der
  Projektkonfiguration. Abgeschaltete Module prüfen den Schalter und werden
  nicht aktiv. Variante 1 bleibt möglich, falls die Zahl der Module stark
  wächst.
- Genehmigungsmodus und Rechte fallen aus der Konfiguration heraus; sie laufen
  über die nativen Claude-Code-Einstellungen.
- Validierung der Konfiguration per Hook beim Session-Start (`STORY-002`).
- `EPIC-005` wird nicht blockiert: `docs/todo/` ist fester Standard, bis die
  Konfiguration existiert.

### Offen

- Ort und Format der Konfigurationsdatei (Vorschlag: `.claude/harness.toml`).
- Spätestens der Verify-Befehl aus `STORY-011` braucht die Konfiguration.
