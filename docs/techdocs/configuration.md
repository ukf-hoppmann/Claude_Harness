# Konfiguration

## `.claude-harness/config.toml`

Liegt im Projekt-Root und wird bei jedem Session-Start und von jedem Hook
gelesen (`tomllib`, Python 3.11+). Vorlage: `plugin/templates/config.toml`.
Fehlt die Datei, meldet der Session-Start das und verweist auf
`/claude-harness:init`; die Module bleiben dann inaktiv.

| Einstellung | Typ | Standard | Pflicht | Wirkung |
|---|---|---|---|---|
| `version` | Ganzzahl | – | ja | Schema-Version; muss `1` sein |
| `docs.root` | Pfad | `"docs"` | nein | Ordner für alle Harness-Dokumente, relativ zum Projekt-Root |
| `docs.language` | ISO-639-1-Code | `"en"` | nein | Sprache aller erzeugten Dokumente (Fließtext und Überschriften, nicht maschinell geprüfte Feldnamen) |
| `modules.todo` | Boolean | `false` | nein | Schaltet das Backlog-Modul ein |
| `modules.daily` | Boolean | `false` | nein | Schaltet die Tagesberichte ein |
| `modules.techdocs` | Boolean | `false` | nein | Schaltet die Systemdoku-Regeln ein |
| `todo.path` | Pfad | `"todo"` | nein | Backlog-Ordner, relativ zu `docs.root` |
| `daily.path` | Pfad | `"daily"` | nein | Ordner der Tagesberichte, relativ zu `docs.root` |
| `techdocs.path` | Pfad | `"techdocs"` | nein | Ordner der Systemdoku, relativ zu `docs.root` |
| `techdocs.documents` | Liste | `["architecture", "interfaces", "configuration"]` | nein | Geführte Dokumente; erlaubt sind `architecture`, `interfaces`, `configuration`, `operations`; Dateiname `<Art>.md`. `README.md` im Projekt-Root gehört immer dazu |

Nicht aufgeführte Module sind aus. Die Vorlage schaltet `todo` und
`techdocs` ein und `daily` aus.

Validierung (Fehler werden beim Session-Start gemeldet, Hooks tun dann
nichts):

- unbekannte Schlüssel, Tabellen oder Module;
- absolute Pfade oder Pfade mit `..`;
- `docs.language` nicht aus genau zwei Kleinbuchstaben;
- unbekannte oder doppelte Einträge in `techdocs.documents`.

Beispiel:

```toml
version = 1

[docs]
root = "docs"
language = "de"

[modules]
todo = true
daily = true
techdocs = true

[todo]
path = "todo"

[daily]
path = "daily"

[techdocs]
path = "techdocs"
documents = ["architecture", "interfaces", "configuration"]
```

## Umgebungsvariablen

| Variable | Gesetzt von | Wirkung |
|---|---|---|
| `CLAUDE_PROJECT_DIR` | Claude Code | Projekt-Root für Hooks und Skripte; sonst `cwd` aus der Hook-Eingabe bzw. das aktuelle Verzeichnis |
| `CLAUDE_PLUGIN_DATA` | Claude Code | Ordner für Merker pro Session; sonst `<tmp>/claude-harness/` |
| `CLAUDE_PLUGIN_ROOT` | Claude Code | Pfad des Plugins in Hook-Befehlen und Skills |
