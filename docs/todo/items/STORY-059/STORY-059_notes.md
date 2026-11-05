# STORY-059 — Techdocs als Zusammenfassung der development-Doku

## State

- Goal/Status: Regel freigegeben, Spec geschrieben; bereit zur Umsetzung (2026-11-05)
- Next step: Umsetzung in einer Sonnet-Session (2026-11-05)
- Open: keine (2026-11-05)
- Decided:
  - Allgemeine Regel für alle Projekte statt Überarbeitung dieses Repos; Kriterium 3 entfällt (2026-11-05)
  - Techdocs fassen zusammen und verlinken auf development, sonst vollständig; README, configuration, operations vollständig (2026-11-05)
  - README verweist auf alle Techdocs (2026-11-05)
  - Änderungen unter development/interfaces zählen für die Techdocs-Erinnerung (2026-11-05)
  - Sprache bleibt docs.language, im Init abgefragt (2026-11-05)
- References: Spec STORY-059_spec.md; EPIC-011 (2026-11-05)

State confirmed after entry 2026-11-05 — Regel für Techdocs freigegeben (1ae803986d2c)

## 2026-11-05 — Ziel der Story geklärt: allgemeine Regel für Techdocs

### Discussed

- Frage: Ist STORY-059 die Überarbeitung der Techdocs dieses Repos (Kriterium 3)? Befund: der Harness hat selbst keine development-Schnittstellen-Doku, die Techdocs könnten nichts zusammenfassen.
- Bisher laufen Techdocs (deutsch, für Menschen) und development-Doku (englisch, für die AI) parallel und duplizieren Inhalte.

### Decided

- Besitzer: Es geht um eine allgemeine Regel für alle Projekte, nicht um die Überarbeitung der Techdocs dieses Repos. Techdocs werden eine zusammenfassende Doku, die für konkrete Elemente (z. B. Schnittstellen) auf die englische development-Doku verlinkt, statt sie zu duplizieren.

### Open

- Kriterium 3 (Techdocs dieses Repos überarbeiten) streichen; Freigabe des Besitzers nötig.
- Regel je Dokument: was fasst zusammen und verlinkt, was bleibt vollständig.
- Ob Änderungen an der development-Doku die Techdocs-Erinnerung zum Schweigen bringen.
- Umgang mit bestehenden Projekten (schrittweise, nicht erzwungen).

## 2026-11-05 — Regel für Techdocs freigegeben

### Discussed

- Vorschlag: Techdocs sind die Übersicht für Menschen; Elemente, die die development-Doku beschreibt, werden zusammengefasst und verlinkt, sonst vollständig beschrieben. Je Dokument: README vollständig, architecture Überblick plus Links, interfaces Übersicht mit einer Zeile je Schnittstelle plus Link, configuration und operations vollständig.
- Sprache: docs.language ist schon konfigurierbar (ISO 639-1, Standard en) und wird im Skill init abgefragt; keine Änderung nötig.
- Techdocs-Erinnerung: Änderungen unter development/interfaces/** sollen als Doku-Pflege zählen.
- Bestehende Projekte: schrittweise Umstellung beim Bearbeiten, nichts erzwungen.

### Decided

- Besitzer hat den Regelvorschlag angenommen.
- Ergänzung des Besitzers: Die README verweist auf alle vorhandenen Techdocs, damit z. B. die Konfiguration auffindbar ist.
- Kriterium 3 (Techdocs dieses Repos überarbeiten) entfällt; ersetzt durch die Regel und ihre Prüfung.
- Sprache der Techdocs bleibt über docs.language konfigurierbar; keine Code-Änderung.
