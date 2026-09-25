# STORY-029 – Spec: Modul `semver`

## Ziel und Warum

Die Versionsnummer eines Projekts steigt nachvollziehbar nach SemVer
(MAJOR.MINOR.PATCH) und nicht höher als nötig. Jede abgeschlossene Änderung
ergibt höchstens einen Versionsschritt. Teilschritte und Ausprobieren
innerhalb einer Änderung werden gebündelt. Claude stuft die Änderungen ein und schreibt die Version.
Ein Skript prüft deterministisch, ob Versionsdatei, Spiegel-Dateien und Tags
zusammenpassen (Automatisierungsstufe 2).

Hintergrund und Entscheidungen: `STORY-029_notes.md`.

## Begriffe

- **Versionsdatei:** `<docs.root>/VERSION` (Name konfigurierbar). Sie
  enthält nur die Version, z. B. `0.2.0`, optional mit abschließendem
  Zeilenumbruch. Maßgeblich für die Prüfung.
- **Spiegel-Dateien:** Projekteigene Dateien, in denen die Version für
  Werkzeuge ebenfalls stehen muss (`package.json`, `Cargo.toml`,
  `plugin.json` …). Claude pflegt sie beim Release mit; das Skript prüft
  nur, ob sie die Versionszeichenkette enthalten.
- **Release-Tag:** Git-Tag `<Präfix><Version>` auf dem Release-Commit.
  Präfix `v` im Root-Projekt, `<Projektname>-v` in einem Teilprojekt, z. B.
  `v0.2.0` bzw. `ezf-ui-v1.4.0`. Kein Config-Key.
- **Letztes Release:** der höchste (nach SemVer, nicht nach Datum) Tag mit
  dem Präfix des Projekts, dessen Rest eine gültige Version ist. Tags anderer
  Projekte oder fremder Form werden ignoriert.

## Konfiguration

Neue Einträge in `.claude-harness/config.toml`, validiert in
`harness_config.py` (Regel 4):

| Einstellung | Typ | Standard | Wirkung |
|---|---|---|---|
| `modules.semver` | Boolean | `false` | Schaltet das Modul ein |
| `semver.file` | Pfad | `"VERSION"` | Versionsdatei, relativ zu `docs.root` |
| `semver.sync` | Liste von Pfaden | `[]` | Spiegel-Dateien, relativ zum Projektordner |
| `semver.paths` | Liste von Pfaden | `["."]` | Was zum ausgelieferten Produkt zählt; nur Commits, die diese Pfade ändern, gelten als „unveröffentlicht“ |

- Pfade: relativ, ohne `..`, wie bei den anderen Modulen. `semver.paths`
  eines Root-Projekts mit Teilprojekten schließt deren Ordner aus.
- Die Vorlage `plugin/templates/config.toml` führt `semver = false` und eine
  auskommentierte bzw. Standard-`[semver]`-Tabelle.
- Beispiel Claude_Harness: `sync = ["plugin/.claude-plugin/plugin.json"]`,
  `paths = ["plugin"]`.

## Prüfung (Skript, Stop-Hook)

`check_semver.py` läuft am Ende jedes Turns für jedes Projekt mit
eingeschaltetem Modul. Es bleibt still, wenn alles passt, wenn das Projekt
kein Git-Repo ist oder Git fehlt. Es meldet (Exit 2, kurze Meldung mit
Verweis auf den Skill):

1. Versionsdatei fehlt oder enthält keine gültige Version
   `MAJOR.MINOR.PATCH` (Ganzzahlen ohne führende Nullen; Pre-Release und
   Build-Metadaten sind nicht unterstützt).
2. Die Version ist kleiner als das letzte Release oder mehr als **ein**
   SemVer-Schritt darüber. Erlaubt bei letztem Release `X.Y.Z`: `X.Y.Z`,
   `X.Y.(Z+1)`, `X.(Y+1).0`, `(X+1).0.0`. Ohne jedes Release-Tag entfällt
   diese Prüfung.
3. Eine Spiegel-Datei fehlt oder enthält die Versionszeichenkette nicht
   (reine Textsuche, formatunabhängig).

Jeder Befund wird pro Session und Zustand (Projekt, Inhalt der
Versionsdatei, letztes Release, Inhalte der Spiegel-Dateien) nur einmal
gemeldet, damit ein bewusst stehengelassener Zustand nicht jeden Turn
blockiert (Muster wie `check_daily.py`, Zustand über `state.py`).

## Session-Start

Eine Zeile je aktivem Projekt nach dem bestehenden Muster, z. B.:

`SemVer: docs/VERSION (0.1.0; 7 unreleased commits since v0.1.0); rules in
skill claude-harness:semver (load it when the user asks for a release or the
semver hook reminds you).`

Ohne Release-Tag: „no release tag yet“. Fehler aus der Prüfung erscheinen
nicht hier, sondern im Stop-Hook.

## Skript-Schnittstelle

`plugin/scripts/semver.py` bündelt die deterministische Arbeit (Regel 9) und
wird von Hook, Session-Start und Skill genutzt:

- `python3 semver.py status [--project <Name>]`: aktuelle Version, letztes
  Release, erlaubte nächste Versionen, Befunde der Prüfung und die Commits
  seit dem letzten Release unter `semver.paths` (Hash, Datum, Betreff).

