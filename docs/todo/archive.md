# Project Backlog Archive

Completed and rejected work items, moved unchanged from `TODO.md` after the
project owner's decision.

Format: Claude_Harness backlog format version 2. The rules are defined in
`docs/techdocs/interfaces.md` of the ToDo Viewer.

## Work items

- `STORY-026` **Abschnitte an Subagenten übergeben**
  - Uid: 015f0224-81db-43e5-b3c7-be07aba87287.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: No.
  - Status: Rejected.
  - Created: 2026-09-24.
  - Area: Entwicklung.
  - Priority: Prospective.
  - Dependencies: `STORY-004`.
  - Goal: Prüfen, ob und wie Plan-Abschnitte an einen Subagenten mit
    günstigerem Modell übergeben werden: eigener Agent im Plugin, Auftrag
    aus dem Abschnitts-Vertrag samt nötiger Architekturregeln, Rückmeldung
    in festem Format, Kontrolle jedes Abschnitts durch die Hauptsession,
    Verhalten der Hooks im Subagenten und eine Schwelle, ab wann sich die
    Übergabe lohnt.
  - Completion criteria: Es ist entschieden, ob Abschnitte übergeben werden.
    Falls ja, wurde mindestens ein Abschnitt eines realen Features von einem
    Subagenten ohne Rückfrage korrekt umgesetzt und von der Hauptsession
    geprüft.
  - Resolution: Rejected by the project owner on 2026-09-25 — kein konkreter
    Bedarf, Priorität Prospective; bei spürbarem Kostendruck bei großen
    Plänen neu aufsetzen.

- `TASK-004` **Scope-Tracking für den Change**
  - Uid: 05c56678-35aa-40ce-b67d-df57a397769d.
  - Type: Task.
  - Parent: `STORY-022`.
  - Required for parent: No.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Important.
  - Dependencies: `TASK-003`.
  - Goal: Festhalten, welche Dateien/Pfade zu einem Change gehören, damit
    Merge und Cleanup nachvollziehbar nur diesen Umfang betreffen.
  - Completion criteria: Nach einem Change lässt sich ohne Rückfrage sagen,
    welche Pfade dazugehörten und welche nicht.
  - Resolution: Rejected by the project owner on 2026-09-24: folded into the
    spec of `STORY-022`; the native worktree tools cover the rest.

- `STORY-031` **Backlog-Format an den ToDo-Viewer angleichen**
  - Uid: 07344749-7bf9-44fa-832f-9ec72b9c1b33.
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-28.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: None.
  - Goal: `format.md` und `backlog.py` kennen das Feld `Deleted`
    (Papierkorb), akzeptieren nur `No entries.` als Leer-Markierung,
    erlauben das Ablehnen eines Epics ohne Pflichtkind und melden Verweise
    auf unbekannte IDs.
  - Completion criteria: `Deleted`-Einträge in `archive.md` werden von der
    Archiv-Statusregel und den Parent-Regeln ausgenommen und im Index
    markiert; `Keine Einträge.` wird als Fehler gemeldet; ein leeres Epic
    mit `Rejected` ist kein Fehler; `Parent`/`Dependencies` auf unbekannte
    IDs sind Fehler; `format.md` beschreibt `Deleted` und das
    Wiederherstellen; Tests in `tests/test_backlog.py` decken alle Punkte
    ab.
  - Resolution: Vom Projektverantwortlichen am 2026-09-28 bestätigt.

- `STORY-027` **Harness pro Teilprojekt**
  - Uid: 079fe702-e048-4b68-887d-bfeb6b2befb0.
  - Type: Story.
  - Parent: `EPIC-001`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Ein Repository kann mehrere Teilprojekte mit je eigener
    Harness-Konfiguration, Doku, Backlog und Architekturregeln enthalten (z.
    B. Plugin-Core im Root, jedes Plugin in seinem Ordner). Startet die
    Session im Teilprojekt, liegt im Repo-Root keine Harness-Datei. Beim
    Start im Root legt eine optionale, minimale Registry fest, welche
    Konfiguration für welche Datei gilt. Hooks, Daily Reports und der
    Worktree-Workflow arbeiten korrekt, wenn Teilprojekt-Root und Git-Root
    verschieden sind.
  - Completion criteria: In einem Test-Repo mit Root-Projekt und zwei
    Plugin-Teilprojekten gilt beim Bearbeiten einer Datei nachweislich die
    Konfiguration ihres Teilprojekts, sowohl beim Start im Teilprojekt als
    auch beim Start im Root mit Registry. Ein Daily Report im Teilprojekt
    enthält nur dessen Änderungen. Tests decken beides ab.
  - Summary: Der Harness soll in einem gemeinsamen Repo nur für einzelne
    Teile gelten können, z. B. für ein einzelnes Plugin, mit eigener Doku
    und eigenen Regeln, ohne dass Kollegen im Repo-Root etwas davon sehen.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-028` **Keine hartkodierten Pfade/Config-Werte im Code**
  - Uid: 08853fab-9e54-4076-a88b-f079bff931bb.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Eine Regel festlegen, dass Pfade und Verweise auf Configs,
    Datenbanken o. Ä. nicht fest im Code stehen, sondern über eine Config
    änderbar sind, da sie sich zwischen Umgebungen typischerweise
    unterscheiden. Fälle, in denen ein Pfad/eine URL bewusst fix im Code
    stehen soll, bleiben als benannte Ausnahme möglich.
  - Completion criteria: Die Regel ist als bindende Architekturregel
    dokumentiert und deckt ab: Pfade/Config-Verweise gehören in eine Config
    statt in den Code, mit einer klar benannten Ausnahme für bewusst fixe
    Werte.
  - Summary: Pfade und Verweise auf Configs/DBs/Services gehören in eine
    Config statt hartkodiert in den Code, außer sie sind bewusst und
    erkennbar fix.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-019` **Ladestufen-Regel festlegen**
  - Uid: 0be66ed7-89b0-4cda-8890-1f4d8f76d082.
  - Type: Story.
  - Parent: `EPIC-007`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Architektur.
  - Priority: Important.
  - Dependencies: `STORY-018`, `STORY-023`.
  - Goal: Verbindlich festlegen, welche Inhalte in die Root-`CLAUDE.md`, in
    Skills, in Unterordner-`CLAUDE.md` und in Hooks gehören.
  - Completion criteria: Die Regel ist dokumentiert, und für jedes
    bestehende Modul ist nachvollziehbar, auf welcher Stufe es liegt und
    warum.
  - Summary: Regel, wohin neue Harness-Regeln gehören (Hook, Scope, Skill,
    Skript oder Root-`CLAUDE.md`), steht in den Architekturregeln; die
    Systemdoku zeigt für jedes Modul, wo es liegt und warum.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `EPIC-009` **Notes und Topics: Erinnerungen neben dem Backlog**
  - Uid: 0ee1d70e-f11c-4a42-b930-bb699343973a.
  - Type: Epic.
  - Status: Completed.
  - Created: 2026-10-06.
  - Area: Dokumentation.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Der Harness kennt ein zweites Pflegegebiet neben dem Backlog:
    Notes und Topics im ToDo-Viewer (dort EPIC-005). Ein Modul `notes` mit
    eigenem Skill legt fest, wie Claude Notes erkennt, anlegt, pflegt und
    liest. Die Technik (Datenbank, Auslöser, Fälligkeit, Index) liefert
    allein der Viewer über seine API; der Harness spricht nur diese API an,
    hat keinen Dateizugriff und prüft keine Fälligkeiten.
  - Completion criteria: Alle Pflicht-Stories sind abgeschlossen; ein
    Projekt mit `[modules].notes = true` bekommt den Skill
    `claude-harness:notes` und eine Zeile im Session-Start; Claude kann über
    den Helfer Topics und Notes lesen, anlegen, ändern, verlinken,
    zurückstellen, erledigen, verwerfen und befördern; bei nicht
    erreichbarem Server fragt er nach; es gibt kein Markdown-Backend für
    Notes.
  - Summary: Der Harness bringt Claude bei, Erinnerungen, Fragen und Ideen
    als Notes im ToDo-Viewer zu pflegen, getrennt von der Arbeit im Backlog.
    Der Viewer baut die Technik, der Harness die Regeln dazu.
  - Resolution: Vom Projektverantwortlichen am 2026-10-08 bestätigt.

- `EPIC-003` **Change-Workflow (Workspace, Ablauf, Cleanup)**
  - Uid: 139c1ee2-77ac-411c-8958-30373387fd1b.
  - Type: Epic.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Urgent.
  - Dependencies: None.
  - Goal: Einen verbindlichen Ablauf für Changes festlegen: Planen →
    Worktree erstellen oder lokal arbeiten → Coden → Mergen →
    Aufräumen/Worktree löschen, inklusive klarer Entscheidung, woher die
    Workspace-Wahl ihre Quelle zieht und ob diese Quelle konfigurierbar sein
    muss.
  - Completion criteria: Der Ablauf ist Schritt für Schritt dokumentiert,
    inklusive Abbruch-/Cleanup-Fällen, und wurde an einem realen Change
    durchlaufen.
  - Resolution: Rejected by the project owner on 2026-09-24: merged into
    `EPIC-004` as `STORY-022`; STORY-006, STORY-007, STORY-008 (renamed to
    TASK-002, TASK-003, TASK-004 on 2026-09-24) and TASK-001 became its
    tasks.

- `STORY-037` **Testkonventionen: Ablage, Gliederung, Test-Arten**
  - Uid: 1c8a38e0-449b-494d-99e1-70f9e1721d50.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-28.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Verbindlich festlegen, wo und wie Tests in einem Projekt liegen:
    alle Tests in einem Testordner (keine Inline-Tests), mit fester
    Gliederung, getrennt nach Implementierungstests (vom Agenten für die
    eigene Absicherung gebaut) und Funktionalitätstests (für den
    Projekt-Owner, um fachliche Funktionen wie Filter oder größere Abläufe
    gezielt selbst zu prüfen).
  - Completion criteria: Die Regeln zu Testordner, Gliederung, Benennung und
    den beiden Test-Arten stehen im Plugin (Suite development) und sind für
    Projekte mit anderer Sprache oder anderem Test-Framework anwendbar. Der
    Owner kann Funktionalitätstests getrennt von den Implementierungstests
    aufrufen und findet sie über ihren Funktionsnamen. Funktionalitätstests
    laufen nicht im Gesamtlauf mit, ihre Szenarien lassen sich über
    Parameter setzen, und sie zeigen den Output. Dieses Repo ist nach den
    Regeln gegliedert und die Tests laufen weiter durch.
  - Summary: Legt fest, dass alle Tests in einem Ordner liegen und wie er
    gegliedert ist. Unterscheidet Tests, die der Agent für sich baut, von
    Tests, mit denen der Owner Funktionen selbst prüft.
  - Resolution: Vom Projektverantwortlichen am 2026-09-29 bestätigt: Skill
    testing, Einstellungen development.testing/development.tests,
    Sessionstart-Zeile und neue Testgliederung dieses Repos umgesetzt
    (v0.7.0).

- `TASK-016` **Backlog-Ziel aus der Config statt aus einem Pfadparameter**
  - Uid: 1d034359-bc5d-4e6d-b604-32185dfe26a1.
  - Type: Task.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-28.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: `backlog_api.py` ermittelt den Backlog-Ordner selbst aus der
    Harness-Config (Root-Projekt oder `--project <Name>` für Teilprojekte)
    statt aus einem frei angegebenen Pfad; beim Anlegen einer Quelle im
    ToDo-Viewer wird der Projektname mitgegeben.
  - Completion criteria: Der Helfer nimmt keinen Ordner mehr entgegen;
    unbekannte Projekte, abgeschaltetes Modul `todo` und fehlende `TODO.md`
    enden mit Fehler, ohne eine Quelle anzulegen; neue Quellen tragen den
    Projektnamen (Teilprojekt) bzw. den Repo-Namen (Root); Tests decken
    Root, Teilprojekt, Worktree und die Fehlerfälle ab; `api.md` und
    `docs/techdocs/interfaces.md` beschreiben den neuen Aufruf.
  - Resolution: Vom Projektverantwortlichen am 2026-09-28 bestätigt.

