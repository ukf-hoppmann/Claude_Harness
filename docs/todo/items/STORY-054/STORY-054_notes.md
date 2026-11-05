# STORY-054 — Pflichtlektüre je Scope

## State

- Goal/Status: Umgesetzt, gemergt in main, Release v0.12.12; wartet auf Bestätigung (2026-11-05)
- Next step: Bestätigung durch den Besitzer; danach STORY-057 (2026-11-05)
- Open: keine (2026-11-05)
- Decided: Spalte per Kopfzeile, ungültige Einträge verworfen, fehlende Dateien als (missing) genannt, Erweiterungspunkt counted_reads (2026-11-05)
- References: Commits 885f302, 86e8a0d; Release v0.12.12 (2026-11-05)

State confirmed after entry 2026-11-05 — Umsetzung ohne Abweichung von der Spec (68098e4fab2a)

## 2026-11-05 — Umsetzung ohne Abweichung von der Spec

### Discussed

- Spalte Required reading über die Kopfzeile erkannt; ungültige Einträge werden verworfen und gemeldet, der Scope bleibt gültig
- Fehlende Pflichtdateien bleiben im Hook verlangt und werden mit (missing) genannt
- Markierung über architecture.counted_reads(projects): Pflichtlektüre aller Projekte der Session plus geerbte Dateien; Erweiterungspunkt für STORY-057

### Decided

- Release v0.12.12 (patch: optionale Spalte in bestehendem Feature)
