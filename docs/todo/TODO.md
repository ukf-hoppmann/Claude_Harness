# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 2. The rules are defined in
`docs/techdocs/interfaces.md` of the ToDo Viewer.

## Work items

- `EPIC-008` **Backlog über die API des ToDo-Viewers**
  - Uid: 6da1ed5f-d947-48b4-b198-8bd2e96ef709.
  - Type: Epic.
  - Status: In progress.
  - Created: 2026-09-28.
  - Area: Konfiguration.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Agenten pflegen Backlogs standardmäßig über die HTTP-API des
    ToDo-Viewers statt die Markdown-Dateien direkt zu schreiben; der direkte
    Dateizugriff bleibt als wählbarer Modus und als Rückfall erhalten. Das
    Backlog-Format in `format.md` ist verbindlich, der Viewer setzt es um.
  - Completion criteria: Alle Pflicht-Stories sind abgeschlossen; ein
    Projekt mit Standard-Config arbeitet über die API, ein Projekt mit
    `backend = "files"` wie bisher; ist der Server nicht erreichbar, weist
    der Agent darauf hin und fragt, wie er vorgehen soll.
  - Summary: Der Backlog wird künftig über den ToDo-Viewer gepflegt. Der
    Server prüft Format und Regeln und vergibt IDs; direkter Dateizugriff
    bleibt als Rückfall.

- `STORY-050` **Skills auf den MCP-Server des ToDo-Viewers umstellen**
  - Uid: 4846f8a8-2123-46a5-b63f-8fe463446f92.
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-10-19.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: `STORY-049`.
  - Goal: Claude arbeitet im API-Modus über die MCP-Tools des Viewers an
    Backlog, Notes und Weckern, sobald der MCP-Server im Viewer überarbeitet
    ist. Das Projekt gibt Claude dabei nicht selbst an: Ein PreToolUse-Hook
    des Harness setzt das eigene Projekt deterministisch ein und fragt bei
    einem fremden Projekt nach.
  - Completion criteria: Das Plugin bringt eine .mcp.json mit
    http://localhost:5411/mcp mit; ein PreToolUse-Hook setzt das eigene
    Projekt ein (aus Config und Hauptarbeitskopie) und fragt bei fremdem
    Projekt nach; der Session-Start meldet Projekt und Erreichbarkeit des
    Viewers; die Skills todo und notes beschreiben die Tools, die Helfer
    bleiben als Rückfall; Lese-Tools lassen sich über init/update in den
    Projekt-Settings freigeben; Lese-, Schreib- und Notizfluss sind über MCP
    gegen den laufenden Viewer geprüft.
  - Summary: Spätere Umstellung von den Helfer-Skripten auf die nativen
    MCP-Tools des Viewers. Sie wartet auf STORY-049 und auf den Umbau des
    MCP-Servers im ToDo-Viewer.

- `EPIC-010` **Weg von der Claude-Code-App: Harness und ToDo-Viewer über claude.ai nutzen**
  - Uid: 0bb9fc23-a57b-4616-b5b1-3cf7f0d8b9e9.
  - Type: Epic.
  - Status: In progress.
  - Created: 2026-10-14.
  - Area: Architektur.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Der Claude_Harness ist auch in Cloud-Sessions auf claude.ai/code
    nutzbar, z. B. bei der Arbeit an ezf-ui, ohne die
    Claude-Code-Desktop-App. Lokal arbeitet der Harness mit Backlog und
    Notes über die API des ToDo-Viewers, in der Cloud über die
    Markdown-Dateien im Repository. Beide Seiten bleiben über den Sync des
    ToDo-Viewers (Git und Spiegel-Ordner) im Gleichstand.
  - Completion criteria: 1. Geklärt und dokumentiert, wie Skill, Hooks und
    Skripte des Harness in einer Cloud-Session eines Fremdprojekts (z. B.
    ezf-ui) verfügbar sind; das Plugin selbst wird dort nicht geladen. 2.
    Lokal gilt die API, in der Cloud der Dateimodus für Backlog und Notes;
    die Umschaltung braucht keine Änderung der eingecheckten Config. 3. Der
    Abgleich zwischen den Cloud-Dateien und der lokalen Datenbank ist
    beschrieben und läuft ohne Verlust, auch bei gleichzeitiger Arbeit auf
    beiden Seiten und bei gleichen IDs. 4. Ein Fremdprojekt läuft in einer
    claude.ai-Session mit Harness, Backlog und Notes nachweislich durch, und
    der Stand ist danach lokal im Viewer.
  - Summary: Lokal bleibt die API des ToDo-Viewers, in der Cloud arbeitet
    der Harness mit den Markdown-Dateien im Repository; beide Seiten bleiben
    über den Sync im Gleichstand. Offen: wie der Harness dort ohne Plugin
    läuft.

