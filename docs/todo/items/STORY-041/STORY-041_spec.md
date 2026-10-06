# Spec: Abgrenzung im todo-Skill, Techdocs, Release

## Umfang

- `plugin/skills/todo/SKILL.md`: kurzer Abschnitt "Notes": Arbeit mit
  Fertig-Definition gehört ins Backlog, Erinnerungen, Fragen, Beobachtungen
  und Ideen in Notes (`claude-harness:notes`); Umwandlung Item zu Note und
  zurück läuft über den Notes-Skill; beim Abschluss eines Items mit
  verlinkter Note zeigt der Viewer einen Hinweis, Claude greift ihn nur auf,
  wenn der Besitzer es will.
- `docs/techdocs/interfaces.md`: Helfer `notes_api.py` und Skill;
  `architecture.md`: Modul `notes` und gemeinsamer API-Client;
  `configuration.md`: bereits durch STORY-038; `README.md`: Modulliste.
- Der daily-Skill bleibt unverändert, solange es kein Missverständnis gibt;
  Notes stehen nicht im Tagesbericht.
- Release nach `claude-harness:semver` (neues Modul: Minor).

## Grenzen

Keine Notes-Inhalte in Repository-Dateien. Die Doku verweist für das
Notes-Modell auf die Doku des Viewers, kopiert sie nicht.

## Abnahme

Siehe Abnahmekriterien der Story.
