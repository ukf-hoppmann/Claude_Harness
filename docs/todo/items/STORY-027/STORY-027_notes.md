# STORY-027 — Harness pro Teilprojekt

## 2026-09-25 — Anforderung und erste Entscheidungen

### Discussed

- Beispiel EZF-Backend: Arbeit mit Claude nur am Plugin VariantFilter. Dort
  gehören Architekturregeln und Doku hin. Ein Kollege möchte keine
  Harness-Dateien im Repo-Root. Weitere Plugins brauchen jeweils eine eigene
  Struktur.
- Idee des Owners: eine minimale Liste im Root, die Teilprojekte definiert,
  z. B. Root → Plugin-Core, VariantCaller → `Plugins/VariantCaller`,
  OtherPlugin → `Plugins/OtherPlugin`. So kann auch ein Hauptprojekt mit
  eigenem Harness neben Teilprojekten mit separatem Harness bestehen.
- Claude-Code-Settings (`.claude/settings.json`: Plugin-Aktivierung, Hooks,
  Rechte) und Harness-Konfiguration (`.claude-harness/config.toml`: Module,
  Pfade, Sprache) sind getrennt. Annahme, noch zu prüfen: Claude Code lädt
  `.claude/settings.json` nur aus dem Startverzeichnis der Session, nicht aus
  Unterordnern.

### Decided

- Eine minimale Registry im Root ist zulässig. Harness-Dateien können über
  `.gitignore` für Kollegen unsichtbar bleiben.
- Die Doku liegt im jeweiligen Teilprojekt: Arbeit am Core → Doku im Core,
  Arbeit an einem Plugin → Doku im Plugin.
- Die Settings können pro Teilprojekt liegen, sodass das Plugin je
  Teilprojekt eigens konfiguriert wird.
- Der Worktree umfasst weiterhin das ganze Repo. Plan und Prüfungen beziehen
  sich nur auf das Teilprojekt.

### Open

- Form und Ort der Registry (Abschnitt in `CLAUDE.md` oder eigene Datei).
- Wie ein Hook die Konfiguration einer bearbeiteten Datei findet
  (Registry-Eintrag, Suche nach oben).
- ~~Ob verschachtelte `.claude/settings.json` geladen werden~~ (geklärt am 2026-09-25, siehe unten).
- Gitignorierte Harness-Dateien fehlen in einem frisch angelegten Worktree.
  Klären, wie der Worktree-Workflow damit umgeht.
- Daily Reports: nur Commits, die den Ordner des Teilprojekts betreffen.

## 2026-09-25 — Ladeverhalten der Claude-Code-Settings geprüft

### Discussed

- Versuch mit Claude Code 2.1.278 in einem Test-Repo mit
  `repo/.claude/settings.json` und `repo/Plugins/VC/.claude/settings.json`.
  Beide Dateien enthalten SessionStart- und PreToolUse-Hooks, die ausgeben,
  welche Datei gilt und welchen Wert `CLAUDE_PROJECT_DIR` hat.
  - Start im Root, Lesen einer Datei im Teilprojekt: Nur die Root-Settings
    greifen. Die Settings im Teilprojekt werden auch dann nicht geladen, wenn
    dort Dateien bearbeitet werden. `CLAUDE_PROJECT_DIR` ist das Root.
  - Start im Teilprojekt: Nur die Settings des Teilprojekts greifen. Die
    Root-Settings werden nicht geladen, obwohl das Git-Root darüber liegt.
    `CLAUDE_PROJECT_DIR` ist der Ordner des Teilprojekts.
  - Start im Teilprojekt ohne eigene Settings: Es greifen gar keine Hooks,
    Claude Code sucht also nicht nach oben.
- Welche Settings und damit welche Hooks gelten, hängt am
  Startverzeichnis, nicht an der bearbeiteten Datei.
- Ein Teilprojekt mit eigener `settings.json` ist beim Start dort also
  vollständig eigenständig. Der Harness sieht es heute schon als
  Projekt-Root, weil er `CLAUDE_PROJECT_DIR` nutzt. Probleme macht nur, was
  vom Git-Root abhängt (Worktree, Daily Reports über `git log`).
