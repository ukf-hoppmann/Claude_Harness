# EPIC-010 — Weg von der Claude-Code-App: Harness und ToDo-Viewer über claude.ai nutzen

## 2026-10-14 — Ausgangslage und offene Fragen

### Discussed

- Cloud-Sessions auf claude.ai/code klonen nur das gewählte Repo in eine VM; ~/.claude und localhost des Rechners fehlen.
- Das Plugin müsste über .claude/settings.json des Fremdprojekts (extraKnownMarketplaces, enabledPlugins) aus einer von der VM erreichbaren Quelle (z.B. GitHub) geladen werden.
- Der ToDo-Viewer läuft lokal in einem Container (localhost:5411) und ist aus der Cloud nicht erreichbar.

### Decided

- Epic angelegt; die Details stammen aus Wissen, nicht aus der Doku geprüft.

### Open

- Funktionieren Projekt-Plugins und Hooks in Cloud-Sessions wie erwartet (gegen Doku prüfen)?
- Welche Netzwerkregeln gelten für ausgehende Zugriffe der VM (Zugriff auf einen extern erreichbaren Viewer)?
- ToDo-Viewer: Tunnel/Hosting mit Authentifizierung, Dateimodus (TODO.md im Repo) oder anderer Ersatz?
- Mehrere Repos pro Session: Liegt das Backlog zentral in Claude_Harness oder je Projekt?

## 2026-10-14 — Doku-Prüfung: Plugins in Cloud-Sessions

### Discussed

- Laut Doku (code.claude.com: claude-code-on-the-web, cloud-environments, plugins/install) installiert eine Cloud-Session keine Plugins aus enabledPlugins/extraKnownMarketplaces und keine lokalen oder Konto-Plugins. Plugin-Hooks und CLAUDE_PLUGIN_ROOT sind damit nicht aktiv (Folgerung, nicht wörtlich belegt).
- Repo-Inhalte laufen: CLAUDE.md, .claude/skills, agents, commands, rules, Hooks in .claude/settings.json (SessionStart-Hooks ausdrücklich). User-Level (~/.claude) fehlt.
- VM: Ubuntu 24.04, Python 3.x (Minor-Version nicht dokumentiert), git, gh, jq. Setup-Script (Bash, root) möglich. Netzwerk je Environment: None, Trusted (Default), Full, Custom (Hostliste). Eigene Hosts nur über Custom oder Full.
- Mehrere Repos pro Session möglich, dann zählen aus den Repo-Settings nur enabledPlugins und extraKnownMarketplaces, keine Hooks. GitHub-Proxy sperrt GraphQL, also gh pr/issue nicht nutzbar, gh api (REST) geht. Worktrees in der Cloud nicht dokumentiert.

### Decided

- Der Plugin-Weg (enabledPlugins) scheidet für die Cloud aus; Harness-Inhalte müssten unter .claude/ im Zielprojekt liegen.

### Open

- Python-Minor-Version in der Cloud-VM prüfen (Harness braucht 3.11+), sonst per Setup-Script.
- Wie kommen Skills, Hooks und Skripte des Harness als .claude/-Inhalt ins Zielprojekt (Export-/Sync-Befehl, Duplikation, Submodul)?
- Cloud-Verhalten des Worktree-Moduls testen oder abschalten.
- ToDo-Viewer: Custom-Allowlist plus Authentifizierung, oder Dateimodus.

## 2026-10-16 — Dateimodus in der Cloud: Abgleich mit dem ToDo-Viewer und Stories

### Discussed

- Besitzer-Vorgabe: Lokal bleibt die API; in der Cloud wird wieder über die Markdown-Dateien gearbeitet. Die Notes sind im ToDo-Viewer (v0.8.8) inzwischen als Dateien nachgezogen (Ordner notes/, Format in dessen Techdoc interfaces.md, Abschnitt Dateiformat: Notes-Ordner; Sync mit Konfliktdialog).
- Vergleich mit dem Harness: Der Backlog-Dateimodus ist vollständig (TODO.md, archive.md, items/, backlog.py, Stop-Hook; das Feld Deleted wird schon verstanden). Notes gibt es im Harness nur bei Backend api (notes_enabled), die Skill-Regeln und die README sagen ausdrücklich, dass nichts davon im Repository liegt. Das Backend gilt als eine einzige Einstellung der eingecheckten config.toml für alle Umgebungen.
- Der Viewer bricht den gesamten Sync bei einem einzigen Formatfehler in notes/ ab (400 note_format); Backlog-Items haben kein Verfahren für vorläufige IDs (nur Notes mit new-<kurzname>.md).

