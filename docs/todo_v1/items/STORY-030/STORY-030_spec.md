# STORY-030 — Harness-Konfiguration aktualisieren

## Was und warum

Projekte, die den Harness schon nutzen, haben keine Möglichkeit, ihre
`.claude-harness/config.toml` gegen den aktuellen Stand des Harness prüfen und
auffüllen zu lassen, außer die Datei manuell mit dem Template zu vergleichen.
Ein `update`-Skill (Pendant zu `init`) soll das übernehmen: Owner sagt "update
den Harness", der Skill prüft die Config und trägt fehlende Ergänzungen nach
Freigabe ein.

Dafür braucht es einen Mechanismus, der erkennt, *dass* und *was* sich am
Config-Schema geändert hat. Bisher ist `CONFIG_VERSION` in `harness_config.py`
eine einzelne Zahl, die exakt mit `version` in der Config übereinstimmen muss
(`parse_config`); jede Abweichung ist heute ein harter Fehler ohne
Unterscheidung zwischen "veraltet, reparierbar" und "kaputt".

## Entscheidung: Integer-Version + Migrationsliste statt SemVer

Siehe `STORY-030_notes.md`, Abschnitt "Decided" vom 2026-09-25. Kurz: ein
Integer-Schema-Level mit einer Migrationsliste (`from_version → to_version`,
Kurzbeschreibung, optional eine Transformationsfunktion) reicht, weil es genau
einen Konsumenten gibt (den Harness selbst) und additive Änderungen ohnehin
keinen Versionsbump brauchen.

## Constraints

- Architekturregel 4 (`docs/development/architecture.md`): jeder
  Configuration-Key bleibt in `harness_config.py` validiert; unbekannte Keys
  bleiben Fehler.
- Architekturregel 5: Dokumente/Configs im Projekt werden von der KI gemäß
  Skill geschrieben, nicht von einem Hook generiert. Der `update`-Skill
  schreibt `.claude-harness/config.toml` also selbst (wie `init`), nicht ein
  Skript, damit Kommentare und Formatierung der Datei erhalten bleiben.
- Architekturregel 9 (Ladestufen): die deterministische Prüfung (aktuelle vs.
  Ziel-Version, welche Migrationen fehlen) ist ein Skript, das der Skill und
  der Session-Start-Hook aufrufen; der Hinweis "Config ist veraltet" MUSS ein
  Hook sein (Regel 9.1: darf nie vergessen werden), nicht nur im Skill stehen.
- Kein echter Breaking Change am Schema wird durch diese Story erzwungen: die
  Migrationsliste startet leer; `CONFIG_VERSION` bleibt vorerst 1. Der
  Mechanismus wird durch Tests mit einer synthetischen Migration abgedeckt,
  nicht durch eine unnötige echte Schemaänderung.
- Scope: ein Aufruf aktualisiert die Config des einen gewählten Projekts
  (Root oder ein registriertes Subprojekt, gleiche Auswahl wie bei `init`),
  kein automatischer Durchlauf über alle registrierten Subprojekte in einem
  Aufruf.

## Betroffene Dateien (voraussichtlich)

- `plugin/scripts/harness_config.py`: Migrationsrahmen (Datentyp, Liste,
  Auflösefunktion), Unterscheidung "veraltet" vs. "ungültig".
- `plugin/scripts/session_start.py`: eigene Hook-Zeile für eine veraltete
  (aber migrierbare) Config statt der generischen Fehlermeldung.
- `plugin/skills/update/SKILL.md` (neu): Ablauf analog `plugin/skills/init/SKILL.md`.
- `docs/techdocs/` (dieses Repo) und ggf. `plugin/templates/techdocs/`:
  Erwähnung des neuen Skills/Befehls.
- Tests: `tests/test_config.py`, `tests/test_session_start.py` (Namen laut
  bestehender Testsuite prüfen).

## Acceptance criteria

- Eine Config mit veralteter, aber migrierbarer Version wird vom
  Migrationsrahmen erkannt; die fehlenden Schritte lassen sich programmatisch
  auflisten (Beschreibungstexte).
- Der Session-Start-Hook meldet eine veraltete Config mit einem eigenen,
  kurzen Hinweis auf `/claude-harness:update`, unterscheidbar von einer
  tatsächlich ungültigen Config.
- Der `update`-Skill: erkennt "bereits aktuell" (keine Änderung, klare
  Meldung); wendet bei Rückstand die Migrationsschritte an, fragt nur bei
  echten neuen Entscheidungen nach, zeigt das Ergebnis vor dem Schreiben und
  überschreibt nichts ohne Freigabe; validiert die geschriebene Datei danach.
- Bestehende Tests bleiben grün; neue Tests decken den Migrationsrahmen und
  die Hook-Unterscheidung ab.
