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

## 2026-10-16 — Test 1 und Test 2 in Code-Sitzungen (2026-10-16)

### Discussed

- Test 1 (Code-Sitzung, nur my_story_game zugeordnet): Arbeitsverzeichnis /home/user/my_story_game, die CLAUDE.md des Repositorys ist geladen (AGENTS.md und .harness/ liegen im Repository, werden aber nicht geladen). CLAUDE_CODE_REMOTE=true, CLAUDE_PROJECT_DIR leer (in der Shell des Werkzeugs). Skills kommen nur von der Plattform: session-start-hook unter ~/.claude/skills und 14 Skills aus dem Konto-Sync unter ~/.claude/skills/synced; das Repository hat keine eigenen Skills. Kein ~/.claude/settings.json; der claude-Prozess läuft über environment-manager im Remote-Modus.
- Test 1, Klon-Frage (Q1): git ls-remote und git clone von Claude_Harness über https scheitern mit could not read Username (Exit 128). Der Proxy hat nicht geblockt (keine Relay-Fehler, kein 403/407); git bekommt für nicht zugeordnete Repositories schlicht keine Zugangsdaten (credential.interactive=false, kein Credential-Helper, GitHub-Zugriff der Session laut Systemkontext auf my_story_game beschränkt). Das Repository war zwar für Claude freigegeben (in der Auswahl sichtbar), aber der Sitzung nicht zugeordnet. Antwort auf Q1 zur Laufzeit: nein. Für das Setup-Script nicht geprüft; laut Doku läuft der Agent-Proxy erst nach dem Setup-Script, ein Klon eines privaten Repositories dort ist deshalb unwahrscheinlich.
- Test 1, Plattform: Die Sitzung bietet die Werkzeuge list_repos und add_repo (Server claude-code-remote); add_repo ändert den Sitzungs-Scope. Nicht ausgeführt. Der README des Proxys (/root/.ccr/README.md) beschreibt nur Proxy, CA-Bundle und Git-Umschreibung (SSH nach HTTPS), nichts zu Hooks oder Plugins.
- Test 2 (Code-Sitzung, my_story_game und Claude_Harness zugeordnet): Beide Repositories liegen unter /home/user (Claude_Harness und my_story_game), das Arbeitsverzeichnis /home/user ist kein Repository. Die CLAUDE.md beider Repositories ist im Kontext (Q5: ja). Skills und Hooks der Repositories fehlen, wie erwartet: Claude_Harness hat kein .claude/skills, die Skills liegen in plugin/skills.
- Test 2, Lesen und Schreiben: python3 plugin/scripts/backlog.py docs/todo --index läuft im Harness-Klon, docs/todo/notes ist mit den fünf Dateien da, git remote und status funktionieren, git push --dry-run auf einen neuen Branch endet mit Exit 0. Der Harness-Klon steht auf einem Sitzungs-Branch claude/sharp-newton-2o6z8p ohne Upstream: Schreiben aus der Cloud landet auf claude/*-Branches, nicht auf main.
- Folgerung: Das Plugin selbst und seine Hooks gibt es in der Cloud nicht, aber Skills sind Markdown und Skripte sind Python 3.13 ohne Zusatzpakete. Ist der Harness der Sitzung zugeordnet, kann die KI die Skills im Klon lesen und befolgen und die Skripte direkt aufrufen. Das ist ein weiterer Weg: Weg D (Harness als zugeordnetes Repository, Regeln und Skripte aus dem Klon, Hinweis darauf in der CLAUDE.md des Zielprojekts, die in der Cloud geladen wird). Er braucht weder Setup-Script noch Kopie im Projekt, liefert aber keine Hooks (kein Sitzungsstart-Hinweis, keine Prüfungen am Turn-Ende) und der Platzhalter ${CLAUDE_PLUGIN_ROOT} in den Skilltexten muss die KI selbst durch den Klon-Pfad ersetzen.

### Open

- Test 3: Lässt sich der Harness in einer Sitzung mit nur einem Repository per add_repo nachträglich zuordnen (Zustimmung nötig? danach klonbar und lesbar)? Das beantwortet die Ausgangsfrage, in ezf-ui zu arbeiten und Daten aus dem Harness-Repository zu holen.
- Weg B (Setup-Script) ist mit privatem Harness-Repository unwahrscheinlich. Bleibt nur mit öffentlichem Repository, einem Token in den Umgebungsvariablen des Environments oder einem Paket über PyPI oder npm. Ob Hooks und Skills unter ~/.claude der Maschine in der Sitzung wirken (Q2, Q3), ist weiter ungeprüft; die Plattform legt dort selbst Skills und Hook-Skripte ab.
- Entscheidung des Besitzers: Weg A, Weg D oder Kombination (D für Regeln und Skripte, A nur für Hooks).

## 2026-10-16 — Test 3: add_repo und die Idee einer Sitzungskopie

### Discussed

- Test 3 (Code-Sitzung, nur my_story_game): list_repos nennt zehn Repositories, darunter ukf-hoppmann/Claude_Harness (privat, can_push true). add_repo (owner ukf-hoppmann, repo Claude_Harness) antwortet sofort mit status appended, ohne Rückfrage in der Sitzung; ob der Client einen Bestätigungsdialog zeigte, sah die Sitzung nicht. Damit ist die Ausgangsfrage beantwortet: Ein Harness-Repository lässt sich während einer Sitzung zuordnen, auch wenn es beim Start fehlte.
- add_repo klont nicht selbst. Die Antwort verlangt einen einmaligen git clone --depth 1 nach /home/user/claude_harness (Kleinschreibung, nicht Claude_Harness; auf Linux ein anderer Pfad) mit großzügigem Timeout, höchstens zwei gleichzeitige Git-Vorgänge je Repository (sonst 429) und danach den Aufruf des Werkzeugs register_repo_root mit owner, repo und dem Klon-Pfad. Laut Antwort lädt die Sitzung dann ab dem nächsten Turn CLAUDE.md, Skills und Plugins des Repositories. Beides wurde in Test 3 nicht ausgeführt.
- Hinweis zu den Pfaden: Die Prompts des Besitzers nutzten /home/user/Claude_Harness mit großem C; das war ein Fehler des Prompts, nicht des Werkzeugs.
- Idee des Besitzers: Beim Sitzungsstart eine Kopie des Harness im Zielprojekt erzeugen, damit die Hooks wiederkommen, und sie danach löschen, um das Repository sauber zu halten. Bewertung: Hooks werden nach dem Verhalten von Claude Code beim Start der Sitzung eingelesen, eine Kopie, die erst während der Sitzung entsteht, aktiviert sie nicht (in der Cloud nicht getestet). Ein SessionStart-Hook im Zielprojekt, der kopieren würde, wird in Sitzungen mit zwei Repositories laut Doku nicht geladen. Das Setup-Script läuft vor dem Start und wird gecacht, taugt also nicht für eine Kopie, die vom jeweiligen Repository abhängt. Löschen ist unnötig: Die Cloud-Maschine ist je Sitzung frisch; die Kopie genügt unversioniert zu bleiben (Eintrag in .git/info/exclude, lokal und nicht im Repository). Außerdem schreibt ein Hook nach Architekturregel 5 nicht in das Projekt.

### Open

- Test 4: Harness klonen und register_repo_root aufrufen, dann prüfen, ob ab dem nächsten Turn die Skills claude-harness:* und das Plugin samt Hooks in der Sitzung sind. Wenn ja, ersetzt das Weg A und Weg D, ohne Kopie. Offen wäre dann, ob die Hooks das richtige Projekt finden, wenn das Arbeitsverzeichnis /home/user ist.

## 2026-10-16 — Test 4: register_repo_root lädt das Plugin nicht

### Discussed

- Test 4 (Code-Sitzung mit my_story_game, Harness per add_repo nachträglich zugeordnet): git clone --depth 1 nach /home/user/claude_harness gelang im ersten Versuch, HEAD war 7c40d0c, also der zuletzt gepushte Stand von main; register_repo_root antwortete context_reload_requested.
- Nach dem Neuladen war die CLAUDE.md des Harness-Repositories im Kontext (zusätzlich zu der von my_story_game). Das Plugin war nicht aktiv: keine Skills claude-harness:*, claude plugin list meldet keine Plugins, keine Hook-Meldung, kein Sitzungsstart-Hinweis. .claude/ im Harness-Repository enthält nur settings.json mit enabledPlugins und dem Directory-Marketplace ./. Das bestätigt die Doku: Plugins aus der settings.json eines Repositories werden in der Cloud nicht installiert, auch nicht über register_repo_root. Vermutung der Sitzung, nicht getestet: settings.json greift nur, wenn das Arbeitsverzeichnis im Repository liegt (hier /home/user).
- Das rohe SKILL.md von todo enthält ${CLAUDE_PLUGIN_ROOT} dreimal als Platzhalter (Zeilen 19, 33, 45). Beim Laden als Plugin wird er ersetzt; lesen wir die Datei aus dem Klon, muss der Platzhalter durch /home/user/claude_harness/plugin ersetzt werden.
- Folgerung: Die Plugin-Route über register_repo_root ist erledigt (nein). Offen ist, ob register_repo_root Skills aus .claude/skills des registrierten Repositories lädt (so sagt es die Antwort von add_repo) und ob Hooks aus dessen .claude/settings.json zur Sitzung kommen. Läden Skills dort, könnte das Harness-Repository seine Skills als erzeugten Export unter .claude/skills bereithalten (Weg E: eine Stelle, keine Kopie je Projekt; Namen ohne Präfix claude-harness:, Platzhalter beim Export ersetzt).

### Open

- Test 5: In dem Klon lokale, unversionierte Testdateien anlegen (.claude/skills/probe-skill/SKILL.md und einen Marker-Hook in .claude/settings.json), register_repo_root erneut aufrufen und prüfen, ob der Skill erscheint und der Hook feuert.

## 2026-10-16 — Test 5: Skills über register_repo_root ja, Hooks nein

### Discussed

- Test 5 (gleiche Sitzung): Ein lokaler, unversionierter Skill unter /home/user/claude_harness/.claude/skills/probe-skill/ wurde nach register_repo_root im nächsten Turn in der Skill-Liste geführt (ohne Präfix, Basisverzeichnis im Klon) und war ladbar (Probewort ORANGER-FALKE-7). Die Meldung zum Turnbeginn lautete Additional working directories added: /home/user/claude_harness: register_repo_root fügt das Verzeichnis als zusätzliches Arbeitsverzeichnis hinzu.
- Ein in dessen .claude/settings.json nachträglich eingetragener Stop-Hook feuerte nicht (/tmp/hook-probe.log fehlt, keine Hook-Meldung im Kontext). Der SessionStart-Hook sagt nichts aus, weil die Einstellung erst nach dem Sitzungsstart entstand. Die Einstellung wurde zudem erst während der Sitzung geändert; ausgeschlossen ist ein Laden beim Start damit nicht, ein Laden aus zusätzlichen Arbeitsverzeichnissen aber unwahrscheinlich und gegenüber der Doku (Hooks nur aus dem Projekt-Verzeichnis, nicht bei mehreren Repositories) erwartbar.
- Zwischenstand der Wege: Plugin in der Cloud: nein. Skills: ja, aus .claude/skills eines zugeordneten und registrierten Repositories (Namen ohne Präfix; gleiche Namen wie eingebaute Skills wie init müssten beim Export vermieden werden, z. B. durch ein Präfix). Hooks aus der settings.json eines zugeordneten Repositories: nein. Offen: Hooks auf Ebene des Environments oder der Maschine (Q2).
- Möglicher Weg F: Weg E für die Skills (Harness-Repository liefert einen erzeugten Export unter .claude/skills mit ersetztem Pfadplatzhalter) und kleine, statische Hooks in ~/.claude/settings.json der Maschine, die ein Setup-Script des Environments schreibt, ohne Geheimnis und ohne Klon. Die Hooks rufen die Skripte im Klon des Harness auf, wenn er vorhanden ist (Pfade /home/user/Claude_Harness oder /home/user/claude_harness, je nachdem wie er zugeordnet wurde), und tun sonst nichts. Voraussetzung ist, dass Hooks in ~/.claude/settings.json der Cloud-Maschine geladen werden; ungetestet. Zusätzlich müssten die Hooks das richtige Projekt finden, wenn das Arbeitsverzeichnis /home/user ist.

### Open

- Test 6: Setup-Script mit Marker-Hooks in ~/.claude/settings.json (ohne Klon) in einem eigenen Environment: Feuern Stop- und SessionStart-Hook in einer Sitzung mit einem und mit zwei Repositories?
- Test 6b: Werden Skills unter .claude/skills eines beim Start ausgewählten zweiten Repositories (statt per add_repo) geladen, und wo liegt es (Groß- oder Kleinschreibung des Pfads)?
- Entscheidung des Besitzers über die Richtung: Weg E ohne Hooks, Weg F mit Environment-Hooks oder Weg A.

## 2026-10-16 — Beschluss: Weg A, Kopie im Projekt

### Discussed

- Der Besitzer fragte, ob sich alle weiteren Tests sparen lassen, wenn der Harness als Kopie in die Projekte kommt und mit eingecheckt wird. Antwort: Die Probeläufe (Weg B, Environment-Hooks, Skills bei Start-Auswahl) entfallen, weil Weg A nur Repository-Inhalt nutzt, den die Doku als geladen nennt. Es bleibt ein Abnahmelauf nach dem Bau.
- Hinweise zur Umsetzung: Nur plugin/ kopieren, nicht das Harness-Repository (sonst gelangen dessen Backlog, Notes und Tagesberichte in jedes Projekt). Kein Git-Submodul (die Cloud gibt für nicht zugeordnete private Repositories keine Zugangsdaten). Lokal lädt auch die Kopie mit: Hooks müssten sich dort still beenden, Skills brauchen ein Präfix (schon wegen des eingebauten init). Hooks laufen nur in Sessions mit einem Repository. In der Shell der Cloud-Session ist CLAUDE_PROJECT_DIR leer, Skilltexte brauchen deshalb Pfade relativ zum Projekt. Die Config und .claude-harness/ müssen eingecheckt sein; der Vorschlag von init (Schritt 11), .claude-harness/ in die .gitignore zu nehmen, widerspricht dem bei Projekten mit Cloud-Kopie.
- Der Besitzer legt fest, dass /claude-harness:init und /claude-harness:update die Kopie in .claude oder .claude-harness anlegen und aktualisieren.

### Decided

- Weg A (Besitzer, 2026-10-16): Der Harness liegt als erzeugte, eingecheckte Kopie im Projekt. /claude-harness:init legt sie an, /claude-harness:update hält sie aktuell. Ziel, Abnahmekriterien und Summary der Story sind entsprechend neu gefasst, die Probeläufe entfallen. Der Ordner experiments/cloud-probe kann nach dem Abnahmelauf entfernt werden.

### Open

- Plan und Zerlegung in Tasks stehen zur Freigabe an: Generator, Hook-Einträge mit Cloud-Wächter, Versionsvermerk, Config-Schlüssel, init- und update-Schritte, Doku, Abnahmelauf.

## 2026-10-16 — Anforderung: Rückführbarkeit

### Discussed

- Der Besitzer verlangt, dass sich die Kopie einfach wieder auf den aktuellen Stand zurückführen lässt, weil er hofft, künftig wieder lokal zu arbeiten.

### Decided

- Kriterium 8 neu: vollständiger, nachvollziehbarer Rückbau der Kopie. Umsetzung im Plan: Manifest mit allen erzeugten Dateien, Hashes und Hook-Einträgen unter .claude-harness/runtime/manifest.json; cloud_export.py --remove mit Vorschau und Freigabe; von Hand geänderte Dateien bleiben stehen und werden gemeldet; fremde Einträge in .claude/settings.json bleiben; eine Rundreise-Prüfung (Export, dann Rückbau ergibt den Ausgangsstand). Zusätzlich: Die Kopie wird in einem eigenen Commit eingecheckt, damit auch ein git revert genügt. Ist cloud.export auf false, aber das Manifest noch da, meldet der Sitzungsstart und update die Reste und bietet den Rückbau an.

### Open

- Plan mit dem neuen Abschnitt Rückbau steht zur Freigabe an.

## 2026-10-16 — Plan freigegeben, Umsetzung im Worktree gestartet

### Discussed

- Plan mit neun Abschnitten freigegeben (Skill-Export, Hook-Einträge, Export mit Manifest, Rückbau, Config cloud.export, Sitzungsstart-Zeile, Skills init und update, Doku, Integration). Der Besitzer akzeptiert die doppelten Skill-Beschreibungen lokal.

### Decided

- Umsetzung im Worktree worktree-story-047-cloud-kopie, Basis main (7c40d0c). Die uncommittete README-Änderung des Besitzers bleibt im Hauptcheckout und kommt nicht mit.

### Open

- Abnahmelauf in der Cloud (Kriterium 7) durch den Besitzer nach dem Merge.
