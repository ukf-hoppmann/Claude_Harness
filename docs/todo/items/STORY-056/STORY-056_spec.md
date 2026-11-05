# STORY-056 — Spec: Pflege-Erinnerung bei Änderungen an öffentlichen APIs

Teil von EPIC-011. Unabhängig von STORY-053/054 (Entscheidung E4).

## Konfiguration

```toml
[development]
# Files of the project's public APIs (patterns like scope paths). A change there
# reminds the AI to check architecture responsibilities, catalog, interface docs, links.
public_api = []   # e.g. ["src/core/index.ts", "src/shared/index.ts", "src/plugins/*/index.ts"]
```

- Liste von Strings, Muster relativ zum Projekt-Root, Syntax wie Scope-Pfade
  (`match_path` aus `architecture.py`), kein führender `/`, kein `..`; Standard `[]`.
- Prüfung in `harness_config.py` (unbekannte Keys bleiben Fehler), Vorlage
  `plugin/templates/config.toml` mit Kommentar, `config_update.py` zieht den Key nach,
  Doku in `docs/techdocs/configuration.md`, Test in `tests/implementation/unit/test_config.py`
  (Architekturregel 4).

## Hook

- PostToolUse Write/Edit/MultiEdit: passt die geänderte Datei auf ein Muster und ist der
  Teil architecture aktiv, wird ein Marker je Session und Projekt gesetzt (`state.py`).
- Stop: Marker gesetzt, noch nicht erinnert → eine Meldung (Englisch, kurz) auf stderr,
  Exit 2, Erinnerung als erledigt markieren. Einmal je Session und Projekt, wie die
  Techdocs-Erinnerung in `check_techdocs.py`. Nichts bei `stop_hook_active`.
- Vorschlag für den Text: `Claude_Harness architecture: public API files changed (<n> files,
  e.g. <path>). Check that the architecture responsibilities, the catalog of reusable
  building blocks, the interface docs in <development.path>/ and their links still match.
  Load skill claude-harness:architecture. (Shown once per session.)`
- Mit Subprojekten eine gemeinsame Meldung mit einer Angabe je Projekt (wie techdocs).

## Doku und Tests

Techdocs des Harness (configuration, interfaces). Unit-Tests: Config gültig/ungültig,
Markierung nur bei Treffer, Erinnerung einmal, keine Erinnerung ohne Muster oder bei
abgeschaltetem Teil, Subprojekte.