- `STORY-016` **Umgang mit Secrets/Credentials**
  - Uid: 2b396cc1-c894-4b34-a6fd-0297003f6790.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Sicherheit.
  - Priority: Prospective.
  - Dependencies: None.
  - Goal: Eine Regel festlegen, dass Secrets nie direkt im Code oder in
    einzucheckenden Dateien landen, sondern in einer zentralen, nicht
    versionierten Config gehalten werden, auf die der Code zur Laufzeit
    verweist. Eine Template-Datei mit Platzhaltern wird eingecheckt, damit
    ersichtlich ist, was konfiguriert werden kann. Welche Config im
    Einzelfall genutzt wird, ist zu klären, sofern nicht bereits eindeutig.
  - Completion criteria: Die Regel ist als bindende Architekturregel
    dokumentiert und deckt ab: kein Secret im Code, Ablage in einer
    zentralen gitignorten Config, eingecheckte Template-Datei mit
    Platzhaltern, Klärung der Config-Zuordnung mit dem Projekt-Owner.
  - Summary: Secrets landen nie im Code, sondern in einer zentralen,
    gitignorten Config; eine Template-Datei zeigt, was konfigurierbar ist.
    Welche Config genutzt wird, wird im Zweifel mit dem Owner geklärt.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-014` **Backlog-Lebenszyklus verfeinern**
  - Uid: 32a3334e-a75b-4e55-93ed-858f4d4c14c8.
  - Type: Story.
  - Parent: `EPIC-005`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Die Statusübergänge dieses Backlogs (Open → In progress → Awaiting
    confirmation → Completed/Rejected) im Alltag konsequent anwenden,
    inklusive der Regel, dass nur der Projekteigner final bestätigt.
  - Completion criteria: Mindestens ein Eintrag hat den vollständigen
    Lebenszyklus bis `Completed` oder `Rejected` durchlaufen.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `STORY-024` **Testdisziplin & Verifikation**
  - Uid: 4e345bb6-112f-49fb-b4da-44022badbacc.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-24.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Festlegen, wie getestet wird: wann der Test vor dem Code entsteht
    und wie umfangreich nach einer Änderung getestet wird.
  - Completion criteria: Die Skill `claude-harness:decomposition` enthält
    Regeln zu Test zuerst und zum Testumfang; der Verifikationsnachweis ist
    abgelehnt.
  - Summary: Bündelt alles zum Testen: Testumfang (TASK-006) und TDD
    (TASK-005) sind Tasks dieser Story.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `TASK-009` **Geerbte Architekturregeln**
  - Uid: 51ce4883-0b18-4ed6-81be-cf57e4316293.
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-008`.
  - Goal: Ein Projekt kann in `## Inherited rules` seiner `architecture.md`
    Regeln eines anderen Projekts übernehmen (Hauptdatei oder einzelne
    Scopes). Der Hook verlangt sie zusätzlich.
  - Completion criteria: Tests zeigen: Erbt ein Teilprojekt `root:
    architecture.md`, verlangt eine Änderung dort beide Regeldateien.
    Fehlerhafte Einträge meldet der Session-Start. Template und Skill
    `architecture` sind angepasst.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-021` **Harness in Projekten initialisieren**
  - Uid: 5352d92f-d114-4d64-88d3-7c323c14e7da.
  - Type: Story.
  - Parent: `EPIC-007`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Architektur.
  - Priority: Important.
  - Dependencies: `STORY-018`.
  - Goal: Ein Befehl `/claude-harness:init` richtet den Harness in einem
    Projekt ein: Er legt `.claude-harness/config.toml` aus einer Vorlage an
    und bietet bei aktivem `todo`-Modul an, den Backlog aus Vorlagen
    anzulegen — jeweils erst nach Freigabe und ohne Bestehendes zu
    überschreiben.
  - Completion criteria: In einem Projekt ohne Harness entstehen nach dem
    Befehl und Freigabe eine gültige Config und ein gültiger leerer Backlog;
    in einem bereits eingerichteten Projekt wird nichts verändert.
  - Summary: In my_story_game getestet: Einrichtung nach Rückfragen
    erfolgreich, ein zweiter Aufruf ändert nichts. Zwei kleine
    Verbesserungsideen stehen in den Notizen.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-039` **API-Helfer für Notes und Topics**
  - Uid: 54f4d16e-bd47-4904-8c9b-6005e0699453.
  - Type: Story.
  - Parent: `EPIC-009`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-06.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Ein Helfer `notes_api.py` spricht die Notes-API des ToDo-Viewers
    an (Topics und Notes lesen, anlegen, ändern, verlinken, Status wechseln,
    befördern, zurückstufen, Papierkorb) nach dem Muster von
    `backlog_api.py`. HTTP-Client, Projektwahl, Fehlerbehandlung und
    Exit-Codes liegen in einem gemeinsamen Modul statt doppelt. Er nutzt nur
    die Standardbibliothek, liest die API-URL aus der Config und kennt
    keinen Dateizugriff auf Notes. Die genauen Befehle richten sich nach der
    API-Story im Backlog des ToDo-Viewers (EPIC-005 dort); Umsetzung erst
    nach deren Festlegung.
  - Completion criteria: Der gemeinsame Client ist aus `backlog_api.py`
    herausgelöst und die bestehenden Backlog-Tests laufen unverändert grün;
    `notes_api.py` deckt alle in der Notes-Spec genannten Befehle ab; Exit 3
    bei nicht erreichbarem Server; Tests mit einem Stub-Server für Erfolg,
    Konflikt, Fehlercodes und Unerreichbarkeit.
  - Summary: Ein Helfer-Skript, über das Claude Notes im Viewer liest und
    ändert, wie beim Backlog.
  - Resolution: Vom Projektverantwortlichen am 2026-10-08 bestätigt.

- `TASK-003` **Verbindlicher Change-Ablauf**
  - Uid: 56bb2668-c060-4489-a661-11f8afe780d6.
  - Type: Task.
  - Parent: `STORY-022`.
  - Required for parent: No.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Urgent.
  - Dependencies: `TASK-002`.
  - Goal: Die Schrittfolge Plan → Worktree/Lokal → Code → Merge → Cleanup
    als verbindliche Regel in `CLAUDE.md` festhalten, inklusive der Punkte,
    an denen eine Freigabe eingeholt wird.
  - Completion criteria: Jeder Schritt hat eine klare
    Ein-/Ausstiegsbedingung; kein Schritt wird stillschweigend übersprungen.
  - Resolution: Rejected by the project owner on 2026-09-24: folded into the
    spec of `STORY-022`; the native worktree tools cover the rest.

- `STORY-018` **Plugin-Grundgerüst**
  - Uid: 5d2a5d19-f9af-4633-865c-640b248eb5ee.
  - Type: Story.
  - Parent: `EPIC-007`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Architektur.
  - Priority: Urgent.
  - Dependencies: None.
  - Goal: Die Plugin-Struktur anlegen (Manifest, Ordner für Skills und
    Hooks) und das Plugin in diesem Repo selbst aktivieren.
  - Completion criteria: Claude Code erkennt das Plugin in diesem Repo; ein
    Test-Skill ist aufrufbar und ein Test-Hook wird nachweislich ausgelöst.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `EPIC-001` **Konfigurierbarer Harness (Policy)**
  - Uid: 5d367de4-789c-488b-8060-b17063be87f6.
  - Type: Epic.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Eine projekteigene Konfigurationsdatei für das
    Claude_Harness-Plugin definieren, die nur echte Projektwerte enthält
    (Pfade, Sprache, aktive Module) und von Skills und Hooks gelesen wird.
    Weitere Felder bringt jedes Modul selbst mit. Genehmigungen und Rechte
    bleiben bei den nativen Claude-Code-Einstellungen.
  - Completion criteria: Das Konfigurationsschema ist validiert und
    dokumentiert und wird von den Hooks mehrerer Module tatsächlich gelesen
    und angewendet.
  - Summary: Jedes Projekt bekommt eine kleine Einstellungsdatei, in der
    steht, wo Dinge liegen, wie getestet wird und welche Harness-Teile an
    sind.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `TASK-001` **Cleanup-Kriterien festlegen**
  - Uid: 6b161dee-64a6-439b-944c-727f100d8dab.
  - Type: Task.
  - Parent: `STORY-022`.
  - Required for parent: No.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Important.
  - Dependencies: `TASK-003`.
  - Goal: Definieren, wann ein Worktree/Branch gefahrlos gelöscht werden
    darf (z. B. nur nach erfolgreichem Merge und sauberem Zustand) und wann
    nicht.
  - Completion criteria: Die Kriterien verhindern nachweislich das Löschen
    eines Worktrees mit unverarbeiteten Änderungen.
  - Resolution: Rejected by the project owner on 2026-09-24: folded into the
    spec of `STORY-022`; the native worktree tools cover the rest.

- `TASK-018` **todo-Skill: Lücken beim Wiedereröffnen und bei geschlossenen Parents**
  - Uid: 6e935c76-1ddb-4ff5-ba81-ec7564f1462c.
  - Type: Task.
  - Parent: None.
  - Status: Completed.
  - Created: 2026-09-28.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Der todo-Skill beschreibt den Umgang mit geschlossenen Parents so,
    wie der ToDo-Viewer ihn umsetzt, und sagt dem Agenten, was er tun soll,
    wenn der passende Parent eines neuen Items geschlossen ist.
  - Completion criteria: format.md und das Verhalten des Servers
    widersprechen sich nicht mehr: Entweder nimmt ein abgeschlossener Parent
    kein Kind mehr an, auch kein optionales, oder der Server erlaubt
    optionale Kinder. api.md beschreibt, wie ein geschlossenes oder
    archiviertes Item wieder geöffnet wird. SKILL.md legt fest: Ist der
    passende Parent eines neuen Items geschlossen, fragt der Agent den Owner
    vor dem Anlegen, ob er ihn wieder öffnen soll, statt das Item ohne
    Parent anzulegen.
  - Summary: Schließt drei Lücken im todo-Skill, die beim Anlegen von
    STORY-037 aufgefallen sind: Die Regel zu geschlossenen Parents passt
    nicht zum Server, das Wiedereröffnen über die API ist nicht beschrieben,
    und es fehlt eine Vorgabe, was bei einem geschlossenen Parent zu tun
    ist.
  - Resolution: Vom Projektverantwortlichen am 2026-09-29 bestätigt:
    todo-Skill behandelt geschlossene Parents wie der ToDo-Viewer,
    Wiedereröffnen und parent_closed in api.md beschrieben (Merge 3f48fac,
    v0.7.1).

- `STORY-032` **Backend-Einstellung für den Backlog**
  - Uid: 7419af17-fdb0-4fcf-97ef-2404bfa3c94f.
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-28.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: `config.toml` bekommt `[todo].backend` (`api` oder `files`,
    Standard `api`) und `[todo].api_url` (Standard
    `http://localhost:5411/api/v2`).
  - Completion criteria: Die Werte werden geladen und validiert; fehlende
    Schlüssel ergeben die Standardwerte, bestehende Configs laufen ohne
    Migration weiter; `docs/techdocs/configuration.md` beschreibt beide
    Schlüssel; Tests decken Standard, gültige und ungültige Werte ab.
  - Resolution: Vom Projektverantwortlichen am 2026-09-28 bestätigt.

