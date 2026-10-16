# Claude_Harness

Claude_Harness ist ein Plugin für Claude Code, das Projektregeln als
schaltbare Module bereitstellt. Regeln werden als Skills erst geladen, wenn sie
zur Aufgabe passen; Pflichtprüfungen laufen als Hooks. Welche Module aktiv
sind und wo die Dokumente liegen, steht pro Projekt in
`.claude-harness/config.toml`.

## Module

| Modul | Zweck |
|---|---|
| `todo` | Typisierter Projekt-Backlog (über die ToDo-Viewer-API; im Modus `files` als `TODO.md`, `archive.md`, Notizen und Specs pro Eintrag) mit automatischer Formatprüfung. Gehört dazu: Notes und Topics (Erinnerungen, Fragen, Beobachtungen, Ideen) im ToDo-Viewer, getrennt vom Backlog; nur mit Backend `api`, nichts davon liegt im Repository |
| `daily` | Ein Tagesbericht pro Arbeitstag über relevante Änderungen, geschrieben auf dem Branch, in den sie gemerged wurden |
| `techdocs` | Technische Systemdoku (README, Architektur, Schnittstellen, Konfiguration, Betrieb) mit Erinnerung, sie im selben Change mitzupflegen |
| `development` | Suite verbindlicher Entwicklungsregeln für die AI (englisch). Teilbereich `architecture`: Architekturregeln mit Scopes, die vor der ersten Code-Änderung einer Session gelesen werden müssen. Teilbereich `decomposition`: Aufgaben werden in kleine, einzeln testbare Schritte zerlegt; für Bugfixes und neues Verhalten entsteht der Test zuerst. Teilbereich `worktree`: Changes mit freigegebenem Plan laufen in einem eigenen Worktree vom aktuell ausgecheckten Branch; die AI merged sie danach selbst dorthin zurück und löscht den Worktree. Teilbereich `testing`: alle Tests liegen in einem Testordner neben dem Quellcode (`development.tests`, Standard `tests`), getrennt in Implementierungstests der AI (Unit- und Integrationstests, optional Systemtests über die echten Einstiegspunkte) und Funktionalitätstests für den Owner, die nur auf Aufruf laufen und ihre Szenarien über Parameter setzen |
| `semver` | Versionsnummer nach SemVer: eine einheitliche Versionsdatei (Standard `docs/VERSION`), gespiegelt in die projekteigenen Dateien. Jede gemergte Änderung ergibt höchstens einen Versionsschritt mit Release-Tag; ein Hook prüft Schritt und Spiegel. Standardmäßig aus |

Unabhängig von den Modulen gilt: Widerspricht eine Anforderung oder ein Wunsch
des Projektverantwortlichen den Projektregeln oder einer Vorgabe des Harness,
benennt die AI den Konflikt und schlägt Lösungen vor; der
Projektverantwortliche entscheidet. Wünsche an den Harness selbst kann sie an
den Backlog dieses Repos übergeben (`harness.repo` in der Config).

## Voraussetzungen

- Claude Code mit Plugin-Unterstützung
- Python 3.11 oder neuer (nur Standardbibliothek)
- Git (für die Module `daily` und `semver` und den Teilbereich `worktree`)

## Installation

Das Repo enthält einen Marketplace (`.claude-plugin/marketplace.json`) mit dem
Plugin unter `plugin/`. In einem Projekt einbinden, z. B. über
`.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "claude-harness-dev": {
      "source": { "source": "directory", "path": "/pfad/zu/Claude_Harness" }
    }
  },
  "enabledPlugins": { "claude-harness@claude-harness-dev": true }
}
```

### Globaler Einstieg

Damit `/harness-init` in jedem Projekt verfügbar ist, auch ohne aktiviertes
Plugin, liegt der Skill `~/.claude/skills/harness-init/SKILL.md`. Er verweist
auf `plugin/skills/init/SKILL.md` in diesem Repo und aktiviert am Ende das
Plugin im Projekt. Bei einem anderen Repo-Pfad die Pfade im Skill anpassen.

## Schnellstart

1. Claude Code im Projekt starten.
2. `/claude-harness:init` ausführen. Der Befehl fragt Sprache, Doku-Ordner und
   Module ab und legt die Config sowie auf Wunsch Backlog und Dokumente aus
   Vorlagen an, ohne Bestehendes zu überschreiben.
3. Beim nächsten Session-Start meldet der Harness die aktiven Module.

Nach einem Plugin-Update bringt `/claude-harness:update` die Config auf den
aktuellen Stand: Er ergänzt fehlende Einstellungen, Module und Erklärungen
aus der Vorlage und fragt nur, wo etwas zu entscheiden ist.

Teilprojekte: In einem Repository mit mehreren Teilen, etwa einer Anwendung
mit Plugins, bekommt jedes Teilprojekt eigene Config, Doku, Backlog und
Architekturregeln in seinem Ordner. `/claude-harness:init` richtet ein
Teilprojekt ein und trägt es in `[projects]` der Root-Config ein; die Session
startet weiter im Repo-Root. Details:
[Konfiguration, Abschnitt Teilprojekte](docs/techdocs/configuration.md#teilprojekte).

## Cloud-Sitzungen (claude.ai/code)

Eine Cloud-Sitzung klont das Repository und lädt das Plugin nicht. Damit der
Harness dort wirkt, kann ein Projekt eine eingecheckte Kopie davon halten:

1. In `.claude-harness/config.toml` `[cloud] export = true` setzen (nur im
   Root-Projekt) und `/claude-harness:init` bzw. `/claude-harness:update`
   ausführen. Beide zeigen eine Vorschau und schreiben erst nach Freigabe:
   Skills `harness-<Name>` unter `.claude/skills/`, Skripte und Vorlagen unter
   `.claude-harness/runtime/`, Hooks in `.claude/settings.json`.
2. Die Kopie in einem eigenen Commit einchecken und pushen.
3. Nach einem Plugin-Update meldet der Session-Start eine veraltete Kopie;
   `/claude-harness:update` aktualisiert sie.
4. Soll nur noch lokal gearbeitet werden, nimmt `/claude-harness:update` die
   Kopie wieder heraus (`cloud.export = false`); das Manifest
   `.claude-harness/runtime/manifest.json` stellt den Stand davor wieder her,
   alternativ nimmt ein `git revert` des Commits sie zurück.

Grenzen: Die Hooks der Kopie laufen nur in einer Sitzung mit einem Repository
und nur in der Cloud (`CLAUDE_CODE_REMOTE=true`); lokal gelten die Hooks des
Plugins. Der ToDo-Viewer ist aus der Cloud nicht erreichbar, der Backlog dort
braucht `todo.backend = "files"`. Skills und Hooks der Kopie kosten lokal
zusätzlich je Skill eine Beschreibung im Kontext. Details:
[Schnittstellen, Skript `cloud_export.py`](docs/techdocs/interfaces.md#skript-cloud_exportpy).

## Entwicklung

- `plugin/` ist das ausgelieferte Produkt; alles andere dient der Entwicklung.
- Dieses Repo nutzt das Plugin selbst (`.claude/settings.json`).
- Tests: `python3 -m unittest discover -s tests/implementation -t tests`; Aufbau und Funktionalitätstests: `tests/README.md`
- Backlog: `docs/todo/`, Tagesberichte: `docs/daily/`, Architekturregeln: `docs/development/architecture.md`

## Dokumentation

- [Architektur](docs/techdocs/architecture.md)
- [Schnittstellen](docs/techdocs/interfaces.md)
- [Konfiguration](docs/techdocs/configuration.md)