- Beim Start im Root greifen nur die Root-Settings. Dort muss das Plugin
  aktiv sein, z. B. über `.claude/settings.local.json`. Welches Teilprojekt
  gilt, muss dann der Harness selbst über die Registry bestimmen.
- Folgerung: Individuelle Settings pro Teilprojekt gibt es nur beim Start im
  Teilprojekt. Beim Start im Root gelten für alle Teilprojekte dieselben
  Claude-Code-Settings. Nur die Harness-Konfiguration kann dann pro
  Teilprojekt verschieden sein.

## 2026-09-25 — Priorität der beiden Fälle

### Discussed

- Wer Plugins entwickelt, muss die Hauptanwendung lesen (API usw.) und
  gegen sie testen. Die Session startet deshalb in der Regel im Repo-Root.
- Start im Teilprojekt: Der Owner öffnet nur den Ordner des Teilprojekts als
  Projekt, dann ist das Teilprojekt das Root und der Harness läuft wie
  bisher. Zwei Lücken bleiben, weil das Git-Root darüber liegt:
  - Daily Reports vergleichen Pfade aus `git diff` (relativ zum Git-Root)
    mit Modulpfaden relativ zum Projekt-Root (`daily.py`,
    `_changed_files`/`_counts`). Commits, die nur den Backlog ändern, zählen
    dann fälschlich. Commits außerhalb des Teilprojekts lösen eine
    Erinnerung an den Daily Report aus.
  - Worktree: Ungetestet ist, ob die Session im Worktree im
    Teilprojekt-Unterordner landet und die Konfiguration dort findet.

### Decided

- Der Start im Root mit Registry und mehreren Teilprojekten ist der
  Hauptfall und hat Vorrang.
- Der Start im Teilprojekt bekommt keinen eigenen Umbau. Seine beiden Lücken
  werden mitgelöst, weil sie auf dieselbe Ursache zurückgehen:
  Teilprojekt-Root und Git-Root sind verschieden.

## 2026-09-25 — Entwurf für den Start im Root

### Discussed

- Registry als Tabelle `[projects]` (Name → Pfad) in der
  `.claude-harness/config.toml` im Repo-Root. Das Root kann selbst ein
  Harness-Projekt sein oder nur als Registry dienen. Jedes Teilprojekt hat
  seine eigene `<pfad>/.claude-harness/config.toml`.
- Zuordnung: Eine Datei gehört zum tiefsten eingetragenen Teilprojekt, das
  sie enthält, sonst zum Root-Projekt. Hooks nutzen Konfiguration und
  Dokumente dieses Projekts.
- Daily Reports pro Projekt, nur mit Commits, die Dateien dieses Projekts
  ändern.
- Beim Sessionstart nennt der Harness kurz alle Projekte mit ihren Modulen
  und Doku-Pfaden.
- Vererbung von Architekturregeln: Ein Abschnitt `## Inherited rules` in der
  `architecture.md` des Teilprojekts nennt Projekt und Regeln, entweder
  `architecture.md` oder einzelne Scopes. Der Architektur-Hook verlangt dann
  auch diese Dateien. Bei Widersprüchen gilt die Regel des Teilprojekts, und
  der Konflikt wird benannt.

### Decided

- Architekturregeln sind pro Projekt eigenständig. Ob die Core-Architektur
  mitgilt, legt das Teilprojekt in seiner `architecture.md` selbst fest.
- Jedes Teilprojekt hat ein eigenes Backlog. Ein gemeinsames Backlog im Root
  wird erst besprochen, wenn sich zeigt, dass es gebraucht wird.
- Ein Change über mehrere Projekte hinweg: Jede Datei folgt den Regeln ihres
  Projekts, und der Plan nennt alle betroffenen Projekte.

### Open

- Registry, Zuordnungsregel, Daily-Report-Filter, Sessionstart-Ausgabe und
  das Format von `## Inherited rules` sind Entwurf und sollen mit der Spec
  bestätigt werden.

## 2026-09-25 — Spec und Zerlegung