- `STORY-025` **Regelverstöße und Regeländerungen**
  - Uid: 7504ca6c-6088-4d86-8e30-ea19c1feb65b.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-24.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `STORY-023`.
  - Goal: Festlegen, wie die AI vorgeht, wenn eine Anforderung, eine
    gestaltete Architektur oder ein Wunsch des Projektverantwortlichen nicht
    zu den Regeln der Suite `development` oder zu den Vorgaben des Harness
    passt: Konflikt benennen und Lösungen vorschlagen, Entscheidung durch
    den Projektverantwortlichen, gewünschte Harness-Änderungen an den
    Harness-Backlog übergeben.
  - Completion criteria: Das Verfahren ist im Plugin festgelegt und gilt für
    alle Teilbereiche der Suite `development` und für die Vorgaben aller
    Module. Ein Wunsch nach einer Harness-Änderung lässt sich aus einem
    anderen Projekt heraus an das Harness-Repo übergeben. Das Verfahren
    wurde an mindestens einem echten Konfliktfall durchgespielt.
  - Summary: Klärt, was passiert, wenn eine Architektur oder ein Wunsch des
    Projektverantwortlichen nicht zu den dokumentierten Regeln oder zu den
    Vorgaben des Harness passt: Die AI benennt den Konflikt, der
    Projektverantwortliche entscheidet.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `TASK-006` **Testumfang je Änderung**
  - Uid: 80c0299b-c288-4d35-9569-0203bf9799b7.
  - Type: Task.
  - Parent: `STORY-024`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `STORY-001`.
  - Goal: Festlegen, wie umfangreich nach einer Änderung getestet wird: was
    die Änderung betreffen kann, nicht immer die ganze Suite.
  - Completion criteria: Die Skill `claude-harness:decomposition` enthält
    Regeln zum Testumfang: betroffene Tests inkl. Aufrufer, erneuter Lauf
    nach der letzten Änderung, Nennen des nicht Getesteten, Prüfen roter
    Tests vor dem Abtun. Kein eigenes Verify-Skript.
  - Resolution: Confirmed by the project owner on 2026-09-24 (Ziel auf
    Testumfang gekürzt, Verify-Skript entfällt).

- `TASK-019` **Verifikations-Nachweis-Format**
  - Uid: 874f0c95-de49-4115-94c0-24725bb1e23e.
  - Type: Task.
  - Parent: `STORY-024`.
  - Required for parent: No.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Prospective.
  - Dependencies: `TASK-006`.
  - Goal: Ein einfaches, lesbares Format festlegen, in dem ein Verify-Lauf
    protokolliert wird (Befehl, Ergebnis, Zeitpunkt, betroffener Scope).
  - Completion criteria: Nach einem Change liegt ein solcher Nachweis vor
    und lässt sich ohne Rückfrage nachvollziehen.
  - Resolution: Rejected by the project owner on 2026-09-24: ein Protokoll,
    das der Agent selbst schreibt, belegt nichts; wird nicht gebraucht.

- `STORY-022` **Change-Workflow im Worktree**
  - Uid: 8b0a0291-ae58-4539-9ef3-b47745910935.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-24.
  - Area: Governance.
  - Priority: Urgent.
  - Dependencies: None.
  - Goal: Changes mit freigegebenem Plan laufen in einem eigenen Worktree,
    der vom aktuell ausgecheckten Branch abzweigt. Nach Abschluss committet
    die AI, merged selbstständig in diesen Ausgangsbranch zurück und löscht
    den Worktree. Changes ohne Plan laufen lokal. So kann parallel
    gearbeitet werden, ohne dass fremde Worktrees angefasst werden.
  - Completion criteria: Der Ablauf ist als Teilbereich der Suite
    `development` umgesetzt (Schalter, Session-Start-Hinweis, Skill) und
    getestet. Ein realer Change mit Plan ist vom Ausgangsbranch über
    Worktree, Merge-Commit und Löschen des Worktrees ohne Rückfrage
    durchgelaufen; Worktrees anderer Sessions blieben unberührt.
  - Summary: Größere Änderungen macht die AI in einer eigenen Arbeitskopie
    und führt sie danach selbst in den Branch zurück, von dem sie gestartet
    ist. Die früheren Tasks TASK-001 bis TASK-004 sind in der Spec
    aufgegangen.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-002` **Policy laden und validieren**
  - Uid: 8b5314f8-a6ad-4304-8c3b-8bddde71f359.
  - Type: Story.
  - Parent: `EPIC-001`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `STORY-001`, `STORY-018`.
  - Goal: Die Konfigurationsdatei beim Session-Start per Hook einlesen und
    gegen das Schema prüfen, damit Fehler auffallen, bevor ein Verify- oder
    Change-Vorgang startet.
  - Completion criteria: Ein fehlerhafter oder unvollständiger
    Konfigurationswert wird beim Session-Start erkannt und klar gemeldet
    statt stillschweigend ignoriert zu werden.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `TASK-007` **Registry und Projektzuordnung**
  - Uid: 8d109c5c-262e-427f-8ffa-44ac659370b7.
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Die Root-Konfiguration kann Teilprojekte in `[projects]`
    eintragen. Ein gemeinsamer Helfer lädt alle Projekte und ordnet jede
    Datei ihrem Projekt zu. Der Session-Start listet die Projekte und meldet
    Registry-Fehler.
  - Completion criteria: Schema, Validierung, Doku in `configuration.md` und
    Tests sind vorhanden. Der Session-Start zeigt in einem Test-Repo mit
    zwei Teilprojekten alle Projekte und meldet ein ungültiges Teilprojekt,
    ohne die anderen unwirksam zu machen. Ohne `[projects]` ist die Ausgabe
    unverändert.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `EPIC-007` **Plugin-Architektur**
  - Uid: 8df3c7de-01c1-4f23-aede-11be8b2d9abd.
  - Type: Epic.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Architektur.
  - Priority: Urgent.
  - Dependencies: None.
  - Goal: Claude_Harness als Claude-Code-Plugin aufbauen, in dem die Module
    als Skills und die harten Regeln als Hooks umgesetzt sind, sodass Regeln
    gestuft geladen werden und bei unbeteiligten Aufgaben kaum Tokens
    kosten.
  - Completion criteria: Das Plugin ist in diesem Repo aktiv, mindestens ein
    Modul läuft als Skill mit zugehörigem Hook, und die Root-`CLAUDE.md`
    enthält nur Verweise statt Regeltexten.
  - Summary: Der Harness wird ein Zusatzpaket für Claude Code. Regeln werden
    nur dann geladen, wenn sie zur aktuellen Aufgabe passen; Pflichtregeln
    prüft ein Skript automatisch.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-009` **Entwicklungsprinzipien-Dokument**
  - Uid: 8ef63110-bbcc-4bd3-a445-cfd209c11c9e.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: No.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Projektbezogene Entwicklungsprinzipien (z. B. keine unnötigen
    Abstraktionen, keine spekulativen Features) explizit und
    projekt-konfigurierbar festhalten statt nur implizit im Systemverhalten
    zu belassen.
  - Completion criteria: Ein kurzes, prüfbares Prinzipien-Dokument liegt
    vor.
  - Resolution: Rejected by the project owner on 2026-09-25: the named
    principles are native Claude behavior; project-specific rules belong in
    `architecture.md`. `EPIC-004` Goal and Completion criteria adjusted.

- `STORY-013` **Daily-Development-Report**
  - Uid: 9158c276-c6bd-4b08-9ae5-7fa615bab8f5.
  - Type: Story.
  - Parent: `EPIC-005`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Dokumentation.
  - Priority: Prospective.
  - Dependencies: None.
  - Goal: Format und Materialitätskriterium für einen Tagesbericht
    festlegen, der nur bei tatsächlich relevanter Arbeit entsteht (nicht bei
    jeder kleinen Änderung).
  - Completion criteria: Ein Beispieltag mit relevanter Arbeit erzeugt einen
    Report; ein Tag ohne relevante Arbeit erzeugt keinen.
  - Summary: Ein optionales Modul schreibt pro Arbeitstag einen deutschen
    Bericht über die relevanten Änderungen, mit Verweisen auf Backlog und
    Commits. Ein Hook erinnert nach Änderungen daran, ihn aktuell zu halten.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `STORY-005` **Dimensions-Checkliste je Teilaufgabe**
  - Uid: 933b003a-8b8f-43f8-b933-5ed08bf9a5d6.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Prospective.
  - Dependencies: `STORY-004`.
  - Goal: Eine Prüfliste relevanter Dimensionen (Persistenz, Schnittstellen,
    Sicherheit, Tests, Dokumentation) für jede zerlegte Teilaufgabe
    bereitstellen, damit nichts vergessen wird.
  - Completion criteria: Die Checkliste wird bei einer zerlegten Aufgabe
    sichtbar durchlaufen und im Ergebnis referenziert.
  - Summary: Wird zusammen mit STORY-004 geplant und landet im selben Skill;
    die Entscheidungen stehen in dessen Notizen.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-041` **Abgrenzung im todo-Skill und Techdocs zu Notes**
  - Uid: 97bcdf96-3f30-4a41-826a-864f711349e5.
  - Type: Story.
  - Parent: `EPIC-009`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-06.
  - Area: Dokumentation.
  - Priority: Normal.
  - Dependencies: `STORY-040`.
  - Goal: Der todo-Skill grenzt das Backlog von Notes ab und verweist auf
    `claude-harness:notes`, inklusive Umwandlung Item zu Note und Note zu
    Item. Die Techdocs (Interfaces, Architektur, README) beschreiben das
    Modul und verweisen für das Notes-Modell auf die Dokumentation des
    Viewers. Notes kommen nicht in den Tagesbericht; das steht im
    daily-Skill nur dann, wenn es Missverständnisse gibt. Danach folgt das
    Release (SemVer, Minor).
  - Completion criteria: `plugin/skills/todo/SKILL.md` nennt die Abgrenzung
    in höchstens einem kurzen Abschnitt; `docs/techdocs/interfaces.md`,
    `architecture.md` und `README.md` nennen Modul, Helfer und Skill; kein
    Notes-Inhalt wird in Repository-Dateien geschrieben; Release mit
    passender Version und Tag.
  - Summary: Kleine Querverweise im todo-Skill, Anpassung der Dokumentation
    und das Release.
  - Resolution: Vom Projektverantwortlichen am 2026-10-08 bestätigt.

- `STORY-034` **todo-Skill für den API-Modus**
  - Uid: 995c65f8-9770-455f-ae02-c68adec822f7.
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-28.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: `STORY-033`.
  - Goal: `SKILL.md` und `format.md` beschreiben die Arbeit im API-Modus
    über den Helfer und im Datei-Modus wie bisher; die Entscheidungsbefugnis
    bleibt im Skill. Löschen in den Papierkorb ist bei klarem Auftrag ohne
    Rückfrage erlaubt, endgültiges Löschen nur durch den
    Projektverantwortlichen.
  - Completion criteria: Der Skill nennt je Modus Lesen, Anlegen, Ändern,
    Notes/Specs und Löschen; bei nicht erreichbarem Server gibt der Agent
    einen Hinweis und fragt, ob der Server gestartet, auf Dateien
    ausgewichen oder abgebrochen wird; Konflikte (409) werden neu gelesen
    und geprüft, nicht blind wiederholt.
  - Resolution: Vom Projektverantwortlichen am 2026-09-28 bestätigt.

- `TASK-008` **Architekturregeln pro Projekt**
  - Uid: a01fcfe6-9c95-4123-bbd6-6f8b88713863.
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-007`.
  - Goal: Die Architektur-Hooks verlangen die Regeln des Projekts, zu dem
    die geänderte Datei, die Spec oder der Plan gehört.
  - Completion criteria: Tests zeigen: Eine Änderung im Teilprojekt verlangt
    dessen Regeln, eine Änderung im Core die Root-Regeln. Ein Plan verlangt
    die Regeln jedes darin genannten Projekts.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `TASK-011` **Daily Reports pro Projekt**
  - Uid: aa911b91-34a1-469a-a3bc-e092194b4a43.
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-007`.
  - Goal: Jedes Projekt hat eigene Daily Reports mit eigenem
    Bestätigungsstand. Ein Commit zählt nur für das Projekt, dessen Dateien
    er ändert, auch wenn das Git-Root über dem Projekt liegt.
  - Completion criteria: Tests zeigen: Ein Commit nur in einem Teilprojekt
    erscheint nur in dessen Daily. Ein reiner Backlog-Commit zählt nirgends.
    Beim Start im Teilprojekt mit Git-Root darüber zählen Commits außerhalb
    nicht. `daily.py --project` funktioniert.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-029` **SemVer-Versionierung klären und ggf. automatisieren**
  - Uid: aec479a4-22fa-4450-b0b7-2d7730b9e631.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Klären, ob und wie Versionierung nach SemVer (Major/Minor/Patch)
    automatisiert werden soll – etwa die Einstufung einer Änderung und das
    Anheben der Version in den Paketmetadaten – und das Vereinbarte
    umsetzen, damit Versionen nachvollziehbar und konsistent steigen.
  - Completion criteria: Die Entscheidung (ob, was und wie weit
    automatisiert wird) ist mit dem Owner geklärt und in den Notizen
    festgehalten; das Vereinbarte ist umgesetzt und an mindestens einer
    Änderung angewendet.
  - Summary: Klären, ob Claude bei Änderungen die Versionsnummer nach SemVer
    selbst einstufen und hochzählen soll, und das dann umsetzen.
  - Resolution: Completed on 2026-09-25 under the project owner's advance
    authorization to close it once done; module implemented and enabled in
    this repo (`924a972`), first release tag `v0.1.0` follows the closure by
    owner decision.