- `STORY-052` **Branch-Stand beim Start einer Cloud-Session mit origin abgleichen**
  - Uid: 3b72b84e-cf3a-43f0-b071-d6d79331e4f1.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: In progress.
  - Created: 2026-11-04.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Eine Cloud-Session eines Projekts mit cloud.export arbeitet nicht
    unbemerkt auf einem veralteten Branch-Stand. Beim Start holt der
    Session-Start den aktuellen Branch von origin, spult bei sauberem Stand
    vor und meldet sonst in einer Zeile, wie weit der Stand abweicht und
    welcher Befehl passt. Er überschreibt nie etwas.
  - Completion criteria: 1. Ein Skript plugin/scripts/cloud_sync.py holt
    beim Start einer Cloud-Session (CLAUDE_CODE_REMOTE=true, Quelle startup)
    nur den aktuellen Branch von origin, ohne --unshallow und mit Zeitlimit,
    und läuft als erster Schritt von session_start.py, damit dessen Hinweise
    den neuen Stand sehen. Lokal tut es nichts.
    2. Bei sauberem Arbeitsbaum und HEAD als Vorfahr von origin spult es per
    git merge --ff-only vor und meldet das in einer Zeile; bei gleichem
    Stand oder nur lokal vorausliegenden Commits schweigt es.
    3. Bei unsauberem Arbeitsbaum, beidseitigen Commits, fehlendem
    gemeinsamem Vorfahren (Shallow Clone, Force-Push) oder gescheitertem
    Fetch ändert es nichts und meldet eine Zeile mit Abweichung (Zahl der
    Commits oder Hash und Datum beider Stände) und passendem Befehl; git
    reset --hard nur nach Rückfrage beim Nutzer.
    4. Die Konfiguration cloud.sync (Boolean, Standard true) schaltet den
    Abgleich ab; geprüft in harness_config.py, dokumentiert in
    configuration.md, getestet in test_config.py.
    5. architecture.md enthält die freigegebene, auf Cloud-Sessions
    begrenzte Ausnahme von Regel 2 (Netz) und Regel 5 (Schreiben ins
    Projekt).
    6. Unit-Tests mit einem lokalen Bare-Repo als origin decken alle Fälle
    aus 2 und 3 ab, dazu Zeitlimit und lokale Session; Techdocs
    (interfaces.md, configuration.md) beschreiben das Verhalten.
    7. Ein Lauf in einer echten Cloud-Session eines Projekts mit
    aktualisierter Kopie zeigt den Abgleich oder die Meldung.
  - Summary: Cloud-Sessions starteten auf einem veralteten, gecachten
    Branch-Stand, ohne dass es jemand merkte. Künftig holt der Session-Start
    den Branch von origin, aktualisiert ihn, wenn das gefahrlos geht, und
    meldet sonst die Abweichung.

