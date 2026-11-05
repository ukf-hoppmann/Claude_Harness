# STORY-053 — Spec: Architektur-Scopes in Unterordnern

Teil von EPIC-011 (Entscheidungen dort in den Notes).

## Anlass

Große Projekte (ezf-ui: Core, Shared, Plugins, je Plugin eigene Regeln) wollen ihre
Scopes nach Bereichen ordnen. Heute erlaubt `_SCOPE_NAME` in
`plugin/scripts/architecture.py` nur flache Namen, und
`plugin/scripts/mark_architecture_read.py` markiert nur Reads mit
`rel.parent == scopes_dir(config)`; eine Datei in einem Unterordner würde nie als
gelesen gelten.

## Namensschema

- Scope-Name: ein oder mehrere Segmente `[a-z0-9]+(?:-[a-z0-9]+)*`, getrennt durch `/`.
  Kein führender oder abschließender `/`, keine leeren Segmente.
- Datei: `architecture/<Name>.md`. Beispiel: `plugins` → `architecture/plugins.md`,
  `plugins/patient` → `architecture/plugins/patient.md`. Beide dürfen nebeneinander
  bestehen (Konvention E1: Datei `X.md` neben Ordner `X/`).
- Keine harte Grenze der Tiefe im Code; der Skill empfiehlt höchstens zwei Ebenen
  (Bereich, Teil).

## Betroffene Stellen

- `architecture.py`: `_SCOPE_NAME`, Fehlermeldung für ungültige Namen, `parse_inherited`
  (gleiche Namensregel), `scope_path` bleibt `scopes_dir / f"{name}.md"`.
- `mark_architecture_read.py`: markieren, wenn `rel == rules_path` oder `rel` unterhalb
  von `scopes_dir` liegt und auf `.md` endet (`is_relative_to`).
- Alle weiteren Nutzer von `_SCOPE_NAME` oder Scope-Namen (grep, u. a. `session_start.py`,
  `cloud_export.py`, Tests) prüfen.
- Doku: Skill `plugin/skills/architecture/SKILL.md` (Abschnitt Scope table format),
  Kommentar in `plugin/templates/development/architecture.md`,
  `docs/techdocs/interfaces.md` und ggf. `architecture.md` des Harness.

## Abwärtskompatibilität

Flache Namen sind ein Sonderfall des neuen Schemas; bestehende Tabellen und Tests
bleiben gültig.

## Tests

Unit-Tests (Ort und Art: Skill `claude-harness:testing`): gültige und ungültige Namen
(`a/b`, `a//b`, `/a`, `a/`, `A/b`, `a/../b`), Pfad der Scope-Datei, fehlende Datei im
Unterordner als Fehler, Markierung eines vollständigen Reads im Unterordner, Hook
verlangt die Datei, Vererbung mit `plugins/patient`.