- `TASK-014` **Abgelehnte Pflicht-Kinder im Backlog-Lebenszyklus klären**
  - Uid: af124a5c-e4d0-4fc5-8feb-e4d2e8c7656e.
  - Type: Task.
  - Parent: None.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Backlog-Format (`format.md`) und Prüfskript (`backlog.py`)
    behandeln abgelehnte Pflicht-Kinder gleich. Heute blockiert das Skript
    `Awaiting confirmation` auch bei abgelehnten Pflicht-Kindern, obwohl das
    Format nur `Open` und `In progress` nennt. Die Meldung nennt abgelehnte
    Kinder außerdem „active“. Für `Completed` verlangt das Format, dass alle
    Pflicht-Kinder abgeschlossen sind; eine abgelehnte Pflicht-Task
    blockiert den Parent damit dauerhaft.
  - Completion criteria: Die Regel für abgelehnte Pflicht-Kinder ist
    entschieden, in `format.md` beschrieben und im Prüfskript umgesetzt.
    Tests decken `Awaiting confirmation` und `Completed` mit abgelehnten
    Pflicht-Kindern ab, und die Meldungen benennen den Status richtig.
  - Summary: Das Backlog-Prüfskript und die Formatbeschreibung widersprechen
    sich, wenn eine Pflicht-Aufgabe abgelehnt wurde. Das wird
    vereinheitlicht.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-038` **Modulschalter notes in Config und Session-Start**
  - Uid: b0138257-608c-4d08-bf7b-b64ac94d89b3.
  - Type: Story.
  - Parent: `EPIC-009`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-06.
  - Area: Konfiguration.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: `[modules].notes` ist ein gültiger Schlüssel der Harness-Config
    (Standard aus). Bei aktivem Modul gibt der Session-Start eine statische
    Zeile mit Skill-Hinweis aus (ohne Netzwerk und ohne Abfrage von
    Fälligem), bei mehreren Projekten einmal je Hinweis. `init`, `update`
    und die Vorlage kennen den Schalter. Das Modul braucht keine eigenen
    Config-Schlüssel (kein Prüf-Intervall, keine Uhrzeit für relative
    Angaben).
  - Completion criteria: Unbekannte Modulnamen bleiben Fehler, `notes` wird
    akzeptiert; `session_start.py` zeigt die Zeile nur bei aktivem Modul,
    einfach und mit Teilprojekten; `plugin/templates/config.toml`,
    `docs/techdocs/configuration.md` und die Tests in `test_config.py` und
    den Session-Start-Tests sind angepasst; `init` und `update` erwähnen das
    Modul; die Tests laufen grün.
  - Summary: Das Modul notes lässt sich wie die anderen Module in der Config
    einschalten; der Session-Start nennt es nur mit einer Zeile.
  - Resolution: Vom Projektverantwortlichen am 2026-10-08 bestätigt.

- `STORY-040` **Skill notes: Regeln für Notes und Topics**
  - Uid: b053891d-e34e-4423-a619-842816f2aa1a.
  - Type: Story.
  - Parent: `EPIC-009`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-06.
  - Area: Dokumentation.
  - Priority: Normal.
  - Dependencies: `STORY-039`.
  - Goal: Der Skill `claude-harness:notes` (mit `api.md`) legt fest, wie
    Claude Notes erkennt (Note oder Backlog-Eintrag oder Wecker), anlegt,
    pflegt, liest, verlinkt, befördert und zurückstuft, was er ohne
    Rückfrage darf, wie er relative Zeitangaben in feste Zeitpunkte auflöst,
    und dass Notes privat sind. Der Skill nennt Fälligkeit nur als Zustand,
    den der Viewer setzt; Claude prüft nichts und spricht Fälliges nicht von
    sich aus an, sondern liest es nur auf Zuruf.
  - Completion criteria: `plugin/skills/notes/SKILL.md` und `api.md`
    enthalten alle in der Spec (STORY-040) genannten Regeln, die
    Beschreibung ist ein Satz ohne Regeln (Architekturregel 9), alle Texte
    sind englisch; `api.md` stimmt mit den Befehlen von `notes_api.py`
    überein; ein Funktionstest oder eine dokumentierte Probe zeigt
    Erkennung, Anlegen mit Bestätigung des aufgelösten Zeitpunkts und Lesen
    über den Index vor dem Langtext.
  - Summary: Der Skill, der Claude beibringt, wann etwas eine Note ist und
    wie er sie anlegt, liest und pflegt.
  - Resolution: Vom Projektverantwortlichen am 2026-10-08 bestätigt.

- `STORY-020` **TODO-Modul als Skill und Hook**
  - Uid: b2da701f-f576-410d-a096-3af72582a3e8.
  - Type: Story.
  - Parent: `EPIC-007`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: `STORY-017`, `STORY-018`.
  - Goal: Die Backlog-Regeln aus `TODO.md` in einen `todo`-Skill überführen
    und die Formatprüfung als Hook umsetzen; der Kopf von `TODO.md` wird auf
    einen Verweis gekürzt.
  - Completion criteria: Ein fehlerhafter Eintrag wird vom Hook gemeldet;
    bei einer Aufgabe ohne Backlog-Bezug wird der Skill nicht geladen.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `STORY-023` **Architektur-Definitionen**
  - Uid: bbdbc790-1ed7-4308-8a11-39862c6ecc99.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-24.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Festlegen, wo und wie die grundlegende, für das ganze Projekt
    verbindliche Architektur definiert wird (Vorbild:
    `.harness/architecture-rules.md` in my_story_game): Ort, Aufbau, Umgang
    mit Teilbereichen, wann sie geladen wird, wie sie durchgesetzt und wie
    sie geändert wird.
  - Completion criteria: Ort, Format, Ladeweg und Änderungsverfahren der
    Architektur-Definitionen sind festgelegt und in mindestens einem Projekt
    angewendet.
  - Summary: Architekturregeln werden Teil einer Modul-Suite `development`,
    liegen englisch im Doku-Ordner und werden per Hook vor der ersten
    Code-Änderung einer Session gelesen.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-004` **Zerlegungs-Heuristik definieren**
  - Uid: bcd1e2a7-cf8d-40c2-8df1-2f74ad69d129.
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Kriterien festlegen, nach denen Aufgaben zerlegt werden: im
    Backlog grob in Tasks mit eigenständigem Ergebnis, beim Planen fein in
    logische, einzeln testbare Abschnitte, die in Abhängigkeitsreihenfolge
    umgesetzt werden und ohne den Kontext der planenden Session umsetzbar
    sind; einschließlich wann bewusst nicht zerlegt wird.
  - Completion criteria: Die Kriterien stehen im Skill `decomposition` der
    Suite `development`. An einem realen Feature wurde ein Plan danach in
    Abschnitte mit je eigenem Test zerlegt und so umgesetzt. Zwei ähnliche
    Aufgaben werden nachvollziehbar gleich zerlegt.
  - Summary: Beim Planen sollen kleine, gut kontrollierbare Schritte
    entstehen, die auch ein einfaches Modell umsetzen kann. Die Kriterien
    kommen in einen neuen Skill der Suite `development`.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-035` **Hooks und Sitzungsstart je Backend**
  - Uid: c0c1c33f-ca48-4684-bdfd-99f9e6975557.
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-28.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: `STORY-032`.
  - Goal: Der Backlog-Check läuft nur im Datei-Modus; der Hinweis beim
    Sitzungsstart nennt im API-Modus die API statt `TODO.md`.
  - Completion criteria: Im API-Modus markiert `mark_backlog_dirty.py`
    nichts und `check_backlog.py` prüft nichts; `session_start.py` meldet je
    Modus den passenden Hinweis; Tests decken beide Modi ab.
  - Resolution: Vom Projektverantwortlichen am 2026-09-28 bestätigt.

- `TASK-010` **Backlog und techdocs pro Projekt**
  - Uid: c83bf593-3684-4f86-be37-1bf7c0e79c8b.
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-007`.
  - Goal: Backlog-Prüfung und techdocs-Erinnerung arbeiten pro Projekt.
  - Completion criteria: Tests zeigen: Eine Änderung im Backlog eines
    Teilprojekts prüft nur dieses Backlog. Die techdocs-Erinnerung erscheint
    pro Projekt, dessen Code geändert wurde.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-001` **Policy-Schema definieren**
  - Uid: cd481e14-5668-4892-b01f-37636e3c5217.
  - Type: Story.
  - Parent: `EPIC-001`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Die Projektkonfiguration `.claude-harness/config.toml` festlegen:
    Grundfelder (Version, Doku-Wurzel, Sprache, Modulschalter) und die
    Regel, dass jedes Modul seine Felder selbst ergänzt, in
    `configuration.md` dokumentiert und ihre Validierung testet. Kein
    Approval-Modus.
  - Completion criteria: Ein dokumentiertes Schema (Ort, Felder, Typen,
    Pflicht vs. optional, Standardwerte) liegt vor und deckt alle
    bestehenden Module ab.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-017` **Backlog-Format/Aufbau festlegen**
  - Uid: d33116f5-3eb8-4af4-bfc6-b3f3d4a10b9b.
  - Type: Story.
  - Parent: `EPIC-005`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Entscheiden und dokumentieren, wie der Backlog unter `docs/todo/`
    aufgebaut ist — welche Felder ein Eintrag mindestens braucht, welche
    Typen/Areas/Prioritäten gelten, wie Notes und Specs pro Item abgelegt
    werden und welche Teile des Agent_Harness-Formats v2 übernommen werden.
  - Completion criteria: Ein dokumentierter Aufbau-Standard liegt vor, an
    dem sich jeder neue Eintrag ohne Rückfrage orientieren kann.
  - Summary: Die Struktur steht und ist im Plugin: Hauptliste, Archiv und
    pro Aufgabe bei Bedarf Notizen und technische Beschreibung. Dazu Regeln
    für den Abschluss von Epics/Stories und für das Einordnen neuer
    Aufgaben.
  - Resolution: Confirmed by the project owner on 2026-09-23 (after
    reopening on the same day).

