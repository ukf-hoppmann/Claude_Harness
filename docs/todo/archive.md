# Project Backlog Archive

Completed and rejected work items, moved unchanged from `TODO.md` after the
project owner's decision.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `EPIC-001` **Konfigurierbarer Harness (Policy)**
  - Type: Epic.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Eine projekteigene Konfigurationsdatei für das Claude_Harness-Plugin
    definieren, die nur echte Projektwerte enthält (Pfade, Sprache, aktive
    Module) und von Skills und Hooks gelesen wird. Weitere Felder bringt jedes
    Modul selbst mit. Genehmigungen und Rechte bleiben bei den nativen
    Claude-Code-Einstellungen.
  - Completion criteria: Das Konfigurationsschema ist validiert und
    dokumentiert und wird von den Hooks mehrerer Module tatsächlich gelesen und
    angewendet.
  - Summary: Jedes Projekt bekommt eine kleine Einstellungsdatei, in der steht,
    wo Dinge liegen, wie getestet wird und welche Harness-Teile an sind.
  - Notes: `items/EPIC-001/EPIC-001_notes.md`.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-022` **Change-Workflow im Worktree**
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
    den Worktree. Changes ohne Plan laufen lokal. So kann parallel gearbeitet
    werden, ohne dass fremde Worktrees angefasst werden.
  - Completion criteria: Der Ablauf ist als Teilbereich der Suite
    `development` umgesetzt (Schalter, Session-Start-Hinweis, Skill) und
    getestet. Ein realer Change mit Plan ist vom Ausgangsbranch über Worktree,
    Merge-Commit und Löschen des Worktrees ohne Rückfrage durchgelaufen;
    Worktrees anderer Sessions blieben unberührt.
  - Summary: Größere Änderungen macht die AI in einer eigenen Arbeitskopie
    und führt sie danach selbst in den Branch zurück, von dem sie gestartet
    ist. Die früheren Tasks TASK-001 bis TASK-004 sind in der Spec
    aufgegangen.
  - Notes: `items/STORY-022/STORY-022_notes.md`.
  - Spec: `items/STORY-022/STORY-022_spec.md`.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `TASK-014` **Abgelehnte Pflicht-Kinder im Backlog-Lebenszyklus klären**
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
    Pflicht-Kinder abgeschlossen sind; eine abgelehnte Pflicht-Task blockiert
    den Parent damit dauerhaft.
  - Completion criteria: Die Regel für abgelehnte Pflicht-Kinder ist
    entschieden, in `format.md` beschrieben und im Prüfskript umgesetzt.
    Tests decken `Awaiting confirmation` und `Completed` mit abgelehnten
    Pflicht-Kindern ab, und die Meldungen benennen den Status richtig.
  - Summary: Das Backlog-Prüfskript und die Formatbeschreibung widersprechen
    sich, wenn eine Pflicht-Aufgabe abgelehnt wurde. Das wird vereinheitlicht.
  - Notes: `items/TASK-014/TASK-014_notes.md`.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-027` **Harness pro Teilprojekt**
  - Type: Story.
  - Parent: `EPIC-001`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Ein Repository kann mehrere Teilprojekte mit je eigener
    Harness-Konfiguration, Doku, Backlog und Architekturregeln enthalten
    (z. B. Plugin-Core im Root, jedes Plugin in seinem Ordner). Startet die
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
    Teile gelten können, z. B. für ein einzelnes Plugin, mit eigener Doku und
    eigenen Regeln, ohne dass Kollegen im Repo-Root etwas davon sehen.
  - Notes: `items/STORY-027/STORY-027_notes.md`.
  - Spec: `items/STORY-027/STORY-027_spec.md`.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `TASK-008` **Architekturregeln pro Projekt**
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-007`.
  - Goal: Die Architektur-Hooks verlangen die Regeln des Projekts, zu dem die
    geänderte Datei, die Spec oder der Plan gehört.
  - Completion criteria: Tests zeigen: Eine Änderung im Teilprojekt verlangt
    dessen Regeln, eine Änderung im Core die Root-Regeln. Ein Plan verlangt
    die Regeln jedes darin genannten Projekts.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `TASK-009` **Geerbte Architekturregeln**
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

- `TASK-010` **Backlog und techdocs pro Projekt**
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

- `TASK-011` **Daily Reports pro Projekt**
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `TASK-007`.
  - Goal: Jedes Projekt hat eigene Daily Reports mit eigenem
    Bestätigungsstand. Ein Commit zählt nur für das Projekt, dessen Dateien er
    ändert, auch wenn das Git-Root über dem Projekt liegt.
  - Completion criteria: Tests zeigen: Ein Commit nur in einem Teilprojekt
    erscheint nur in dessen Daily. Ein reiner Backlog-Commit zählt nirgends.
    Beim Start im Teilprojekt mit Git-Root darüber zählen Commits außerhalb
    nicht. `daily.py --project` funktioniert.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `TASK-012` **Skills, init und Worktree für Teilprojekte**
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

- `TASK-013` **Worktree-Ablauf: Merge und Hook-Pfade korrigieren**
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

- `TASK-007` **Registry und Projektzuordnung**
  - Type: Task.
  - Parent: `STORY-027`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-25.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Die Root-Konfiguration kann Teilprojekte in `[projects]` eintragen.
    Ein gemeinsamer Helfer lädt alle Projekte und ordnet jede Datei ihrem
    Projekt zu. Der Session-Start listet die Projekte und meldet
    Registry-Fehler.
  - Completion criteria: Schema, Validierung, Doku in `configuration.md` und
    Tests sind vorhanden. Der Session-Start zeigt in einem Test-Repo mit zwei
    Teilprojekten alle Projekte und meldet ein ungültiges Teilprojekt, ohne
    die anderen unwirksam zu machen. Ohne `[projects]` ist die Ausgabe
    unverändert.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-018` **Plugin-Grundgerüst**
  - Type: Story.
  - Parent: `EPIC-007`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Architektur.
  - Priority: Urgent.
  - Dependencies: None.
  - Goal: Die Plugin-Struktur anlegen (Manifest, Ordner für Skills und Hooks)
    und das Plugin in diesem Repo selbst aktivieren.
  - Completion criteria: Claude Code erkennt das Plugin in diesem Repo; ein
    Test-Skill ist aufrufbar und ein Test-Hook wird nachweislich ausgelöst.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `STORY-002` **Policy laden und validieren**
  - Type: Story.
  - Parent: `EPIC-001`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: `STORY-001`, `STORY-018`.
  - Goal: Die Konfigurationsdatei beim Session-Start per Hook einlesen und gegen
    das Schema prüfen, damit Fehler auffallen, bevor ein Verify- oder
    Change-Vorgang startet.
  - Completion criteria: Ein fehlerhafter oder unvollständiger
    Konfigurationswert wird beim Session-Start erkannt und klar gemeldet statt
    stillschweigend ignoriert zu werden.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `STORY-020` **TODO-Modul als Skill und Hook**
  - Type: Story.
  - Parent: `EPIC-007`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: `STORY-018`, `STORY-017`.
  - Goal: Die Backlog-Regeln aus `TODO.md` in einen `todo`-Skill überführen und
    die Formatprüfung als Hook umsetzen; der Kopf von `TODO.md` wird auf einen
    Verweis gekürzt.
  - Completion criteria: Ein fehlerhafter Eintrag wird vom Hook gemeldet; bei
    einer Aufgabe ohne Backlog-Bezug wird der Skill nicht geladen.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `STORY-017` **Backlog-Format/Aufbau festlegen**
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
  - Completion criteria: Ein dokumentierter Aufbau-Standard liegt vor, an dem
    sich jeder neue Eintrag ohne Rückfrage orientieren kann.
  - Summary: Die Struktur steht und ist im Plugin: Hauptliste, Archiv und pro
    Aufgabe bei Bedarf Notizen und technische Beschreibung. Dazu Regeln für den
    Abschluss von Epics/Stories und für das Einordnen neuer Aufgaben.
  - Notes: `items/STORY-017/STORY-017_notes.md`.
  - Spec: `items/STORY-017/STORY-017_spec.md`.
  - Resolution: Confirmed by the project owner on 2026-09-23 (after reopening on the same day).

