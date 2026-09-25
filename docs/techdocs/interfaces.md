# Schnittstellen

Öffentliche Schnittstellen des Plugins: Befehle, Skills, Hooks, Skripte und
Dateiformate.

## Befehl `/claude-harness:init`

- Zweck: Harness in einem Projekt oder einem Teilprojekt einrichten.
- Aufruf: nur durch den Nutzer (`disable-model-invocation`).
- Wirkung: fragt zuerst, ob das Projekt selbst oder ein Teilprojekt (Ordner
  und Name) eingerichtet wird; alle Pfade gelten dann relativ zu diesem
  Zielordner. Fragt Sprache, Doku-Ordner, Module und deren Pfade sowie, nur
  im Root-Projekt, den Pfad zum Harness-Repo (Vorschlag über
  `harness_repo.py --suggest`) ab; schreibt `.claude-harness/config.toml` und
  auf Wunsch Backlog, Systemdoku und Architekturregeln aus den Vorlagen,
  jeweils erst nach Freigabe. Ein Teilprojekt wird in `[projects]` der
  Root-Config eingetragen (fehlt sie, auf Freigabe als reine Registry
  angelegt); auf Wunsch übernimmt es Regeln des Root-Projekts unter
  `## Inherited rules`. Fragt, ob `.claude-harness/` in die `.gitignore`
  soll, und weist auf die Aktivierung über `.claude/settings.local.json` hin.
- Fehlerfall: Ist die Config im Zielordner schon vorhanden, zeigt er sie und
  ändert nichts.

## Befehl `/claude-harness:update`

- Zweck: die `.claude-harness/config.toml` eines bereits eingerichteten
  Projekts oder Teilprojekts auf das aktuelle Schema bringen.
- Aufruf: nur durch den Nutzer (`disable-model-invocation`).
- Wirkung: fragt, welches Projekt (Root oder ein registriertes
  Teilprojekt) aktualisiert wird; vergleicht dessen `version` mit
  `CONFIG_VERSION` (`harness_config.py`). Ist sie gleich, meldet er
  "bereits aktuell" und ändert nichts. Ist sie älter und es gibt einen
  durchgängigen Migrationspfad (`MIGRATIONS`), zeigt er die fehlenden
  Schritte in Klartext, fragt nur bei neuen, nicht aus der
  Migrationsbeschreibung ableitbaren Werten nach, zeigt die konkrete
  Änderung an der Datei und schreibt sie erst nach Freigabe — bestehende
  Kommentare und unveränderte Werte bleiben erhalten. Ein Aufruf
  aktualisiert genau ein Projekt; Teilprojekte werden einzeln aufgerufen.
- Fehlerfall: Fehlt die Config im Zielordner, verweist er auf
  `/claude-harness:init` statt etwas anzulegen. Ist die Version neuer als
  `CONFIG_VERSION` oder gibt es keinen durchgängigen Migrationspfad, meldet
  er das als ungültige Konfiguration, wie `init` und der
  Session-Start-Hook es auch sonst tun.

## Skills

| Skill | Wird geladen, wenn … |
|---|---|
| `claude-harness:todo` | mit dem Backlog gearbeitet wird |
| `claude-harness:daily` | der Daily-Hook erinnert oder nach Tagesberichten gefragt wird |
| `claude-harness:techdocs` | eine Änderung Nutzung, Komponenten, Schnittstellen, Einstellungen oder Betrieb betrifft oder der techdocs-Hook erinnert |
| `claude-harness:architecture` | Code geplant oder geändert wird, Architekturregeln geändert werden, eine Anforderung den Regeln widerspricht oder der Architektur-Hook eine Änderung ablehnt |
| `claude-harness:decomposition` | eine Umsetzung geplant oder begonnen, ein Umsetzungsplan vorgelegt oder überlegt wird, ob ein Backlog-Item Kind-Tasks bekommt |
| `claude-harness:semver` | eine Änderung in den Hauptzweig gemergt wird, ein Release gewünscht ist, der SemVer-Hook erinnert oder das Modul eingerichtet wird |
| `claude-harness:conflicts` | eine Anforderung oder ein Wunsch des Projektverantwortlichen den Projektregeln oder einer Harness-Vorgabe widerspricht oder der Harness selbst ein Problem verursacht; gilt unabhängig von den Modul-Schaltern |

## Hooks