- `STORY-030` **Harness-Konfiguration aktualisieren**
  - Uid: d81606c2-609b-4a7d-982b-558563a701c0.
  - Type: Story.
  - Parent: `EPIC-007`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Architektur.
  - Priority: Normal.
  - Dependencies: `STORY-021`.
  - Goal: Ein `update`-Schritt (Skill) als Pendant zum `init`-Skill: Ein
    Projekt, das den Harness schon nutzt, kann prüfen, ob seine
    `.claude-harness/config.toml` dem aktuellen Schema entspricht, und
    fehlende Ergänzungen (i. d. R. neue Module oder Schema-Migrationen) nach
    Freigabe eintragen, ohne Bestehendes zu überschreiben. Dazu gehört ein
    Versionierungsmechanismus fürs Config-Schema: `CONFIG_VERSION` in
    `harness_config.py` wird um eine Migrationsliste je Versionsschritt
    erweitert, statt auf SemVer umzustellen.
  - Completion criteria: Der Aufruf des Update-Schritts auf ein Projekt mit
    veralteter Config wendet die fehlenden Migrationen an (mit Rückfragen
    nur bei neuen, wirklich zu entscheidenden Werten) und schreibt die
    Config auf die aktuelle Version; auf eine bereits aktuelle Config wird
    gemeldet, dass nichts zu tun ist; das Ergebnis besteht die bestehende
    Config-Validierung.
  - Summary: Der neue Befehl `/claude-harness:update` bringt die
    Harness-Config eines Projekts automatisch auf den neuesten Stand,
    ähnlich wie der Einrichtungs-Befehl das für neue Projekte tut. Er
    erkennt "bereits aktuell" ohne etwas zu ändern und würde bei einer
    künftigen Schema-Änderung die fehlenden Schritte nachtragen.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `TASK-002` **Workspace-Entscheidung formalisieren**
  - Uid: e114f1f5-271d-41db-93b7-732f2ef523c4.
  - Type: Task.
  - Parent: `STORY-022`.
  - Required for parent: No.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Urgent.
  - Dependencies: `STORY-002`.
  - Goal: Klären, wonach heute nativ entschieden wird, ob ein Change lokal
    oder in einem Worktree läuft (welche Quelle, welche Signale), und ob
    diese Quelle projektseitig einstellbar sein sollte statt fest im
    Verhalten zu stecken.
  - Completion criteria: Dokumentiert ist, welche Quelle die Entscheidung
    heute tatsächlich steuert; eine Entscheidung liegt vor, ob/wie sie
    konfigurierbar gemacht wird. Wird sie konfigurierbar, sind die Felder in
    `configuration.md` dokumentiert und ihre Validierung ist getestet.
  - Resolution: Rejected by the project owner on 2026-09-24: folded into the
    spec of `STORY-022`; the native worktree tools cover the rest.

- `STORY-033` **API-Helfer für den Backlog**
  - Uid: e13e9c82-6daf-4a28-a02b-4e5a71665b2a.
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-28.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `STORY-032`.
  - Goal: Ein Skript im Plugin kapselt die Aufrufe der Viewer-API
    (Erreichbarkeit, Quelle zum Backlog-Ordner finden oder anlegen, Index,
    Item lesen, anlegen, ändern, löschen, Notes und Specs lesen und
    schreiben, Papierkorb ohne endgültiges Löschen), damit der Agent keine
    JSON-Aufrufe von Hand bauen muss.
  - Completion criteria: Das Skript nutzt nur die Standardbibliothek, liest
    `api_url` aus der Config, gibt Antworten und Fehler (inkl.
    `version_conflict`) verständlich aus und endet bei nicht erreichbarem
    Server mit eigenem Exit-Code; Tests laufen gegen einen lokalen
    Testserver; `docs/techdocs/interfaces.md` beschreibt die Befehle.
  - Resolution: Vom Projektverantwortlichen am 2026-09-28 bestätigt.

- `EPIC-004` **Entwicklungsprozess & Prinzipien**
  - Uid: e2bc7e21-a9a6-4257-9061-7749a440476b.
  - Type: Epic.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Verbindlich festlegen, wie in einem Projekt entwickelt wird:
    projektweite Architektur-Definitionen, Heuristik zur Task-Zerlegung,
    Change-Ablauf (Workspace, Ablauf, Cleanup), TDD-Ritual und einheitliche
    Testebenen (Unit/Integration/System), damit Qualität nicht vom Zufall
    abhängt.
  - Completion criteria: Architektur-Definitionen, Zerlegungs-Heuristik,
    Change-Ablauf und Testkommando sind dokumentiert und werden bei
    mindestens einem Change sichtbar angewendet.
  - Summary: Legt fest, wie entwickelt wird: Architekturregeln, Zerlegung,
    Change-Ablauf im Worktree, Tests und Versionierung. Ein eigenes
    Prinzipien-Dokument gehört nicht mehr dazu.
  - Resolution: Confirmed by the project owner on 2026-09-29.

- `TASK-013` **Worktree-Ablauf: Merge und Hook-Pfade korrigieren**
  - Uid: e306e052-6d2c-44dc-bbe5-0a09d8d45bef.
  - Type: Task.
  - Parent: `STORY-022`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Governance.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Der Worktree-Ablauf funktioniert in einer isolierten
    Worktree-Session von Claude Code ohne Umweg, und die Hooks bewerten
    Dateien im Worktree so, als lägen sie im Projekt. Der Merge in den
    Haupt-Checkout läuft nach dem Verlassen des Worktrees, danach werden
    Worktree und Branch entfernt. Dateipfade unter
    `.claude/worktrees/<Name>/` werden relativ zu diesem Worktree bewertet.
  - Completion criteria: Der Skill `worktree` beschreibt einen Abschluss,
    den Claude Code nicht blockiert, und ein realer Change ist so
    durchgelaufen. Tests zeigen: Eine Doku-Änderung im Worktree zählt für
    den techdocs-Hook als Doku, und der Architektur-Hook verlangt für eine
    Datei im Worktree dieselben Regeln wie im Haupt-Checkout.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `EPIC-006` **Verifikationsnachweis & Umgang mit sensiblen Daten (Vorschlag)**
  - Uid: e3bd0781-9ccd-4b43-a5da-fd9a93ecd6cd.
  - Type: Epic.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Sicherheit.
  - Priority: Prospective.
  - Dependencies: None.
  - Goal: Festlegen, wie ein Testlauf/Verifikationsergebnis nachvollziehbar
    festgehalten wird (was wurde geprüft, mit welchem Ergebnis) und wie mit
    Geheimnissen/Zugangsdaten in Logs, Output und Dateien umgegangen wird,
    da beides in Agent_Harness fest verankert ist, bei Claude aber komplett
    fehlt.
  - Completion criteria: Ein Nachweis-Format für Verifikationsergebnisse
    existiert; eine Regel zum Umgang mit erkennbaren Geheimnissen in Output
    und Dateien ist dokumentiert und wurde mindestens einmal angewendet.
  - Resolution: Rejected by the project owner on 2026-09-24: merged into
    `EPIC-004`; TASK-019 became a task of `STORY-024`, STORY-016 a story of
    `EPIC-004`.

- `TASK-017` **update-Skill: Projekt-Config mit dem aktuellen Harness-Stand abgleichen**
  - Uid: e4e25200-5b98-4d88-8e87-bcb168ba0388.
  - Type: Task.
  - Parent: None.
  - Status: Completed.
  - Created: 2026-09-28.
  - Area: Konfiguration.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: `/claude-harness:update` gleicht die `.claude-harness/config.toml`
    des Projekts mit dem aktuellen Stand des Harness ab, also mit der
    Config-Vorlage (`plugin/templates/config.toml`) und den bekannten
    Schlüsseln in `harness_config.py`. Er trägt fehlende Abschnitte,
    Optionen, Module und die erklärenden Kommentare der Vorlage nach, damit
    die Config dem aktuellen Stand entspricht. Das gilt auch, wenn die
    Config-Version schon aktuell ist; der Abgleich hängt nicht mehr allein
    an `version` und `MIGRATIONS`. Neue Werte mit festem Standard setzt der
    Skill ohne Rückfrage. Nach Werten, die wirklich zu entscheiden sind,
    fragt er wie `init`, z. B. nach neuen Modulen oder danach, ob der
    Backlog über die API (`api`) oder direkt auf den Dateien (`files`)
    läuft.
  - Completion criteria: Auf ein Projekt, dessen Config Abschnitte,
    Optionen, Module oder Kommentare der aktuellen Vorlage nicht enthält,
    zeigt `update` die konkreten Ergänzungen und schreibt sie erst nach
    Freigabe. Bestehende Werte, eigene Kommentare und die Reihenfolge
    bleiben erhalten. Rückfragen gibt es nur für zu entscheidende Werte,
    darunter das Backlog-Backend, wenn `todo` aktiv ist. Beim Backend `api`
    prüft der Skill mit `backlog_api.py health`, ob der Server erreichbar
    ist, und meldet das Ergebnis. Auf eine vollständige Config meldet
    `update`, dass nichts zu tun ist, und ändert die Datei nicht. Das
    Ergebnis besteht die Config-Validierung. Die Config dieses Repos ist
    damit auf den aktuellen Stand gebracht. README/techdocs beschreiben das
    neue Verhalten.
  - Summary: `/claude-harness:update` soll die Einstellungen eines Projekts
    mit dem aktuellen Stand des Harness vergleichen und alles nachtragen,
    was fehlt: neue Optionen, Module und Erklärungen. Nur wo es wirklich
    etwas zu entscheiden gibt, zum Beispiel ob der Backlog über die
    ToDo-Viewer-API läuft, fragt es nach. Bisher prüft `update` nur die
    Versionsnummer der Config und ändert sonst nichts.
  - Resolution: Confirmed by the project owner on 2026-09-29.

- `EPIC-002` **Task-Zerlegung**
  - Uid: eb0bd752-781f-4371-9a61-8803252040f7.
  - Type: Epic.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Eine Heuristik festlegen, wann eine größere Aufgabe in unabhängig
    verifizierbare Teilaufgaben zerlegt wird und wann sie bewusst am Stück
    bleibt, angelehnt an das Dimensions-Prinzip aus Agent_Harness.
  - Completion criteria: Die Heuristik ist als Regel dokumentiert und wurde
    an mindestens einer realen, mittelgroßen Aufgabe erprobt.
  - Resolution: Rejected by the project owner on 2026-09-24: merged into
    `EPIC-004`; STORY-004 and STORY-005 moved there.

- `EPIC-005` **Dokumentation & Nachverfolgung**
  - Uid: ef6e90d3-2e6d-483f-acab-512ac1d01f86.
  - Type: Epic.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Technische Dokumentationspflichten, ein Daily-Development-Report
    und der Backlog-Lebenszyklus (dieses Dokument) sauber definieren, damit
    Entscheidungen und Fortschritt über Sessions hinweg nachvollziehbar
    bleiben.
  - Completion criteria: Alle drei Bausteine sind dokumentiert und werden
    bei laufender Arbeit tatsächlich gepflegt statt nur einmalig angelegt.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `STORY-036` **Backlog-Änderungen im API-Modus committen**
  - Uid: f05e288e-2442-4ee7-823f-dee7b11fa9c4.
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-28.
  - Area: Governance.
  - Priority: Normal.
  - Dependencies: `STORY-034`.
  - Goal: Der Worktree-Skill regelt, dass Backlog-Änderungen im API-Modus im
    Haupt-Checkout landen und dort vom Agenten mit eigenem Commit (`Backlog:
    …`) festgehalten werden; im Datei-Modus bleibt die Regel „im selben
    Branch“.
  - Completion criteria: `worktree`- und `todo`-Skill beschreiben beide Modi
    widerspruchsfrei; ein Merge des Worktrees kollidiert nicht mit
    Backlog-Änderungen im Haupt-Checkout.
  - Resolution: Vom Projektverantwortlichen am 2026-09-28 bestätigt.

