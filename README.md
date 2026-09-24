# Claude_Harness

Claude_Harness ist ein Plugin für Claude Code, das Projektregeln als
schaltbare Module bereitstellt. Regeln werden als Skills erst geladen, wenn sie
zur Aufgabe passen; Pflichtprüfungen laufen als Hooks. Welche Module aktiv
sind und wo die Dokumente liegen, steht pro Projekt in
`.claude-harness/config.toml`.

## Module

| Modul | Zweck |
|---|---|
| `todo` | Typisierter Projekt-Backlog (`TODO.md`, `archive.md`, Notizen und Specs pro Eintrag) mit automatischer Formatprüfung |
| `daily` | Ein Tagesbericht pro Arbeitstag über relevante Änderungen, die auf dem Hauptzweig angekommen sind |
| `techdocs` | Technische Systemdoku (README, Architektur, Schnittstellen, Konfiguration, Betrieb) mit Erinnerung, sie im selben Change mitzupflegen |
| `development` | Suite verbindlicher Entwicklungsregeln für die AI (englisch). Teilbereich `architecture`: Architekturregeln mit Scopes, die vor der ersten Code-Änderung einer Session gelesen werden müssen. Teilbereich `decomposition`: Aufgaben werden in kleine, einzeln testbare Schritte zerlegt; für Bugfixes und neues Verhalten entsteht der Test zuerst |

Unabhängig von den Modulen gilt: Widerspricht eine Anforderung oder ein Wunsch
des Projektverantwortlichen den Projektregeln oder einer Vorgabe des Harness,
benennt die AI den Konflikt und schlägt Lösungen vor; der
Projektverantwortliche entscheidet. Wünsche an den Harness selbst kann sie an
den Backlog dieses Repos übergeben (`harness.repo` in der Config).

## Voraussetzungen

- Claude Code mit Plugin-Unterstützung
- Python 3.11 oder neuer (nur Standardbibliothek)
- Git (für das Modul `daily`)

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

## Schnellstart

1. Claude Code im Projekt starten.
2. `/claude-harness:init` ausführen. Der Befehl fragt Sprache, Doku-Ordner und
   Module ab und legt die Config sowie auf Wunsch Backlog und Dokumente aus
   Vorlagen an, ohne Bestehendes zu überschreiben.
3. Beim nächsten Session-Start meldet der Harness die aktiven Module.

## Entwicklung

- `plugin/` ist das ausgelieferte Produkt; alles andere dient der Entwicklung.
- Dieses Repo nutzt das Plugin selbst (`.claude/settings.json`).
- Tests: `python3 -m unittest discover tests`
- Backlog: `docs/todo/`, Tagesberichte: `docs/daily/`, Architekturregeln: `docs/development/architecture.md`

## Dokumentation

- [Architektur](docs/techdocs/architecture.md)
- [Schnittstellen](docs/techdocs/interfaces.md)
- [Konfiguration](docs/techdocs/configuration.md)