### Decided

- Fünf Stories unter diesem Epic angelegt: STORY-042 (Backend je Umgebung umschalten), STORY-043 (Notes und Topics im Dateimodus), STORY-044 (Formatprüfung für notes/), STORY-045 (Ablauf zwischen Cloud, Git und lokalem Viewer), STORY-046 (doppelt vergebene IDs; nicht Pflicht für das Epic).
- Reihenfolge: STORY-042 zuerst; STORY-043 und STORY-045 hängen davon ab, STORY-044 von STORY-043.

### Open

- Das Plugin wird in Cloud-Sitzungen nicht geladen (siehe Eintrag vom 2026-10-14). Solange Skill, Hooks und Skripte nicht aus dem Repository des Zielprojekts kommen, wirken STORY-042 bis STORY-045 in der Cloud nicht. Dafür ist noch keine Story angelegt; das bleibt Inhalt dieses Epics.
- Notes liegen im Dateimodus im Repository (GitHub). Der Besitzer entscheidet pro Projekt, ob das für seine Notes in Ordnung ist (betrifft STORY-043, Kriterium 5).
- Ob das Epic-Ziel zum Viewer (erreichbar oder ersetzt) auf den Weg Dateimodus plus lokaler Sync umgeschrieben wird, entscheidet der Besitzer.

## 2026-10-16 — Epic-Ziel an den Dateimodus in der Cloud angepasst

### Discussed

- Besitzer-Vorgabe: lokal API, Cloud Markdown-Dateien, beides im Sync.

### Decided

- Ziel, Abnahmekriterien und Summary des Epics neu gefasst: Der ToDo-Viewer muss aus der Cloud weder erreichbar sein noch ersetzt werden; die Cloud arbeitet mit den Dateien im Repository, der Sync des Viewers hält beide Seiten im Gleichstand. Der Plugin-Teil bleibt als Kriterium 1 (Skill, Hooks und Skripte ohne Plugin in der Cloud verfügbar).
- STORY-046 (doppelt vergebene IDs) ist jetzt Pflicht für dieses Epic (Required for parent: Yes), weil der Gleichstand auch bei gleichzeitiger Arbeit auf beiden Seiten ohne Verlust gelten soll.

### Open

- Für Kriterium 1 (Harness ohne Plugin in der Cloud) ist noch keine Story angelegt.
- Notes liegen im Dateimodus im Repository (GitHub); der Besitzer entscheidet pro Projekt (STORY-043, Kriterium 5).

## 2026-10-16 — docs/todo komplett nach GitHub; Arbeit künftig über die Web-Oberfläche

### Discussed

- Der Besitzer hat den Vorab-Test in einem Chat-Projekt auf claude.ai ausgeführt (Chat mit Code-Sandbox, keine Code-Sitzung: Arbeitsverzeichnis /home/claude, kein geklontes Repository, CLAUDE_PROJECT_DIR leer). Künftig soll die Arbeit über die Web-Oberfläche statt über die lokale Version laufen.
- Der ToDo-Viewer hat den Notes-Spiegel docs/todo/notes/ in das Repository geschrieben (NOTE-001, NOTE-002, topics.md, counters.md).

### Decided

- Der Besitzer entscheidet: docs/todo wird komplett committet und nach GitHub gepusht, einschließlich docs/todo/notes/. Das ist sein Sync. Damit ist die offene Frage zu Notes auf GitHub für dieses Projekt beantwortet (siehe STORY-043, Kriterium 5). Notes-Inhalte werden trotzdem nicht in andere eingecheckte Dokumente kopiert.

### Open

- Ob der Besitzer in der Web-Oberfläche den Bereich Chat oder den Bereich Code (claude.ai/code) meint, ist zu klären: Nur in einer Code-Sitzung wird das Repository geklont und .claude/ geladen, nur dort greift der Harness.