- `TASK-012` **Skills, init und Worktree für Teilprojekte**
  - Uid: f18b7fb2-cabe-42c5-97c1-af8c2298fd7c.
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-007`.
  - Goal: Die Skills beschreiben die Arbeit mit mehreren Projekten, `init`
    kann Teilprojekte anlegen, und der Worktree übernimmt gitignorierte
    Teilprojekt-Dateien nachweislich.
  - Completion criteria: Skill-Texte und `init` sind angepasst und in einem
    Test-Repo einmal durchgespielt. Ein Test zeigt, dass `worktree.py start`
    eine gitignorierte Teilprojekt-Konfiguration spiegelt.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-012` **Technische Dokumentationspflicht definieren**
  - Uid: f25d8054-e6d2-4b42-81bf-f6f64f94ce13.
  - Type: Story.
  - Parent: `EPIC-005`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Dokumentation.
  - Priority: Prospective.
  - Dependencies: None.
  - Goal: Festlegen, welche Systemdokumente ein Projekt standardmäßig hat
    (z. B. README, Architektur, Schnittstellen, Konfiguration), welche Art
    von Änderung welches Dokument betrifft und wann eine Anpassung entfällt.
  - Completion criteria: Eine schlanke, pro Projekt anpassbare
    Standardstruktur mit Vorlagen liegt vor; eine klare Schwelle trennt
    dokumentationspflichtige von trivialen Änderungen; die Struktur ist in
    diesem Repo angewendet.
  - Summary: Der Harness legt fest, welche Dokumente beschreiben, wie ein
    Projekt aktuell aufgebaut ist und benutzt wird, und sorgt dafür, dass
    sie bei Änderungen mitgepflegt werden.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `TASK-015` **Einzelitem-Abruf in backlog.py für archive.md**
  - Uid: f472f425-6305-4902-807e-8a7e158ed41d.
  - Type: Task.
  - Parent: None.
  - Status: Completed.
  - Created: 2026-09-27.
  - Area: Dokumentation.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: `backlog.py` bekommt einen Modus, der ein einzelnes Item per ID
    aus `TODO.md` oder `archive.md` ausgibt, ohne die jeweilige Datei
    komplett einzulesen. Die Leseregel in `plugin/skills/todo/format.md`
    ("Read an archived item in full") wird darauf umgestellt, diesen Modus
    statt eines Volllesens von `archive.md` zu nutzen.
  - Completion criteria: `backlog.py <backlog-ordner> --show <ID>` (oder
    vergleichbare Option) gibt genau den Eintrag mit ID, Feldern und
    Freitext-Feldern (Goal, Completion criteria, Resolution) aus; Tests in
    `tests/test_backlog.py` decken den neuen Modus ab (gefundene ID,
    fehlende ID); `format.md` und `SKILL.md` verweisen auf den neuen Modus
    statt auf Volllesen von `archive.md`; `docs/techdocs/interfaces.md`
    beschreibt die neue Option.
  - Summary: Das Archiv soll nicht mehr als ganze Datei geladen werden. Erst
    kommt eine kurze Liste aller Einträge, danach werden nur die Einträge
    geöffnet, die gerade gebraucht werden.
  - Resolution: Vom Projektverantwortlichen am 2026-09-28 bestätigt.

- `STORY-003` **Module unabhängig aktivierbar/deaktivierbar machen**
  - Uid: fa282f4e-83ac-4822-93ef-cf00250772c9.
  - Type: Story.
  - Parent: `EPIC-001`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Konfiguration.
  - Priority: Prospective.
  - Dependencies: `STORY-001`, `STORY-018`.
  - Goal: Jedes Regelmodul (Testing, TDD, Daily-Report, Backlog, …) soll pro
    Projekt über eine Schalterliste in der Konfiguration ein- oder
    ausschaltbar sein. Alle Module liegen in einem Plugin; die Skills und
    Hooks eines abgeschalteten Moduls prüfen den Schalter und werden nicht
    aktiv.
  - Completion criteria: Ein abgeschaltetes Modul greift nachweislich nicht
    (seine Hooks tun nichts, sein Skill verweist auf den Schalter), ein
    eingeschaltetes Modul greift vollständig.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `TASK-005` **TDD-Ritual (Red/Green/Refactor)**
  - Uid: facdfffe-18d1-42af-9094-2b886607b9e2.
  - Type: Task.
  - Parent: `STORY-024`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `TASK-006`.
  - Goal: Festlegen, für welche Art von Änderungen der Test vor dem Code
    entsteht (TDD) und für welche nicht.
  - Completion criteria: Die Regeln stehen in der Skill
    `claude-harness:decomposition`; ein Plan-Abschnitt nennt, ob sein Test
    zuerst entsteht. Der Zyklus selbst wird nicht dokumentiert.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-049` **Helfer für Backlog, Notes und Wecker auf die neue Viewer-API umstellen**
  - Uid: 2ce085bd-4cec-4365-b046-a19fd2ccd8d6.
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-19.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: backlog_api.py und notes_api.py arbeiten wieder: Sie sprechen die
    neuen HTTP-Routen des Viewers (/api/backlog, /api/notes, /api/workspace,
    /api/alarms) an. Das Projekt kommt weiter deterministisch aus Config und
    Hauptarbeitskopie, Claude gibt es nie selbst an. Der Helfer gleicht
    Schwächen der Schnittstelle aus (Labels statt uids in parent und
    dependencies, Yes/No, unbekanntes Projekt als Fehler) und legt Projekte
    im Viewer nur auf ausdrücklichen Befehl an. Wecker kommen als neue
    Befehle und im Skill dazu.
  - Completion criteria: Alle bisherigen Befehle von backlog_api.py und
    notes_api.py laufen gegen den neuen Viewer; parent und dependencies
    nehmen Labels; ein unbekanntes oder nicht registriertes Projekt bricht
    mit klarer Meldung ab, statt still leer zu antworten oder ein Projekt
    anzulegen; Projekte werden nur mit einem eigenen Befehl nach Rückfrage
    registriert; Wecker lassen sich lesen, stellen, ändern, zurückstellen
    und erledigen; Session-Start, Config-Vorlage (api_url ohne /api/v2),
    Skills todo/notes und Techdocs beschreiben den neuen Stand; die
    Integrationstests sind umgestellt und grün; Lese-, Schreib- und
    Notizfluss sind gegen den laufenden Viewer geprüft.
  - Summary: Der Viewer-Neubau hat /api/v2 entfernt. Die Helfer werden auf
    die neue HTTP-API umgestellt; die Anbindung über MCP folgt später, wenn
    der MCP-Server im Viewer überarbeitet ist.
  - Resolution: Vom Projektverantwortlichen am 2026-10-19 bestätigt: Helfer
    für Backlog, Notes und Wecker laufen auf der neuen Viewer-API (v0.11.0).

- `TASK-022` **Kopf-Prüfsumme im Files-Modus**
  - Uid: 3d2a5e66-74c1-459a-8b7a-2b493a3c1995.
  - Type: Task.
  - Parent: `STORY-051`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-20.
  - Area: Entwicklung.
  - Priority: Urgent.
  - Dependencies: `TASK-021`.
  - Goal: backlog.py kann den Kopf einer Notes-Datei bestätigen und schreibt
    dabei den Stempel mit der Prüfsumme des Protokolls; die Backlog-Prüfung
    am Turn-Ende meldet Notes, deren Stempel nicht zum Protokoll passt.
  - Completion criteria: Bestätigungsbefehl und Prüfung sind umgesetzt und
    mit Unit-Tests abgedeckt (Kopf aktuell, veraltet, fehlend, Stempel ohne
    Kopfänderung gesetzt); Doku in format.md bzw. Techdocs aktualisiert.
  - Summary: Im Dateimodus kann der Harness die Übersicht einer Notes-Datei
    bestätigen und hält das Turn-Ende an, solange sie veraltet ist.
  - Resolution: Vom Owner am 2026-10-21 bestätigt.

- `TASK-021` **Notes-Regeln und Format im todo-Skill**
  - Uid: 5a3e2a33-b822-45e7-86c8-4678f5be0e3e.
  - Type: Task.
  - Parent: `STORY-051`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-20.
  - Area: Dokumentation.
  - Priority: Urgent.
  - Dependencies: None.
  - Goal: SKILL.md, format.md und api.md beschreiben den Aufbau der Notes
    (Kopf 'Stand' mit Stempel, darunter das Protokoll), die Rollen von Notes
    und Spec (Spec fortlaufend, am Ende geprüft) sowie die vom Owner
    beschlossenen Regeln 1–4 zu Ort, Inhalt und Zeitpunkt.
  - Completion criteria: Die Texte entsprechen der Spec von STORY-051;
    offene Regelpunkte sind vom Owner entschieden und eingearbeitet;
    funktionale Tests zu den Skill-Texten (falls vorhanden) laufen.
  - Summary: Die Regeln, wie Claude Besprechungen protokolliert und wie die
    Übersicht oben in den Notes aussieht, stehen jetzt in der Anleitung des
    Harness.
  - Resolution: Vom Owner am 2026-10-21 bestätigt.

- `TASK-025` **Nachfrage bei Notes an eine Story mit Kind in Arbeit**
  - Uid: 45d14f50-cb70-43f8-911c-57dd9c710f0e.
  - Type: Task.
  - Parent: `STORY-051`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-20.
  - Area: Entwicklung.
  - Priority: Urgent.
  - Dependencies: `TASK-021`.
  - Goal: Schreibt die LLM einen Notes-Eintrag an eine Story, während eines
    ihrer Kinder In progress ist, gibt der Helfer einen Hinweis aus ('TASK-x
    ist in Arbeit, gehört das dorthin?'). Der Eintrag wird trotzdem
    geschrieben (Prüfidee A, nur Nachfrage).
  - Completion criteria: 1. Hinweis in backlog_api.py (note, put-doc auf
    Notes) und im Files-Modus in der Backlog-Prüfung umgesetzt.
    2. Unit-Tests für Story mit/ohne Kind in Arbeit und für Tasks (kein
    Hinweis).
    3. Der Eintrag wird nie abgelehnt.
    4. Doku in api.md bzw. format.md.
  - Summary: Schreibt Claude Protokolle an eine Story, während einer ihrer
    Tasks in Arbeit ist, fragt der Harness nach, ob das dorthin gehört.
  - Resolution: Vom Owner am 2026-10-21 bestätigt.

- `TASK-023` **Kopf-Befehle im API-Helfer**
  - Uid: a62d3a80-a788-4d27-8a5f-e693881bc93f.
  - Type: Task.
  - Parent: `STORY-051`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-20.
  - Area: Entwicklung.
  - Priority: Urgent.
  - Dependencies: `TASK-021`.
  - Goal: backlog_api.py bietet Befehle zum Lesen des Kopfs (ohne
    Protokoll), zum Ersetzen und zum Bestätigen; note nimmt optional einen
    neuen Kopf mit; veraltete Köpfe meldet der Helfer. Voraussetzung ist die
    Umsetzung im ToDo-Viewer.
  - Completion criteria: Befehle sind umgesetzt, in api.md beschrieben und
    mit Unit-Tests gegen einen Test-Server bzw. Mock abgedeckt; die
    Schnittstelle stimmt mit der Umsetzung im ToDo-Viewer überein.
  - Summary: Im API-Modus kann der Harness die Übersicht einer Notes-Datei
    getrennt lesen, ersetzen und bestätigen.
  - Resolution: Vom Owner am 2026-10-22 bestätigt.

- `STORY-042` **Backlog-Backend je Umgebung umschalten**
  - Uid: 1632383e-cadd-4a3d-8b11-54032266fadc.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-16.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Das Backend des Backlogs (`api` oder `files`) lässt sich je
    Umgebung wählen, ohne die eingecheckte `.claude-harness/config.toml` zu
    ändern: lokal bleibt `api`, in einer Cloud-Session gilt `files`. Eine
    Umgebungsvariable überschreibt `[todo].backend`.
  - Completion criteria: 1. Die Umgebungsvariable
    `CLAUDE_HARNESS_TODO_BACKEND` (Werte `api`, `files`) überschreibt
    `[todo].backend` bei der Config-Auswertung; ein ungültiger Wert wird wie
    ein Config-Fehler gemeldet. 2. Sitzungsstart, Backlog-Hooks und Hinweise
    der Skills folgen dem wirksamen Backend. 3. Techdocs (Konfiguration) und
    der todo-Skill beschreiben die Variable. 4. Tests decken beide Backends
    und den Fehlerfall ab. 5. Die Cloud wird automatisch erkannt
    (Entscheidung des Besitzers, 2026-10-16): Ist `CLAUDE_CODE_REMOTE` auf
    `true` gesetzt, gilt der Dateimodus. Rangfolge:
    `CLAUDE_HARNESS_TODO_BACKEND` vor der Cloud-Erkennung vor
    `[todo].backend`.
  - Summary: Lokal arbeitet der Harness weiter über die API des
    ToDo-Viewers, in der Cloud automatisch über die Markdown-Dateien. Die
    gemeinsame Config bleibt dafür unverändert.
  - Resolution: Vom Besitzer bestätigt (2026-10-22).

- `STORY-047` **Harness als Kopie im Projekt für Cloud-Sessions bereitstellen**
  - Uid: c008f326-5e4c-4764-9381-8e2ddf6c4c20.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-16.
  - Area: Architektur.
  - Priority: Important.
  - Dependencies: None.
  - Goal: In einer Cloud-Session eines Projekts, in der das Plugin nicht
    geladen wird, stehen Regeln, Hooks und Skripte des Harness bereit, weil
    eine erzeugte Kopie davon im Projekt liegt und eingecheckt ist (Weg A,
    Beschluss des Besitzers vom 2026-10-16). `/claude-harness:init` und
    `/claude-harness:update` legen die Kopie an und halten sie aktuell.
    Lokal bleibt das Plugin maßgeblich; die Kopie darf dort nichts doppelt
    tun.
  - Completion criteria: 1. Die Belege stehen in den Notes: Die Cloud lädt
    das Plugin nicht, wohl aber CLAUDE.md, .claude/skills und die Hooks aus
    .claude/settings.json (in Sessions mit einem Repository); Python 3.13
    und CLAUDE_CODE_REMOTE=true sind dort gesetzt. 2. Ein Generator erzeugt
    aus plugin/ die Kopie im Projekt: Skills unter .claude/skills mit Präfix
    (kein Namenskonflikt mit eingebauten Skills, Querverweise und
    Pfadplatzhalter im Text ersetzt), Skripte und Vorlagen unter
    .claude-harness/, Hooks in .claude/settings.json (vorhandene Einträge
    bleiben erhalten). Kopiert wird nur plugin/, nie Backlog, Notes oder
    Tagesberichte des Harness-Repositories. 3. `/claude-harness:init`
    richtet die Kopie in einem neuen Projekt ein und
    `/claude-harness:update` aktualisiert sie, mit Diff und Freigabe vor dem
    Schreiben und einem Versionsvermerk, an dem eine veraltete Kopie
    erkennbar ist. 4. Lokal läuft nichts doppelt: Die eingecheckten Hooks
    beenden sich still, wenn sie nicht in einer Cloud-Session laufen. 5.
    Module, die in der Cloud nicht funktionieren (z. B. worktree), sind
    benannt und ausgenommen oder angepasst. 6. Techdocs und README
    beschreiben Einrichtung, Aktualisierung und die Grenzen (Hooks nur in
    Sessions mit einem Repository). 7. Ein Abnahmelauf in einer
    Cloud-Session mit einem Projekt, das die Kopie enthält, zeigt:
    Sitzungsstart-Hinweis, Backlog im Dateimodus und mindestens ein Hook
    wirken. 8. Die Kopie lässt sich einfach und vollständig wieder
    entfernen, damit das Projekt zum Stand ohne Cloud-Kopie zurückkehrt
    (etwa wenn wieder nur lokal gearbeitet wird): Ein Manifest listet alle
    erzeugten Dateien und Hook-Einträge; der Rückbau zeigt vorher, was
    entfällt, schreibt erst nach Freigabe, lässt von Hand geänderte Dateien
    stehen und meldet sie, und lässt fremde Einträge in
    .claude/settings.json unberührt. Ein Test beweist die Rundreise: Export,
    dann Rückbau ergibt denselben Dateistand wie vorher.
  - Summary: Lokal wird der Harness als Plugin geladen. In der Cloud liegt
    stattdessen eine von init und update erzeugte Kopie im Projekt, die mit
    eingecheckt wird und die Regeln, Prüfungen und Skripte dort
    bereitstellt.
  - Resolution: Vom Besitzer bestätigt (2026-10-22): Abnahmelauf der
    Cloud-Kopie in einer echten Cloud-Sitzung geprüft.

- `STORY-043` **Notes und Topics im Dateimodus führen**
  - Uid: 6e490502-1f99-4cba-8eb0-6985f5929ba7.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-16.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: `STORY-042`.
  - Goal: Notes und Topics lassen sich im Dateimodus (`backend = files`, z.
    B. in einer Cloud-Session) über den Ordner `notes/` im Backlog-Ordner
    führen, im Format des ToDo-Viewers (dessen Techdoc `interfaces.md`,
    Abschnitt Dateiformat Version 2: Notes und Topics). Der Viewer liest sie
    beim Sync in seine Datenbank.
  - Completion criteria: 1. Notes sind auch bei `files` aktiv
    (Config-Auswertung und Sitzungsstart-Zeile). 2. Der todo-Skill enthält
    eine Regeldatei für das Dateiformat (Version 2) und die Befugnis: Notes
    anlegen als `new-<kurzname>.md` mit erster Zeile `# NEW`, neue Topics
    als `Topic: new:<Name>` bzw. `NEW`-Zeile in `topics.md`, Zeiten in UTC
    mit `Z`; Labels, `Uid` und der Auslöser-Zustand `fired` gehören dem
    Viewer und werden nicht von Hand gesetzt; es gibt nur die Auslöser
    `event` und `topic_due`, eine `time`-Zeile ist ein Formatfehler. 3. Ein
    Index-Helfer für `notes/` (Gegenstück zu `backlog.py --index`) listet
    Label, Status, Review, Topic und Summary, ohne alle Dateien zu lesen. 4.
    Fälligkeit ohne Viewer ist geregelt: nur auf Nachfrage werden `Review`
    und das Datum des Topics mit dem heutigen Datum verglichen; Zeitpunkte
    sind Sache der Wecker und kommen hier nicht vor. 5. Die Regeln für `api`
    und `files` sind getrennt; die Aussage, Notes seien privat und nie im
    Repository, gilt nur für `api`, und die Dateivariante weist darauf hin,
    dass die Notes dann im Repository (GitHub) liegen. 6. Techdocs und
    README beschreiben Notes im Dateimodus; Tests decken den Helfer ab.
  - Summary: Auch in der Cloud lassen sich Erinnerungen und Notizen führen:
    als Markdown-Dateien im Repository, die der ToDo-Viewer später in seine
    Datenbank übernimmt.
  - Resolution: Vom Besitzer bestätigt (2026-10-22).