- `STORY-013` **Daily-Development-Report**
  - Type: Story.
  - Parent: `EPIC-005`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Dokumentation.
  - Priority: Prospective.
  - Dependencies: None.
  - Goal: Format und Materialitätskriterium für einen Tagesbericht festlegen,
    der nur bei tatsächlich relevanter Arbeit entsteht (nicht bei jeder
    kleinen Änderung).
  - Completion criteria: Ein Beispieltag mit relevanter Arbeit erzeugt einen
    Report; ein Tag ohne relevante Arbeit erzeugt keinen.
  - Summary: Ein optionales Modul schreibt pro Arbeitstag einen deutschen
    Bericht über die relevanten Änderungen, mit Verweisen auf Backlog und
    Commits. Ein Hook erinnert nach Änderungen daran, ihn aktuell zu halten.
  - Notes: `items/STORY-013/STORY-013_notes.md`.
  - Spec: `items/STORY-013/STORY-013_spec.md`.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `STORY-014` **Backlog-Lebenszyklus verfeinern**
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

- `STORY-012` **Technische Dokumentationspflicht definieren**
  - Type: Story.
  - Parent: `EPIC-005`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Dokumentation.
  - Priority: Prospective.
  - Dependencies: None.
  - Goal: Festlegen, welche Systemdokumente ein Projekt standardmäßig hat
    (z. B. README, Architektur, Schnittstellen, Konfiguration), welche Art von
    Änderung welches Dokument betrifft und wann eine Anpassung entfällt.
  - Completion criteria: Eine schlanke, pro Projekt anpassbare
    Standardstruktur mit Vorlagen liegt vor; eine klare Schwelle trennt
    dokumentationspflichtige von trivialen Änderungen; die Struktur ist in
    diesem Repo angewendet.
  - Summary: Der Harness legt fest, welche Dokumente beschreiben, wie ein
    Projekt aktuell aufgebaut ist und benutzt wird, und sorgt dafür, dass sie
    bei Änderungen mitgepflegt werden.
  - Notes: `items/STORY-012/STORY-012_notes.md`.
  - Spec: `items/STORY-012/STORY-012_spec.md`.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `EPIC-005` **Dokumentation & Nachverfolgung**
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
  - Completion criteria: Alle drei Bausteine sind dokumentiert und werden bei
    laufender Arbeit tatsächlich gepflegt statt nur einmalig angelegt.
  - Resolution: Confirmed by the project owner on 2026-09-23.