Alle Hooks lesen die Hook-Eingabe von Claude Code als JSON auf stdin und
tun nichts, wenn ihr Modul aus oder die Config ungültig ist. Arbeitet die
Session in einem Worktree von Claude Code (`.claude/worktrees/<Name>/`),
gilt dieser Worktree als Projekt-Root: erkannt am `cwd` der Hook-Eingabe
oder am Pfad der bearbeiteten Datei. Config, Dokumente und Pfade werden
dann aus dem Worktree gelesen und relativ zu ihm bewertet.

| Ereignis | Skript | Verhalten | Ausgabe |
|---|---|---|---|
| SessionStart (`startup`, `resume`, `clear`, `compact`) | `session_start.py` | Kurzfassung von Config und Zustand, Fehler der Scope-Tabelle und der Tabelle geerbter Regeln; mit Teilprojekten (`[projects]`) eine Zeile pro Projekt, jeder Skill-Hinweis einmal, Meldungen mit Projektnamen, Zeile für jedes Teilprojekt ohne oder mit ungültiger Config; bei aktivem Teilbereich `worktree` in einem Git-Repo eine Fehlerzeile, wenn `worktree.baseRef` nicht `"head"` ist (gelesen aus `.claude/settings.local.json`, `.claude/settings.json` und `~/.claude/settings.json` in dieser Rangfolge; unlesbare Dateien zählen als nicht gesetzt); bei `clear` und `compact` werden die Lese-Merker der Architekturregeln gelöscht | stdout → Kontext |
| PreToolUse (`Write`, `Edit`, `MultiEdit`, `NotebookEdit`, `ExitPlanMode`) | `check_architecture.py` | Lehnt ab, solange die Architekturregeln in der Session nicht vollständig gelesen wurden: das Vorlegen eines Plans (`ExitPlanMode`), das Schreiben einer Backlog-Spec (`<ID>_spec.md`, `<ID>_spec_<Thema>.md`) und die Änderung einer Projektdatei; bei Projektdateien zusätzlich die Datei jedes passenden Scopes. Mit Teilprojekten gelten die Regeln des Projekts, zu dem die Datei gehört (bei einer Spec: dessen Backlog); ein Plan verlangt die Regeln jedes Projekts, dessen Pfad im Plantext vorkommt, sonst die des Root-Projekts. Dateien in unwirksamen Teilprojekten werden nicht geprüft | JSON mit `permissionDecision: deny` und Grund |
| PostToolUse (`Write`, `Edit`, `MultiEdit`) | `mark_backlog_dirty.py` | Merker, wenn eine Datei im Backlog-Ordner geändert wurde; bei Teilprojekten mit dem Namen des Projekts, zu dem der Backlog gehört | keine |
| PostToolUse (`Write`, `Edit`, `MultiEdit`) | `mark_techdocs.py` | Merker „Projekt geändert“ bzw. „Doku geändert“, pro Projekt; `README.md` und Systemdoku zählen nur für ihr eigenes Projekt | keine |
| PostToolUse (`Read`) | `mark_architecture_read.py` | Merker, wenn die Architekturregeln oder eine Scope-Datei vollständig gelesen wurden (kein `offset` > 1, kein `limit` unter der Zeilenzahl); zählt nur für das Projekt, in dem die Datei liegt | keine |
| Stop | `check_backlog.py` | Prüft jeden in der Session geänderten Backlog (pro Projekt, Meldung mit Backlog-Pfad relativ zum Session-Root); neue Hinweise einmal pro Projekt und Session | Exit 2 + stderr bei Fehlern/neuen Hinweisen |
| Stop | `check_daily.py` | Erinnert bei neuen, nicht erfassten Commits auf dem Hauptzweig (nur Haupt-Checkout; Commits nur im Daily- oder Backlog-Ordner zählen nicht), einmal pro HEAD, Projekt und Session; mit Teilprojekten eine Meldung, die jedes Projekt mit offenen Commits nennt, samt Aufruf `daily.py pending --project <Name>` | Exit 2 + stderr |
| Stop | `check_techdocs.py` | Erinnert einmal pro Projekt und Session, wenn Projektdateien, aber keine Systemdoku desselben Projekts geändert wurden; mit Teilprojekten nennt die Meldung jedes betroffene Projekt mit seinen Doku-Pfaden | Exit 2 + stderr |
| Stop | `check_semver.py` | Nur in einem Git-Repo. Meldet pro Projekt mit Modul `semver`: Versionsdatei fehlt oder enthält keine gültige Version; Version liegt unter dem letzten Release oder mehr als einen Schritt darüber; eine Spiegel-Datei fehlt oder enthält die Version nicht. Derselbe Befund wird einmal pro Projekt und Session gemeldet; mit Teilprojekten nennt die Meldung jedes Projekt samt Aufruf `semver.py status --project <Name>` | Exit 2 + stderr |

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

