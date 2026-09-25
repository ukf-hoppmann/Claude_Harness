# STORY-029 – Notizen

## Summary
Klären, ob Claude bei Änderungen die Versionsnummer nach SemVer selbst
einstufen und hochzählen soll, und das dann umsetzen.

## 2026-09-25 — Ausgangslage

### Discussed
- Ist-Zustand: Die Version steht nur in `plugin/.claude-plugin/plugin.json`
  (`0.1.0`). Es gibt keinen Changelog und keine Git-Tags.
- Vorlage Agent_Harness (`rules/modules/semver.md`): Vor Abschluss jeder
  Änderung stuft der Agent die Auswirkung ein (major/minor/patch/keine),
  hebt die Version in den Paketmetadaten in derselben Änderung an und trägt
  sie mit Begründung in den Changelog ein. Rein interne Änderungen und reine
  Doku-Änderungen bleiben ohne Versionssprung.

## 2026-09-25 — Grundentscheidungen

### Decided
- Automatisierungsstufe 2: Claude stuft ein und hebt die Version an, ein
  Skript prüft deterministisch. Kein Conventional-Commits-Tooling.
- Releases werden gesammelt, nicht bei jedem Merge. Der Owner will keine
  unnötig hohen Versionen.
- Kein eigener Changelog, die Daily-Reports reichen.
- Umsetzung gleich als schaltbares Modul für Zielprojekte.

## 2026-09-25 — Entwurf, Runde 2

### Decided
- Die maßgebliche Versionsdatei liegt standardmäßig unter `docs.root`.
- Das Modul ist bei `init` standardmäßig aus.

### Discussed
- Projekte speichern ihre Version an unterschiedlichen Orten (ezf-ui:
  `package.json`, EZF-Backend: `Cargo.toml`). Vorschlag: Die Datei in `docs`
  ist die einheitliche Quelle. Projekteigene Dateien werden als
  Spiegel-Dateien eingetragen, und das Skript prüft, ob sie gleich sind.
- Tag-Präfix erklärt. Vorschlag: automatisch `v` beim Root-Projekt und
  `<Projektname>-v` bei Teilprojekten, ohne eigenen Config-Key.

## 2026-09-25 — Entwurf, Runde 3

### Decided
- Git-Tags markieren Releases.
- Es gibt keine zentrale Versionsdatei und keine Spiegel-Dateien. Jedes
  Projekt und jedes Teilprojekt trägt in seiner eigenen `config.toml` ein,
  wo seine Version steht. Nur ohne projekteigene Versionsdatei gilt eine
  Datei unter `docs` als Standard. Der Spiegel-Vorschlag aus Runde 2 ist
  damit verworfen.

### Discussed
- Heterogene Formate: Nur das Prüfskript muss die Version lesen. Das
  Schreiben beim Release übernimmt Claude, und zwar in jedem Format.
  Vorschlag: für JSON/TOML ein Schlüsselpfad (mit Standard je bekanntem
  Dateinamen), für alles andere ein Regex, sonst Klartext.

## 2026-09-25 — Entwurf, Runde 4: doch Spiegel

### Discussed
- Owner-Vorschlag: Die Version steht immer in `docs/VERSION` (einheitliches
  Format, der Hook liest nur diese Datei) und zusätzlich in der
  projekteigenen Datei. Ohne projekteigene Datei genügt `docs/VERSION`.
- Einwand: Zwei Quellen können auseinanderlaufen, und ausgeliefert wird die
  projekteigene Datei. Lösung ohne Format-Parsing: Das Skript prüft nur, ob
  die Spiegel-Datei die Versionszeichenkette aus `docs/VERSION` enthält.
- `config.toml` ist als Ort ungeeignet: Sie ist Konfiguration, darf laut
  Doku gitignored sein, und die Version ändert sich bei jedem Release.

### Decided
- Owner hat den Spiegel-Entwurf freigegeben und die Spec beauftragt:
  `STORY-029_spec.md`.

### Open
- Die Spec muss der Owner noch freigeben.

## 2026-09-25 — Wann wird die Version angehoben?

### Discussed
- Owner präzisiert: Nicht „Release nur auf Wunsch“, sondern jede
  abgeschlossene Änderung soll die Version ändern. Teilschritte eines
  Plans oder Ausprobieren (z. B. Farben) sollen aber keinen eigenen Sprung
  auslösen, sondern gebündelt werden.
- Vorschlag: ein Versionsschritt pro abgeschlossener Änderung, also beim
  Merge des Worktrees in den Hauptbranch. Direkte kleine Commits auf dem
  Hauptbranch werden vom nächsten Release mit erfasst.

### Decided
- Der Owner hat den Vorschlag bestätigt: ein Versionsschritt pro Merge
  eines Worktrees. Die Spec ist angepasst und die Umsetzung freigegeben.
