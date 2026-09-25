# STORY-027 — Spec: Harness pro Teilprojekt

## Ziel

Ein Repository enthält mehrere Harness-Projekte: optional das Root-Projekt
(z. B. Plugin-Core) und beliebig viele Teilprojekte (z. B. je ein Plugin unter
`Plugins/<Name>`). Jedes Projekt hat eigene Konfiguration, Sprache, Backlog,
Daily Reports, techdocs und Architekturregeln. Die Session startet im
Repo-Root. Für jede bearbeitete Datei gelten Konfiguration und Dokumente des
Projekts, zu dem sie gehört.

Nebenbei wird der Fall „Session startet im Teilprojekt, Git-Root liegt
darüber“ (Fall 1) korrekt, soweit er von derselben Ursache abhängt:
Projekt-Root und Git-Root sind verschieden.

## Hintergrund (geprüft am 2026-09-25)

Claude Code lädt `.claude/settings.json` nur aus dem Startverzeichnis der
Session, weder aus Unterordnern noch aus Ordnern darüber (Notes, gleiches
Datum). Beim Start im Root gelten deshalb für alle Projekte dieselben
Claude-Code-Settings und Hooks. Die Unterscheidung nach Projekt leistet der
Harness selbst.

## Begriffe

- **Session-Root:** `CLAUDE_PROJECT_DIR` bzw. cwd, wie heute
  (`project_root()` in `harness_config.py`).
- **Root-Projekt:** das Projekt mit der Konfiguration
  `<Session-Root>/.claude-harness/config.toml`. Name `root`.
- **Teilprojekt:** ein Eintrag in `[projects]` des Root-Projekts mit eigener
  `<pfad>/.claude-harness/config.toml`.
- **Projekt-Root:** das Verzeichnis, gegen das die Pfade einer Konfiguration
  aufgelöst werden. Beim Root-Projekt ist das das Session-Root, beim
  Teilprojekt `<Session-Root>/<pfad>`.

## Config

Neue Tabelle, nur in der Konfiguration des Root-Projekts erlaubt (bleibt
`version = 1`):

```toml
[projects]
VariantFilter = "Plugins/VariantFilter"
OtherPlugin   = "Plugins/OtherPlugin"
```

- Schlüssel: Projektname, Muster `[A-Za-z][A-Za-z0-9_-]*`. `root` ist
  reserviert.
- Wert: relativer Pfad ohne `..`, nicht leer, nicht `.`.
- Pfade dürfen sich nicht überlappen: Kein Pfad liegt in einem anderen.
  Verschachtelte Teilprojekte gibt es nicht.
- In der Konfiguration eines Teilprojekts ist `[projects]` ein Fehler,
  ebenso `[harness]`. Das gilt nur für das Root-Projekt.
- Das Root-Projekt kann nur als Registry dienen: `[modules]` fehlt oder alle
  Module sind aus. Dann gelten für Dateien außerhalb der Teilprojekte keine
  Harness-Regeln.
- Ohne `[projects]` verhält sich alles wie heute: ein Projekt, `root`.

Validierung in `harness_config.py`, Doku in `docs/techdocs/configuration.md`,
Tests in `tests/test_config.py` (Architekturregel 4).

Eine Teilprojekt-Konfiguration ohne Eintrag in der Registry wird beim Start
im Root nicht beachtet. Beim Start im Teilprojekt selbst gilt sie wie heute
als eigenes Projekt (Fall 1).

## Gemeinsamer Helfer `plugin/scripts/projects.py`

Deterministische Logik gehört in ein Skript (Architekturregel 7, Stufe 4).
Alle Hooks und CLIs benutzen nur diesen Helfer, statt selbst
`load_config(root)` aufzurufen.

- `Project`: `name`, `root: Path` (Projekt-Root), `config: HarnessConfig`.
- `load_projects(session_root) -> ProjectSet`: lädt die Root-Konfiguration und
  alle eingetragenen Teilprojekte. Liefert Projekte und Fehler pro Projekt.
  Eine ungültige oder fehlende Teilprojekt-Konfiguration macht nur dieses
  Projekt unwirksam, nicht die anderen. Eine ungültige Root-Konfiguration
  macht alle unwirksam, weil dann die Registry unbekannt ist.
