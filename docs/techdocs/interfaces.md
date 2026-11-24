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
  `## Inherited rules`. Fragt im Root-Projekt, ob Cloud-Sitzungen genutzt
  werden (`cloud.export`); bei `true` zeigt er die Vorschau von
  `cloud_export.py` (siehe unten) und legt die Kopie nach Freigabe an.
  Fragt, ob `.claude-harness/` in die `.gitignore` soll (nicht bei
  `cloud.export = true`: Kopie und Config müssen eingecheckt sein), und weist
  auf die Aktivierung über `.claude/settings.local.json` hin.
- Fehlerfall: Ist die Config im Zielordner schon vorhanden, zeigt er sie und
  ändert nichts.

## Befehl `/claude-harness:update`

- Zweck: die `.claude-harness/config.toml` eines bereits eingerichteten
  Projekts oder Teilprojekts auf den aktuellen Stand des Harness bringen.
- Aufruf: nur durch den Nutzer (`disable-model-invocation`).
- Wirkung: fragt, welches Projekt (Root oder ein registriertes
  Teilprojekt) aktualisiert wird. Ist `version` älter als `CONFIG_VERSION`
  und gibt es einen durchgängigen Migrationspfad (`MIGRATIONS`), zeigt er
  die Schritte in Klartext und schreibt sie nach Freigabe. Danach gleicht er
  die Config mit `config_update.py` gegen die Config-Vorlage ab: Fehlende
  Abschnitte, Einstellungen, Module und Kommentare der Vorlage werden
  ergänzt, bestehende Zeilen bleiben unverändert. Fragen stellt er wie
  `init`: welche neuen Module aktiv sein sollen, welches Backlog-Backend
  gilt (bei aktivem `todo`), welcher Harness-Repo-Pfad (nur Root) und, bei
  einem von der Vorlage abweichenden Kommentar, ob er bleibt oder ersetzt
  wird. Er zeigt den Diff und schreibt erst nach Freigabe. Danach prüft er
  bei Backend `api` den ToDo-Viewer (`backlog_api.py health`), bei `files`
  den Backlog, und bietet für neu aktivierte Module die Dokumente an, die
  `init` anlegen würde. Im Root-Projekt gleicht er danach die Cloud-Kopie mit
  `cloud_export.py --status` ab: Ist `cloud.export` an und die Kopie fehlt
  oder ist veraltet, zeigt er die Vorschau und schreibt nach Freigabe (von
  Hand geänderte Dateien nennt er und fragt, ob sie überschrieben werden
  dürfen). Ist `cloud.export` aus, aber eine Kopie da, bietet er den Rückbau
  an (`--remove`, ebenfalls mit Vorschau und Freigabe); ohne Kopie bietet er
  einmal an, die Option einzuschalten. Ein Aufruf aktualisiert genau ein
  Projekt.
- Fehlerfall: Fehlt die Config im Zielordner, verweist er auf
  `/claude-harness:init` statt etwas anzulegen. Ist die Version neuer als
  `CONFIG_VERSION`, gibt es keinen durchgängigen Migrationspfad oder ist die
  Config ungültig, meldet er das und ändert nichts. Ist nichts zu ergänzen,
  meldet er „aktuell“.

## Skills

