# Architektur

Beschreibt den aktuellen Stand. Der Verlauf steht in den Tagesberichten
(`docs/daily/`), die Begründungen in den Backlog-Notizen.

## Überblick

Claude_Harness ist ein Claude-Code-Plugin. Regeln, die nur bei bestimmten
Aufgaben gelten, liegen als Skills vor; Claude Code lädt dauerhaft nur ihre
einzeilige Beschreibung und den Inhalt erst beim passenden Thema. Regeln, die
nicht vergessen werden dürfen, prüfen Hooks: Python-Skripte, die Claude Code
bei Ereignissen aufruft und die keine Tokens kosten, solange sie nichts melden.
Jedes Modul prüft selbst, ob es in der Projektkonfiguration eingeschaltet ist.

## Komponenten

| Komponente | Aufgabe | Ort |
|---|---|---|
| Plugin-Manifest | Name, Version, Beschreibung des Plugins | `plugin/.claude-plugin/plugin.json` |
| Marketplace | Macht das Plugin lokal installierbar | `.claude-plugin/marketplace.json` |
| Hook-Registrierung | Verknüpft Ereignisse mit Skripten | `plugin/hooks/hooks.json` |
| Config-Lader | Liest und validiert `.claude-harness/config.toml` | `plugin/scripts/harness_config.py` |
| Projekte | Lädt das Root-Projekt und die in `[projects]` eingetragenen Teilprojekte und ordnet jede Datei ihrem Projekt zu | `plugin/scripts/projects.py` |
| Session-Start | Meldet aktive Module, Sprache, fehlende Dateien und Backlog-Fehler, bei Teilprojekten pro Projekt; meldet eine Cloud-Kopie, die nicht zu `cloud.export` passt | `plugin/scripts/session_start.py` |
| Modul `todo` | Skill mit Backlog-Regeln und, als Unterdatei, den Regeln für Notes und Topics (Erinnerungen, Fragen, Beobachtungen, Ideen) im ToDo-Viewer; Backend `api`: Helfer für die HTTP-API des ToDo-Viewers (der Server prüft Format und Regeln); Backend `files`: Formatprüfung und Prüf-Hooks; der Weg des Backlogs zwischen Cloud-Sitzung (Dateien, Branch `claude/<Name>`), Git (Pull Request, `git pull`) und lokalem Viewer (Spiegel-Ordner, Auto-Sync, Konflikte im Sync-Dialog) steht als Unterdatei `sync-flow.md` im Skill | `plugin/skills/todo/`, `plugin/scripts/backlog_api.py`, `notes_api.py`, `backlog.py`, `mark_backlog_dirty.py`, `check_backlog.py` |
| Notes (Teil von `todo`) | Backend `api`: Skript `notes_api.py` für die HTTP-API des Viewers; die Notes liegen nur in der Datenbank des Viewers, der Viewer entscheidet über Fälligkeit und Auslöser. Backend `files` (auch in der Cloud): Notes und Topics als Markdown-Dateien in `notes/` unter dem Backlog-Ordner im Dateiformat Version 2 des Viewers, der sie beim Sync liest; Index und Fälligkeit nach Review- und Topic-Datum liefert `notes_files.py`, die Formatprüfung nach den Regeln des Viewer-Decoders `notes_format.py` (CLI `--check`; der Stop-Hook `check_backlog.py` ruft sie, wenn in der Session eine Datei unter `notes/` geändert wurde). In beiden Fällen prüft der Harness nichts und hat keinen Hook außer der statischen Zeile beim Session-Start | `plugin/skills/todo/notes.md`, `notes-api.md`, `notes-files.md`, `plugin/scripts/notes_api.py`, `notes_files.py`, `notes_format.py` |
| Wecker (Teil von `todo`) | Nur Backend `api`: Skript `alarms_api.py` für die Wecker des Viewers (Erinnerung zu einem festen Zeitpunkt, frei oder an Items und Notes gebunden). Der Viewer lässt sie klingeln, lässt sie erlöschen und räumt sie auf; der Harness prüft nichts | `plugin/skills/todo/alarms.md`, `plugin/scripts/alarms_api.py` |
| API-Client | Gemeinsamer HTTP-Client für die Helfer `backlog_api.py`, `notes_api.py` und `alarms_api.py`: Aufruf, Fehlertexte und Exit-Codes, Projektwahl aus der Config, Auffinden des Viewer-Projekts über den Spiegel-Ordner des Backlog-Ordners (Registrieren nur auf Befehl), Auflösen von Labels in `uid`s | `plugin/scripts/viewer_api.py` |
| Modul `daily` | Skill, Git-Auswertung, Erinnerungs-Hook | `plugin/skills/daily/`, `plugin/scripts/daily.py`, `check_daily.py` |
| Modul `techdocs` | Skill, Dateiklassifikation, Erinnerungs-Hooks | `plugin/skills/techdocs/`, `plugin/scripts/techdocs.py`, `mark_techdocs.py`, `check_techdocs.py` |
| Suite `development`, Teil `architecture` | Skill, Scope-Tabelle, geerbte Regeln anderer Projekte, Lese-Merker, Hook vor Änderungen | `plugin/skills/architecture/`, `plugin/scripts/architecture.py`, `mark_architecture_read.py`, `check_architecture.py` |
| Suite `development`, Teil `decomposition` | Skill mit Kriterien zur Zerlegung von Epics in Stories, von Stories in Tasks und von Plänen in Abschnitte, Regeln, wann der Test zuerst entsteht (TDD), Dimensions-Checkliste; Ausführen von Tests verweist auf Teil `testing` | `plugin/skills/decomposition/` |
| Suite `development`, Teil `testing` | Skill mit Regeln zu Testordner (`development.tests`), Gliederung, Implementierungs- und Funktionalitätstests und zum Ausführen von Tests; Zeile beim Session-Start | `plugin/skills/testing/` |
| Suite `development`, Teil `worktree` | Skill für den Change-Workflow im Worktree, Skript für Ausgangsbranch, Spiegeln ignorierter Dateien und Vorprüfung vor dem Merge, Prüfung von `worktree.baseRef` beim Session-Start | `plugin/skills/worktree/`, `plugin/scripts/worktree.py` |
| Modul `semver` | Skill für Einstufung und Release, Prüfung von Versionsdatei, Tag-Schritt und Spiegel-Dateien, Prüf-Hook | `plugin/skills/semver/`, `plugin/scripts/semver.py`, `check_semver.py` |
| Konflikte | Skill für Konflikte mit Projektregeln und Harness-Vorgaben, Suche des Harness-Repos für die Übergabe von Harness-Wünschen | `plugin/skills/conflicts/`, `plugin/scripts/harness_repo.py` |
| Befehl `init` | Richtet den Harness in einem Projekt oder Teilprojekt ein, auf Wunsch auch die Cloud-Kopie | `plugin/skills/init/` |
| Befehl `update` | Bringt die Config eines Projekts auf den aktuellen Stand: Migrationen, Abgleich mit der Config-Vorlage; hält die Cloud-Kopie aktuell oder nimmt sie wieder heraus | `plugin/skills/update/`, `plugin/scripts/config_update.py` |
| Cloud-Kopie | Erzeugt aus dem Plugin eine eingecheckte Kopie im Projekt (Skills, Skripte, Vorlagen, Hooks), weil Cloud-Sitzungen das Plugin nicht laden, wohl aber den Inhalt des Repositories; Manifest, Vorschau mit Diff, Rückbau | `plugin/scripts/cloud_export.py` |
| Vorlagen | Config, Backlog, Tagesbericht, Systemdoku, Architekturregeln | `plugin/templates/` |
| Sitzungszustand | Pfade für Merker pro Session | `plugin/scripts/state.py` |