- `ProjectSet.for_file(file_path) -> Project | None`: das Teilprojekt, dessen
  Pfad die Datei enthält, sonst das Root-Projekt. `None` außerhalb des
  Session-Roots oder wenn das zuständige Projekt unwirksam ist.
- `project.relative(file_path)`: Pfad relativ zum Projekt-Root. Ersetzt
  `project_relative(root, …)` in den Hooks.
- Für das Root-Projekt gehören die Ordner der Teilprojekte nicht zum Projekt
  (`for_file` liefert dort das Teilprojekt). Sie sind für Root-Regeln also
  nie „Projektdateien“.

## Hooks

Grundsatz: Jeder Hook bestimmt das Projekt der Datei und prüft den Schalter
**dieses** Projekts (Architekturregel 3). Meldungen nennen Projekt und Pfade
relativ zum Session-Root, damit die AI die Dateien direkt findet.

### Architektur (`check_architecture.py`, `mark_architecture_read.py`)

- Datei ändern: Verlangt werden die Regeln des zuständigen Projekts
  (`architecture.md` plus passende Scopes, Muster relativ zum Projekt-Root)
  und die geerbten Regeln (siehe unten).
- Spec schreiben: Verlangt werden die Regeln des Projekts, in dessen Backlog
  die Spec liegt.
- `ExitPlanMode`: Verlangt werden die Regeln jedes Projekts mit aktiver
  Architektur, dessen Pfad im Plantext (`tool_input.plan`) vorkommt. Kommt
  keiner vor, gilt das Root-Projekt. Hat das Root-Projekt keine Architektur,
  wird nichts verlangt.
- Gelesen-Status: Gespeichert werden Pfade relativ zum Session-Root, damit
  gleichnamige Dateien verschiedener Projekte nicht verwechselt werden.

### Geerbte Architekturregeln

Neuer, optionaler Abschnitt in der `architecture.md` eines Projekts:

```markdown
## Inherited rules

| Project | Rules |
|---|---|
| root | `architecture.md`, `plugin-api` |
```

- `Project`: ein Name aus der Registry oder `root`, nicht das eigene Projekt.
- `Rules`: in Backticks `architecture.md` (die Hauptdatei) oder Namen von
  Scopes dieses Projekts. Ein geerbter Scope gilt unabhängig von seinen
  Pfadmustern, weil diese sich auf das andere Projekt beziehen.
- Keine Weitervererbung: Geerbt wird nur, was direkt genannt ist.
- Fehler (unbekanntes Projekt, fehlende Datei, Projekt ohne Architektur)
  meldet der Session-Start. Der Hook überspringt fehlerhafte Einträge.
- Inhaltliche Widersprüche: Es gilt die Regel des eigenen Projekts, der
  Konflikt wird benannt (Skill `claude-harness:conflicts`). Das steht im
  Skill `architecture`, nicht im Hook.
- Das Template `plugin/templates/development/architecture.md` bekommt den
  Abschnitt als Kommentar mit Beispiel.

### Backlog (`mark_backlog_dirty.py`, `check_backlog.py`)

- Die Markierung „Backlog geändert“ merkt sich pro Session die Namen der
  betroffenen Projekte.
- Der Stop-Hook prüft jedes markierte Backlog einzeln. Meldungen nennen den
  Backlog-Pfad relativ zum Session-Root. Bereits gemeldete Hinweise werden
  pro Projekt und Session gemerkt.

### techdocs (`mark_techdocs.py`, `check_techdocs.py`)

- Markierungen `project`, `docs` und `reminded` pro Projekt und Session.
- Der Stop-Hook erinnert einmal pro Projekt und Session, wenn in diesem
  Projekt Projektdateien, aber keine Doku-Dateien geändert wurden.
- `README.md` bedeutet `README.md` im Projekt-Root.