- Aufruf: `python3 plugin/scripts/daily.py pending|ack [--project <Name>]`
  im Projekt-Root (oder mit gesetztem `CLAUDE_PROJECT_DIR`). Ohne
  `--project` gilt das Root-Projekt.
- `pending`: Pfad des heutigen Berichts relativ zum Session-Root
  (`exists`/`new`), Dokumentsprache und offene Commits (kurzer Hash, Datum,
  Betreff), älteste zuerst. Ein Commit zählt nur, wenn er Dateien des
  Projekts außerhalb seines Daily- und Backlog-Ordners ändert; für das
  Root-Projekt zählen Dateien in eingetragenen Teilprojekten nicht. Das gilt
  auch, wenn das Projekt unterhalb des Git-Roots liegt.
- `ack`: setzt den bestätigten Stand des Projekts auf HEAD.
- Exit-Code 1, wenn das Modul im gewählten Projekt aus ist (die Meldung
  nennt die Projekte mit Daily), das Projekt unbekannt oder unwirksam ist
  oder nicht im Haupt-Checkout auf dem Hauptzweig aufgerufen wird; 2 bei
  falschem Aufruf.
- Hauptzweig: Ziel von `origin/HEAD`, sonst `main`, sonst `master`.

## Skript `harness_repo.py`

- Aufruf: `python3 plugin/scripts/harness_repo.py [--suggest]` im
  Projekt-Root (oder mit gesetztem `CLAUDE_PROJECT_DIR`).
- Ohne Option: gibt den ersten Pfad aus `harness.repo` aus, der existiert und
  das Harness-Repo ist (`plugin/.claude-plugin/plugin.json` mit
  `"name": "claude-harness"`); sonst keine Ausgabe, auch bei fehlender oder
  ungültiger Config.
- `--suggest`: schlägt einen Pfad aus
  `~/.claude/plugins/known_marketplaces.json` vor, nur aus Marketplaces mit
  Quelle `directory`, deren Verzeichnis das Harness-Repo ist. Die Datei gehört
  Claude Code und dient nur dem Vorschlag; fehlt sie oder passt ihr Format
  nicht, gibt es keine Ausgabe.
- Exit-Code 0, 2 bei falschem Aufruf.

## Skript `worktree.py`

- Aufruf: `python3 plugin/scripts/worktree.py start|check` im Worktree eines
  Changes (Arbeitsverzeichnis, nicht `CLAUDE_PROJECT_DIR`). Die AI ruft es
  laut Skill `worktree` auf.
- Ausgabe: Zeilen `key: value`; bei Fehlern `error: <Grund>`.
- `start`: speichert den im Haupt-Checkout ausgecheckten Branch als
  Ausgangsbranch in `branch.<worktree-branch>.harnessBase` und spiegelt die
  ignorierten Dateien des Haupt-Checkouts in den Worktree. `node_modules`,
  `.venv` und `venv` werden verlinkt, `__pycache__`, `.pytest_cache`,
  `.mypy_cache`, `dist` und `build` ausgelassen, `.git` und
  `.claude/worktrees/` nie übernommen; vorhandene Dateien bleiben
  unverändert. Ausgabe: `base`, `copied: <n> files`, `linked`, `skipped`
  (Listen oder `none`).
- `check`: Befunde vor dem Merge: `base`, `main` (Pfad des Haupt-Checkouts),
  `clean` (keine nicht committeten oder unversionierten, nicht ignorierten
  Dateien im Worktree), `base_moved` (Ausgangsbranch hat Commits, die im
  Worktree fehlen), `main_on_base` (Haupt-Checkout steht noch auf dem
  Ausgangsbranch).
- Exit-Code: 0; 1 bei Fehlern (nicht in einem Worktree, Haupt-Checkout
  detached, kein Ausgangsbranch gespeichert) und bei `check`, wenn `clean`
  oder `main_on_base` `no` ist; 2 bei falschem Aufruf.