## Module und Ladestufen

Wo jedes Modul liegt und warum. Die Regel dahinter steht in
`docs/development/architecture.md`, Abschnitt 7. Immer im Kontext sind nur
die Skill-Beschreibungen (je ein Satz) und eine Startzeile pro Modul; bei
Teilprojekten steht jeder Skill-Hinweis einmal, dazu eine Zeile pro Projekt.

| Modul | Hook (prüft, kostet nichts, solange alles stimmt) | Skill (lädt beim Thema) | Skript | Warum so |
|---|---|---|---|---|
| `todo` | Nur Backend `files`: Formatprüfung am Ende eines Turns, nur nach Backlog-Änderungen | Backlog-Regeln; API-Befehle in `api.md`, Formatdetails in `format.md`, jeweils nur bei Bedarf | `backlog_api.py` (API), `backlog.py` (Prüfung, Übersicht) | Im API-Modus prüft der Server jede Änderung; im Datei-Modus lässt sich das Format prüfen und darf nicht kaputtgehen; die Arbeitsregeln betreffen nur Backlog-Arbeit |
| Notes (Teil von `todo`) | Die statische Zeile beim Session-Start (Hooks nutzen das Netzwerk nicht, also fragt kein Hook nach Fälligem); im Dateimodus zusätzlich die Formatprüfung des Ordners `notes/` am Turn-Ende, weil ein Formatfehler den ganzen Sync des Viewers blockiert und nicht vergessen werden darf | Regeln für Notes und Topics; Befehle in `notes-api.md`, Dateiformat und Befugnis in `notes-files.md`, nur bei Bedarf (Unterdateien des Skills `todo`) | `notes_api.py` (API), `notes_files.py` und `notes_format.py` (Dateien; nach einer Änderung unter `notes/` prüft `check_backlog.py` das Format) | Fälligkeit, Auslöser und Hinweise bestimmt der Viewer; die Regeln braucht es nur, wenn der Besitzer etwas merken, erinnern oder Fälliges ansehen will |
| `daily` | Erinnerung bei neuen Commits auf dem Branch, in den gemerged wird | Berichtsregeln | `daily.py` (offene Commits, Bestätigen) | Das Fehlen eines Berichts ist erkennbar; Schreiben ist nur nach Commits Thema; die Git-Auswertung ist stures Abarbeiten |
| `techdocs` | Erinnerung, wenn Code, aber keine Doku geändert wurde | Doku-Regeln | – | Vergessene Doku ist erkennbar; die Regeln braucht es nur bei dokumentationsrelevanten Änderungen |
| `development` / `architecture` | Blockiert Plan, Spec und Code-Änderungen, bis die Regeln gelesen sind | Umgang mit Architekturregeln | – | Die Regeln gelten für jede Code-Änderung und dürfen nicht übergangen werden; Bereichsregeln als Scopes nur für passende Pfade |
| `development` / `decomposition` | – | Kriterien für Stories, Tasks und Plan-Abschnitte, Test-zuerst-Regeln, Dimensions-Checkliste | – | Ob gut zerlegt oder zuerst getestet wurde, kann kein Skript prüfen; die Regeln braucht es nur beim Planen und Umsetzen |
| `development` / `worktree` | Session-Start meldet, wenn `worktree.baseRef` nicht `"head"` ist | Ablauf von der Entscheidung bis zum Aufräumen, Verbote | `worktree.py` (Ausgangsbranch merken, ignorierte Dateien spiegeln, Vorprüfung) | Eine falsche Basis wäre unbemerkt fatal und ist prüfbar; den Ablauf braucht es nur bei Changes mit Plan; die Git-Auswertung ist stures Abarbeiten |
| `semver` | Meldet ungültige Version, zu großen Schritt seit dem letzten Release-Tag und abweichende Spiegel-Dateien; Session-Start zeigt Version und unveröffentlichte Commits | Wann und wie eingestuft und released wird, Einrichtung | `semver.py` (Status, Prüfung, Commits seit dem Release) | Der Schritt lässt sich prüfen, weil die Versionsdatei überall gleich aussieht; die Einstufung braucht Urteil und ist nur beim Merge oder Release Thema |
| Konflikte (kein Modul, immer aktiv) | – | Verfahren bei Konflikten, Übergabe an den Harness-Backlog | `harness_repo.py` (Harness-Repo finden oder vorschlagen) | Konflikte lassen sich nicht mechanisch erkennen; das Verfahren braucht es nur im Konfliktfall, dann aber für alle Module |
| `init` | – | Einrichtungsablauf, nur vom Nutzer aufrufbar | – | Wird einmal pro Projekt gebraucht |
| `update` | – | Aktualisierungsablauf, nur vom Nutzer aufrufbar | `config_update.py` (Abgleich mit der Vorlage), `cloud_export.py` (Cloud-Kopie) | Wird nur nach einem Plugin-Update gebraucht; der Abgleich ist stures Abarbeiten, die Entscheidungen trifft der Nutzer |
| Cloud-Kopie (`cloud.export`) | Session-Start meldet eine fehlende, veraltete oder trotz `cloud.export = false` vorhandene Kopie; die Hooks der Kopie laufen nur in Cloud-Sitzungen | Die Skills der Kopie (`harness-<Name>`) sind erzeugte Texte der Plugin-Skills | `cloud_export.py` (Vorschau, Schreiben, Status, Rückbau) | Cloud-Sitzungen laden das Plugin nicht, wohl aber `CLAUDE.md`, `.claude/skills` und die Hooks aus `.claude/settings.json` des einzigen Repositories der Sitzung; Erzeugen und Zurücknehmen sind stures Abarbeiten, die Freigabe gibt der Nutzer |