### Daily Reports (`daily.py`, `check_daily.py`)

- Jedes Projekt mit aktivem Modul `daily` hat einen eigenen
  Bestätigungsstand: `.git/claude-harness/daily-ack` für `root` (wie heute)
  und `daily-ack-<Name>` für Teilprojekte.
- Ein Commit zählt für ein Projekt, wenn er mindestens eine Datei des
  Projekts ändert, die nicht im Daily- oder Backlog-Ordner dieses Projekts
  liegt. Die Pfade aus Git werden relativ zum Git-Root geliefert und zum
  Vergleich in Pfade relativ zum Projekt-Root umgerechnet. Das behebt auch
  Fall 1.
- Für das Root-Projekt zählen Dateien in Teilprojekt-Ordnern nicht.
- Der Stop-Hook erinnert pro Projekt mit offenen Commits und nennt das
  Projekt.
- CLI: `daily.py <befehl> --project <Name>`. Ohne `--project` gilt `root`.
  Gibt es nur Teilprojekte mit Daily und kein Root-Daily, ist `--project`
  Pflicht und der Fehler nennt die Namen.

### Session-Start (`session_start.py`)

Ohne `[projects]` bleibt die Ausgabe unverändert. Mit Teilprojekten:

1. Die Skill-Hinweise („rules in skill … load it when …“) erscheinen einmal
   für alle Projekte und nur für Module, die in mindestens einem Projekt aktiv
   sind.
2. Eine Zeile pro Projekt: Name, Pfad, Sprache, aktive Module und die Orte
   von Backlog, Daily, techdocs und Architektur relativ zum Session-Root.
3. Kurze Zeilen nur für fehlende Dateien und Fehler, jeweils mit
   Projektnamen. Dazu gehören Registry-Fehler, ungültige
   Teilprojekt-Konfigurationen, Fehler der Scope-Tabelle und Fehler in
   `## Inherited rules`.
4. Ein Hinweis, dass die Datei-Zuordnung zum Projekt die Regeln bestimmt,
   einschließlich Sprache und Backlog.

**Änderung von Architekturregel 7** (vom Owner am 2026-09-25 freigegeben,
umgesetzt mit `TASK-007`): Bisher verlangte die Regel „one line per active
module“. Bei mehreren Projekten wäre das eine Zeile pro Modul und Projekt,
mit denselben Hinweisen mehrfach. Neuer Wortlaut:

> The session start hook prints one line per active module (location and
> skill); with several projects, the skill pointers appear once and each
> project gets one line with its locations. Beyond that, only short lines
> for missing files and errors.

### Worktree (`worktree.py`)

Keine Änderung der Logik. `start` spiegelt bereits alle ignorierten Dateien
des Haupt-Checkouts, also auch gitignorierte Teilprojekt-Konfigurationen und
Dokumente. Das wird mit einem Test abgesichert.

## Skills und Templates

Skills sprechen heute von „`.claude-harness/config.toml` in the project
root“. Neu gilt: „the configuration of the project the work belongs to; the
session start names every project and its locations“. Betroffen sind `todo`,
`daily`, `techdocs`, `architecture`, `decomposition`, `worktree` und `init`.
Die Regeltexte werden dabei nicht verdoppelt (Architekturregel 7).

- `architecture`: Abschnitt `## Inherited rules`, Vorrang der eigenen Regel.
- `todo`: Neue Einträge kommen ins Backlog des Projekts, an dem gearbeitet
  wird. Ist das unklar, fragt die AI nach.
- Plan (Skill `decomposition` oder `worktree`): Ein Plan über mehrere
  Projekte nennt alle betroffenen Projekte. Jede Datei folgt den Regeln ihres
  Projekts.
- `init`: Legt auf Wunsch ein Teilprojekt an. Dazu gehören die Konfiguration
  im Teilprojekt, der Eintrag in `[projects]` und, falls noch nicht
  vorhanden, eine reine Registry-Konfiguration im Root. Die AI fragt, ob
  Harness-Dateien in die `.gitignore` sollen, und schreibt sie nicht
  ungefragt dorthin.