- `EPIC-002` **Task-Zerlegung**
  - Type: Epic.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Eine Heuristik festlegen, wann eine größere Aufgabe in unabhängig
    verifizierbare Teilaufgaben zerlegt wird und wann sie bewusst am Stück
    bleibt, angelehnt an das Dimensions-Prinzip aus Agent_Harness.
  - Completion criteria: Die Heuristik ist als Regel dokumentiert und wurde an
    mindestens einer realen, mittelgroßen Aufgabe erprobt.
  - Resolution: Rejected by the project owner on 2026-09-24: merged into `EPIC-004`; STORY-004 and STORY-005 moved there.

- `EPIC-003` **Change-Workflow (Workspace, Ablauf, Cleanup)**
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
  - Resolution: Rejected by the project owner on 2026-09-24: merged into `EPIC-004` as `STORY-022`; STORY-006, STORY-007, STORY-008 (renamed to TASK-002, TASK-003, TASK-004 on 2026-09-24) and TASK-001 became its tasks.

- `STORY-001` **Policy-Schema definieren**
  - Type: Story.
  - Parent: `EPIC-001`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Die Projektkonfiguration `.claude-harness/config.toml` festlegen:
    Grundfelder (Version, Doku-Wurzel, Sprache, Modulschalter) und die Regel,
    dass jedes Modul seine Felder selbst ergänzt, in `configuration.md`
    dokumentiert und ihre Validierung testet. Kein Approval-Modus.
  - Completion criteria: Ein dokumentiertes Schema (Ort, Felder, Typen, Pflicht
    vs. optional, Standardwerte) liegt vor und deckt alle bestehenden Module
    ab.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-003` **Module unabhängig aktivierbar/deaktivierbar machen**
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
    ausschaltbar sein. Alle Module liegen in einem Plugin; die Skills und Hooks
    eines abgeschalteten Moduls prüfen den Schalter und werden nicht aktiv.
  - Completion criteria: Ein abgeschaltetes Modul greift nachweislich nicht
    (seine Hooks tun nichts, sein Skill verweist auf den Schalter), ein
    eingeschaltetes Modul greift vollständig.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `EPIC-006` **Verifikationsnachweis & Umgang mit sensiblen Daten (Vorschlag)**
  - Type: Epic.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Sicherheit.
  - Priority: Prospective.
  - Dependencies: None.
  - Goal: Festlegen, wie ein Testlauf/Verifikationsergebnis nachvollziehbar
    festgehalten wird (was wurde geprüft, mit welchem Ergebnis) und wie mit
    Geheimnissen/Zugangsdaten in Logs, Output und Dateien umgegangen wird, da
    beides in Agent_Harness fest verankert ist, bei Claude aber komplett
    fehlt.
  - Completion criteria: Ein Nachweis-Format für Verifikationsergebnisse
    existiert; eine Regel zum Umgang mit erkennbaren Geheimnissen in Output
    und Dateien ist dokumentiert und wurde mindestens einmal angewendet.
  - Resolution: Rejected by the project owner on 2026-09-24: merged into `EPIC-004`; STORY-015 became a task of `STORY-024`, STORY-016 a story of `EPIC-004`.

- `STORY-021` **Harness in Projekten initialisieren**
  - Type: Story.
  - Parent: `EPIC-007`.
  - Required for parent: No.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Architektur.
  - Priority: Important.
  - Dependencies: `STORY-018`.
  - Goal: Ein Befehl `/claude-harness:init` richtet den Harness in einem
    Projekt ein: Er legt `.claude-harness/config.toml` aus einer Vorlage an und
    bietet bei aktivem `todo`-Modul an, den Backlog aus Vorlagen anzulegen —
    jeweils erst nach Freigabe und ohne Bestehendes zu überschreiben.
  - Completion criteria: In einem Projekt ohne Harness entstehen nach dem
    Befehl und Freigabe eine gültige Config und ein gültiger leerer Backlog; in
    einem bereits eingerichteten Projekt wird nichts verändert.
  - Summary: In my_story_game getestet: Einrichtung nach Rückfragen
    erfolgreich, ein zweiter Aufruf ändert nichts. Zwei kleine
    Verbesserungsideen stehen in den Notizen.
  - Notes: `items/STORY-021/STORY-021_notes.md`.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-019` **Ladestufen-Regel festlegen**
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
  - Completion criteria: Die Regel ist dokumentiert, und für jedes bestehende
    Modul ist nachvollziehbar, auf welcher Stufe es liegt und warum.
  - Summary: Regel, wohin neue Harness-Regeln gehören (Hook, Scope, Skill,
    Skript oder Root-`CLAUDE.md`), steht in den Architekturregeln; die
    Systemdoku zeigt für jedes Modul, wo es liegt und warum.
  - Notes: `items/STORY-019/STORY-019_notes.md`.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `EPIC-007` **Plugin-Architektur**
  - Type: Epic.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Architektur.
  - Priority: Urgent.
  - Dependencies: None.
  - Goal: Claude_Harness als Claude-Code-Plugin aufbauen, in dem die Module
    als Skills und die harten Regeln als Hooks umgesetzt sind, sodass Regeln
    gestuft geladen werden und bei unbeteiligten Aufgaben kaum Tokens kosten.
  - Completion criteria: Das Plugin ist in diesem Repo aktiv, mindestens ein
    Modul läuft als Skill mit zugehörigem Hook, und die Root-`CLAUDE.md`
    enthält nur Verweise statt Regeltexten.
  - Summary: Der Harness wird ein Zusatzpaket für Claude Code. Regeln werden
    nur dann geladen, wenn sie zur aktuellen Aufgabe passen; Pflichtregeln
    prüft ein Skript automatisch.
  - Notes: `items/EPIC-007/EPIC-007_notes.md`.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-023` **Architektur-Definitionen**
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
    mit Teilbereichen, wann sie geladen wird, wie sie durchgesetzt und wie sie
    geändert wird.
  - Completion criteria: Ort, Format, Ladeweg und Änderungsverfahren der
    Architektur-Definitionen sind festgelegt und in mindestens einem Projekt
    angewendet.
  - Summary: Architekturregeln werden Teil einer Modul-Suite `development`,
    liegen englisch im Doku-Ordner und werden per Hook vor der ersten
    Code-Änderung einer Session gelesen.
  - Notes: `items/STORY-023/STORY-023_notes.md`.
  - Spec: `items/STORY-023/STORY-023_spec.md`.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-025` **Regelverstöße und Regeländerungen**
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
    passt: Konflikt benennen und Lösungen vorschlagen, Entscheidung durch den
    Projektverantwortlichen, gewünschte Harness-Änderungen an den
    Harness-Backlog übergeben.
  - Completion criteria: Das Verfahren ist im Plugin festgelegt und gilt für
    alle Teilbereiche der Suite `development` und für die Vorgaben aller
    Module. Ein Wunsch nach einer Harness-Änderung lässt sich aus einem
    anderen Projekt heraus an das Harness-Repo übergeben. Das Verfahren wurde
    an mindestens einem echten Konfliktfall durchgespielt.
  - Summary: Klärt, was passiert, wenn eine Architektur oder ein Wunsch des
    Projektverantwortlichen nicht zu den dokumentierten Regeln oder zu den
    Vorgaben des Harness passt: Die AI benennt den Konflikt, der
    Projektverantwortliche entscheidet.
  - Notes: `items/STORY-025/STORY-025_notes.md`.
  - Spec: `items/STORY-025/STORY-025_spec.md`.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-015` **Verifikations-Nachweis-Format**
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
  - Completion criteria: Nach einem Change liegt ein solcher Nachweis vor und
    lässt sich ohne Rückfrage nachvollziehen.
  - Resolution: Rejected by the project owner on 2026-09-24: ein
    Protokoll, das der Agent selbst schreibt, belegt nichts; wird nicht
    gebraucht.

- `TASK-006` **Testumfang je Änderung**
  - Type: Task.
  - Parent: `STORY-024`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `STORY-001`.
  - Goal: Festlegen, wie umfangreich nach einer Änderung getestet wird:
    was die Änderung betreffen kann, nicht immer die ganze Suite.
  - Completion criteria: Die Skill `claude-harness:decomposition` enthält
    Regeln zum Testumfang: betroffene Tests inkl. Aufrufer, erneuter Lauf
    nach der letzten Änderung, Nennen des nicht Getesteten, Prüfen roter
    Tests vor dem Abtun. Kein eigenes Verify-Skript.
  - Resolution: Confirmed by the project owner on 2026-09-24 (Ziel auf
    Testumfang gekürzt, Verify-Skript entfällt).

- `TASK-005` **TDD-Ritual (Red/Green/Refactor)**
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

- `STORY-024` **Testdisziplin & Verifikation**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-24.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Festlegen, wie getestet wird: wann der Test vor dem Code
    entsteht und wie umfangreich nach einer Änderung getestet wird.
  - Completion criteria: Die Skill `claude-harness:decomposition` enthält
    Regeln zu Test zuerst und zum Testumfang; der Verifikationsnachweis ist
    abgelehnt.
  - Summary: Bündelt alles zum Testen: Testumfang (TASK-006) und TDD
    (TASK-005) sind Tasks dieser Story.
  - Notes: `items/STORY-024/STORY-024_notes.md`.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `TASK-002` **Workspace-Entscheidung formalisieren**
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
  - Resolution: Rejected by the project owner on 2026-09-24: folded into the spec of `STORY-022`; the native worktree tools cover the rest.

- `TASK-003` **Verbindlicher Change-Ablauf**
  - Type: Task.
  - Parent: `STORY-022`.
  - Required for parent: No.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Urgent.
  - Dependencies: `TASK-002`.
  - Goal: Die Schrittfolge Plan → Worktree/Lokal → Code → Merge → Cleanup als
    verbindliche Regel in `CLAUDE.md` festhalten, inklusive der Punkte, an
    denen eine Freigabe eingeholt wird.
  - Completion criteria: Jeder Schritt hat eine klare Ein-/Ausstiegsbedingung;
    kein Schritt wird stillschweigend übersprungen.
  - Resolution: Rejected by the project owner on 2026-09-24: folded into the spec of `STORY-022`; the native worktree tools cover the rest.

- `TASK-004` **Scope-Tracking für den Change**
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
  - Resolution: Rejected by the project owner on 2026-09-24: folded into the spec of `STORY-022`; the native worktree tools cover the rest.

- `TASK-001` **Cleanup-Kriterien festlegen**
  - Type: Task.
  - Parent: `STORY-022`.
  - Required for parent: No.
  - Status: Rejected.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Important.
  - Dependencies: `TASK-003`.
  - Goal: Definieren, wann ein Worktree/Branch gefahrlos gelöscht werden darf
    (z. B. nur nach erfolgreichem Merge und sauberem Zustand) und wann nicht.
  - Completion criteria: Die Kriterien verhindern nachweislich das Löschen
    eines Worktrees mit unverarbeiteten Änderungen.
  - Resolution: Rejected by the project owner on 2026-09-24: folded into the spec of `STORY-022`; the native worktree tools cover the rest.

- `STORY-004` **Zerlegungs-Heuristik definieren**
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
  - Notes: `items/STORY-004/STORY-004_notes.md`.
  - Spec: `items/STORY-004/STORY-004_spec.md`.
  - Resolution: Confirmed by the project owner on 2026-09-24.

- `STORY-005` **Dimensions-Checkliste je Teilaufgabe**
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

- `STORY-026` **Abschnitte an Subagenten übergeben**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: No.
  - Status: Rejected.
  - Created: 2026-09-24.
  - Area: Entwicklung.
  - Priority: Prospective.
  - Dependencies: `STORY-004`.
  - Goal: Prüfen, ob und wie Plan-Abschnitte an einen Subagenten mit
    günstigerem Modell übergeben werden: eigener Agent im Plugin, Auftrag aus
    dem Abschnitts-Vertrag samt nötiger Architekturregeln, Rückmeldung in
    festem Format, Kontrolle jedes Abschnitts durch die Hauptsession,
    Verhalten der Hooks im Subagenten und eine Schwelle, ab wann sich die
    Übergabe lohnt.
  - Completion criteria: Es ist entschieden, ob Abschnitte übergeben werden.
    Falls ja, wurde mindestens ein Abschnitt eines realen Features von einem
    Subagenten ohne Rückfrage korrekt umgesetzt und von der Hauptsession
    geprüft.
  - Resolution: Rejected by the project owner on 2026-09-25 — kein konkreter
    Bedarf, Priorität Prospective; bei spürbarem Kostendruck bei großen Plänen
    neu aufsetzen.

- `STORY-016` **Umgang mit Secrets/Credentials**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Completed.
  - Created: 2026-09-23.
  - Area: Sicherheit.
  - Priority: Prospective.
  - Dependencies: None.
  - Goal: Eine Regel festlegen, dass Secrets nie direkt im Code oder in
    einzucheckenden Dateien landen, sondern in einer zentralen,
    nicht versionierten Config gehalten werden, auf die der Code zur
    Laufzeit verweist. Eine Template-Datei mit Platzhaltern wird eingecheckt,
    damit ersichtlich ist, was konfiguriert werden kann. Welche Config im
    Einzelfall genutzt wird, ist zu klären, sofern nicht bereits eindeutig.
  - Completion criteria: Die Regel ist als bindende Architekturregel
    dokumentiert und deckt ab: kein Secret im Code, Ablage in einer
    zentralen gitignorten Config, eingecheckte Template-Datei mit
    Platzhaltern, Klärung der Config-Zuordnung mit dem Projekt-Owner.
  - Summary: Secrets landen nie im Code, sondern in einer zentralen,
    gitignorten Config; eine Template-Datei zeigt, was konfigurierbar ist.
    Welche Config genutzt wird, wird im Zweifel mit dem Owner geklärt.
  - Notes: `items/STORY-016/STORY-016_notes.md`.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-028` **Keine hartkodierten Pfade/Config-Werte im Code**
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
  - Notes: `items/STORY-028/STORY-028_notes.md`.
  - Resolution: Confirmed by the project owner on 2026-09-25.