Unterordner-`CLAUDE.md` nutzt der Harness nicht; bereichsbezogene Regeln
sind Architektur-Scopes. Die Root-`CLAUDE.md` schreibt das Plugin nie.

## Ablauf

1. **SessionStart:** `session_start.py` lädt über `projects.py` die Config
   des Root-Projekts und die der Teilprojekte und schreibt eine Kurzfassung in
   den Kontext (aktive Module, Dokumentsprache, Orte der Dokumente, fehlende
   Dateien, Backlog-Fehler). Mit Teilprojekten: eine Zeile pro Projekt mit
   Sprache, Modulen und Orten (Pfade relativ zum Session-Root), jeder
   Skill-Hinweis einmal, Fehler mit Projektnamen; ein Teilprojekt ohne oder
   mit ungültiger Config wird gemeldet, die anderen bleiben wirksam.
2. **PreToolUse (Write/Edit/MultiEdit/NotebookEdit/ExitPlanMode):**
   `check_architecture.py` lehnt das Vorlegen eines Plans, das Schreiben einer
   Backlog-Spec und die Änderung einer Projektdatei ab, bis die
   Architekturregeln (bei Projektdateien auch passende Scope-Dateien) in der
   Session vollständig gelesen wurden.
3. **PostToolUse (Read):** `mark_architecture_read.py` merkt sich vollständig
   gelesene Regel- und Scope-Dateien.