| Skill | Wird geladen, wenn … |
|---|---|
| `claude-harness:todo` | mit dem Backlog gearbeitet wird, der Besitzer etwas merken oder sich erinnern lassen will, nach offenen oder fälligen Memos fragt oder ein Memo in Backlog-Arbeit (oder zurück) umwandelt (Memo-Regeln in `memos.md` bzw. im Dateimodus `memos-files.md` des Skills, nur bei Bedarf) |
| `claude-harness:daily` | der Daily-Hook erinnert oder nach Tagesberichten gefragt wird |
| `claude-harness:techdocs` | eine Änderung Nutzung, Komponenten, Schnittstellen, Einstellungen oder Betrieb betrifft oder der techdocs-Hook erinnert |
| `claude-harness:architecture` | Code geplant oder geändert wird, Architekturregeln geändert werden, eine Anforderung den Regeln widerspricht oder der Architektur-Hook eine Änderung ablehnt |
| `claude-harness:decomposition` | eine Umsetzung geplant oder begonnen, ein Umsetzungsplan vorgelegt, ein Epic in Stories zerlegt oder überlegt wird, ob eine Story Kind-Tasks bekommt |
| `claude-harness:testing` | Tests geschrieben, abgelegt oder ausgeführt werden oder der Projektverantwortliche einen Funktionalitätstest wünscht |
| `claude-harness:semver` | eine Änderung in ihren Ausgangsbranch zurückgemergt wird, ein Release gewünscht ist, der SemVer-Hook erinnert oder das Modul eingerichtet wird |
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
| SessionStart (`startup`, `resume`, `clear`, `compact`) | `session_start.py` | Kurzfassung von Config und Zustand (Backlog: beim wirksamen Backend `api` (siehe Konfiguration, Umgebungsvariablen) Ordner und API-URL ohne Formatprüfung, ohne Erreichbarkeitsprüfung und ohne Prüfung auf `TODO.md` (im API-Modus nicht erforderlich; der Server darf den Backlog in einer Datenbank halten), bei `files` Pfad von `TODO.md` samt Prüfergebnis; wählt die Umgebung das Backend abweichend von der Config, steht dahinter `(backend <Wert>: <Grund>; config.toml says <Wert>)`), Fehler der Scope-Tabelle und der Tabelle geerbter Regeln; bei aktivem Modul `todo` eine statische Memos-Zeile mit Skill-Hinweis, ohne Abfrage von Fälligem: bei Backend `api` mit API-URL, bei `files` mit dem Ordner `<todo.path>/memos/` (der Ordner wird nicht angelegt); bei aktivem Teilbereich `architecture` eine Zeile mit dem Skill `interfaces` (Schnittstellen-Doku und Katalog, für die AI); die Zeile der Systemdoku heißt `Technical docs (for people)`; bei aktivem Teilbereich `testing` der Testordner (`development.tests`) samt Hinweis auf den Skill; mit Teilprojekten (`[projects]`) eine Zeile pro Projekt (darin auch der Testordner), jeder Skill-Hinweis einmal, Meldungen mit Projektnamen, Zeile für jedes Teilprojekt ohne oder mit ungültiger Config; bei aktivem Teilbereich `worktree` in einem Git-Repo eine Fehlerzeile, wenn `worktree.baseRef` nicht `"head"` ist (gelesen aus `.claude/settings.local.json`, `.claude/settings.json` und `~/.claude/settings.json` in dieser Rangfolge; unlesbare Dateien zählen als nicht gesetzt); bei `clear` und `compact` werden die Lese-Merker der Architekturregeln gelöscht; im Root-Projekt eine Zeile `Cloud copy: …`, wenn die Cloud-Kopie nicht zu `cloud.export` passt (Kopie fehlt, veraltet, trotz `false` vorhanden, nicht prüfbar); läuft der Hook aus einer Kopie, entfällt diese Prüfung. In einer Cloud-Sitzung (`CLAUDE_CODE_REMOTE=true`) beim Start (`startup`) mit `cloud.sync = true` (Root-Projekt) gleicht er zuerst den aktuellen Branch mit `origin` ab ([Skript `cloud_sync.py`](#skript-cloud_syncpy)); dessen Zeile steht vor allen anderen, und nach einem Abgleich liest er Config und Dokumente neu | stdout → Kontext |
| PreToolUse (`Write`, `Edit`, `MultiEdit`, `NotebookEdit`, `ExitPlanMode`) | `check_architecture.py` | Lehnt ab, solange die Architekturregeln in der Session nicht vollständig gelesen wurden: das Vorlegen eines Plans (`ExitPlanMode`), das Schreiben einer Backlog-Spec (`<ID>_spec.md`, `<ID>_spec_<Thema>.md`) und die Änderung einer Projektdatei; bei Projektdateien zusätzlich die Datei jedes passenden Scopes und dessen `Required reading`; danach bei Write, Edit, MultiEdit und NotebookEdit die `Read`-Dateien der Tabellen `Required on use`, deren Bezeichner im neuen Text vorkommen. Mit Teilprojekten gelten die Regeln des Projekts, zu dem die Datei gehört (bei einer Spec: dessen Backlog); ein Plan verlangt die Regeln jedes Projekts, dessen Pfad im Plantext vorkommt, sonst die des Root-Projekts. Dateien in unwirksamen Teilprojekten werden nicht geprüft | JSON mit `permissionDecision: deny` und Grund |
| PostToolUse (`Write`, `Edit`, `MultiEdit`) | `mark_backlog_dirty.py` | Nur beim wirksamen Backend `files` (auch in Cloud-Sitzungen): Merker, wenn eine Datei im Backlog-Ordner geändert wurde; bei Teilprojekten mit dem Namen des Projekts, zu dem der Backlog gehört. Eine geänderte Notes-Datei (`items/<ID>/<ID>_notes.md`) merkt er sich zusätzlich einzeln (und setzt den Reminder-Zähler eines aktiven Items auf 0), eine geänderte Datei im Ordner `memos/` des Backlogs (Memos als Dateien) das Projekt in einer eigenen Marke | keine |
| PostToolUse (`Bash`) | `mark_notes_state.py` | Nur beim wirksamen Backend `api` und nur nach einem erfolgreichen Aufruf von `backlog_api.py` (ohne `--source`; mit `--project <Name>` für dieses Projekt): liest die `[harness]`-Zeilen aus `tool_response.stdout`/`stderr` (`notes-state <ID> <Zustand>`, `active <ID>`) und legt je Projekt und Item Zustand des Notes-Kopfs und, für aktive Items, den Zähler „Prompts seit dem letzten Notes-Eintrag“ ab (ein Notes-Schreibvorgang setzt ihn auf 0); Änderungen am Merker-Speicher sind gesperrt und ersetzen die Datei atomar, weil die Hooks paralleler Bash-Aufrufe gleichzeitig laufen (`state.edit_notes_marks`); kein Netzwerk | keine |
| PostToolUse (`Read`) | `mark_active_item.py` | Nur beim wirksamen Backend `files`: das Lesen von `items/<ID>/<ID>_spec.md` im Backlog-Ordner macht das Item aktiv (Zähler 0, ein laufender Zähler bleibt) | keine |
| PostToolUse (`Write`, `Edit`, `MultiEdit`) | `mark_techdocs.py` | Merker „Projekt geändert“ bzw. „Doku geändert“, pro Projekt; `README.md` und Systemdoku zählen nur für ihr eigenes Projekt | keine |
| PostToolUse (`Write`, `Edit`, `MultiEdit`) | `mark_doclinks.py` | Merkt je Session die geänderten Dokumente, deren Links geprüft werden (siehe Abschnitt „Linkprüfung“); Projekt und Pfad stehen in der Zustandsdatei `doclinks-changed-<Session>.json` | – |
| PostToolUse (`Write`, `Edit`, `MultiEdit`) | `mark_public_api.py` | Nur bei aktivem Teil `architecture` und nicht leerem `development.public_api`: Merker (Liste der Pfade), wenn die geänderte Datei auf ein Muster passt (Syntax der Scope-Pfade, relativ zum Projekt-Root); pro Projekt | keine |
| PostToolUse (`Read`) | `mark_architecture_read.py` | Merker, wenn die Architekturregeln, eine Scope-Datei (`.md` an beliebiger Stelle unterhalb von `architecture/`) oder eine Datei aus `Required reading` eines Scopes oder aus `Read` einer Tabelle `Required on use` (`architecture.counted_reads`) vollständig gelesen wurden (kein `offset` > 1, kein `limit` unter der Zeilenzahl); zählt nur für das Projekt, in dem die Datei liegt | keine |
| Stop | `check_backlog.py` | Nur beim wirksamen Backend `files` (auch in Cloud-Sitzungen): prüft jeden in der Session geänderten Backlog (pro Projekt, Meldung mit Backlog-Pfad relativ zum Session-Root); neue Hinweise einmal pro Projekt und Session. Für jede in der Session geänderte Notes-Datei: Kopf `missing` oder `stale` ist ein Fehler, bis er angepasst oder mit `backlog.py --confirm-state` bestätigt ist; Hinweise bei mehr als 15 Punkten unter `- Decided:`, wenn die Notes eines Epics oder einer Story geändert wurden, während eines ihrer Kinder `In progress` ist (Frage, ob die Besprechung dorthin gehört), und wenn ein älterer Protokolleintrag gegenüber dem letzten Commit geändert wurde (ohne Git kein Hinweis). Wurde in der Session eine Datei im Ordner `memos/` des Backlogs geändert, prüft er den ganzen Ordner nach Format Version 2 (`memos_format.py`): Fehler blockieren mit `memos/<Datei>:<Zeile>: <Code>: <Text>`, bis sie behoben sind; Hinweise (nicht gelesene Datei, Dokument ohne Memo) einmal pro Session | Exit 2 + stderr bei Fehlern/neuen Hinweisen |
| Stop | `check_notes_state.py` | Nur beim wirksamen Backend `api`: blockiert, solange ein Item in der Session einen Notes-Kopf mit Zustand `stale` oder `missing` hat (nach der letzten Meldung des Helfers); die Meldung nennt jedes Item (bei Teilprojekten mit `--project <Name>`) und verweist auf `put-state`/`confirm-state`. Bestätigen oder Ersetzen meldet `current` und löst den Block. Kein Netzwerk; `stop_hook_active` verhindert eine Schleife; kennt der Viewer keinen Kopf oder ist er nicht erreichbar, scheitert der Helfer und es entsteht kein Merker. Der Files-Modus läuft über `check_backlog.py` | Exit 2 + stderr |
| UserPromptSubmit | `remind_notes.py` | Beide Backends: zählt je Prompt für jedes aktive Item (auf `In progress` gesetzt oder Spec gelesen) den Zähler hoch und gibt bei 5, 10, 15 … auf stdout eine Erinnerung aus, im Notes-Protokoll festzuhalten, was geklärt, entschieden oder verworfen wurde; ein Notes-Eintrag setzt den Zähler zurück. Blockiert nie (Exit 0, Ausgabe als Kontext) | stdout → Kontext |
| Stop | `check_daily.py` | Erinnert bei neuen, nicht erfassten Commits auf dem Branch, in den gemerged wird (Orte wie bei `daily.py`; Commits nur im Daily- oder Backlog-Ordner zählen nicht), einmal pro HEAD, Projekt und Session; mit Teilprojekten eine Meldung, die jedes Projekt mit offenen Commits nennt, samt Aufruf `daily.py pending --project <Name>` | Exit 2 + stderr |
| Stop | `check_techdocs.py` | Erinnert einmal pro Projekt und Session, wenn Projektdateien, aber keine Systemdoku desselben Projekts geändert wurden; mit Teilprojekten nennt die Meldung jedes betroffene Projekt mit seinen Doku-Pfaden | Exit 2 + stderr |
| Stop | `check_doclinks.py` | Prüft die in der Session geänderten Dokumente (siehe „Linkprüfung“); tote Links stehen als `<Datei>:<Zeile>: <Ziel>: <Grund>` in der Meldung (höchstens 20, bei Teilprojekten mit Projektordner davor). Die Liste bleibt, bis alle Links stimmen; danach wird sie geleert | Exit 2 + stderr |
| Stop | `check_public_api.py` | Erinnert einmal pro Projekt und Session, wenn eine Datei aus `development.public_api` geändert wurde: Zuständigkeiten, Katalog, Schnittstellen-Doku und Verweise prüfen, Skills `claude-harness:architecture` und `claude-harness:interfaces` laden; die Meldung nennt Anzahl und ein Beispiel, mit Teilprojekten jedes betroffene Projekt. Nichts bei fehlenden Mustern, abgeschaltetem Teil `architecture`, ungültiger Config oder `stop_hook_active` | Exit 2 + stderr |
| Stop | `check_semver.py` | Nur in einem Git-Repo. Meldet pro Projekt mit Modul `semver`: Versionsdatei fehlt oder enthält keine gültige Version; Version liegt unter dem letzten Release oder mehr als einen Schritt darüber; eine Spiegel-Datei fehlt oder enthält die Version nicht. Derselbe Befund wird einmal pro Projekt und Session gemeldet; mit Teilprojekten nennt die Meldung jedes Projekt samt Aufruf `semver.py status --project <Name>` | Exit 2 + stderr |

Bei gesetztem `stop_hook_active` bleiben die Stop-Hooks still, damit keine
Schleife entsteht.

Klassifikation für `techdocs`: Als Doku zählen `README.md` im Projekt-Root und
Dateien im techdocs-Ordner; ebenso `interfaces.md` und `interfaces/**` im
development-Ordner, solange der Teil `architecture` aktiv ist (die Techdocs
fassen die Schnittstellen-Doku zusammen und verlinken sie; Änderungen an
`architecture.md` und den Scopes zählen nicht). Nicht berücksichtigt werden
Dateien außerhalb des Projekts, im Backlog-, Daily- oder übrigen
development-Ordner, unter `.git/` und
`.claude-harness/` sowie Tests (Pfadteil `test`/`tests`, Dateiname `test_*`, `*_test.*`,
`*.test.*`). Alles andere im Projekt zählt als Projektänderung. Änderungen über Bash statt Write/Edit
erkennt der Hook nicht.

Projektdateien für `architecture`: alle Dateien im Projekt außer `README.md`,
`.git/`, `.claude-harness/` und den Ordnern von Backlog, Tagesberichten,
Systemdoku und `development`. Tests zählen dazu. Backlog-Specs sind
Harness-Dateien, verlangen aber ebenfalls die gelesene Regeldatei, weil sie
die Grundlage eines Plans sind. Fehlt die Regeldatei, wird nichts abgelehnt. Änderungen über Bash sieht der Hook nicht.

## Skript `backlog.py`

- Aufruf: `python3 plugin/scripts/backlog.py <backlog-ordner> [--index | --show <ID> [<ID> ...] | --confirm-state <ID>]`
- Prüft das Backlog-Format Version 3 (wie der Markdown-Spiegel des
  ToDo-Viewers): `TODO.md` und `archive.md` brauchen vor `## Work items`
  einen Absatz `Format: … backlog format version 3 …` (Version 2 wird ebenfalls
  gelesen, Version 1, eine andere oder fehlende Kennung ist ein Fehler).
  Version 3 ist Version 2 ohne das Feld `Area`; ein vorhandenes `Area` wird
  gelesen und ignoriert, nie geschrieben. Jeder Eintrag braucht eine `Uid`
  (UUID, eindeutig); neue Einträge mit Platzhalter `NEW-<kurzname>` haben
  keine `Uid` und dürfen `Created` weglassen. Das verhindert doppelte IDs bei
  paralleler Arbeit in Cloud und lokal: Labels und `Uid` vergibt nur der
  Viewer beim Sync (er gleicht nach `Uid` ab), ein Eintrag mit Label ohne `Uid`
  und ein Platzhalter mit `Uid` sind Fehler, ebenso zwei gleiche
  Platzhalter. `Notes` und `Spec` sind
  unbekannte Felder. Ein Eintrag in der falschen Datei ist ein Hinweis, kein
  Fehler.
  Der Ordner `mindmap/` (Spiegel der Mindmap des Viewers, nur Dateimodus) ist
  bekannt: seine Dateien werden nicht gemeldet und nicht geprüft, das tut der
  Sync des Viewers; die Regeln stehen in `skills/todo/format.md`.
- Ohne Option: listet Fehler und Hinweise und eine Zusammenfassung.
- Mit `--index`: eine Zeile pro Eintrag über `TODO.md` und `archive.md`
  (`ID | Type | Status | Title | Parent`); Einträge im Papierkorb tragen
  `(deleted <Datum>)` hinter dem Status.
- Mit `--show`: gibt nur die genannten Einträge aus, jeweils unverändert aus
  `TODO.md` oder `archive.md` mit einer vorangestellten Zeile
  `Source: <Datei>`, in der angefragten Reihenfolge und durch eine Leerzeile
  getrennt. Die Einträge werden dabei nicht geprüft. Nicht gefundene IDs
  meldet das Skript auf stderr.
- Mit `--confirm-state <ID>`: setzt in `items/<ID>/<ID>_notes.md` die
  Stempelzeile des Kopfs (`State confirmed after entry … (<Prüfsumme>)`) auf
  den letzten Protokolleintrag und die aktuelle Prüfsumme; sonst ändert sich
  an der Datei nichts (auch die Zeilenenden bleiben). Gibt
  `confirmed <ID>: <Datum> — <Thema> (<Prüfsumme>)` aus. Zerlegen, Prüfsumme
  und Zustand liegen in `plugin/scripts/notes_head.py`; die Testvektoren teilt
  der Harness mit dem ToDo-Viewer (`tests/fixtures/notes-state/checksum.json`).
- Exit-Code: 0 ohne Fehler, 1 bei Fehlern (bei `--show`: eine ID nicht
  gefunden; bei `--confirm-state`: keine Notes-Datei, kein Kopf oder kein
  Protokolleintrag), 2 bei falschem Aufruf (bei `--show` auch: keine oder
  ungültige ID, zusammen mit `--index`; bei `--confirm-state`: keine oder
  ungültige ID).

## Skript `backlog_api.py`

- Zweck: Backlog über die HTTP-API des ToDo-Viewers pflegen
  (`todo.backend = "api"`), ohne JSON-Aufrufe von Hand zu bauen. Maßgeblich
  für die API selbst ist `docs/techdocs/interfaces.md` im ToDo-Viewer.
- Aufruf: `python3 plugin/scripts/backlog_api.py [--project <Name>] <befehl>
  [argumente]` im Projekt der Session (Session-Root wie bei den Hooks).
  Ohne `--project` gilt das Root-Projekt, sonst das eingetragene
  Teilprojekt. Backlog-Ordner (`todo.path`) und URL (`todo.api_url`) kommen
  aus dessen Config; einen Pfad nimmt das Skript nicht entgegen.
- Projekt: Das Skript sucht in `GET /workspace/projects` das Viewer-Projekt,
  dessen `mirror_folder` der Backlog-Ordner ist, und schickt dessen `uid` bei
  jedem Aufruf mit (`projects`/`project`). Liegt der Ordner in einem
  Git-Worktree, gilt derselbe Ordner im Haupt-Checkout: Der Server schreibt
  immer dort. Gibt es kein solches Projekt, bricht das Skript mit Exit 4 ab
  und legt nichts an; registriert wird nur mit dem eigenen Befehl `register`.
- Labels: Die KI nennt Items mit ihren IDs. Wo der Server interne `uid`s
  verlangt (`parent`, `dependencies`, Papierkorb), löst das Skript die IDs
  über `GET /workspace/projects/{uid}/labels/{ID}` auf; eine unbekannte ID
  bricht vor dem Schreiben ab (Exit 1, `not_found`). `required_for_parent`
  nimmt `Yes`/`No` oder `true`/`false`.
- Fremdes Backlog: `--source <Name>` (statt `--project`; beide zusammen sind
  ein Aufruffehler, Exit 2) spricht das Viewer-Projekt mit genau diesem Namen
  an, auch eines ohne Spiegel-Ordner wie `Allgemein`. Die URL kommt weiter aus
  der Config des Session-Projekts, dessen Modul `todo` an sein muss. Ein
  unbekannter Name bricht ab (Exit 2, mit Liste der bekannten); es wird nie
  ein Projekt angelegt. Wann die KI das nutzen darf, regelt der Skill `todo`
  (ausdrückliche Freigabe des Owners); das Skript prüft das nicht.
- Befehle (Routen unter `todo.api_url`):

  | Befehl | Wirkung |
  |---|---|
  | `health` | Erreichbarkeit (`GET /core/health`) |
  | `sources` | `Project \| Folder` jedes Viewer-Projekts (die Namen für `--source`; `-` ohne Spiegel-Ordner) |
  | `register` | Backlog-Ordner als Viewer-Projekt anlegen (`POST /workspace/projects`, Spiegel und Auto-Sync an); Name beim Root-Projekt der Ordnername des Haupt-Checkouts, sonst der Name des Teilprojekts. Abgelehnt (Exit 2), wenn der Ordner schon registriert ist oder mit `--source` |
  | `index [--with-trash]` | Eine Zeile pro Eintrag: `ID \| Type \| Status \| Title \| Parent \| Notes` (`GET /backlog/index`); Einträge im Papierkorb (`GET /workspace/trash`) fehlen, mit `--with-trash` stehen sie mit dem Zusatz `(Papierkorb)` da |
  | `show <ID>` | Eintrag als JSON mit `version`, auch archivierte; gelöschte Kinder tragen ein `note`-Feld und zählen nicht als offene Arbeit (nicht geschlossene nennt ein Hinweis auf stderr) |
  | `create` | Neuer Eintrag; stdin: flaches JSON mit `type` und den Feldern; die ID vergibt der Server |
  | `update <ID> <version>` | stdin: `{"fields": {...}, "resolution": ...}` (`PUT /backlog/items/{ID}`) |
  | `move <ID> <version> <parent\|-> [--position N]` | Neuer Parent (`-` = keiner) und Position unter den Geschwistern |
  | `reopen <ID>` | Eintrag und geschlossene Vorfahren auf `In progress`, von oben nach unten |
  | `note <ID>` | Notes-Eintrag anhängen; stdin: `{topic, discussed, decided, open, summary?, state?, state_version?}` (`state` ersetzt den Kopf im selben Aufruf); die `hints` des Servers (alle schreibenden Notes-Befehle) stehen zeilenweise als `hint: …` auf stderr; nach jedem erfolgreichen Schreiben von Notes (`note`, `put-state`, `confirm-state`, `put-doc` auf `<ID>_notes.md`) folgt auf stderr die Zeile `[harness] notes-state <ID> <current|stale|missing>` (Zustand aus der Antwort, sonst aus den Hinweisen `notes_state_stale`/`notes_state_missing`, ohne Hinweis `current`), und `[harness] active <ID>` meldet ein Item, das auf `In progress` gesetzt (`update`, `reopen`) oder dessen Spec gelesen wurde (`doc <ID> <ID>_spec.md`); beide Zeilen fehlen mit `--source`; der Helfer legt selbst nichts ab, die Zeilen liest `mark_notes_state.py`; bei einem Epic oder einer Story mit Kind `In progress` (nicht im Papierkorb) fragt ein Hinweis auf stderr, ob die Besprechung dorthin gehört; der Eintrag wird immer geschrieben |
  | `state <ID>` | Kopf der Notes ohne Protokoll als JSON (`GET /backlog/items/{ID}/notes/state`): `content`, `stamp`, `state` (`current`/`stale`/`missing`), `checksum`, `last_entry`, `version` des Kopfs |
  | `put-state <ID> <version>` | Kopf mit dem Text von stdin ersetzen (`PUT …/notes/state`); der Server stempelt gegen den letzten Eintrag |
  | `confirm-state <ID> <version>` | Kopf unverändert bestätigen (`POST …/notes/state/confirm`); nur der Stempel zieht nach |
  | `entries <ID> [--last N]` | Protokolleinträge (alle oder die letzten N) als `{position, day, topic, text}` (`GET …/notes/entries`) |
  | `doc <ID> <name>` | Notes oder Spec ausgeben: `version: <v>`, Leerzeile, Inhalt |
  | `put-doc <ID> <name> <version\|new> [--summary TEXT]` | Dokument mit dem Text von stdin ersetzen oder neu anlegen; bei `<ID>_notes.md` gilt derselbe Hinweis wie bei `note` |
  | `retype <ID> <version> <type>` | Typ ändern (`Epic`, `Story`, `Task`); der Eintrag erhält die nächste freie ID des neuen Typs, Verweise in den Texten des Projekts ziehen mit; Antwort mit `old_label` und `new_label` |
  | `delete <ID> <version> [--cascade]` | In den Papierkorb (`DELETE /workspace/elements/{uid}`), mit `--cascade` samt Nachfahren |
  | `trash` | Backlog-Einträge des Projekts im Papierkorb als JSON |
  | `restore <ID>` | Aus dem Papierkorb zurückholen, samt der mit ihm gelöschten Nachfahren |

  Eine `version` ist eine Zahl (Revision des Registers); eine andere Angabe
  ist ein Aufruffehler (Exit 2), bevor etwas an den Server geht. Endgültiges
  Löschen aus dem Papierkorb bietet das Skript bewusst nicht an; das macht nur
  der Projektverantwortliche.
- Exit-Code: 0 bei Erfolg; 1 bei einer Fehlerantwort des Servers (stderr:
  `HTTP <Status> <code>: <message>`, dazu `details`; bei `version_conflict`
  der Hinweis, neu zu lesen statt blind zu wiederholen); 2 bei falschem
  Aufruf, ungültigem JSON auf stdin, ungültiger Version, fehlender oder
  ungültiger Config, unbekanntem Projekt oder abgeschaltetem Modul `todo`; 3,
  wenn der Server nicht erreichbar ist; 4, wenn der Backlog-Ordner nicht als
  Viewer-Projekt registriert ist.

## Skript `memos_api.py`

- Zweck: Memos und Topics über die HTTP-API des ToDo-Viewers pflegen
  (Teil des Moduls `todo`). Die Memos liegen nur in der Datenbank des Viewers; das
  Skript hat keinen Dateizugriff darauf. Maßgeblich für die API selbst ist
  die Doku des ToDo-Viewers (`docs/techdocs/neubau-server.md`, Plugin
  `memos`, Routen unter `/memos/…`).
- Aufruf: `python3 plugin/scripts/memos_api.py [--project <Name>] <befehl>
  [argumente]` wie bei `backlog_api.py`: Projekt der Session, ohne
  `--project` das Root-Projekt, gefunden über den Spiegel-Ordner des
  Backlog-Ordners (Exit 4, wenn nicht registriert; `register` gibt es nur in
  `backlog_api.py`). Das Modul `todo` muss an sein und das Backend `api` haben
  (Memos gibt es nur im Viewer). `--source <Name>` wie bei `backlog_api.py`
  spricht die Memos eines anderen Projekts des Viewers an (Freigabe: Skill
  `todo`).
- Labels: Memos, Topics und Ziele von Ereignis-Auslösern im eigenen Projekt
  löst der Server selbst auf. Für Verknüpfungen (`POST /workspace/links`),
  Papierkorb und Auslöser-Ziele in anderen Projekten (`target_project`) löst
  das Skript die Labels in `uid`s auf. Die alten Namen `topic_due` (Art) und
  `target_status` (Feld) eines Auslösers werden als `topic_date` und `status`
  weitergegeben; Zeit-Auslöser lehnt das Skript ab (Exit 2, Hinweis auf
  `alarms_api.py`).
- Befehle (vollständig: Aufruf ohne Argumente und `plugin/skills/todo/memos-api.md`):
  Lesen: `health`, `sources`, `index` (kompakte Tabellen aus
  `GET /memos/index/lines`, Filter `--status`, `--due`, `--archived`,
  `--query`, `--all-projects`), `due` (alle Projekte), `show`, `topics`,
  `topic` (Unter-Topics und Memos), `links`, `backlinks` (ausgehende bzw.
  eingehende Verknüpfungen aus `GET /workspace/elements/{uid}/links`),
  `memos-of-item`, `docs`, `doc`, `hints` (eines Memos, mit `--side item`
  eines Items), `trash` (Memos und Topics des Projekts), `settings`.
  Schreiben (JSON auf stdin, `<version>` als Zahl): `create`, `update`,
  `keep`, `snooze`, `finish` (`done` oder `dropped`), `move`, `delete`
  (Papierkorb über `workspace`), `restore` (aus dem Papierkorb über
  `workspace`, aus dem Archiv über `memos`), `trigger-add`, `trigger-remove`,
  `link-add`, `link-remove`, `put-doc`, `memo-entry`, `decide`, `promote`
  (IDs in `parent` und `dependencies` wie bei `backlog_api.py`), `demote`,
  `topic-create`, `topic-update`, `topic-move`, `topic-archive`,
  `topic-reactivate`, `topic-delete` (mit der Wahl des Servers für den
  Inhalt), `topic-restore`.
- Bewusst nicht vorhanden: endgültiges Löschen und das Ändern der
  Einstellungen des Viewers (`settings` liest nur).
- Exit-Code: wie bei `backlog_api.py`; Exit 2 auch bei abgeschaltetem Modul
  `todo` oder Backend `files`.

## Skript `memos_files.py`

- Zweck: Index und Fälligkeit der Memos im Dateimodus (Teil des Moduls
  `todo`, Backend `files`), das Gegenstück zu `backlog.py --index`. Es liest
  nur die Kopfzeilen der Dateien `memos/MEMO-<n>.md` und
  `memos/new-<Name>.md` im Backlog-Ordner, nie den Langtext, die Dokumente
  der Memos, `topics.md` oder `counters.md`. Das Format ist das Dateiformat
  Version 2 des ToDo-Viewers; der Helfer prüft es nicht vollständig (die
  Formatprüfung ist eine eigene Story) und schreibt nichts.
- Aufruf: `python3 plugin/scripts/memos_files.py <Backlog-Ordner> [--index |
  --due [--today JJJJ-MM-TT] | --check]`. `--index` ist die Vorgabe.
- `--index`: eine Kopfzeile `File | Status | Review | Topic | Summary`, dann
  eine Zeile je Memo, sortiert nach Dateiname. Das Topic steht mit Namen aus
  `topics.md` (Sonderzeichen so, wie sie dort stehen, `|` als `\|`), ein
  Topic ohne Label als `new:<Name>` aufgelöst, fehlende Werte als `-`. Memos im
  Papierkorb (`Deleted:` gesetzt) und archivierte Memos fehlen.
- `--due`: nur offene Memos (`waiting`, `due`, `snoozed`), deren
  Review-Tag oder deren Topic-Fälligkeit (`due=` in `topics.md`) heute oder
  früher liegt; mit der Spalte `Reason` (`review <Tag>`, `topic due <Tag>`).
  `--today` ersetzt das Tagesdatum. Auslöser auf Ereignisse kennt nur der
  Viewer und werden nicht ausgewertet.
- `--check`: prüft den ganzen Ordner `memos/` nach den Regeln des Decoders des
  Viewers (Format Version 2) mit `memos_format.py` und gibt je Fund eine Zeile
  `memos/<Datei>:<Zeile>: <Code>: <Text>` aus, Fehler vor Hinweisen; Exit 1 bei
  Fehlern, sonst 0 (Hinweise allein ändern den Exit-Code nicht). Je Datei wird
  der erste Fehler gemeldet, wie beim Viewer, dazu die Fehler über Dateien
  hinweg. Fehlercodes (die des Viewers): `invalid_value` (ungültige Kopf-,
  Auslöser-, Link- oder Topic-Zeile, Status, `Mode`, `Archived`, Zeitpunkt;
  `due` steht nie in einer Datei; ein neues Memo hat keine `Uid`),
  `unknown_field`, `missing_field` (`Summary`, `Status`, `Uid` bei einem Memo
  mit Label, Topic-Name und `uid=` bei einem Topic mit Label),
  `file_label_mismatch` (erste Zeile passt nicht zum Dateinamen),
  `invalid_placeholder` (Kurzname nicht `a-z`, `0-9`, `-`, oder ein Platzhalter
  doppelt), `unknown_trigger` (`time` und alles außer `event` und
  `topic_due`), `duplicate_uid`, `duplicate_label`; dazu `merge_markers`
  (Anfangs- und Endmarker eines Merge-Konflikts in einer Datei) und
  `unreadable` (nicht UTF-8 oder nicht lesbar). Hinweise, die nicht
  blockieren: `ignored_file` (eine `.md`-Datei, die der Viewer nicht liest,
  meist ein Tippfehler im Namen) und `document_without_memo` (ein Dokument, zu
  dem es kein Memo gibt). Verweise (Ziele von Links, Triggern, Topics) werden
  nicht auf Existenz geprüft, `counters.md` wird ignoriert. Die Beispiele des
  Viewers (`tests/fixtures/memos-format`, Kopie aus dessen
  `tests/fixtures/mirror-v2`) sind die gemeinsame Vorlage; der Stop-Hook ruft
  dieselbe Prüfung.
- Ausgabe leer, wenn es keinen Ordner `memos/` oder keine Treffer gibt. Exit 0;
  1, wenn eine Datei sich nicht lesen lässt oder keine `Summary`-Zeile hat
  (Meldung auf stderr, die übrigen Memos erscheinen trotzdem); 2 bei falschem
  Aufruf.

## Skript `alarms_api.py`

- Zweck: Wecker über die HTTP-API des ToDo-Viewers pflegen (Teil des Moduls
  `todo`, nur mit Backend `api`). Ein Wecker meldet sich im Viewer zu seinem
  Zeitpunkt; erledigte und erloschene räumt der Viewer nach 24 Stunden selbst
  auf. Maßgeblich für die API ist die Doku des ToDo-Viewers
  (`docs/techdocs/neubau-server.md`, Plugin `alarms`, Routen unter
  `/alarms/…`).
- Aufruf: `python3 plugin/scripts/alarms_api.py [--project <Name> | --source
  <Name>] <befehl> [argumente]`; Projekt, `--source` und Exit-Codes wie bei
  `backlog_api.py`.
- Befehle: `list [--due] [--all-projects]`, `show <ALARM>`, `create` (stdin
  `{at, text?, targets?}`), `update <ALARM> <version>` (stdin `{at?, text?,
  targets?}`, `targets: []` löst alle), `snooze <ALARM> <version> [--until
  T]`, `finish <ALARM> <version>`, `reopen <ALARM> <version>`, `delete
  <ALARM> <version>` (Papierkorb über `workspace`), `restore <ALARM>`.
- `targets`: Labels des eigenen Projekts gehen unverändert an den Server, der
  sie auflöst; `Projekt:LABEL` eines anderen Viewer-Projekts löst das Skript
  in die `uid` auf.

## Skript `viewer_api.py`

Gemeinsamer Client von `backlog_api.py`, `memos_api.py` und `alarms_api.py`,
kein eigener Befehl: HTTP-Aufruf mit Zeitlimit, Fehlertext aus der
Fehlerantwort des Servers (`code`, `message`, `details`, Hinweis bei
`version_conflict`), Exit-Codes (1 Fehlerantwort, 2 falscher Aufruf, 3 Server
nicht erreichbar, 4 Backlog-Ordner nicht als Viewer-Projekt registriert),
Auswahl des Projekts aus der Config (`--project`, Viewer-Projekt über den
Spiegel-Ordner im Haupt-Checkout) oder eines Viewer-Projekts nach exaktem
Namen (`--source`, `sources`), Registrieren nur auf ausdrücklichen Befehl,
Auflösen von Labels in `uid`s, Umsetzen der Item-Felder (`parent`,
`dependencies`, `required_for_parent`), Prüfen der Versionsnummer und Lesen von
JSON auf stdin.

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
  Offen ist ein Commit, den kein bestätigter Stand irgendeines Branches
  enthält; ein Merge, dessen eingemergte Seite schon bestätigt ist, zählt
  nicht. Ohne verwertbaren bestätigten Stand wird HEAD still zum Startpunkt.
- `ack`: setzt den bestätigten Stand des Projekts für den ausgecheckten
  Branch auf HEAD. Eine alte Ack-Datei mit nur einem Commit gilt weiter.
- Erlaubte Orte: der Haupt-Checkout auf einem beliebigen Branch, oder ein
  Worktree, der gerade den Ausgangsbranch eines Changes ausgecheckt hat
  (Merge im Worktree, siehe `worktree.py check`). Nicht erlaubt: detached
  HEAD, der Branch eines laufenden Changes (hat `harnessBase`) und andere
  Worktrees, z. B. von der App angelegte.
- Exit-Code 1, wenn das Modul im gewählten Projekt aus ist (die Meldung
  nennt die Projekte mit Daily), das Projekt unbekannt oder unwirksam ist
  oder der Ort nicht erlaubt ist; 2 bei falschem Aufruf.

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

## Skript `config_update.py`

- Aufruf: `python3 plugin/scripts/config_update.py <Ordner> [--subproject]
  [--set <Schlüssel>=<Wert> ...] [--write]`; `<Ordner>` enthält
  `.claude-harness/config.toml`, `--subproject` für ein Teilprojekt (dort
  weder `[harness]` noch `[cloud]`).
- Wirkung: vergleicht die Config mit `plugin/templates/config.toml` und
  ergänzt fehlende Abschnitte, Einstellungen, Module und Kommentare der
  Vorlage textbasiert an der Stelle der Vorlage; vorhandene Zeilen, eigene
  Kommentare, Reihenfolge und fremde Abschnitte wie `[projects]` bleiben.
  Eine fehlende Einstellung bekommt den Wert, der ohne sie gilt, damit sich
  das Verhalten nicht ändert. Ohne `--write` wird nichts geschrieben.
- Entscheidungen (`--set`):
  - `modules.<Name>=true|false`: Modul fehlt in `[modules]` (Standard
    `false`);
  - `todo.backend=api|files`: fehlt, während `todo` aktiv ist (Standard
    `api`);
  - `harness.repo=<Pfad oder TOML-Liste>`: `[harness]` bzw. `repo` fehlt, nur
    im Root-Projekt (Standard `[]`);
  - `comment:<Stelle>=keep|replace`: ein vorhandener Kommentar weicht von
    der Vorlage ab (Stelle `top`, `<Tabelle>` für den Block über der
    Überschrift, `<Tabelle>.<Schlüssel>` für den Zeilenkommentar; Standard
    `keep`).
- Ausgabe: je Entscheidung
  `decision: <Schlüssel> = <Wert> (pending|set; <Auswahl>)`, bei
  Kommentaren gefolgt von `  project: …` und `  template: …`; dann
  `changes: <n>` und der Unified Diff; nach dem Schreiben
  `written: .claude-harness/config.toml`.
- `--write` schreibt nur, wenn keine Entscheidung mehr offen ist; das
  Ergebnis wird vorher wie beim Laden der Config geprüft.
- Exit-Code 0; 1 bei fehlender oder ungültiger Config, veralteter Version,
  unbekannter oder ungültiger Entscheidung und bei `--write` mit offenen
  Entscheidungen (Meldung `error: …` auf stderr); 2 bei falschem Aufruf.

## Skript `cloud_export.py`

- Zweck: eine Kopie des Plugins im Projekt, weil eine Cloud-Sitzung
  (claude.ai/code) das Plugin nicht lädt, wohl aber `CLAUDE.md`,
  `.claude/skills` und die Hooks aus `.claude/settings.json` des einzigen
  Repositories der Sitzung. Es wird nur `plugin/` kopiert, nie Backlog, Notes
  oder Tagesberichte des Harness-Repositories.
- Aufruf: `python3 plugin/scripts/cloud_export.py <Projektordner> [--status |
  --remove] [--write]`; der Ordner enthält `.claude-harness/config.toml`.
  Ohne Option eine Vorschau, `--write` schreibt, `--status` meldet nur
  `missing`, `current` oder `outdated`, `--remove` nimmt die Kopie wieder
  heraus. Die Skills `init` und `update` rufen es auf; es gibt kein Netz und
  nichts wird ohne `--write` geschrieben.
- Die Kopie besteht aus:
  - den Skills unter `.claude/skills/harness-<Name>/` (alle Skills des Plugins
    außer `init`, `update` und `worktree`, samt Unterdateien); im Text ist der
    Name der Frontmatter mit `harness-` versehen, `claude-harness:<Name>` zu
    ausgelieferten Skills zu `harness-<Name>` umgeschrieben und
    `${CLAUDE_PLUGIN_ROOT}` durch den projektrelativen Pfad
    `.claude-harness/runtime` ersetzt (in der Cloud ist `CLAUDE_PROJECT_DIR`
    in der Shell leer);
  - den Skripten und Vorlagen unter `.claude-harness/runtime/scripts/` und
    `.claude-harness/runtime/templates/` (ohne Caches) und einer
    `.gitignore` im Ordner `runtime/`, die Bytecode-Caches (`__pycache__/`,
    `*.pyc`) aus Git heraushält, die das Ausführen der Skripte in der Cloud
    erzeugt;
  - den Hook-Einträgen in `.claude/settings.json`, erzeugt aus
    `plugin/hooks/hooks.json`: gleiche Ereignisse, Matcher und Zeitlimits, der
    Befehl lautet `[ "$CLAUDE_CODE_REMOTE" != "true" ] || python3
    "${CLAUDE_PROJECT_DIR:-.}/.claude-harness/runtime/scripts/<Skript>"`. Eigene
    Hooks und andere Schlüssel der Datei bleiben, Einträge der Kopie erkennt
    das Skript am Pfad `.claude-harness/runtime/scripts/`; ungültiges JSON
    bricht ab, ohne etwas zu schreiben;
  - dem Manifest `.claude-harness/runtime/manifest.json`: Format, Plugin-Version,
    Hash jeder erzeugten Datei, ob die `settings.json` vom Export angelegt
    wurde, ihr Text vor dem ersten Export und der Hash des zuletzt
    geschriebenen Texts.
- Ausgabe: `plugin: <Version>`, `copy: <Version oder none>`, je Änderung eine
  Zeile `create|update|delete <Pfad>` (`(edited)`: die Datei weicht von dem ab,
  was der letzte Export schrieb, etwa von Hand geändert), beim Rückbau Zeilen
  `kept <Pfad> (edited)`, dann `changes: <n>`, der Unified Diff jedes
  `update` und nach `--write` `written: <n>`; `--status` gibt stattdessen
  `status: <Zustand>` aus.
- Aktualisieren: Eine Datei, die der Plugin-Stand anders schreiben würde, wird
  `update`, eine aus dem Plugin verschwundene Datei `delete`; von Hand
  geänderte Dateien werden überschrieben, wenn der Nutzer das nach der
  Vorschau freigibt. Die Hook-Einträge werden ersetzt, nicht verdoppelt.
- Rückbau (`--remove`): löscht jede im Manifest genannte, unveränderte Datei
  und die Bytecode-Caches unter `runtime/`, lässt von Hand geänderte stehen
  (`kept`), stellt die `settings.json` wieder
  her (den Text vor dem ersten Export Byte für Byte, solange die Datei seit
  dem Export unberührt ist; sonst werden nur die Einträge der Kopie entfernt,
  und eine vom Export angelegte Datei, die dann leer wäre, wird gelöscht) und
  löscht das Manifest zuletzt, sodass ein unterbrochener Rückbau wiederholbar
  ist. Eine Rundreise aus Export und Rückbau ergibt den Ausgangsstand.
- Der Pfad jeder Datei wird vor dem ersten Schreiben geprüft; Pfade außerhalb
  des Projekts werden verweigert.
- Exit-Code 0; 1 bei Fehlern (Zeile `error: …` auf stdout, nichts
  geschrieben); 2 bei falschem Aufruf.

## Skript `cloud_sync.py`

- Zweck: Eine Cloud-Sitzung kann auf einem veralteten, gecachten Clone
  starten. Das Modul bringt den aktuellen Branch auf den Stand von `origin`
  oder meldet, wie weit er abweicht. Es überschreibt nie etwas.
- Aufruf: kein CLI; `session_start.py` ruft `sync_branch(root,
  fetch_timeout=15)` nur in einer Cloud-Sitzung beim Start (`startup`) mit
  `cloud.sync = true` auf. Rückgabe: eine Zeile für den Kontext oder `None`.
  Netz und Vorspulen sind eine freigegebene Ausnahme von den
  Architekturregeln 2 und 5.
- Ablauf: Branch über `git symbolic-ref` (detached HEAD, kein Repository oder
  kein Remote `origin`: nichts tun); dann
  `git fetch --no-tags --no-recurse-submodules origin
  +refs/heads/<Branch>:refs/remotes/origin/<Branch>`, nur dieser Branch, ohne
  `--unshallow` und ohne `--depth`, mit Zeitlimit (15 s, der Hook hat 30 s;
  Git läuft in einer eigenen Prozessgruppe, die bei Zeitüberschreitung ganz
  beendet wird, `GIT_TERMINAL_PROMPT=0`). Ein Branch, den es auf `origin`
  nicht gibt, ist kein Fehler.
- Fälle und Ausgabe (eine Zeile, Präfix `Git:`):

| Fall | Aktion | Meldung |
|---|---|---|
| Gleicher Stand | keine | keine |
| HEAD ist Vorfahr von `origin/<Branch>`, keine Änderungen an versionierten Dateien (unversionierte zählen nicht) | `git merge --ff-only` | `fast-forwarded <Branch> from <alt> to <neu> (<n> new commit(s) from origin)` |
| HEAD ist Vorfahr, Arbeitsbaum geändert | keine | Zahl der fehlenden Commits und `git merge --ff-only origin/<Branch>` nach Commit oder Stash |
| Vorspulen scheitert (z. B. unversionierte Datei im Weg) | keine | Grund und `git merge --ff-only origin/<Branch>` |
| Nur lokale Commits voraus | keine | keine (normaler Zustand vor einem Push) |
| Commits auf beiden Seiten | keine | Zahl je Seite, `git rebase origin/<Branch>`; `git reset --hard origin/<Branch>` nur, wenn der Nutzer es verlangt |
| Kein gemeinsamer Vorfahr (Shallow Clone nach Force-Push oder alter Cache) | keine | Hash und Datum beider Stände (Zahlen sind dort nicht verlässlich), Hinweis, den Nutzer vor der Arbeit zu informieren, `git reset --hard origin/<Branch>` nur auf Wunsch |
| Fetch scheitert oder dauert zu lange | keine | `could not fetch origin/<Branch> (<Grund>); the checkout may be stale.` |

- Hängt ein lokaler Git-Aufruf oder fehlt Git, gibt es keine Zeile; der
  Session-Start läuft weiter.

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
  Ausgangsbranch), `merge_in` (`main`: Merge im Haupt-Checkout; `worktree`:
  der Haupt-Checkout hat gewechselt und der Ausgangsbranch ist nirgends
  ausgecheckt, der Worktree checkt ihn selbst aus und merged dort; `none`:
  der Ausgangsbranch ist in einem anderen Worktree ausgecheckt).
- Exit-Code: 0; 1 bei Fehlern (nicht in einem Worktree, Haupt-Checkout
  detached, kein Ausgangsbranch gespeichert) und bei `check`, wenn `clean`
  `no` oder `merge_in` `none` ist; 2 bei falschem Aufruf.

## Linkprüfung (`doclinks.py`)

Gemeinsamer Helfer für Sitzungsstart und Stop-Hook; nur Standardbibliothek,
kein Netz. Manuell: `python3 plugin/scripts/doclinks.py [Projekt-Root]` gibt die
toten Links aus (Exit 1) oder `No dead links.`.

- **Geprüfte Dokumente je Projekt:** `README.md` und alle `.md` unter
  `techdocs.path`, wenn das Modul `techdocs` aktiv ist; alle `.md` unter
  `development.path`, wenn der Teil `architecture` aktiv ist.
- **Linkformen:** Inline-Links `[Text](ziel.md#anker)`, Bilder, Ziele in
  `<…>` (mit Leerzeichen), Titel werden abgeschnitten, `%20` wird
  dekodiert, `?query` entfällt, Referenz-Definitionen `[id]: ziel` werden
  geprüft (`[^fußnote]:` nicht). Das Ziel ist relativ zur verweisenden Datei
  (`/x.md` relativ zum Projekt-Root); `#anker` allein meint die eigene Datei.
- **Nicht geprüft:** Links mit Schema (`https:`, `mailto:` …) oder `//`, Links in
  Code-Blöcken (```` ``` ````/`~~~`) und Inline-Code, eingerückte Code-Blöcke werden
  nicht erkannt.
- **Fehler:** Ziel liegt außerhalb des Projekts; Datei oder Ordner fehlt;
  Anker fehlt in einer `.md`-Zieldatei (ohne Beachtung der Groß-/Kleinschreibung).
- **Anker:** Slug wie bei GitHub: Überschrift klein, alles außer Buchstaben
  (auch Umlaute), Ziffern, `-`, `_` und Leerzeichen entfernt, Leerzeichen zu
  `-`; Duplikate bekommen `-1`, `-2`; Überschriften in Code-Blöcken zählen
  nicht; `<a id="…">` und `<a name="…">` zählen als Anker. Setext-Überschriften
  gelten.
- **Sitzungsstart:** je Projekt `Dead links in docs: <n>` mit den ersten fünf
  Meldungen und `- … <m> more`; bei Teilprojekten mit dem Projektnamen
  davor.
- **Stop-Hook:** prüft nur die in der Session geänderten Dokumente (Änderungen
  über Bash sieht `mark_doclinks.py` nicht). Links anderer Dateien, die auf eine
  geänderte oder gelöschte Datei zeigen, meldet nur der Sitzungsstart.

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
| `.claude-harness/runtime/manifest.json` | JSON, von `cloud_export.py` geschrieben | Abschnitt Skript `cloud_export.py` |
| `TODO.md`, `archive.md`, `items/<ID>/` | Backlog-Format v2 (Markdown); Item-Notes mit Kopf `## State` (feste englische Marker, Stempelzeile mit Prüfsumme) über dem datierten Protokoll, Prüfsumme gemeinsam mit dem ToDo-Viewer | `plugin/skills/todo/format.md` (Abschnitt *Notes*) |
| `<YYYY-MM-DD>_daily.md` | Markdown nach Vorlage | `plugin/templates/daily/daily.md`, Skill `daily` |
| Systemdoku | Markdown nach Vorlagen | `plugin/templates/techdocs/` |
| Versionsdatei (`semver.file`, Standard `docs/VERSION`) | eine Zeile `MAJOR.MINOR.PATCH` (Ganzzahlen ohne führende Nullen), keine Vorabversionen | Skill `semver` |
| Release-Tag | annotierter Tag `<Präfix><Version>`, z. B. `v0.2.0`, `ezf-ui-v1.4.0` | Skill `semver` |
| `interfaces.md`, `interfaces/**` | Markdown, englisch, Doku des Wie für die AI (optional, keine Warnung bei fehlendem Index): Index mit einer Zeile und einem Link je Datei unterhalb von `interfaces/`; `X.md` darf neben einem Ordner `X/` stehen; Kataloge je Besitzer mit Tabelle `\| Building block \| Purpose \| Use when \| Details \|` (Details = Link) | `plugin/templates/development/interfaces.md`, `interface.md`, `catalog.md`, Skill `interfaces` |
| `architecture.md`, `architecture/<Scope>.md` | Markdown, englisch, Regeln mit MUST/SHOULD/MAY; Abschnitt `## Scopes` mit Tabelle `\| Scope \| Paths \| Covers \|` (optional mit Spalte `Required reading`), optional `## Required on use` mit Tabelle `\| Uses \| Read \|`, optional `## Inherited rules` mit Tabelle `\| Project \| Rules \|` | `plugin/templates/development/architecture.md` und `scope.md` (Scope-Datei), Skill `architecture` |

Scope-Tabelle: Name aus einem oder mehreren Segmenten aus Kleinbuchstaben,
Ziffern und `-`, getrennt durch `/` (kein führendes oder abschließendes `/`,
keine leeren Segmente); Datei `architecture/<Scope>.md` neben der Regeldatei,
also `plugins/patient` in `architecture/plugins/patient.md`. Ein Scope `plugins`
und ein Scope `plugins/patient` können nebeneinander bestehen; empfohlen sind
höchstens zwei Ebenen. Dieselbe Namensregel gilt für die Tabelle der geerbten
Regeln. Pfadmuster relativ zum
Projekt-Root in Backticks, kommagetrennt; `*` und `?` innerhalb eines
Pfadteils, `**` über beliebig viele Pfadteile. HTML-Kommentare werden
ignoriert. Ein Scope gilt zusätzlich zur Regeldatei.

Optionale Spalte `Required reading`: erkannt über die Kopfzeile (Zelle
`Required reading`, Groß-/Kleinschreibung egal); `Scope` und `Paths` bleiben
Spalte 1 und 2, ohne die Spalte gilt die Tabelle mit drei Spalten unverändert.
Einträge sind Dateipfade relativ zum Projekt-Root in Backticks, kommagetrennt,
leer erlaubt; Muster, führendes `/` und `..` sind ungültig (der Eintrag wird
verworfen, der Scope bleibt gültig). Der Session-Start meldet ungültige
Einträge und fehlende Dateien. Der Architektur-Hook verlangt vor der Änderung
einer Projektdatei zusätzlich diese Dateien aller passenden Scopes und nennt
fehlende Dateien mit dem Zusatz `(missing)`. Bei geerbten Scopes gilt ihre
Pflichtlektüre unabhängig von den Pfadmustern mit; die Pfade sind relativ zum
Projekt, das den Scope definiert.

Abschnitt `## Required on use` (optional, in `architecture.md` und in
Scope-Dateien) mit Tabelle `| Uses | Read |`. `Uses` sind Bezeichner in
Backticks, kommagetrennt; erlaubt sind `A-Z a-z 0-9 _ $ .` mit mindestens einem
Buchstaben. `Read` sind Dateipfade relativ zum Projekt-Root in Backticks
(gleiche Regeln wie bei `Required reading`, die Dateien müssen existieren). In
`architecture.md` gilt eine Zeile für alle Projektdateien (außer
Harness-Dateien), in einer Scope-Datei nur für Dateien, auf die die Pfade des
Scopes passen. Der Architektur-Hook sucht jeden Bezeichner im neuen Text
(`content`, `new_string`, alle `new_string` bei `MultiEdit`, `new_source`) als
Literal mit Wortgrenzen: er darf nicht direkt von `A-Z a-z 0-9 _ $` umgeben
sein, ein `.` im Bezeichner ist wörtlich (`reportErrorX` trifft nicht,
`this.reportError` trifft). Ist ein Treffer da und die `Read`-Datei nicht
vollständig gelesen, lehnt er mit Bezeichner, Datei und Pfad der geänderten
Datei ab (mehrere fehlende Dateien in einer Meldung, fehlende mit `(missing)`).
Die Prüfung läuft erst, wenn die Pflichtlektüre erfüllt ist. Geerbte Tabellen
(Hauptdatei und Scopes, unabhängig von den Pfadmustern) gelten mit; ihre Pfade
sind relativ zum Projekt, das sie definiert. Der Session-Start meldet ungültige
Bezeichner und Pfade sowie fehlende Dateien (eigene Tabellen als
`Architecture 'Required on use' tables have N errors`, geerbte unter
`Inherited rules`).

Tabelle der geerbten Regeln (nur bei Teilprojekten sinnvoll): `Project` ist
ein Name aus `[projects]` der Root-Config oder `root`, nicht das eigene
Projekt; `Rules` sind in Backticks `architecture.md` (Hauptdatei jenes
Projekts) oder Scope-Namen jenes Projekts. Ein geerbter Scope gilt unabhängig
von seinen Pfadmustern; es wird nicht weitervererbt. Der Architektur-Hook
verlangt die geerbten Dateien vor jeder Änderung einer Projektdatei;
fehlerhafte Einträge (unbekanntes oder unwirksames Projekt, Projekt ohne
Architektur, unbekannter Scope, fehlende Datei) überspringt er, der
Session-Start meldet sie.
