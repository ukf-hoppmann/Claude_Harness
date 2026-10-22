# Konfiguration

## `.claude-harness/config.toml`

Liegt im Projekt-Root und wird bei jedem Session-Start und von jedem Hook
gelesen (`tomllib`, Python 3.11+). Vorlage: `plugin/templates/config.toml`.
Fehlt die Datei, meldet der Session-Start das und verweist auf
`/claude-harness:init`; die Module bleiben dann inaktiv.

| Einstellung | Typ | Standard | Pflicht | Wirkung |
|---|---|---|---|---|
| `version` | Ganzzahl | – | ja | Schema-Version, aktuell `1`. Eine ältere Version mit bekanntem Migrationspfad wird erkannt und über `/claude-harness:update` aktualisiert statt sofort abgelehnt zu werden |
| `docs.root` | Pfad | `"docs"` | nein | Ordner für alle Harness-Dokumente, relativ zum Projekt-Root |
| `docs.language` | ISO-639-1-Code | `"en"` | nein | Sprache aller erzeugten Dokumente (Fließtext und Überschriften, nicht maschinell geprüfte Feldnamen) |
| `modules.todo` | Boolean | `false` | nein | Schaltet das Backlog-Modul ein. Dazu gehören Notes und Topics (Erinnerungen, Fragen, Ideen im ToDo-Viewer, Regeln in `notes.md` des Skills `todo`); sie gibt es nur mit `todo.backend = "api"`, nutzen `todo.path` (Projektzuordnung) und `todo.api_url` und haben keine eigenen Einstellungen. Der Session-Start nennt sie nur, er fragt keine fälligen Notes ab. Der frühere Schalter `modules.notes` entfällt; eine Config damit meldet einen Fehler, die Zeile ist zu streichen |
| `modules.daily` | Boolean | `false` | nein | Schaltet die Tagesberichte ein |
| `modules.techdocs` | Boolean | `false` | nein | Schaltet die Systemdoku-Regeln ein |
| `modules.development` | Boolean | `false` | nein | Schaltet die Suite `development` mit allen Teilbereichen ein |
| `modules.semver` | Boolean | `false` | nein | Schaltet die Versionierung nach SemVer ein (Skill `claude-harness:semver`) |
| `todo.path` | Pfad | `"todo"` | nein | Backlog-Ordner, relativ zu `docs.root` |
| `todo.backend` | Text | `"api"` | nein | Wie die AI den Backlog pflegt: `api` über die HTTP-API des ToDo-Viewers (der Server prüft Format und Regeln, kein Backlog-Check am Turn-Ende), `files` direkt in den Markdown-Dateien (mit Backlog-Check). Ist der Server nicht erreichbar, fragt die AI, ob er gestartet oder auf Dateien ausgewichen wird. Der Wert ist die Vorgabe; je Umgebung kann er überschrieben werden (siehe Umgebungsvariablen unten): in einer Cloud-Sitzung gilt `files`, ohne dass die Config geändert wird |
| `todo.api_url` | URL | `"http://localhost:5411/api"` | nein | Basis-URL der HTTP-API des ToDo-Viewers (darunter `/backlog`, `/notes`, `/alarms`, `/workspace`, `/core`); nur für `todo.backend = "api"`. Die Adresse des alten Viewers (`…/api/v2`) wird als `…/api` gelesen, alte Configs laufen ohne Änderung weiter |
| `daily.path` | Pfad | `"daily"` | nein | Ordner der Tagesberichte, relativ zu `docs.root` |
| `techdocs.path` | Pfad | `"techdocs"` | nein | Ordner der Systemdoku, relativ zu `docs.root` |
| `development.path` | Pfad | `"development"` | nein | Ordner der Regeln der Suite, relativ zu `docs.root` |
| `development.architecture` | Boolean | `true` | nein | Teilbereich Architektur; nur wirksam, wenn die Suite an ist; `false` schaltet ihn ab |
| `development.decomposition` | Boolean | `true` | nein | Teilbereich Zerlegung (Skill `claude-harness:decomposition`); nur wirksam, wenn die Suite an ist; `false` schaltet ihn ab |
| `development.worktree` | Boolean | `true` | nein | Teilbereich Change-Workflow (Skill `claude-harness:worktree`): Changes mit freigegebenem Plan laufen in einem Worktree vom aktuellen Branch und werden von der AI zurückgemerged; nur wirksam, wenn die Suite an ist; `false` schaltet ihn ab |
| `development.testing` | Boolean | `true` | nein | Teilbereich Tests (Skill `claude-harness:testing`): Ablage und Gliederung des Testordners, Implementierungs- und Funktionalitätstests; nur wirksam, wenn die Suite an ist; `false` schaltet ihn ab |
| `development.tests` | Pfad | `"tests"` | nein | Testordner, relativ zum Projekt-Root (nicht zu `docs.root`); in der Regel neben dem Quellordner |
| `techdocs.documents` | Liste | `["architecture", "interfaces", "configuration"]` | nein | Geführte Dokumente; erlaubt sind `architecture`, `interfaces`, `configuration`, `operations`; Dateiname `<Art>.md`. `README.md` im Projekt-Root gehört immer dazu |
| `semver.file` | Pfad | `"VERSION"` | nein | Versionsdatei, relativ zu `docs.root`; enthält nur die Version `MAJOR.MINOR.PATCH` |
| `semver.sync` | Liste von Pfaden | `[]` | nein | Spiegel-Dateien, relativ zum Projekt, z. B. `["package.json"]`; jede muss die Version aus der Versionsdatei enthalten |
| `semver.paths` | Liste von Pfaden | `["."]` | nein | Was zum ausgelieferten Produkt zählt, relativ zum Projekt; nur Commits unter diesen Pfaden gelten als unveröffentlicht. Beim Root-Projekt zählen Ordner von Teilprojekten nicht mit |
| `projects.<Name>` | Pfad | – | nein | Trägt ein Teilprojekt ein: Name → Ordner relativ zum Projekt-Root. Nur in der Konfiguration des Root-Projekts erlaubt; siehe „Teilprojekte“ |
| `cloud.export` | Boolean | `false` | nein | Das Projekt hält eine eingecheckte Kopie des Plugins für Cloud-Sitzungen (claude.ai/code), die `/claude-harness:init` anlegt und `/claude-harness:update` aktuell hält (Skills unter `.claude/skills/harness-*`, Skripte unter `.claude-harness/runtime/`, Hooks in `.claude/settings.json`). Nur im Root-Projekt erlaubt; ein Teilprojekt mit `[cloud]` meldet einen Fehler. Ist die Option aus, aber eine Kopie da, oder umgekehrt, meldet der Session-Start es. Aufbau, Vorschau und Rückbau: [Schnittstellen, Skript `cloud_export.py`](interfaces.md#skript-cloud_exportpy). Bei `true` müssen `.claude-harness/` und `.claude/` eingecheckt sein |
| `harness.repo` | Liste von Pfaden | `[]` | nein | Mögliche Orte des Claude_Harness-Repos, einer pro Rechner; absolut oder mit `~` beginnend. Gilt der erste, der auf dem Rechner existiert und das Harness-Repo ist. Wird für die Übergabe von Harness-Wünschen an den Harness-Backlog gebraucht (Skill `claude-harness:conflicts`); ohne passenden Eintrag gibt die AI den Auftrag als Text aus |

Nicht aufgeführte Module sind aus. Teilbereiche der Suite `development` sind
an, solange die Suite an ist, außer sie stehen auf `false`. Die Vorlage
schaltet `todo`, `techdocs` und `development` ein und `daily` und `semver` aus.

Validierung (Fehler werden beim Session-Start gemeldet, Hooks tun dann
nichts):

- unbekannte Schlüssel, Tabellen oder Module;
- absolute Pfade oder Pfade mit `..`;
- `docs.language` nicht aus genau zwei Kleinbuchstaben;
- unbekannte oder doppelte Einträge in `techdocs.documents`;
- Teilbereiche von `development`, die kein Boolean sind;
- `semver.sync` oder `semver.paths`, die keine Liste relativer Pfade ohne
  `..` sind; ein leeres `semver.paths`;
- `harness.repo`, das keine Liste nicht leerer Strings ist oder relative
  Pfade enthält;
- `[projects]`, das keine Tabelle ist; Projektnamen, die nicht mit einem
  Buchstaben beginnen, andere Zeichen als Buchstaben, Ziffern, `_` und `-`
  enthalten oder `root` heißen; Projektpfade, die leer, absolut, `.` oder mit
  `..` sind; Projektpfade, die gleich sind oder ineinander liegen;
- `cloud.export`, das kein Boolean ist;
- `[projects]`, `[harness]` oder `[cloud]` in der Konfiguration eines Teilprojekts.

`harness.repo` enthält rechnerspezifische Pfade in einer eingecheckten Datei.
Deshalb ist es eine Liste: Jeder Rechner ergänzt seinen Pfad; Einträge, die
auf einem Rechner nicht existieren, werden übersprungen.

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
development = true

[todo]
path = "todo"
backend = "api"
api_url = "http://localhost:5411/api"

[daily]
path = "daily"

[techdocs]
path = "techdocs"
documents = ["architecture", "interfaces", "configuration"]

[development]
path = "development"
architecture = true

[harness]
repo = ["~/Documents/GitHub/Claude_Harness"]
```

## Teilprojekte

Ein Repository kann neben dem Root-Projekt (Name `root`) Teilprojekte mit
eigener Konfiguration, Sprache und eigenen Dokumenten enthalten, z. B. je ein
Plugin einer Anwendung. Die Session startet im Repo-Root; Claude Code lädt
`.claude/settings.json` nur aus dem Startverzeichnis, deshalb unterscheidet
der Harness die Projekte selbst
(Hintergrund: `docs/todo/items/STORY-027/STORY-027_notes.md`).

- Die Konfiguration des Root-Projekts trägt die Teilprojekte in
  `[projects]` ein:

  ```toml
  [projects]
  VariantFilter = "Plugins/VariantFilter"
  OtherPlugin = "Plugins/OtherPlugin"
  ```

- Jedes Teilprojekt hat eine eigene `<Pfad>/.claude-harness/config.toml`
  mit denselben Einstellungen wie oben. Ihre Pfade gelten relativ zum Ordner
  des Teilprojekts. `[projects]` und `[harness]` sind dort nicht erlaubt;
  verschachtelte Teilprojekte gibt es nicht.
- Das Root-Projekt kann reine Registry sein: Ohne eingeschaltete Module
  gelten für Dateien außerhalb der Teilprojekte keine Harness-Regeln.
- Eine Datei gehört zu dem Teilprojekt, dessen Ordner sie enthält, sonst zum
  Root-Projekt. Fehlt die Konfiguration eines Teilprojekts oder ist sie
  ungültig, meldet der Session-Start das; die anderen Projekte bleiben
  wirksam.
- Ist die Konfiguration des Root-Projekts ungültig, ist kein Projekt wirksam.
- Die Konfigurationsdateien dürfen in die `.gitignore`; das Plugin kann über
  die nicht eingecheckte `.claude/settings.local.json` aktiviert werden. Die
  Dokumente unter `docs/` jedes Projekts werden eingecheckt.

Alle Hooks wenden die Einstellungen des Projekts an, zu dem eine Datei
gehört; Tagesberichte zählen pro Projekt nur dessen Commits.

## Umgebungsvariablen

| Variable | Gesetzt von | Wirkung |
|---|---|---|
| `CLAUDE_PROJECT_DIR` | Claude Code | Projekt-Root für Hooks und Skripte; sonst `cwd` aus der Hook-Eingabe bzw. das aktuelle Verzeichnis. Liegen `cwd` oder die bearbeitete Datei in `<Projekt-Root>/.claude/worktrees/<Name>/`, gilt dieser Worktree als Projekt-Root |
| `CLAUDE_PLUGIN_DATA` | Claude Code | Ordner für Merker pro Session; sonst `<tmp>/claude-harness/` |
| `CLAUDE_PLUGIN_ROOT` | Claude Code | Pfad des Plugins in Hook-Befehlen und Skills |
| `CLAUDE_HARNESS_TODO_BACKEND` | Nutzer (Shell, Umgebung der Sitzung) | Wert `api` oder `files`; überschreibt `todo.backend` bei jedem Laden der Config. Ein anderer Wert ist ein Config-Fehler (Meldung nennt die Variable). Leer zählt als nicht gesetzt |
| `CLAUDE_CODE_REMOTE` | Claude Code | `true` in Cloud-Sitzungen (claude.ai/code): dort gilt der Dateimodus (`files`), weil der ToDo-Viewer nicht erreichbar ist. Jeder andere Wert zählt als lokal |

Wirksames Backend (Rangfolge): `CLAUDE_HARNESS_TODO_BACKEND`, dann die
Cloud-Erkennung über `CLAUDE_CODE_REMOTE`, dann `todo.backend`. Es gilt für
Session-Start, Backlog-Hooks, Notes und Alarme; die Config-Datei selbst bleibt
unverändert und wird von `/claude-harness:update` weiter so geprüft, wie sie
dasteht. In einer Cloud-Sitzung sind Notes und Alarme aus (sie brauchen `api`).
