# STORY-057 — Spec: Pflichtlektüre bei Nutzung bestimmter Bezeichner

Teil von EPIC-011. Baut auf STORY-054 auf (Pflichtlektüre, Markierung).

## Anlass

In ezf-ui zeigten zwei Plugins technische Fehler nur mit `modals.alert` statt über
`reportError`, obwohl das festgelegt war. Der Fehler entsteht beim Schreiben von Code, nicht
beim Lesen; eine Pflicht über Pfade fängt ihn nicht, eine allgemeine Rückfrage per Hook
wird abgenickt (Notes EPIC-011).

## Format

In `architecture.md` oder in einer Scope-Datei:

```
## Required on use

| Uses | Read |
|---|---|
| `reportError`, `modals.alert` | `docs/development/interfaces/core/errors.md` |
```

- In `architecture.md`: gilt für alle Projektdateien außer Harness-Dateien.
  In einer Scope-Datei: gilt nur für Dateien in den Pfaden dieses Scopes.
- Uses: Bezeichner in Backticks, kommagetrennt; erlaubt sind Zeichen
  `[A-Za-z0-9_$.]`, mindestens ein Buchstabe. Read: Dateien relativ zum Projekt-Root
  (wie Required reading).
- Fehler (Sitzungsstart): ungültiger Bezeichner, ungültiger Pfad, Datei fehlt.

## Hook

- `check_architecture.py` bei Write (content), Edit (new_string), MultiEdit (alle
  new_string), NotebookEdit (new_source): sucht jeden Bezeichner als Literal mit
  Wortgrenzen (nicht direkt von `[A-Za-z0-9_$]` umgeben; `.` im Bezeichner ist literal).
- Treffer und Read-Datei nicht gelesen → deny: `before using <bezeichner> in <datei>,
  read <doc> in full with the Read tool, then retry.` Mehrere fehlende zusammenfassen.
- Läuft nach der bestehenden Pflichtprüfung, im selben Aufruf.
- Geerbte Scopes: ihre Tabellen gelten mit (Pfade relativ zum definierenden Projekt).
  `architecture.md` eines geerbten Projekts ebenfalls, wenn sie geerbt wird.
- Vollständige Reads der Read-Dateien markiert `mark_architecture_read.py`.

## Kosten

Pro Edit werden `architecture.md` und die passenden Scope-Dateien ohnehin geparst; die
Tabellen kommen hinzu. Keine Netz- oder Git-Aufrufe.

## Doku und Tests

Skill architecture (Abschnitt Format, kurz), Vorlagen (Abschnitt als Kommentar), Techdocs
des Harness. Unit-Tests: Parsing und Fehler, Treffer/Nicht-Treffer mit Wortgrenzen
(`reportErrorX`, `x.reportError`), Gültigkeit nur in Scope-Pfaden, alle Tool-Arten,
Freigabe nach Read, Vererbung.