- `EPIC-011` **Hierarchische Architektur- und Schnittstellen-Doku für die AI**
  - Uid: 37382d27-0b2a-4d59-b52f-4401524a99b2.
  - Type: Epic.
  - Status: Open.
  - Created: 2026-11-05.
  - Area: Architektur.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Projekte können ihre verbindlichen Regeln für die AI (development)
    als Baum führen: Architektur sagt, was wohin gehört und was Pflicht ist;
    eine Schnittstellen-Doku mit Katalog wiederverwendbarer Bausteine sagt,
    wie es geht. Der Harness stellt sicher, dass die AI die passenden
    Dokumente liest (Pflicht über Pfade und über Nutzung), dass Verweise
    gültig bleiben und dass bei Änderungen an öffentlichen APIs an die
    Pflege erinnert wird. Bestehende Projekte mit flachen Scopes
    funktionieren unverändert.
  - Completion criteria: 1. Scopes können in Unterordnern liegen
    (STORY-053).
    2. Scopes können Pflichtlektüre außerhalb der Architektur nennen, der
    Hook erzwingt sie (STORY-054).
    3. Tote relative Links in development- und techdocs-Dateien werden
    gemeldet (STORY-055).
    4. Änderungen an konfigurierten öffentlichen API-Dateien lösen eine
    Pflege-Erinnerung aus (STORY-056).
    5. Nutzung bestimmter Bezeichner erzwingt das Lesen der zugehörigen Doku
    (STORY-057).
    6. Vorlagen und Skills beschreiben den Aufbau; Projekte ohne die neuen
    Teile laufen unverändert (STORY-058).
  - Summary: Aus ezf-ui kam der Wunsch, Architektur und Schnittstellen nicht
    in großen Einzeldateien, sondern als Baum zu führen, und
    sicherzustellen, dass die AI die passenden Teile liest und vorhandene
    Bausteine wiederverwendet. Das Epic baut die nötigen Mechanismen in den
    Harness: Scopes in Unterordnern, Pflichtlektüre, Linkprüfung,
    Pflege-Erinnerung, Pflicht über Nutzung, Vorlagen und Skills.

- `STORY-053` **Architektur-Scopes in Unterordnern**
  - Uid: 49348b4e-d877-4cbc-813c-8d068de5a3da.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-11-05.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Scope-Namen dürfen Unterordner enthalten (z. B. plugins/patient →
    architecture/plugins/patient.md). Hook, Lese-Markierung, geerbte Regeln
    und Sitzungsstart kommen damit zurecht; flache Scopes funktionieren
    unverändert.
  - Completion criteria: 1. Ein Scope-Name besteht aus Segmenten
    [a-z0-9]+(-[a-z0-9]+)*, getrennt durch /; die Datei ist
    architecture/<Name>.md. Ein Scope plugins und ein Scope plugins/patient
    können nebeneinander bestehen.
    2. Ein vollständiger Read einer Scope-Datei in einem Unterordner wird
    als gelesen markiert; der Hook verlangt sie wie flache Scopes.
    3. ## Inherited rules akzeptiert solche Scope-Namen.
    4. Unit-Tests decken Namen, Pfade, Markierung und Vererbung ab;
    bestehende Tests laufen unverändert.
    5. Skill architecture, Vorlage architecture.md und die Techdocs des
    Harness beschreiben das Namensschema.
  - Summary: Scopes der Architektur können künftig in Unterordnern liegen,
    damit große Projekte ihre Regeln nach Bereichen und Teilen ordnen
    können.

- `STORY-054` **Pflichtlektüre je Scope**
  - Uid: 9754a82d-0d7e-472f-b8e2-a711e50332ab.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-11-05.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `STORY-053`.
  - Goal: Ein Scope kann in einer optionalen Spalte Required reading weitere
    Dateien nennen (z. B. seine Schnittstellen-Doku). Wer eine Datei in den
    Pfaden des Scopes ändert, muss sie vorher vollständig gelesen haben; der
    Hook erzwingt das wie bei den Scopes selbst.
  - Completion criteria: 1. Die Scope-Tabelle hat optional die Spalte
    Required reading; sie wird über die Kopfzeile erkannt, Tabellen mit drei
    Spalten gelten unverändert.
    2. Einträge sind Dateipfade relativ zum Projekt-Root in Backticks;
    fehlende Dateien oder ungültige Pfade meldet der Sitzungsstart als
    Tabellenfehler.
    3. Der Hook verlangt vor der ersten Änderung einer Datei die
    Pflichtlektüre aller passenden Scopes, auch geerbter Scopes, und nennt
    fehlende Dateien beim Namen.
    4. Vollständige Reads dieser Dateien werden markiert.
    5. Unit-Tests decken altes und neues Tabellenformat, Hook, Markierung
    und Vererbung ab; Skill, Vorlage und Techdocs des Harness beschreiben
    die Spalte.
  - Summary: Ein Bereich der Architektur kann künftig weitere
    Pflichtdokumente nennen, etwa seine Schnittstellen-Doku, und der Harness
    sorgt dafür, dass sie vor Änderungen gelesen werden.