- `STORY-009` **Entwicklungsprinzipien-Dokument**
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
  - Completion criteria: Ein kurzes, prüfbares Prinzipien-Dokument liegt vor.
  - Resolution: Rejected by the project owner on 2026-09-25: the named principles are native Claude behavior; project-specific rules belong in `architecture.md`. `EPIC-004` Goal and Completion criteria adjusted.

- `STORY-029` **SemVer-Versionierung klären und ggf. automatisieren**
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
    umsetzen, damit Versionen nachvollziehbar und
    konsistent steigen.
  - Completion criteria: Die Entscheidung (ob, was und wie weit
    automatisiert wird) ist mit dem Owner geklärt und in den Notizen
    festgehalten; das Vereinbarte ist umgesetzt und an mindestens einer
    Änderung angewendet.
  - Summary: Klären, ob Claude bei Änderungen die Versionsnummer nach SemVer
    selbst einstufen und hochzählen soll, und das dann umsetzen.
  - Notes: `items/STORY-029/STORY-029_notes.md`.
  - Spec: `items/STORY-029/STORY-029_spec.md`.
  - Resolution: Completed on 2026-09-25 under the project owner's advance authorization to close it once done; module implemented and enabled in this repo (`924a972`), first release tag `v0.1.0` follows the closure by owner decision.

- `EPIC-004` **Entwicklungsprozess & Prinzipien**
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
  - Notes: `items/EPIC-004/EPIC-004_notes.md`.
  - Resolution: Completed on 2026-09-25 under the project owner's advance authorization to close it once done; all criteria applied in the STORY-029 change (architecture rules read, sectioned plan with tests first, worktree workflow, full test run).
