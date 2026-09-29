# Tests

Regeln zu Ablage und Gliederung: Skill `claude-harness:testing`.

| Ordner | Inhalt |
|---|---|
| `implementation/unit/` | Tests einzelner Skripte aus `plugin/scripts/` ohne Prozessaufruf |
| `implementation/integration/` | Tests, die Hooks und Skripte als Prozess starten, mit Git-Repos oder einem lokalen Testserver |
| `functional/<funktion>/` | Funktionalitätstests für den Projektverantwortlichen, je Szenario eine Datei |
| `helpers/` | gemeinsamer Testcode (u. a. `REPO_ROOT`, `SCRIPTS`) |

## Implementierungstests

Alle Implementierungstests (Python 3.11+, nur Standardbibliothek):

```bash
python3 -m unittest discover -s tests/implementation -t tests
```

Eine einzelne Datei, z. B. die Config-Tests:

```bash
python3 -m unittest discover -s tests/implementation -t tests -p test_config.py
```

## Funktionalitätstests

Sie laufen nicht im Gesamtlauf mit. Jeder Test wird einzeln aufgerufen; ohne
Parameter läuft ein Standardszenario, mit Parametern ein eigenes:

```bash
python3 tests/functional/<funktion>/test_<szenario>.py --help
```

Vorhandene Funktionalitätstests:

| Funktion | Szenario | Prüft |
|---|---|---|
| – | – | noch keine |