## Skript `semver.py`

- Aufruf: `python3 plugin/scripts/semver.py status [--project <Name>]` im
  Projekt-Root (oder mit gesetztem `CLAUDE_PROJECT_DIR`). Ohne `--project`
  gilt das Root-Projekt.
- `status`: Versionsdatei und Version, letztes Release, erlaubte nächste
  Versionen (unverändert, patch, minor, major), Tag-Format, Spiegel-Dateien,
  Befunde wie beim Stop-Hook und die Commits seit dem letzten Release unter
  `semver.paths` (kurzer Hash, Datum, Betreff), älteste zuerst. Für das
  Root-Projekt zählen Commits in eingetragenen Teilprojekten nicht.
- Letztes Release: der Tag `<Präfix><MAJOR.MINOR.PATCH>` mit der höchsten
  Version (nicht dem jüngsten Datum). Präfix `v` im Root-Projekt,
  `<Projektname>-v` in einem Teilprojekt. Andere Tags werden ignoriert.
- Das Skript liest nur; Versionsdatei, Spiegel-Dateien, Release-Commit und
  Tag schreibt Claude nach Skill `semver`.
- Exit-Code 1, wenn das Modul im gewählten Projekt aus ist oder die Config
  ungültig ist; 2 bei falschem Aufruf.
- In diesem Repo spiegelt `plugin/.claude-plugin/plugin.json` die Version.
  Claude Code hält installierte Plugins auf dieser Version fest, bis sie sich
  ändert. Zielprojekte erhalten Änderungen am Plugin also erst mit einem
  Release. Ausgenommen sind Plugins, die direkt aus einem lokal
  hinzugefügten Marketplace-Ordner geladen werden.

## Dateiformate

| Datei | Format | Definition |
|---|---|---|
| `.claude-harness/config.toml` | TOML | [configuration.md](configuration.md) |
| `TODO.md`, `archive.md`, `items/<ID>/` | Backlog-Format v1 (Markdown) | `plugin/skills/todo/format.md` |
| `<YYYY-MM-DD>_daily.md` | Markdown nach Vorlage | `plugin/templates/daily/daily.md`, Skill `daily` |
| Systemdoku | Markdown nach Vorlagen | `plugin/templates/techdocs/` |
| Versionsdatei (`semver.file`, Standard `docs/VERSION`) | eine Zeile `MAJOR.MINOR.PATCH` (Ganzzahlen ohne führende Nullen), keine Vorabversionen | Skill `semver` |
| Release-Tag | annotierter Tag `<Präfix><Version>`, z. B. `v0.2.0`, `ezf-ui-v1.4.0` | Skill `semver` |
| `architecture.md`, `architecture/<Scope>.md` | Markdown, englisch, Regeln mit MUST/SHOULD/MAY; Abschnitt `## Scopes` mit Tabelle `\| Scope \| Paths \| Covers \|`, optional `## Inherited rules` mit Tabelle `\| Project \| Rules \|` | `plugin/templates/development/architecture.md`, Skill `architecture` |

Scope-Tabelle: Name aus Kleinbuchstaben, Ziffern und `-`; Datei
`architecture/<Scope>.md` neben der Regeldatei. Pfadmuster relativ zum
Projekt-Root in Backticks, kommagetrennt; `*` und `?` innerhalb eines
Pfadteils, `**` über beliebig viele Pfadteile. HTML-Kommentare werden
ignoriert. Ein Scope gilt zusätzlich zur Regeldatei.

Tabelle der geerbten Regeln (nur bei Teilprojekten sinnvoll): `Project` ist
ein Name aus `[projects]` der Root-Config oder `root`, nicht das eigene
Projekt; `Rules` sind in Backticks `architecture.md` (Hauptdatei jenes
Projekts) oder Scope-Namen jenes Projekts. Ein geerbter Scope gilt unabhängig
von seinen Pfadmustern; es wird nicht weitervererbt. Der Architektur-Hook
verlangt die geerbten Dateien vor jeder Änderung einer Projektdatei;
fehlerhafte Einträge (unbekanntes oder unwirksames Projekt, Projekt ohne
Architektur, unbekannter Scope, fehlende Datei) überspringt er, der
Session-Start meldet sie.