4. **PostToolUse (Write/Edit/MultiEdit):** `mark_backlog_dirty.py` merkt sich
   Änderungen im Backlog-Ordner; `mark_techdocs.py` merkt sich, ob
   Projektdateien oder Systemdoku geändert wurden.
5. **Stop:** Die Prüf-Hooks laufen nacheinander. Melden sie etwas, beenden sie
   sich mit Exit-Code 2; Claude Code gibt die Meldung an Claude zurück, das
   daraufhin weiterarbeitet.
   - `check_backlog.py`: prüft jeden Backlog, der in der Session geändert
     wurde, bei Teilprojekten also pro Projekt.
   - `check_daily.py`: erinnert an den Tagesbericht, wenn neue Commits auf dem
     Branch, in den gemerged wird, noch nicht erfasst sind, pro Projekt. Ein Commit zählt nur für
     das Projekt, dessen Dateien er ändert; Commits, die nur Daily- oder
     Backlog-Ordner ändern, zählen nicht, der Backlog dokumentiert sich selbst.
   - `check_techdocs.py`: erinnert einmal pro Projekt und Session, wenn
     Projektdateien, aber keine Systemdoku desselben Projekts geändert wurden.
   - `check_semver.py`: prüft pro Projekt Versionsdatei, Schritt seit dem
     letzten Release-Tag und Spiegel-Dateien; derselbe Befund einmal pro
     Session.

### In einer Cloud-Sitzung

Eine Cloud-Sitzung (claude.ai/code, `CLAUDE_CODE_REMOTE=true`) klont das
Repository und lädt das Plugin nicht. Hat das Projekt eine Cloud-Kopie, wirken
dort dieselben Ereignisse wie lokal, nur aus den Dateien des Projekts: Die
Skills `harness-<Name>` liegen unter `.claude/skills/`, die Hooks stehen in
`.claude/settings.json` und rufen die Skripte unter `.claude-harness/runtime/`
auf. Jeder Hook-Befehl beginnt mit einem Wächter
(`[ "$CLAUDE_CODE_REMOTE" != "true" ] || …`): Lokal beendet er sich sofort, dort
gelten die Hooks des Plugins, und der Exit-Code eines blockierenden Hooks
bleibt in der Cloud erhalten. Die Hooks der Kopie gelten nur in Sitzungen mit
einem Repository; bei mehreren Repositories lädt die Cloud keine Hooks aus
deren `settings.json`.

Den ToDo-Viewer erreicht eine Cloud-Sitzung nicht. Beim Laden der Config
(`load_config`) gilt deshalb dort das Backend `files`, auch wenn
`todo.backend` auf `api` steht; `CLAUDE_HARNESS_TODO_BACKEND` hat Vorrang vor
dieser Erkennung. Session-Start, Backlog-Hooks und Skills folgen diesem
wirksamen Backend; die Config-Datei bleibt unverändert.

## Zustand und Ablage