- `STORY-044` **Formatprüfung für den Notes-Ordner**
  - Uid: 452b2474-a5e3-428c-b8cf-6a43fa6f62a5.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-16.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: `STORY-043`.
  - Goal: Eine Prüfung findet Formatfehler in den Dateien unter `notes/`
    (Dateimodus), bevor der ToDo-Viewer sie liest. Der Viewer bricht bei
    einem einzigen Formatfehler den ganzen Sync ab (400 `note_format`,
    Backlog und Notes), deshalb muss der Fehler schon beim Schreiben
    auffallen.
  - Completion criteria: 1. Ein Prüfskript (Stop-Hook wie
    `check_backlog.py`, nur bei `files` und nur nach Änderungen unter
    `notes/`) prüft den ganzen Ordner `notes/` nach den Regeln des Decoders
    von Format Version 2 und meldet Datei, Zeile und Fehlercode bei:
    unbekannter, doppelter oder ungültiger Kopfzeile, fehlenden
    Pflichtfeldern, ungültigem Status (auch `due`), `Mode`, `Archived` oder
    Zeitpunkt, Dateiname und Überschrift verschieden, ungültigem
    Platzhalter, ungültigem Auslöser (auch `time`) oder ungültiger
    Verknüpfung, falschem Zeilenaufbau in `topics.md`, doppelter Uid,
    doppeltem Label oder doppeltem Platzhalter und Git-Merge-Markern;
    Dokumente der Notes nur auf Dateiname und zugehörige Note. 2. Die
    Beispiele des Viewers liegen als Testvorlagen im Harness
    (`tests/fixtures/`, aus `tests/fixtures/mirror-v2` des ToDo-Viewers):
    `valid/notes` wird fehlerfrei gelesen, die Notes-Fehlerfälle `invalid/`
    ergeben den erwarteten Code, die Datei und die Zeile; zu jedem
    Fehlercode gibt es einen Test. 3. Weicht das Format des Viewers von der
    Prüfung ab, ist der Unterschied in den Notes der Story festgehalten;
    `counters.md` gibt es in Version 2 nicht und wird nicht geprüft. Die
    Regeldatei `notes-files.md` ist berichtigt (Status `due` steht nie in
    einer Datei) und `notes_files.py` übergeht keine `new-`-Datei mit
    Großbuchstaben mehr. 4. Techdocs beschreiben die Prüfung.
  - Summary: Ein Tippfehler in einer Notes-Datei würde sonst den ganzen
    Abgleich mit dem ToDo-Viewer blockieren. Die Prüfung meldet ihn sofort
    mit Datei und Zeile.
  - Resolution: Vom Besitzer bestätigt (2026-10-22).

- `STORY-045` **Ablauf zwischen Cloud, Git und lokalem Viewer festlegen**
  - Uid: dfc1d2ff-773e-4c7f-87d6-d312bf19de67.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-16.
  - Area: Governance.
  - Priority: Normal.
  - Dependencies: `STORY-042`, `STORY-043`.
  - Goal: Der todo-Skill beschreibt, wie Backlog und Notes zwischen einer
    Cloud-Sitzung (Dateien im Repository) und dem lokalen ToDo-Viewer
    (Datenbank) wandern, und widerspricht dabei nicht den Regeln des
    API-Modus.
  - Completion criteria: 1. Der Skill beschreibt den Ablauf vor der
    Cloud-Sitzung: Viewer-Sync, dann den Backlog-Ordner samt `notes/`
    committen und pushen. 2. Er beschreibt die Cloud-Seite im Dateimodus:
    Änderungen an Backlog und Notes gehören zur Änderung und liegen im
    Branch der Sitzung. 3. Er beschreibt den Rückweg: Branch mergen, lokal
    holen, Viewer-Sync (Auto-Sync oder Dialog), Konflikte im Dialog
    entscheiden; bei Merge-Markern in einer Datei pausiert der Auto-Sync,
    und die Marker sind zuerst zu lösen. 4. Er nennt die Voraussetzung im
    Viewer (Spiegel-Ordner ist der Backlog-Ordner des Repositorys, Auto-Sync
    an). 5. Die Regeln des API-Modus sind abgeglichen: Bei aktivem Spiegel
    werden auch die Dateien unter `notes/` committet (bisher steht dort,
    dass nichts committet wird), `TODO.md` und `archive.md` bleiben für die
    KI lokal unangetastet. 6. Der Ablauf ist einmal von Anfang bis Ende
    durchgespielt (die Cloud-Seite darf von Hand nachgestellt sein, solange
    keine Cloud-Umgebung zur Verfügung steht); das Ergebnis steht in den
    Notes. 7. Techdocs und README beschreiben den Ablauf.
  - Summary: Klare Schritte, wie der Stand zwischen Cloud und dem lokalen
    ToDo-Viewer hin und her wandert, damit nichts verloren geht und lokal
    weiter nur die API genutzt wird.
  - Resolution: Vom Besitzer bestätigt (2026-10-22).