- `STORY-056` **Pflege-Erinnerung bei Änderungen an öffentlichen APIs**
  - Uid: 294b00b7-5b95-4b5b-8f26-abf5c6633557.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-11-05.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Ein Projekt kann in [development].public_api Muster für die
    Dateien seiner öffentlichen APIs nennen. Wird eine passende Datei
    geändert, erinnert ein Hook einmal je Session daran, Zuständigkeiten,
    Katalog, Schnittstellen-Doku und Verweise zu prüfen.
  - Completion criteria: 1. [development].public_api ist eine Liste von
    Mustern relativ zum Projekt-Root (Syntax wie Scope-Pfade), Standard
    leer; geprüft in harness_config.py, in der Config-Vorlage, nachgezogen
    von config_update.py, dokumentiert in configuration.md, getestet in
    test_config.py.
    2. Eine Änderung an einer passenden Datei per Write/Edit wird je Projekt
    vermerkt; am Ende des Turns erinnert der Hook einmal je Session und
    Projekt, mit Verweis auf skill claude-harness:architecture.
    3. Ohne Muster, bei abgeschaltetem Teil architecture oder ungültiger
    Config tut der Hook nichts.
    4. Unit-Tests decken Config, Markierung und Erinnerung ab; Techdocs des
    Harness beschreiben sie.
  - Summary: Ändert sich eine öffentliche Schnittstelle eines Projekts,
    erinnert der Harness daran, die Architektur, den Baustein-Katalog und
    die Schnittstellen-Doku nachzuziehen.