| Zustand | Ort | Lebensdauer |
|---|---|---|
| Projektkonfiguration | `.claude-harness/config.toml` | im Repo versioniert |
| Merker pro Session (Backlog geändert, Hinweise gemeldet, Doku-Erinnerung, gelesene Architekturregeln, gemeldete SemVer-Befunde, Items mit geänderten Notes und aktive Items aus `backlog_api.py`) | `$CLAUDE_PLUGIN_DATA`, sonst `<tmp>/claude-harness/` | pro Session |
| Ausgangsbranch eines Worktrees | Git-Config `branch.<worktree-branch>.harnessBase` | bis der Branch gelöscht wird |
| Bestätigter Stand des Tagesberichts, eine Zeile `<Commit> <Branch>` pro Branch | `.git/claude-harness/daily-ack`, für ein Projekt unterhalb des Git-Roots `daily-ack-<Ordner mit _ statt />` | pro Klon und Projektordner, nie committet |
| Release-Tags | Tags `<Präfix><Version>` | im Repo, nur lokal, bis der Owner sie pusht |
| Backlog, Tagesberichte, Systemdoku, Regeln der Suite `development`, Versionsdatei | unter `docs.root` (Standard `docs/`) bzw. `README.md` | im Repo versioniert |
| Cloud-Kopie: Skills `harness-<Name>`, Skripte und Vorlagen, Hook-Einträge, Manifest | `.claude/skills/harness-*/`, `.claude-harness/runtime/` (mit `manifest.json`), Einträge in `.claude/settings.json` | im Repo versioniert, erzeugt und nie von Hand gepflegt; das Manifest nennt jede erzeugte Datei mit Hash |

## Wichtige Entscheidungen

| Entscheidung | Kurzbegründung | Referenz |
|---|---|---|
| Plugin mit Skills und Hooks statt gerenderter Regeln in `CLAUDE.md` | Regeln kosten nur Tokens, wenn sie gebraucht werden | `EPIC-007` |
| Ein Plugin mit Modulschaltern in der Config | Einfache Installation; Module prüfen ihren Schalter selbst | `EPIC-001` |
| Tagesbericht erst nach dem Merge, auf dem Branch, in den gemerged wird (nie auf dem Branch eines laufenden Changes) | Vermeidet Merge-Konflikte bei parallelen Worktrees; Bericht und Änderung landen im selben Branch | `STORY-013` |
| Change merged in seinen Ausgangsbranch, auch wenn der Haupt-Checkout inzwischen gewechselt hat (dann im Worktree) | Die Arbeit des Owners auf dem anderen Branch bleibt unberührt | – |
| Systemdoku im selben Change wie der Code | Doku und Code bleiben in jedem Stand konsistent | `STORY-012` |
| Gestufte Ablage: Hook → Scope → Skill → Skript → Root-`CLAUDE.md` | Nur das Nötigste ist immer im Kontext; Pflichtregeln prüft ein Hook | `STORY-019` |
| Architekturregeln als Teil der Suite `development`, englisch, Scopes als Tabelle in der Regeldatei, Lesen per Hook erzwungen | Regeln werden zuverlässig gelesen; Spezielles nur, wo es gilt | `STORY-023` |
| Zerlegung als Teil der Suite `development`, Kriterien fest im Plugin, kein Hook | Kleine, einzeln testbare Schritte senken Fehler und Aufwand; die Güte einer Zerlegung ist nicht mechanisch prüfbar | `STORY-004` |
| Changes mit Plan im Worktree vom aktuellen Branch, Merge-Commit zurück ohne Rückfrage, kein Push, fremde Worktrees nie löschen | Paralleles Arbeiten; Ziel ist der Branch, den der Eigner ausgecheckt hat; ein Revert nimmt den ganzen Change zurück | `STORY-022` |
| Nur Python-Standardbibliothek | Keine Installationsschritte in Zielprojekten | `STORY-018` |
| Der Harness läuft in Cloud-Sitzungen als eingecheckte, erzeugte Kopie im Projekt (Weg A); kopiert wird nur `plugin/`; die Hooks der Kopie laufen nur bei `CLAUDE_CODE_REMOTE=true`; die Kopie lässt sich über ihr Manifest vollständig wieder entfernen | Die Cloud lädt das Plugin nicht (Doku und Test), wohl aber den Repository-Inhalt; die Kopie braucht weder Setup-Script noch ein zweites Repository und ist ohne Spuren rückbaubar | `STORY-047`, `EPIC-010` |