- `STORY-046` **Doppelt vergebene IDs bei paralleler Arbeit in Cloud und lokal vermeiden**
  - Uid: 6d64c87c-b4c2-48bf-8c2e-2563ec768a95.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-16.
  - Area: Governance.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Legen die Cloud (Dateimodus, nächste freie Nummer) und der lokale
    Viewer (Datenbank vergibt die ID) unabhängig voneinander ein Item
    gleichen Typs an, geht dabei kein Item verloren. Für Notes löst das
    schon das Verfahren mit `new-<kurzname>.md`, für Backlog-Items gibt es
    keines.
  - Completion criteria: 1. Geprüft und in den Notes festgehalten ist, wie
    der Viewer zwei unabhängig angelegte Items mit gleicher ID beim Sync
    behandelt (laut seiner Doku ein Konflikt `both_new`, bei dem nur eine
    Seite übernommen wird). 2. Die Entscheidung steht in den Notes: Regel im
    Skill (z. B. während einer Cloud-Sitzung lokal keine neuen Items
    gleichen Typs anlegen) oder Erweiterung des Viewers (vorläufige IDs für
    Items wie bei den Notes), jeweils mit Begründung. 3. Umgesetzt ist die
    gewählte Lösung: bei einer Regel im todo-Skill und in den Techdocs
    beschrieben; bei einer Viewer-Erweiterung ein Item im Backlog des
    ToDo-Viewers angelegt (mit Freigabe des Besitzers) und der Skill
    verweist darauf.
  - Summary: Verhindert, dass ein in der Cloud angelegter Eintrag beim
    Abgleich mit dem ToDo-Viewer verloren geht, wenn lokal gleichzeitig ein
    Eintrag mit derselben Nummer entsteht.
  - Resolution: Vom Besitzer bestätigt (2026-10-22).

- `TASK-024` **Hooks für aktuellen Notes-Kopf und Protokoll-Reminder**
  - Uid: 93bf2558-2beb-4088-9d63-c4e980a0fac4.
  - Type: Task.
  - Parent: `STORY-051`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-10-20.
  - Area: Entwicklung.
  - Priority: Urgent.
  - Dependencies: `TASK-022`, `TASK-023`.
  - Goal: Ein Hook am Turn-Ende blockiert, solange Notes, die in der Session
    geändert wurden, einen veralteten Kopf haben, bis der Kopf angepasst
    oder bestätigt ist (API- und Files-Modus). Ein Reminder (Prüfidee B)
    erinnert, wenn ein aktives Item seit mehreren Turns keinen Notes-Eintrag
    bekam.
  - Completion criteria: Beide Hooks sind umgesetzt, in der
    Plugin-Konfiguration registriert, in der Doku beschrieben und getestet
    (Unit-Tests; Endlosschleife ausgeschlossen, weil Bestätigen den Hook
    auflöst).
  - Summary: Ein Hook sorgt dafür, dass die Übersicht nach jeder Änderung
    der Notes geprüft wird, und erinnert ans Protokollieren.
  - Resolution: Vom Besitzer bestätigt (2026-10-22).

- `STORY-051` **todo-Skill: Ort und Inhalt der Diskussionsprotokolle (Notes) festlegen**
  - Uid: 3b18df8f-3832-4a6b-a090-51a845d0cabd.
  - Type: Story.
  - Parent: None.
  - Status: Completed.
  - Created: 2026-10-19.
  - Area: Dokumentation.
  - Priority: Urgent.
  - Dependencies: None.
  - Goal: Der todo-Skill legt Ort, Inhalt, Zeitpunkt und Aufbau der
    Item-Notes fest: Kopf mit dem geltenden Stand, darunter das Protokoll;
    die Spec wird fortlaufend geschrieben. Der Harness stellt mechanisch
    sicher, dass der Kopf nach jeder Änderung der Notes geprüft wird.
  - Completion criteria: Die beschlossenen Regeln stehen im todo-Skill und
    in format.md; die Prüfsumme des Kopfs wird in API- und Files-Modus
    gesetzt und geprüft; der Hook am Turn-Ende und der Reminder B sind
    umgesetzt und getestet; die Schnittstelle zum ToDo-Viewer ist
    beschrieben und dort umgesetzt.
  - Summary: Claude schreibt Besprechungen bisher teils ins falsche Item, zu
    knapp, und lange Notes sind unübersichtlich. Künftig regelt der Harness,
    wo und wie protokolliert wird; jede Notes-Datei bekommt oben eine
    Übersicht über den aktuellen Stand, deren Aktualität der Harness prüft.
  - Resolution: Vom Besitzer bestätigt (2026-10-22). Harness-Release
    v0.12.6.

- `STORY-056` **Pflege-Erinnerung bei Änderungen an öffentlichen APIs**
  - Uid: 294b00b7-5b95-4b5b-8f26-abf5c6633557.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Completed.
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
  - Resolution: Vom Besitzer am 2026-11-05 bestätigt; umgesetzt und in main
    gemergt (bis v0.13.0), Tests grün, Gesamtablauf in einem Testprojekt
    geprüft.

- `STORY-053` **Architektur-Scopes in Unterordnern**
  - Uid: 49348b4e-d877-4cbc-813c-8d068de5a3da.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Completed.
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
  - Resolution: Vom Besitzer am 2026-11-05 bestätigt; umgesetzt und in main
    gemergt (bis v0.13.0), Tests grün, Gesamtablauf in einem Testprojekt
    geprüft.

- `STORY-055` **Tote Verweise in Architektur- und Doku-Dateien melden**
  - Uid: 5c30c318-d0a8-4b84-a1df-5d5cc56eb171.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Completed.
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
  - Resolution: Vom Besitzer am 2026-11-05 bestätigt; umgesetzt und in main
    gemergt (bis v0.13.0), Tests grün, Gesamtablauf in einem Testprojekt
    geprüft.

- `STORY-054` **Pflichtlektüre je Scope**
  - Uid: 9754a82d-0d7e-472f-b8e2-a711e50332ab.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Completed.
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
  - Resolution: Vom Besitzer am 2026-11-05 bestätigt; umgesetzt und in main
    gemergt (bis v0.13.0), Tests grün, Gesamtablauf in einem Testprojekt
    geprüft.

- `STORY-057` **Pflichtlektüre bei Nutzung bestimmter Bezeichner**
  - Uid: e744462d-cc77-4222-b1be-40ab8ce00aca.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Completed.
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
  - Resolution: Vom Besitzer am 2026-11-05 bestätigt; umgesetzt und in main
    gemergt (bis v0.13.0), Tests grün, Gesamtablauf in einem Testprojekt
    geprüft.

- `STORY-058` **Schnittstellen-Doku, Vorlagen und Skill-Regeln für den Doku-Baum**
  - Uid: 9733d627-cae7-47e2-81dd-ea8dfe5342d0.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: Yes.
  - Status: Completed.
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
  - Resolution: Vom Besitzer am 2026-11-05 bestätigt; umgesetzt und in main
    gemergt (bis v0.13.0), Tests grün, Gesamtablauf in einem Testprojekt
    geprüft.

- `STORY-059` **Techdocs als Zusammenfassung der development-Doku**
  - Uid: af537863-8cbf-4786-879c-1a3eff58b8a9.
  - Type: Story.
  - Parent: `EPIC-011`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-11-05.
  - Area: Dokumentation.
  - Priority: Prospective.
  - Dependencies: `STORY-058`.
  - Goal: Eine allgemeine Regel für alle Projekte: Die Techdocs (für
    Menschen, in docs.language) sind eine zusammenfassende Übersicht.
    Elemente, die die englische development-Doku beschreibt, werden
    zusammengefasst und verlinkt statt dupliziert; ohne development-Doku
    beschreiben die Techdocs sie vollständig. Die README verweist auf alle
    Techdocs.
  - Completion criteria: 1. Skill techdocs regelt je Dokument, was
    zusammenfasst und verlinkt (architecture, interfaces) und was
    vollständig bleibt (README, configuration, operations), sowie die
    schrittweise Umstellung bestehender Projekte.
    2. Die README verweist auf alle vorhandenen Techdocs; Skill und Vorlage
    readme.md sagen das.
    3. Die Vorlagen architecture.md und interfaces.md der Techdocs sind
    angepasst (Übersicht mit Links).
    4. Eine Änderung unter development/interfaces zählt für die
    Techdocs-Erinnerung als Doku-Pflege; Unit-Tests decken das ab.
    5. Techdocs des Harness beschreiben das geänderte Verhalten der
    Erinnerung.
  - Summary: Später: Die Doku für Menschen soll die Doku für die AI
    zusammenfassen und darauf verweisen, statt sie doppelt zu führen.
  - Resolution: Vom Besitzer am 2026-11-05 bestätigt; umgesetzt und in main
    gemergt (v0.13.1), 796 Tests grün.

- `EPIC-011` **Hierarchische Architektur- und Schnittstellen-Doku für die AI**
  - Uid: 37382d27-0b2a-4d59-b52f-4401524a99b2.
  - Type: Epic.
  - Status: Completed.
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
  - Resolution: Vom Besitzer am 2026-11-05 bestätigt; STORY-053 bis
    STORY-059 umgesetzt (v0.12.9 bis v0.13.1), Gesamtablauf in einem
    Testprojekt geprüft.

- `STORY-060` **Notes heißen Memos: Harness an den umbenannten Viewer anpassen**
  - Uid: b14b4a8c-5f7c-4c38-8f3e-fb90b681f663.
  - Type: Story.
  - Parent: `EPIC-008`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-11-12.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Der Harness arbeitet mit Memos, Topics und Hints des ToDo-Viewers
    (ab 0.10.0) über die Routen /api/memos, im Dateimodus mit dem Ordner
    memos/. Der Begriff Note bezeichnet im Harness nur noch die Notiz zu
    einem Backlog-Item.
  - Completion criteria: 1. Der Helfer für Memos (memos_api.py) nutzt die
    Routen /api/memos/… und die neuen Feldnamen (memos, memo_count, hints,
    active_memos); notices heißt hints.
    2. Dateimodus (memos_files.py, memos_format.py): Ordner memos/, Dateien
    MEMO-…, Verweise memo:.
    3. Sitzungsstart, Konfiguration und der Hook für geänderte
    Backlog-Dateien sprechen von Memos und erkennen den Ordner memos/.
    4. Der todo-Skill (memos.md, memos-api.md, memos-files.md, SKILL.md,
    sync-flow.md, format.md, alarms.md) benutzt Memo und Hint; Item-Notizen
    sind klar abgegrenzt.
    5. Tests und Fixtures sind umbenannt und grün; Techdocs sind
    nachgezogen.
    6. Die Kopie des Harness im Projekt ist neu exportiert, falls vorhanden,
    und der alte Ordner docs/todo/notes/ ist entfernt.
  - Summary: Umstellung des Harness auf die Begriffe Memo und Hint des
    ToDo-Viewers ab 0.10.0.
  - Resolution: Vom Owner am 2026-11-12 bestätigt; umgesetzt in Release
    v0.14.0.

- `STORY-052` **Branch-Stand beim Start einer Cloud-Session mit origin abgleichen**
  - Uid: 3b72b84e-cf3a-43f0-b071-d6d79331e4f1.
  - Type: Story.
  - Parent: `EPIC-010`.
  - Required for parent: Yes.
  - Status: Completed.
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
  - Resolution: Vom Owner am 2026-11-12 abgeschlossen. Kriterien 1 bis 6
    erfüllt (v0.12.8). Kriterium 7: in einer frischen Cloud-Session
    Schweigen bei gleichem Stand gesehen, der Vorspul-Fall wurde nicht
    belegt; der Owner meldet sich, falls der Abgleich in der Praxis nicht
    funktioniert.
