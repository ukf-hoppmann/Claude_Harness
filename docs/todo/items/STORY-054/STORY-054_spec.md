# STORY-054 — Spec: Pflichtlektüre je Scope

Teil von EPIC-011. Baut auf STORY-053 auf (gleiche Dateien, deshalb danach).

## Ziel

Wer eine Datei in den Pfaden eines Scopes ändert, hat vorher die Regeln des Bereichs
und dessen Schnittstellen-Doku gelesen. Die Pflicht ergibt sich vollständig aus der
einen Scope-Tabelle in `architecture.md`, nicht aus Verweisketten.

## Tabellenformat

```
| Scope | Paths | Required reading | Covers |
|---|---|---|---|
| plugins | `src/plugins/**` | `docs/development/interfaces/plugins.md` | Plugin contract |
```

- Die Spalte `Required reading` ist optional. Erkannt wird sie über die Kopfzeile
  (Zelle `Required reading`, Groß-/Kleinschreibung egal). `Scope` und `Paths` bleiben
  Spalte 1 und 2. Ohne die Spalte gilt die Tabelle unverändert (drei Spalten).
- Werte: Dateipfade relativ zum Projekt-Root (Entscheidung E2) in Backticks,
  kommagetrennt, leer erlaubt. Keine Muster, kein führender `/`, kein `..`.
- Fehler (Sitzungsstart, wie heutige Tabellenfehler): ungültiger Pfad, Datei fehlt.

## Hook

- `required_files` liefert zusätzlich die Pflichtlektüre aller passenden Scopes;
  `check_architecture.py` verlangt sie wie Scope-Dateien und nennt fehlende Dateien.
- Geerbte Scopes (`## Inherited rules`): ihre Pflichtlektüre gilt mit, Pfade relativ
  zum Projekt, das den Scope definiert, im Zustand relativ zur Session-Wurzel gespeichert
  (wie heute bei geerbten Dateien).
- Ausnahme `is_harness_file` und die Prüfung bei ExitPlanMode bleiben unverändert.

## Markierung

`mark_architecture_read.py` markiert einen vollständigen Read zusätzlich, wenn die Datei
als Pflichtlektüre in einem Scope des eigenen Projekts steht oder in einem Scope, den ein
Projekt der Session erbt. Gleiche Vollständigkeitsregel wie heute. Zustand bleibt in
`architecture_read_file`; so gestalten, dass STORY-057 weitere Dateien markieren kann
(z. B. eine Hilfsfunktion „Dateien, deren Read zählt“).

## Doku

Skill architecture (Tabellenformat, kurzer Satz: Pflichtlektüre kurz halten), Vorlage
`plugin/templates/development/architecture.md` (Spalte und Beispielzeile), Techdocs des
Harness. Inhaltliche Regeln zu Pflicht gegen Nachschlagen kommen in STORY-058.

## Tests

Altes und neues Format, ungültige und fehlende Pflichtdateien, Hook blockiert und gibt
frei, Markierung, Vererbung.
