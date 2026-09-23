# STORY-013 — Spec: Daily-Development-Report

## Goal

Ein optionales Modul `daily` führt pro Arbeitstag einen Bericht über die
relevanten Änderungen, die auf dem Hauptzweig angekommen sind. So bleibt
nachvollziehbar, wann was geändert wurde, ohne jede Kleinigkeit festzuhalten.

## Config

Erweiterung der Projektkonfiguration (bleibt `version = 1`):

```toml
[docs]
root = "docs"                # relativ zum Projekt-Root; Standard "docs"
language = "de"              # ISO 639-1, zwei Kleinbuchstaben; Standard "en"

[modules]
daily = true                 # Standard: aus

[todo]
path = "todo"                # relativ zu docs.root; Standard "todo"

[daily]
path = "development/daily"   # relativ zu docs.root; Standard
```

- `docs.language` gilt für alle vom Harness erzeugten Dokumente (Fließtext und
  Überschriften), nicht für maschinell geprüfte Feldnamen. Ein Sprachwechsel
  übersetzt bestehende Dokumente nicht.
- Validierung wie bisher: unbekannte Schlüssel, absolute Pfade und `..` sind
  Fehler; zusätzlich ein ungültiger Sprachcode.

## Storage

- Datei: `<docs.root>/<daily.path>/<YYYY-MM-DD>_daily.md`.
- Ein Bericht pro Kalendertag mit relevanter Arbeit; kein leerer Bericht.
  Mehrere Sessions ergänzen denselben Bericht.
- Geschrieben wird nur im Haupt-Checkout (kein verknüpfter Worktree) auf dem
  Hauptzweig, nachdem die Änderung dort angekommen ist (Merge oder lokaler
  Commit). Datum ist das lokale Systemdatum beim Schreiben, also der Tag der
  Ankunft auf dem Hauptzweig.
- Hauptzweig: Ziel von `origin/HEAD`, falls gesetzt; sonst `main`, sonst
  `master`.

## Format

- Titel `# Daily Development — YYYY-MM-DD`; Überschriften in
  `docs.language`.
- Nachträglich erstellte Berichte tragen direkt unter dem Titel einen
  entsprechenden Hinweis.
- Zusammenfassung als kurzer Fließtext.
- Danach Tabellen: Features (neu, geändert, entfernt/abgelehnt/
  zurückgestellt), Bugfixes, technische/Doku-/Betriebsänderungen,
  Entscheidungen und Alternativen, Verifikation, offene Punkte und nächste
  Schritte, Referenzen. Leere Abschnitte entfallen.
- Evidence-Spalte: kurzer Commit-Hash und Backlog-ID. Bei aktivem
  `todo`-Modul ist die ID ein relativer Link auf `items/<ID>/`, falls der
  Ordner existiert, sonst nur die ID. Uhrzeiten liefert Git.
- Vorlage: `plugin/templates/daily/daily.md`.

## Rules

- Relevanz ist ergebnisorientiert; zusammenhängende Schritte werden gebündelt.
  Erkundungen, Zwischenentwürfe, kleine Formulierungs- und Formatänderungen
  und Wiederholungen bestehender Entscheidungen zählen nicht. Planung zählt,
  wenn sie eine Entscheidung, ein umsetzungsreifes Ziel, eine Abgrenzung, ein
  Risiko oder einen wichtigen nächsten Schritt festlegt oder ändert.
- Wahrhaftigkeit: keine behauptete Verifikation; Gemessenes und Vermutetes
  getrennt; nachträglich Erstelltes gekennzeichnet, Lücken bleiben sichtbar;
  unfertige, abgelehnte und zurückgestellte Arbeit bleibt sichtbar.
- Vor dem Schreiben den bestehenden Bericht lesen und vorhandene Zeilen
  aktualisieren statt doppelt einzutragen.
- Nur der heutige Bericht wird geändert; frühere Berichte nur per datierter
  Korrektur, die ursprüngliche Aussage bleibt stehen.
- Keine Geheimnisse und keine rohen Logs im Bericht.

## Hook

`Stop`-Hook `check_daily.py`. Er erinnert Claude (Exit 2), wenn alle Bedingungen
gelten:

- Modul `daily` ist an und die Config gültig;
- das Projekt ist der Haupt-Checkout und der Hauptzweig ist ausgecheckt;
- seit dem bestätigten Stand gibt es Commits, die nicht ausschließlich
  Dateien im Daily-Ordner ändern;
- für diesen HEAD wurde in dieser Session noch nicht erinnert, und
  `stop_hook_active` ist nicht gesetzt.

Ohne gespeicherten Stand setzt der Hook den aktuellen HEAD still als
Ausgangspunkt. Ist der gespeicherte Stand kein Vorfahre von HEAD mehr, gilt
dasselbe.

## Confirmed state

- Pro Klon im Git-Verzeichnis (`.git/claude-harness/daily-ack`), damit Hook
  und `daily.py` denselben Stand sehen und er nie committet wird.
- `daily.py pending` zeigt Zielpfad des heutigen Berichts und die offenen
  Commits (Hash, Datum, Betreff).
- `daily.py ack` setzt den bestätigten Stand auf HEAD, auch wenn nichts
  relevant war und kein Bericht entsteht.

## Affected files

- `plugin/scripts/harness_config.py`, `plugin/templates/config.toml`,
  `.claude-harness/config.toml`
- `plugin/scripts/daily.py`, `plugin/scripts/check_daily.py`,
  `plugin/scripts/state.py`, `plugin/scripts/session_start.py`,
  `plugin/hooks/hooks.json`
- `plugin/skills/daily/SKILL.md`, `plugin/templates/daily/daily.md`,
  `plugin/skills/init/SKILL.md`
- `tests/test_config.py`, `tests/test_hooks.py`, `tests/test_daily.py`

## Acceptance criteria

- Relevante Commits auf dem Hauptzweig führen zu einer Erinnerung und zu einem
  Bericht für den heutigen Tag.
- Nur irrelevante Commits führen nach `ack` zu keinem Bericht.
- Keine Erinnerung in einem Worktree, auf einem anderen Zweig, bei
  abgeschaltetem Modul oder wenn nur der Daily-Ordner geändert wurde.
- Pro HEAD und Session höchstens eine Erinnerung.