## Betroffene Dateien

- Neu: `plugin/scripts/projects.py`, `tests/test_projects.py`
- Geändert: `plugin/scripts/harness_config.py`, `architecture.py`,
  `check_architecture.py`, `mark_architecture_read.py`, `check_backlog.py`,
  `mark_backlog_dirty.py`, `techdocs.py`, `check_techdocs.py`,
  `mark_techdocs.py`, `daily.py`, `check_daily.py`, `session_start.py`,
  `state.py`
- Skills unter `plugin/skills/*`, Template
  `plugin/templates/development/architecture.md`
- Doku: `docs/techdocs/configuration.md`, `architecture.md`,
  `interfaces.md` (Hooks, CLI `--project`), `README.md` falls betroffen
- Tests der betroffenen Hooks und `tests/test_config.py`
- `docs/development/architecture.md` Regel 7 (freigegeben)

## Nicht Teil dieser Story

- Unterschiedliche Claude-Code-Settings pro Teilprojekt beim Start im Root.
  Das ist technisch nicht möglich.
- Ein gemeinsames Backlog im Root für mehrere Teilprojekte. Das wird erst
  besprochen, wenn es gebraucht wird.
- Verschachtelte Teilprojekte.
- Hooks für Änderungen über Bash. Wie heute sieht der Hook sie nicht.

## Abnahmekriterien

1. In einem Test-Repo mit Root-Projekt und zwei Teilprojekten, bei denen
   Sprache und Module unterschiedlich sind, gilt:
   - Eine Änderung in `Plugins/A/src/x.py` verlangt die Architektur von A,
     nicht die von root.
   - Eine Änderung im Core verlangt die Architektur von root.
   - Erbt A `root: architecture.md`, verlangt eine Änderung in A beide
     Regeldateien.
2. Eine Änderung im Backlog von A löst nur die Prüfung des Backlogs von A aus.
3. Der techdocs-Hinweis erscheint pro Projekt, dessen Code geändert wurde.
4. Ein Commit, der nur Dateien in `Plugins/A` ändert, erscheint nur im Daily
   von A. Ein Commit, der nur das Backlog von A ändert, erscheint in keinem
   Daily.
5. Beim Start im Teilprojekt mit Git-Root darüber gilt: Ein Commit, der nur
   das eigene Backlog ändert, zählt nicht. Ein Commit außerhalb des
   Teilprojekts zählt nicht.
6. Der Session-Start listet alle Projekte, meldet Registry-Fehler und
   ungültige Teilprojekte. Die anderen Projekte bleiben wirksam.
7. Ohne `[projects]` ist das Verhalten unverändert. Alle bisherigen Tests
   bestehen.
8. `worktree.py start` übernimmt gitignorierte Teilprojekt-Konfigurationen in
   den Worktree.

## Vorgeschlagene Zerlegung in Tasks

Jeder Task liefert ein eigenständig prüfbares Ergebnis und passt in eine
Session:

1. **Registry und Zuordnung:** Schema `[projects]`, `projects.py`, Doku und
   Tests. Noch ohne Hook-Änderung. Ergebnis: Der Session-Start listet die
   Projekte, einschließlich der Änderung an Regel 7.
2. **Architektur pro Projekt:** Die Architektur-Hooks nutzen die Zuordnung,
   einschließlich `ExitPlanMode` und Spec.
3. **Geerbte Architekturregeln:** Abschnitt `## Inherited rules`, Hook,
   Session-Start-Fehler, Template und Skill.
4. **Backlog und techdocs pro Projekt:** Markierungen und Stop-Hooks.
5. **Daily pro Projekt:** Bestätigungsstand und Pfadfilter pro Projekt,
   `--project` und Fall 1.
6. **Skills, init und Worktree-Absicherung:** Skill-Texte, `init` für
   Teilprojekte und der Worktree-Test.

Abhängigkeiten: 1 vor allen anderen. 2 vor 3. Die übrigen Tasks sind
unabhängig voneinander.
