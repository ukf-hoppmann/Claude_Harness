# STORY-023 — Spec: Architektur-Definitionen (Suite `development`)

## Goal

Ein Projekt legt seine verbindliche Architektur als Regeln für die AI fest.
Die Regeln werden vor der ersten Code-Änderung einer Session zuverlässig
gelesen; spezielle Regeln nur dort, wo sie gelten. Erster Teilbereich der
Modul-Suite `development`.

## Config

Erweiterung der Projektkonfiguration (bleibt `version = 1`):

```toml
[modules]
development = true           # Suite; Standard: aus

[development]
path = "development"         # relativ zu docs.root; Standard "development"
architecture = true          # Teilbereich; Standard: an, wenn die Suite an ist
```

- Bekannte Teilbereiche: zunächst nur `architecture`. Weitere Teilbereiche aus
  `EPIC-004` kommen als weitere Boolean-Schlüssel dazu.
- Ein Teilbereich ist aktiv, wenn die Suite an ist und er nicht auf `false`
  steht. So schaltet ein Schalter alles an; einzelne Teile lassen sich abwählen.
- Validierung wie bisher: unbekannte Schlüssel, Nicht-Booleans, absolute Pfade
  und `..` sind Fehler.

## Storage

- Wurzel: `<docs.root>/<development.path>/architecture.md`.
- Teilbereiche: `<docs.root>/<development.path>/architecture/<scope>.md`.
- Sprache immer Englisch, Regeln mit MUST/SHOULD/MAY (RFC 2119), unabhängig von
  `docs.language`.
- Vorlage: `plugin/templates/development/architecture.md`.

## Format der Wurzel

Freier Aufbau für die Regeln, dazu zwei feste Abschnitte:

```markdown
## Scopes

| Scope | Paths | Covers |
|---|---|---|
| llm-integration | `Backend/app/llm/**`, `Backend/app/prompts/**` | Model calls, prompts |

## Changing these rules
…
```

- `Scope`: Name, Datei `architecture/<Scope>.md`, Kleinbuchstaben, Ziffern, `-`.
- `Paths`: ein oder mehrere Pfadmuster relativ zum Projekt-Root, in
  Backticks, kommagetrennt. `*` innerhalb eines Pfadteils, `**` über
  beliebig viele Pfadteile.
- Ein Teilbereich gilt zusätzlich zur Wurzel, nie statt ihrer.
- Eine mechanisch prüfbare Regel verweist auf ihren Test
  (`Enforced by: tests/architecture/test_layers.py`). Freitext, wird nicht
  ausgewertet.
- Der Abschnitt `## Changing these rules` kommt aus der Vorlage; sein Inhalt
  wird in `STORY-025` ausgearbeitet.

Fehler in der Tabelle (fehlende Datei, ungültiger Name, leeres Muster) meldet
der Session-Start.

## Loading

1. **Session-Start:** eine Zeile mit Pfad der Wurzel und Hinweis auf den Skill.
   Fehlt die Wurzel, der Hinweis, sie nach Freigabe aus der Vorlage anzulegen.
2. **Skill `claude-harness:architecture`:** Beschreibung passt auf das Planen
   und Ändern von Code. Inhalt siehe unten.
3. **PostToolUse auf `Read`:** Liest die AI die Wurzel oder eine Scope-Datei
   vollständig (ohne `offset`, ohne kleineres `limit`), wird das pro Session
   vermerkt.
4. **PreToolUse auf `Write|Edit|MultiEdit|NotebookEdit`:** Ist die Zieldatei
   eine Projektdatei und die Wurzel in dieser Session nicht gelesen, wird die
   Änderung abgelehnt mit dem Hinweis, die Wurzel zu lesen. Passt die Datei zu
   einem Scope, gilt dasselbe für dessen Datei. Nach dem Lesen läuft die
   Änderung durch.
5. **Session-Start mit `compact` oder `clear`:** Die Lese-Merker der Session
   werden gelöscht, weil die Regeln aus dem Kontext verschwunden sein können.

Projektdatei heißt: im Projekt, nicht unter `.git/`, `.claude-harness/` und
nicht in den Ordnern von `todo`, `daily`, `techdocs`, `development`, und
nicht `README.md`. Tests zählen als Projektdateien. Fehlt die Wurzel, wird
nichts blockiert.

Grenzen: Änderungen über Bash sieht der Hook nicht. Gelesen heißt nicht
befolgt. Die Planung vor der ersten Änderung deckt nur der Skill ab.

## Skill-Inhalt

- Vor dem Planen einer Code-Änderung Wurzel und passende Scopes lesen.
- Die Regeln befolgen. Passt eine Anforderung nicht: keine lokale Ausnahme,
  stoppen, Konflikt benennen, kleinste Regeländerung vorschlagen, auf Freigabe
  warten (Details: `STORY-025`).
- Beim Hinzufügen oder Ändern einer mechanisch prüfbaren Regel einen
  Architektur-Test vorschlagen und in der Regel darauf verweisen.
- Regeln englisch mit MUST/SHOULD/MAY schreiben. Die Wurzel kurz halten;
  Spezielles gehört in einen Scope.

## Other modules

- `techdocs`: Der Ordner `development` zählt weder als Doku noch als
  Projektänderung.
- `init`: fragt nach der Suite und ihren Teilbereichen und bietet an, die
  Wurzel aus der Vorlage anzulegen.
- Neu in `interfaces.md` und `configuration.md` dokumentieren.

## Application in this repo

`docs/development/architecture.md` mit einigen bestehenden, tatsächlich
geltenden Regeln dieses Repos (z. B. Skripte nur mit Standardbibliothek,
Produkt nur unter `plugin/`). Die Ladestufen-Regel folgt mit `STORY-019`.

## Tests

- Config: Suite-Schalter, Teilbereich-Standard, unbekannte Schlüssel.
- Scope-Tabelle: Parsen, Pfadmuster mit `*` und `**`, Fehlerfälle.
- Hooks: Blockieren ohne Lesen, Durchlassen nach vollständigem Lesen,
  Teil-Lesen zählt nicht, Scope-Datei nötig nur für passende Pfade,
  ausgenommene Pfade, Reset nach `compact`, Suite aus → nichts.
