# STORY-012 — Notes

## 2026-09-23 — Umfang: Systemdoku mit Standardstruktur

Vorlage aus Agent_Harness: Kernregel `DOC-CORE`
(`rules/core/documentation.md`). Sie verlangt, Doku bei Änderungen an
Verhalten, Schnittstellen, Konfiguration, Daten, Installation, Betrieb,
Integrationen und Workflows im selben Change anzupassen, legt aber weder eine
Trivial-Schwelle noch eine Dokumentstruktur fest.

### Discussed

- Abgrenzung von drei Doku-Arten: Anforderungen (was gebaut werden soll) liegen
  im Backlog (Goal, Kriterien, Specs); die Chronik (was wann passiert ist) im
  Daily (`STORY-013`); die Systemdoku (wie das System jetzt ist) ist Thema
  dieser Story. Ein Pflichtenheft ist sie nicht.
- Variante 1: nur die Pflichtregel, Dokumente wählt das Projekt selbst.
  Variante 2: Pflichtregel plus schlanke Standardstruktur mit Vorlagen.

### Decided

- Variante 2. Begründung: Die Pflicht „Doku anpassen“ ist nur prüfbar, wenn
  feststeht, welches Dokument zu welcher Art Änderung gehört. Die Struktur
  bleibt schlank und pro Projekt anpassbar.
- Goal und Completion criteria entsprechend erweitert (mit Zustimmung des
  Projekteigners).

## 2026-09-23 — Struktur, Zuordnung und Durchsetzung

### Decided

- Umsetzung als Modul `techdocs` (in der Config-Vorlage eingeschaltet), passend
  zu den schaltbaren Modulen aus `STORY-003`. `docs` scheidet als Name aus,
  weil `[docs]` schon Wurzel und Sprache enthält.
- Ablage in einem eigenen Unterordner `<docs.root>/techdocs/` (konfigurierbar
  über `[techdocs] path`), analog zu `todo`. Die README bleibt im
  Projekt-Root.
- Dokumentarten mit festen Dateinamen `<Art>.md`: `architecture`,
  `interfaces`, `configuration`, `operations`. Das Projekt listet in
  `[techdocs] documents`, welche es hat; `readme` ist immer dabei.
- Die Dokumente beschreiben nur den aktuellen Zustand; Verlauf steht im Daily,
  Begründungen in den Backlog-Notizen.
- Zuordnung Änderungsart → Dokument und Trivial-Schwelle wie vorgeschlagen
  (Details in der Spec).
- Durchsetzung: Skill `techdocs` plus Stop-Hook, der einmal pro Session
  erinnert, wenn Projektdateien geändert wurden, aber keine Systemdoku. Die
  Systemdoku gehört in denselben Change (auch im Worktree), anders als das
  Daily.
- Dieses Repo bekommt `README.md` und `docs/techdocs/architecture.md`,
  `interfaces.md`, `configuration.md`; `operations` entfällt.
- Details: `STORY-012_spec.md`.