### Decided

- Die Zerlegung aus der Spec ist freigegeben. Angelegt sind `TASK-007` bis
  `TASK-012` als Pflicht-Tasks unter `STORY-027`.

### Open

- Die Änderung von Architekturregel 7 (Session-Start-Ausgabe bei mehreren
  Projekten) ist noch nicht freigegeben.

## 2026-09-25 — Was im Projekt liegt

### Discussed

- Der Owner schlug vor, den Harness einmal im Root abzulegen und Projekte
  nur über `config.toml` und `docs/` anzupassen. Klarstellung: Skills, Hooks
  und Skripte liegen im installierten Plugin (einmal pro Rechner), nicht in
  `.claude-harness/`. Dort liegt nur die `config.toml`. Der Vorschlag
  entspricht damit der Spec.

### Decided

- `.claude-harness/config.toml` von Root und Teilprojekten darf in die
  `.gitignore`. Sie lässt sich mit `init` schnell wiederherstellen.
- `docs/` jedes Projekts wird eingecheckt. Kollegen sehen nur die Doku.
- Das Plugin wird im Root über `.claude/settings.local.json` aktiviert, nicht
  über die eingecheckte `settings.json`.

## 2026-09-25 — Architekturregel 7

### Decided

- Der Owner hat die Änderung von Architekturregel 7 freigegeben: Skill-Hinweise
  erscheinen einmal pro Modul, das in mindestens einem Projekt aktiv ist
  (wie ein Set, ohne Wiederholung). Jedes Projekt bekommt eine Zeile mit
  seinen Orten. Wortlaut siehe Spec. Umsetzung zusammen mit `TASK-007`.

## 2026-09-25 — TASK-007 umgesetzt

### Discussed

- Umgesetzt:
  - `[projects]` in der Root-Konfiguration samt Validierung.
  - Die Sperre von `[projects]` und `[harness]` in Teilprojekten.
  - Der Helfer `plugin/scripts/projects.py`.
  - Die kompakte Session-Start-Ausgabe nach dem neuen Wortlaut von Regel 7.
- Geprüft mit einem Test-Repo nach dem Vorbild von EZF-Backend: Core in `de`
  sowie `Plugins/VariantFilter` in `en` und `Plugins/Other` ohne
  Konfiguration. Das ergibt 11 Zeilen Session-Start. Ohne `[projects]` ist
  die Ausgabe byte-gleich zu vorher.
- Zwischenstand: Die übrigen Hooks (Architektur, Backlog, techdocs, Daily)
  behandeln Dateien in Teilprojekten noch als Dateien des Root-Projekts.
  Das ändern `TASK-008` bis `TASK-011`.

## 2026-09-25 — TASK-008 umgesetzt

### Discussed

- Architektur-Hooks arbeiten pro Projekt:
  - Eine Datei verlangt die Regeln und Scopes ihres Projekts.
  - Eine Spec verlangt die Regeln des Projekts, in dessen Backlog sie liegt.
  - Ein Plan verlangt die Regeln jedes Projekts, dessen Pfad im Plantext
    vorkommt, sonst die Regeln von root.
  - Der Lese-Status speichert Pfade relativ zum Session-Root, damit
    gleichnamige Regeldateien verschiedener Projekte getrennt bleiben.
- Root-Scopes gelten nicht für Dateien in Teilprojekten, auch wenn ihre
  Muster passen. Die Muster sind relativ zum jeweiligen Projekt.

## 2026-09-25 — TASK-009 umgesetzt

### Discussed

- `## Inherited rules` in `architecture.md`:
  - Der Parser steht in `architecture.py` (`parse_inherited`,
    `inherited_files`).
  - Der Hook verlangt die geerbten Dateien zusätzlich.
  - Der Session-Start meldet fehlerhafte Einträge als Problemzeilen des
    Projekts, auch ohne Teilprojekte.
  - Template und Skill `architecture` sind ergänzt.
- Ein geerbter Scope gilt unabhängig von seinen Pfadmustern. Geerbt wird
  nur, was direkt genannt ist.
