# Schnittstellen

Öffentliche Schnittstellen des Plugins: Befehle, Skills, Hooks, Skripte und
Dateiformate.

## Befehl `/claude-harness:init`

- Zweck: Harness in einem Projekt einrichten.
- Aufruf: nur durch den Nutzer (`disable-model-invocation`).
- Wirkung: fragt Sprache, Doku-Ordner, Module und deren Pfade ab; schreibt
  `.claude-harness/config.toml` und auf Wunsch Backlog, Systemdoku und
  Architekturregeln aus den Vorlagen, jeweils erst nach Freigabe.
- Fehlerfall: Ist die Config schon vorhanden, zeigt er sie und ändert nichts.

## Skills

| Skill | Wird geladen, wenn … |
|---|---|
| `claude-harness:todo` | mit dem Backlog gearbeitet wird |
| `claude-harness:daily` | der Daily-Hook erinnert oder nach Tagesberichten gefragt wird |
| `claude-harness:techdocs` | eine Änderung Nutzung, Komponenten, Schnittstellen, Einstellungen oder Betrieb betrifft oder der techdocs-Hook erinnert |
| `claude-harness:architecture` | Code geplant oder geändert wird, Architekturregeln geändert werden, eine Anforderung den Regeln widerspricht oder der Architektur-Hook eine Änderung ablehnt |

## Hooks

Alle Hooks lesen die Hook-Eingabe von Claude Code als JSON auf stdin und
tun nichts, wenn ihr Modul aus oder die Config ungültig ist.

| Ereignis | Skript | Verhalten | Ausgabe |
|---|---|---|---|
| SessionStart (`startup`, `resume`, `clear`, `compact`) | `session_start.py` | Kurzfassung von Config und Zustand, Fehler der Scope-Tabelle; bei `clear` und `compact` werden die Lese-Merker der Architekturregeln gelöscht | stdout → Kontext |
| PreToolUse (`Write`, `Edit`, `MultiEdit`, `NotebookEdit`, `ExitPlanMode`) | `check_architecture.py` | Lehnt ab, solange die Architekturregeln in der Session nicht vollständig gelesen wurden: das Vorlegen eines Plans (`ExitPlanMode`), das Schreiben einer Backlog-Spec (`<ID>_spec.md`, `<ID>_spec_<Thema>.md`) und die Änderung einer Projektdatei; bei Projektdateien zusätzlich die Datei jedes passenden Scopes | JSON mit `permissionDecision: deny` und Grund |
| PostToolUse (`Write`, `Edit`, `MultiEdit`) | `mark_backlog_dirty.py` | Merker, wenn eine Datei im Backlog-Ordner geändert wurde | keine |
| PostToolUse (`Write`, `Edit`, `MultiEdit`) | `mark_techdocs.py` | Merker „Projekt geändert“ bzw. „Doku geändert“ | keine |
| PostToolUse (`Read`) | `mark_architecture_read.py` | Merker, wenn die Architekturregeln oder eine Scope-Datei vollständig gelesen wurden (kein `offset` > 1, kein `limit` unter der Zeilenzahl) | keine |
| Stop | `check_backlog.py` | Prüft den Backlog nach Änderungen; neue Hinweise einmal pro Session | Exit 2 + stderr bei Fehlern/neuen Hinweisen |
| Stop | `check_daily.py` | Erinnert bei neuen, nicht erfassten Commits auf dem Hauptzweig (nur Haupt-Checkout; Commits nur im Daily- oder Backlog-Ordner zählen nicht), einmal pro HEAD und Session | Exit 2 + stderr |
| Stop | `check_techdocs.py` | Erinnert einmal pro Session, wenn Projektdateien, aber keine Systemdoku geändert wurden | Exit 2 + stderr |

Bei gesetztem `stop_hook_active` bleiben die Stop-Hooks still, damit keine
Schleife entsteht.

Klassifikation für `techdocs`: Als Doku zählen `README.md` im Projekt-Root und
Dateien im techdocs-Ordner. Nicht berücksichtigt werden Dateien außerhalb des
Projekts, im Backlog-, Daily- oder development-Ordner, unter `.git/` und
`.claude-harness/` sowie Tests (Pfadteil `test`/`tests`, Dateiname `test_*`, `*_test.*`,
`*.test.*`). Alles andere im Projekt zählt als Projektänderung. Änderungen über Bash statt Write/Edit
erkennt der Hook nicht.

Projektdateien für `architecture`: alle Dateien im Projekt außer `README.md`,
`.git/`, `.claude-harness/` und den Ordnern von Backlog, Tagesberichten,
Systemdoku und `development`. Tests zählen dazu. Backlog-Specs sind
Harness-Dateien, verlangen aber ebenfalls die gelesene Regeldatei, weil sie
die Grundlage eines Plans sind. Fehlt die Regeldatei, wird nichts abgelehnt. Änderungen über Bash sieht der Hook nicht.

## Skript `backlog.py`

- Aufruf: `python3 plugin/scripts/backlog.py <backlog-ordner> [--index]`
- Ohne `--index`: listet Fehler und Hinweise und eine Zusammenfassung.
- Mit `--index`: eine Zeile pro Eintrag über `TODO.md` und `archive.md`
  (`ID | Type | Status | Title | Parent`).
- Exit-Code: 0 ohne Fehler, 1 bei Fehlern, 2 bei falschem Aufruf.

## Skript `daily.py`

- Aufruf: `python3 plugin/scripts/daily.py pending|ack` im Projekt-Root
  (oder mit gesetztem `CLAUDE_PROJECT_DIR`).
- `pending`: Pfad des heutigen Berichts (`exists`/`new`), Dokumentsprache und
  offene Commits (kurzer Hash, Datum, Betreff), älteste zuerst. Commits, die
  nur den Daily- oder Backlog-Ordner ändern, werden ausgelassen.
- `ack`: setzt den bestätigten Stand auf HEAD.
- Exit-Code 1, wenn das Modul aus ist oder nicht im Haupt-Checkout auf dem
  Hauptzweig aufgerufen wird; 2 bei falschem Aufruf.
- Hauptzweig: Ziel von `origin/HEAD`, sonst `main`, sonst `master`.

## Dateiformate

| Datei | Format | Definition |
|---|---|---|
| `.claude-harness/config.toml` | TOML | [configuration.md](configuration.md) |
| `TODO.md`, `archive.md`, `items/<ID>/` | Backlog-Format v1 (Markdown) | `plugin/skills/todo/format.md` |
| `<YYYY-MM-DD>_daily.md` | Markdown nach Vorlage | `plugin/templates/daily/daily.md`, Skill `daily` |
| Systemdoku | Markdown nach Vorlagen | `plugin/templates/techdocs/` |
| `architecture.md`, `architecture/<Scope>.md` | Markdown, englisch, Regeln mit MUST/SHOULD/MAY; Abschnitt `## Scopes` mit Tabelle `\| Scope \| Paths \| Covers \|` | `plugin/templates/development/architecture.md`, Skill `architecture` |

Scope-Tabelle: Name aus Kleinbuchstaben, Ziffern und `-`; Datei
`architecture/<Scope>.md` neben der Regeldatei. Pfadmuster relativ zum
Projekt-Root in Backticks, kommagetrennt; `*` und `?` innerhalb eines
Pfadteils, `**` über beliebig viele Pfadteile. HTML-Kommentare werden
ignoriert. Ein Scope gilt zusätzlich zur Regeldatei.
