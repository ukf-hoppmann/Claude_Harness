# EPIC-001 — Notes

## 2026-09-23 — Konfiguration im Plugin-Modell

Grundlage ist die Plugin-Architektur aus `EPIC-007`.

### Discussed

- Im Plugin-Modell entfällt das Rendern der Regeln in `CLAUDE.md`. Übrig
  bleiben echte Projektwerte, die Skills und Hooks nachschlagen.
- Varianten für Modul-Schalter (`STORY-003`):
  1. Ein Plugin pro Modul; abschalten = nicht installieren.
  2. Ein Plugin mit Schalterliste in der Projektkonfiguration.

### Decided

- `STORY-003`: Variante 2 — ein Plugin, Schalterliste in der
  Projektkonfiguration. Abgeschaltete Module prüfen den Schalter und werden
  nicht aktiv. Variante 1 bleibt möglich, falls die Zahl der Module stark
  wächst.
- Genehmigungsmodus und Rechte fallen aus der Konfiguration heraus; sie laufen
  über die nativen Claude-Code-Einstellungen.
- Validierung der Konfiguration per Hook beim Session-Start (`STORY-002`).
- `EPIC-005` wird nicht blockiert: `docs/todo/` ist fester Standard, bis die
  Konfiguration existiert.

### Open

- Ort und Format der Konfigurationsdatei (Vorschlag: `.claude/harness.toml`).
- Spätestens der Verify-Befehl aus `STORY-011` braucht die Konfiguration.

## 2026-09-23 — Config v1 umgesetzt

### Decided

- Ort: `.claude-harness/config.toml` im Projekt-Root. Der Harness bringt eine
  Vorlage mit (`plugin/templates/config.toml`), die `/claude-harness:init`
  verwendet (`STORY-021`).
- Schema v1: `version = 1`, `[modules]` mit `todo = true/false` (nicht
  aufgeführte Module sind aus), `[todo] path` relativ zum Projekt-Root,
  Standard `docs/todo`.
- Unbekannte Schlüssel, unbekannte Module, absolute Pfade und `..` sind
  Fehler. Die Config wird mit `tomllib` geladen (Python 3.11+).
- Die Validierung läuft beim Session-Start; Fehler landen als Hinweis im
  Kontext statt stillschweigend ignoriert zu werden.

### Open

- Weitere Felder (Verify-Befehle, Workspace-Regeln) kommen mit den jeweiligen
  Modulen dazu.

## 2026-09-23 — Doku-Wurzel, Sprache und Modul `daily`

### Decided

- Neue Tabelle `[docs]` mit `root` (Standard `docs`) und `language`
  (ISO 639-1, Standard `en`). Die Sprache gilt für alle erzeugten Dokumente,
  nicht für maschinell geprüfte Feldnamen.
- `[todo] path` ist jetzt relativ zu `docs.root` (Standard `todo`).
- Neues Modul `daily` mit `[daily] path` (Standard `development/daily`,
  relativ zu `docs.root`); Details in `STORY-013`.
- Die Config bleibt trotz geänderter Bedeutung von `todo.path` bei
  `version = 1`, da bisher nur dieses Repo sie nutzt.

## 2026-09-24 — Abschlusskriterien angepasst

### Discussed

- Das Schema ist umgesetzt, dokumentiert (`docs/techdocs/configuration.md`)
  und wird von den Hooks von `todo`, `daily` und `techdocs` gelesen. Offen
  waren nur Verify-Befehle und die Quelle der Workspace-Wahl; beide gehören
  inhaltlich zu `STORY-011` bzw. `STORY-006`.

### Decided

- Mit Zustimmung des Projekteigners: Verify-Befehle und Workspace-Quelle
  fallen aus `EPIC-001` und `STORY-001` heraus. Jedes Modul bringt seine
  Config-Felder selbst mit, dokumentiert sie in `configuration.md` und testet
  ihre Validierung.
- `STORY-011` und `STORY-006` haben diese Pflicht in ihren Abschlusskriterien.
- Neues Kriterium für `EPIC-001`: Schema validiert, dokumentiert und von den
  Hooks mehrerer Module tatsächlich gelesen und angewendet.
- `STORY-001` und `EPIC-001` damit auf `Awaiting confirmation`.
