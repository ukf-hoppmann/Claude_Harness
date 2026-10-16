# STORY-047 — Harness ohne Plugin in Cloud-Sessions verfügbar machen

## 2026-10-16 — Doku-Prüfung und Lieferwege

### Discussed

- Doku geprüft am 2026-10-16 (code.claude.com: Plugins installieren, Cloud-Umgebungen, Einstellungen in Cloud-Sessions). Wörtlich belegt: Eine Cloud-Session installiert die Plugins nicht, die im .claude/settings.json des Repositorys unter enabledPlugins stehen (auch nicht aus extraKnownMarketplaces), und nicht die, die lokal installiert sind. Die Folgerung vom 2026-10-14 in den Notes von EPIC-010 ist damit bestätigt.
- Aus dem Repository wirken in der Cloud: CLAUDE.md, .claude/skills, agents, commands und rules, .mcp.json sowie Hooks und Berechtigungsregeln aus .claude/settings.json, die Hooks aber nur in einer Session mit einem Repository (bei mehreren Repositories lädt keines seine Hooks). Das ~/.claude der eigenen Maschine fehlt. Skills, die auf claude.ai aktiviert sind, lädt die Cloud automatisch (nur Skills, keine Hooks oder Skripte).
- Ein Setup-Script des Cloud-Environments (Bash als root, läuft vor dem Start von Claude Code, Ergebnis wird gecacht, wenn es unter etwa fünf Minuten bleibt, Cache läuft nach etwa sieben Tagen ab) kann Dateien schreiben. Dokumentiertes Beispiel: ~/.claude/CLAUDE.md, das Claude Code dann als Nutzeranweisung lädt. Umgebungsvariablen lassen sich je Environment setzen.
- VM: Ubuntu 24.04, Python 3.x (Minor-Version nicht dokumentiert; 24.04 bringt 3.12 mit, zu prüfen mit python3 --version), git, gh, jq. Netzwerk Trusted (Standard) erreicht PyPI und npm; GitHub läuft über einen Proxy.
- CLAUDE_CODE_REMOTE=true ist in der Session-VM gesetzt und lokal nie (dokumentiert). CLAUDE_PROJECT_DIR zeigt in Hooks auf die Repository-Wurzel. Damit ist die automatische Cloud-Erkennung für STORY-042 möglich.
- Lieferweg A: erzeugte Kopie im Zielprojekt unter .claude/ (Skills nach .claude/skills ohne den Namensraum claude-harness:, Hooks in .claude/settings.json mit $CLAUDE_PROJECT_DIR, Skripte unter .claude/harness/). Wirkt laut Doku sicher, weil Repository-Inhalt. Aufwand: Generator mit Pfadersetzung für CLAUDE_PLUGIN_ROOT und CLAUDE_PLUGIN_DATA, eine Kopie in jedem Projekt, Update-Weg nötig, Hooks nur in Sessions mit einem Repository.
- Lieferweg B: Harness einmal im Environment. Das Setup-Script holt Claude_Harness (z. B. nach /opt), schreibt Hooks nach ~/.claude/settings.json der VM, legt die Skills unter ~/.claude/skills ab und setzt CLAUDE_PLUGIN_ROOT; oder es installiert das Plugin mit claude plugin install. Eine Kopie, nichts im Zielprojekt, Aktualisierung über den Cache-Ablauf. Nicht dokumentiert, also zu testen: ob Hooks und Skills unter ~/.claude der VM in der Session wirken, ob claude plugin im Setup-Script läuft, ob die VM das (private) Harness-Repository holen darf, ob es auch in Sessions mit mehreren Repositories wirkt.
- Lieferweg C: Git-Submodul je Projekt. Die Hooks müssten trotzdem in .claude/settings.json stehen; pflegeintensiv, vorerst nicht verfolgt.

### Decided

- Der Plugin-Weg scheidet für die Cloud aus (wörtlich belegt). Offen bleibt nur, wie Skills, Hooks und Skripte sonst in die Session kommen.

### Open

- Vorschlag: Weg B zuerst mit einem Probelauf prüfen, weil er nur eine Kopie braucht; Weg A bleibt der Rückfall. Der Probelauf braucht ein Cloud-Environment mit einem Probe-Setup-Script und eine Session in einem Testrepository.
- Entscheidung des Besitzers: Weg B, Weg A oder beide.

## 2026-10-16 — Eingecheckte settings.json und Zugriff auf das Harness-Repository

### Discussed