Das Skript schreibt nichts (Regel 5).

## Skill `claude-harness:semver`

Beschreibung: ein Satz, wann er geladen wird (Release gewünscht, Hook
erinnert, Modul wird eingerichtet). Inhalt:

- **Wann:** Beim Merge eines Worktrees in den Hauptbranch (Skill
  `claude-harness:worktree` verweist dorthin). Alle Abschnitte eines Plans
  ergeben einen Merge und damit höchstens einen Schritt; ein verworfener
  Worktree ergibt keinen. Ist der Teilbereich `worktree` aus, stuft Claude
  ein, wenn der Owner eine Änderung als fertig bestätigt. Direkte Commits
  auf dem Hauptbranch lösen keinen eigenen Schritt aus; das nächste Release
  erfasst sie mit. Der Owner kann jederzeit ein Release anstoßen.
- **Einstufen:** Claude ruft `semver.py status`
  auf, liest Commits und Diff seit dem letzten Release unter
  `semver.paths` und stuft nach der größten Auswirkung auf Nutzer des
  Projekts ein: inkompatible Änderung eines öffentlichen Vertrags → major,
  neue kompatible Fähigkeit oder Einstellung → minor, kompatible Korrektur →
  patch, nur Internes/Doku → kein Release nötig. Solange MAJOR `0` ist, zählt
  eine inkompatible Änderung als minor. Claude nennt Version und Begründung
  zusammen mit dem Merge; die Freigabe des Merges gilt auch für die Version.
- **Schreiben:** Versionsdatei und alle Spiegel-Dateien ändern (in jedem
  Format, von Hand), ein Commit „Release <Tag>“ auf dem Hauptbranch nach dem
  Merge, dann ein annotierter Tag lokal. Pushen von Commit und Tag bleibt
  beim Owner.
- Commits innerhalb einer Änderung ändern die Versionsdatei nicht.
- **Einrichtung:** Beim Einschalten klärt Claude mit dem Owner die
  Spiegel-Dateien, legt die Versionsdatei mit der aktuellen Version aus der
  projekteigenen Datei an (sonst `0.1.0`) und bietet an, den aktuellen
  Commit als Ausgangs-Release zu taggen.
- Kein Changelog: Das Release erscheint als Änderung im Daily-Report, sofern
  das Modul `daily` an ist.

## Weitere Anpassungen

- `harness_config.py`: Modul `semver`, Tabelle `[semver]`; die
  Versionsdatei zählt als Harness-Datei (`is_harness_file`), damit ihre
  Änderung nicht den Architektur-Hook auslöst.
- `hooks.json`: Stop-Hook `check_semver.py`.
- Skill `worktree`: im Merge-Schritt ein kurzer Verweis auf den Skill
  `claude-harness:semver`, wenn das Modul an ist.
- Skill `init`: Modul `semver` standardmäßig aus; Hinweis auf den Skill,
  falls der Owner es einschaltet.
- Techdocs: `configuration.md` (Keys), `interfaces.md` (Hook, Skript,
  Versionsdatei, Tag-Schema), `README.md` (Modulliste).
- Tests: `tests/test_config.py` (neue Keys), `tests/test_semver.py`
  (Versionsvergleich, Tag-Auswahl mit Präfix, Spiegel-Prüfung, unveröffentlichte
  Commits, kein Git), `tests/test_hooks.py` (Stop-Hook still/meldet/nur
  einmal).
- Dieses Repo: Modul einschalten mit `sync =
  ["plugin/.claude-plugin/plugin.json"]`, `paths = ["plugin"]`,
  `docs/VERSION` = `0.1.0`, Ausgangs-Tag `v0.1.0` nach Owner-Freigabe.

## Abgrenzung

- Keine Conventional Commits, kein semantic-release, keine Werkzeuge
  außerhalb der Standardbibliothek.
- Kein Changelog, keine Pre-Release-Versionen.
- Das Skript liest keine projektspezifischen Formate und schreibt keine
  Dateien; Tags setzt nur Claude nach Freigabe.
- Kein Push durch Hook oder Skill.

## Akzeptanzkriterien

- Mit `modules.semver = false` oder fehlendem Eintrag tut das Modul nichts.
- Ungültige `[semver]`-Einträge werden beim Session-Start gemeldet; das
  Modul bleibt dann still.
- Der Stop-Hook meldet jeden der drei Befunde, bleibt bei korrektem Zustand
  still und meldet denselben Zustand pro Session nur einmal.
- In einem Repo mit Teilprojekten werden nur Tags mit dem Präfix des
  jeweiligen Projekts berücksichtigt.
- Der Session-Start zeigt Version, letztes Release und die Zahl
  unveröffentlichter Commits.
- In Claude_Harness ist das Modul eingerichtet, und mindestens ein Release
  wurde über den Skill erstellt.
- Tests laufen grün (`python3 -m unittest discover tests`).

## Zu prüfen bei der Umsetzung

- Ob Claude Code Plugin-Updates an der Version in `plugin.json` erkennt
  (Doku prüfen); falls ja, in `interfaces.md` festhalten, dass
  Zielprojekte Änderungen erst nach einem Release erhalten.