- `STORY-055` **Tote Verweise in Architektur- und Doku-Dateien melden**
  - Uid: 5c30c318-d0a8-4b84-a1df-5d5cc56eb171.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-11-05.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Relative Markdown-Links (optional mit #anker) in den Dokumenten
    von development und techdocs werden geprüft. Tote Links meldet der
    Sitzungsstart; am Ende eines Turns werden tote Links in in dieser
    Session geänderten Dokumenten gemeldet.
  - Completion criteria: 1. Ein gemeinsamer Helfer
    plugin/scripts/doclinks.py findet relative Markdown-Links außerhalb von
    Code und prüft Ziel-Datei und Anker (Slug wie GitHub).
    2. Geprüft werden README.md und Dateien unter techdocs.path (wenn
    techdocs aktiv) sowie unter development.path (wenn der Teil architecture
    aktiv ist); externe Links werden ignoriert, Ziele außerhalb des Projekts
    sind Fehler.
    3. Der Sitzungsstart meldet tote Links je Projekt in der üblichen
    gekürzten Form.
    4. Ein Stop-Hook meldet tote Links in Dokumenten, die in dieser Session
    geändert wurden, und schweigt bei stop_hook_active.
    5. Unit-Tests decken Linkformen, Anker inkl. Umlaute und Duplikate,
    Code-Blöcke und Hook ab; Techdocs des Harness beschreiben die Prüfung.
  - Summary: Verweise zwischen Dokumenten sollen nicht unbemerkt ins Leere
    zeigen: Der Harness prüft sie beim Sitzungsstart und nach Änderungen.

- `STORY-058` **Schnittstellen-Doku, Vorlagen und Skill-Regeln für den Doku-Baum**
  - Uid: 9733d627-cae7-47e2-81dd-ea8dfe5342d0.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-11-05.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: `STORY-053`, `STORY-054`, `STORY-055`, `STORY-056`,
    `STORY-057`.
  - Goal: development bekommt neben der Architektur eine Schnittstellen-Doku
    für die AI (interfaces.md als Index plus interfaces/**, mit Katalog
    wiederverwendbarer Bausteine). Vorlagen und Skills beschreiben den
    ganzen Aufbau; die Zielgruppen von development (AI, Englisch) und
    techdocs (Menschen) sind überall klar benannt.
  - Completion criteria: 1. Neue Vorlagen unter
    plugin/templates/development/: Bereichs-Scope mit Tabelle der
    Zuständigkeiten, Index interfaces.md, einzelne Schnittstelle, Katalog;
    die Vorlage architecture.md zeigt Required reading, Unterordner-Scopes
    und Links.
    2. Neuer Skill claude-harness:interfaces mit den Regeln für die
    Schnittstellen-Doku; der Sitzungsstart nennt ihn bei aktivem Teil
    architecture.
    3. Skill architecture: Pflichtlektüre gegen Nachschlagen, Architektur
    ohne Wie, Pflichtdateien kurz, höchstens zwei Ebenen.
    4. Skill decomposition: vor neuen Bausteinen Kataloge prüfen; was
    mehrere Besitzer brauchen, in die geteilte Schicht.
    5. Skill techdocs und Sitzungsstart nennen die Zielgruppe (techdocs für
    Menschen, development für die AI).
    6. Cloud-Export überträgt neue Vorlagen und Skill; Techdocs des Harness
    und Tests sind nachgezogen.
  - Summary: Die Mechanismen des Epics bekommen Vorlagen und Regeln, damit
    Projekte ihre AI-Doku als Baum mit Katalog aufbauen können und klar ist,
    welche Doku für die AI und welche für Menschen ist.

- `STORY-057` **Pflichtlektüre bei Nutzung bestimmter Bezeichner**
  - Uid: e744462d-cc77-4222-b1be-40ab8ce00aca.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-11-05.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `STORY-054`.
  - Goal: Architektur und Scopes können festlegen, dass beim Schreiben von
    Code mit bestimmten Bezeichnern (z. B. reportError, modals.alert) eine
    Doku-Datei gelesen sein muss. Der Hook prüft den neuen Text von
    Write/Edit und blockiert, bis die Datei vollständig gelesen wurde.
  - Completion criteria: 1. Ein Abschnitt ## Required on use mit Tabelle |
    Uses | Read | ist in architecture.md (gilt für alle Projektdateien) und
    in Scope-Dateien (gilt für die Pfade des Scopes) möglich; Uses sind
    Bezeichner in Backticks, Read sind Dateien relativ zum Projekt-Root.
    2. Der Hook prüft den neuen Inhalt von Write, Edit, MultiEdit und
    NotebookEdit auf die Bezeichner (Wortgrenzen) und verlangt die
    zugehörigen Dateien; die Meldung nennt Bezeichner und Datei.
    3. Vollständige Reads dieser Dateien werden markiert; geerbte Scopes
    wirken mit.
    4. Fehler in den Tabellen meldet der Sitzungsstart.
    5. Unit-Tests decken Parsing, Treffer und Nicht-Treffer, Hook und
    Vererbung ab; Skill, Vorlagen und Techdocs des Harness beschreiben den
    Abschnitt.
  - Summary: Wer im Code eine bestimmte Funktion benutzt, etwa die
    Fehlermeldung des Core, muss vorher deren Doku gelesen haben. So werden
    festgelegte Lösungen nicht aus Versehen anders gebaut.

- `STORY-059` **Techdocs als Zusammenfassung der development-Doku**
  - Uid: af537863-8cbf-4786-879c-1a3eff58b8a9.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: No.
  - Status: Open.
  - Created: 2026-11-05.
  - Area: Dokumentation.
  - Priority: Prospective.
  - Dependencies: `STORY-058`.
  - Goal: Die Techdocs (für Menschen) fassen die verbindliche
    development-Doku zusammen und verweisen darauf, statt sie zu
    duplizieren. Skill techdocs und Vorlagen sagen, wie.
  - Completion criteria: 1. Skill techdocs regelt, wann Techdocs
    zusammenfassen und auf development verweisen statt zu duplizieren.
    2. Vorlagen der Techdocs sind angepasst.
    3. Die Techdocs dieses Repos sind nach der Regel überarbeitet.
  - Summary: Später: Die Doku für Menschen soll die Doku für die AI
    zusammenfassen und darauf verweisen, statt sie doppelt zu führen.