- Frage des Besitzers: Statt .claude/settings.local.json eine eingecheckte .claude/settings.json verwenden, damit die Plugin-Einstellung in die Cloud kommt und lokal wie dort gleich ist. Stand heute: ezf-ui hat die Plugin-Einstellung in .claude/settings.local.json (nicht eingecheckt, absoluter Pfad auf das lokale Claude_Harness als Marketplace), Claude_Harness selbst in .claude/settings.json (eingecheckt, Pfad ./).
- Laut Doku käme die Datei mit dem Klon in die Cloud, aber enabledPlugins und extraKnownMarketplaces werden dort nicht ausgewertet; der absolute lokale Pfad existiert auf der VM auch nicht. Was eine eingecheckte settings.json in der Cloud wirklich trägt, sind Hooks und Berechtigungsregeln (nur in Sessions mit einem Repository). Die Idee trägt also für Hooks, nicht für das Plugin.
- Zugriff auf das Harness-Repository aus einer Cloud-Session in ezf-ui: Der GitHub-Proxy bedient nur Repositories, die der Session zugeordnet sind. Für andere gibt es 403, auch bei öffentlichen Repositories (Archiv-URLs). Einzelne Dateien öffentlicher Repositories bleiben über raw.githubusercontent.com erreichbar (Trusted-Liste). Ist das Harness-Repository als zweites Repository der Session zugeordnet, ist es les- und schreibbar (Push nur auf Branches). Dann lädt die Session aber keine Hooks aus den settings.json der Repositories; ob CLAUDE.md und .claude/skills der Repositories dann geladen werden, ist nicht dokumentiert.

### Open

- Probelauf (Weg B) um zwei Fragen erweitern: Darf das Setup-Script ein nicht zugeordnetes Repository (das Harness) klonen? Wirkt das Harness als zweites Repository der Session, und was davon wird dann automatisch geladen?

## 2026-10-16 — Probelauf für Weg B vorbereitet

### Discussed

- Probe-Setup-Script, Checkliste mit zwei Sitzungs-Prompts und ein Wegwerf-Zielprojekt liegen unter experiments/cloud-probe/ (setup.sh, README.md, target/). Sie prüfen: Klonen eines nicht zugeordneten Repositories im Setup-Script, Hooks und Skills unter ~/.claude der Maschine, claude plugin install im Setup-Script und den Harness als zweites Repository der Sitzung.
- Lokal geprüft: Syntax des Scripts, das Zusammenführen der settings.json (mit vorhandenen Hooks), der SessionStart-Hook gegen die Wegwerf-Config im Dateimodus; die 302 Implementierungstests laufen weiter grün. Nicht geprüft: alles, was nur in der Cloud geht.

### Open

- Der Besitzer legt das Wegwerf-Repository und das Probe-Environment an und führt Sitzung A und B aus; die Antworttabellen kommen zurück in die Sitzung.
- Der Stand von main auf GitHub liegt fünf Commits hinter dem lokalen main; für den Probelauf ohne Bedeutung.

## 2026-10-16 — Vorab-Test in der Cloud (Sitzung ohne zugeordnetes Repository)

### Discussed

- Ergebnis des Vorab-Tests vom 2026-10-16 (vom Besitzer eingefügt, Wortlaut der Cloud-Sitzung): Python 3.13.16; CLAUDE_CODE_REMOTE=true; CLAUDE_PROJECT_DIR leer; Benutzer root, HOME /root, Arbeitsverzeichnis /home/claude; claude-CLI 2.1.301 unter /opt/node22/bin/claude, claude plugin ist vorhanden. Damit sind die Grundvoraussetzungen für Weg B erfüllt: Python über 3.11 und die CLI auf der Maschine.
- git ls-remote und git clone des Harness-Repositories über https ohne Zugangsdaten scheitern mit could not read Username (Exit 128). Das Repository war der Sitzung nicht zugeordnet und für Claude noch nicht freigegeben, das Ergebnis ist deshalb erwartbar und trennt Nicht-Freigabe nicht von Nicht-Zuordnung. raw.githubusercontent.com: CONNECT-Tunnel mit 403 (der Proxy sperrt den Host in dieser Umgebung, obwohl die Doku ihn in der Trusted-Liste nennt; die Netzwerkstufe der Umgebung ist nicht geprüft).
- ~/.claude der Maschine enthält kein settings.json, aber Skills (Symlinks nach /mnt/skills/public, Ordner session-start-hook und synced) und die Dateien stop-hook-git-check.sh, stop-hook-reply-gate.py, user-prompt-submit-reply-reminder.py und launcher-settings.json. Die Plattform legt dort selbst Skills und Hook-Skripte ab. Das spricht dafür, dass Dateien unter ~/.claude der Maschine zum Betrieb gehören (Hinweis für Weg B, kein Beleg).
- Einschränkung: Die Sitzung sah wahrscheinlich nach einem Chat mit Code-Sandbox aus, nicht nach einer Code-Sitzung (Arbeitsverzeichnis /home/claude, kein geklontes Repository, Memory-Dateien und Preferences im Kontext). Q2, Q3 und Q5 (Wirkung von Hooks und Skills, zwei Repositories) sind damit nicht geprüft.

### Open

- Q1 bleibt offen: Ob ein nicht zugeordnetes, aber für Claude freigegebenes Repository im Setup-Script oder zur Laufzeit klonbar ist, zeigt erst ein Test nach der Freigabe (Claude-GitHub-App auf dem Konto von Claude_Harness mit Zugriff auf genau dieses Repository) in einer Code-Sitzung mit einem anderen zugeordneten Repository.
- Nachfragen in der vorhandenen Sitzung, die ohne Freigabe Aufschluss geben: /root/.ccr/README.md, Proxy-Status, launcher-settings.json (Werte geschwärzt), Skill session-start-hook, Aufrufzeile des claude-Prozesses (zeigt z. B. --settings).
