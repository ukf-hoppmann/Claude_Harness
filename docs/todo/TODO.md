# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `EPIC-001` **Konfigurierbarer Harness (Policy)**
  - Type: Epic.
  - Status: In progress.
  - Created: 2026-09-23.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Eine projekteigene Konfigurationsdatei für das Claude_Harness-Plugin
    definieren, die nur echte Projektwerte enthält (Pfade, Verify-/Testbefehle,
    Workspace-Regeln, aktive Module) und von Skills und Hooks gelesen wird.
    Genehmigungen und Rechte bleiben bei den nativen Claude-Code-Einstellungen.
  - Completion criteria: Ein validiertes Konfigurationsschema existiert und wird
    von mindestens einem realen Verify-Aufruf tatsächlich gelesen und
    angewendet.
  - Summary: Jedes Projekt bekommt eine kleine Einstellungsdatei, in der steht,
    wo Dinge liegen, wie getestet wird und welche Harness-Teile an sind.
  - Notes: `items/EPIC-001/EPIC-001_notes.md`.

- `STORY-001` **Policy-Schema definieren**
  - Type: Story.
  - Parent: `EPIC-001`.
  - Required for parent: Yes.
  - Status: In progress.
  - Created: 2026-09-23.
  - Area: Konfiguration.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Die Projektkonfiguration `.claude-harness/config.toml` festlegen:
    welche Felder sie mindestens braucht
    (Pfade wie der Backlog-Ordner, Verify-/Testbefehle je Ebene, aktive Module,
    Quelle der Workspace-Wahl). Kein Approval-Modus.
  - Completion criteria: Ein dokumentiertes Schema (Ort, Felder, Typen, Pflicht
    vs. optional, Standardwerte) liegt vor und deckt alle Epics ab, die
    Konfigurationswerte referenzieren.

- `STORY-003` **Module unabhängig aktivierbar/deaktivierbar machen**
  - Type: Story.
  - Parent: `EPIC-001`.
  - Required for parent: No.
  - Status: Open.
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

- `EPIC-002` **Task-Zerlegung**
  - Type: Epic.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Eine Heuristik festlegen, wann eine größere Aufgabe in unabhängig
    verifizierbare Teilaufgaben zerlegt wird und wann sie bewusst am Stück
    bleibt, angelehnt an das Dimensions-Prinzip aus Agent_Harness.
  - Completion criteria: Die Heuristik ist als Regel dokumentiert und wurde an
    mindestens einer realen, mittelgroßen Aufgabe erprobt.

- `STORY-004` **Zerlegungs-Heuristik definieren**
  - Type: Story.
  - Parent: `EPIC-002`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Kriterien festlegen (Umfang, Kopplung, Unterbrechbarkeit,
    Integrationsrisiko), nach denen entschieden wird, ob eine Aufgabe zerlegt
    wird.
  - Completion criteria: Die Kriterien sind so konkret, dass zwei ähnliche
    Aufgaben nachvollziehbar gleich behandelt werden.

- `STORY-005` **Dimensions-Checkliste je Teilaufgabe**
  - Type: Story.
  - Parent: `EPIC-002`.
  - Required for parent: No.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Prospective.
  - Dependencies: `STORY-004`.
  - Goal: Eine Prüfliste relevanter Dimensionen (Persistenz, Schnittstellen,
    Sicherheit, Tests, Dokumentation) für jede zerlegte Teilaufgabe
    bereitstellen, damit nichts vergessen wird.
  - Completion criteria: Die Checkliste wird bei einer zerlegten Aufgabe
    sichtbar durchlaufen und im Ergebnis referenziert.

- `EPIC-003` **Change-Workflow (Workspace, Ablauf, Cleanup)**
  - Type: Epic.
  - Status: Open.
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

- `STORY-006` **Workspace-Entscheidung formalisieren**
  - Type: Story.
  - Parent: `EPIC-003`.
  - Required for parent: Yes.
  - Status: Open.
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
    konfigurierbar gemacht wird.

- `STORY-007` **Verbindlicher Change-Ablauf**
  - Type: Story.
  - Parent: `EPIC-003`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Urgent.
  - Dependencies: `STORY-006`.
  - Goal: Die Schrittfolge Plan → Worktree/Lokal → Code → Merge → Cleanup als
    verbindliche Regel in `CLAUDE.md` festhalten, inklusive der Punkte, an
    denen eine Freigabe eingeholt wird.
  - Completion criteria: Jeder Schritt hat eine klare Ein-/Ausstiegsbedingung;
    kein Schritt wird stillschweigend übersprungen.

- `STORY-008` **Scope-Tracking für den Change**
  - Type: Story.
  - Parent: `EPIC-003`.
  - Required for parent: No.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Important.
  - Dependencies: `STORY-007`.
  - Goal: Festhalten, welche Dateien/Pfade zu einem Change gehören, damit
    Merge und Cleanup nachvollziehbar nur diesen Umfang betreffen.
  - Completion criteria: Nach einem Change lässt sich ohne Rückfrage sagen,
    welche Pfade dazugehörten und welche nicht.

- `TASK-001` **Cleanup-Kriterien festlegen**
  - Type: Task.
  - Parent: `EPIC-003`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Governance.
  - Priority: Important.
  - Dependencies: `STORY-007`.
  - Goal: Definieren, wann ein Worktree/Branch gefahrlos gelöscht werden darf
    (z. B. nur nach erfolgreichem Merge und sauberem Zustand) und wann nicht.
  - Completion criteria: Die Kriterien verhindern nachweislich das Löschen
    eines Worktrees mit unverarbeiteten Änderungen.

- `EPIC-004` **Entwicklungsprinzipien & Testdisziplin**
  - Type: Epic.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Verbindliche Entwicklungsprinzipien, ein TDD-Ritual und einheitliche
    Testebenen (Unit/Integration/System) festlegen, damit Qualität nicht vom
    Zufall abhängt.
  - Completion criteria: Prinzipien, TDD-Ablauf und Testkommando sind
    dokumentiert und werden bei mindestens einem Change sichtbar angewendet.

- `STORY-009` **Entwicklungsprinzipien-Dokument**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Projektbezogene Entwicklungsprinzipien (z. B. keine unnötigen
    Abstraktionen, keine spekulativen Features) explizit und
    projekt-konfigurierbar festhalten statt nur implizit im Systemverhalten
    zu belassen.
  - Completion criteria: Ein kurzes, prüfbares Prinzipien-Dokument liegt vor.

- `STORY-010` **TDD-Ritual (Red/Green/Refactor)**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: No.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `STORY-011`.
  - Goal: Festlegen, für welche Art von Änderungen TDD verbindlich ist und
    wie der Rot-Grün-Refactor-Zyklus nachvollziehbar dokumentiert wird.
  - Completion criteria: Ein Beispiel-Change zeigt den Zyklus nachvollziehbar
    (fehlschlagender Test → Implementierung → grüner Test → Refactor).

- `STORY-011` **Test-Ebenen & einheitliches Verify-Kommando**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `STORY-001`.
  - Goal: Unit-, Integrations- und Systemtests über einen einzigen,
    konsistenten Aufrufpunkt (Verify-Skript) statt ad-hoc-Befehlen ausführen.
  - Completion criteria: Ein Befehl führt alle konfigurierten Testebenen aus
    und liefert ein lesbares Ergebnis (bestanden/fehlgeschlagen je Ebene).

- `EPIC-005` **Dokumentation & Nachverfolgung**
  - Type: Epic.
  - Status: In progress.
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

- `STORY-012` **Technische Dokumentationspflicht definieren**
  - Type: Story.
  - Parent: `EPIC-005`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Dokumentation.
  - Priority: Prospective.
  - Dependencies: None.
  - Goal: Festlegen, wann und wo technische Änderungen dokumentiert werden
    müssen (z. B. README, Architekturnotizen) und wann das entfällt.
  - Completion criteria: Eine klare Schwelle trennt dokumentationspflichtige
    von trivialen Änderungen.

- `STORY-013` **Daily-Development-Report**
  - Type: Story.
  - Parent: `EPIC-005`.
  - Required for parent: No.
  - Status: Awaiting confirmation.
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

- `STORY-014` **Backlog-Lebenszyklus verfeinern**
  - Type: Story.
  - Parent: `EPIC-005`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Dokumentation.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Die Statusübergänge dieses Backlogs (Open → In progress → Awaiting
    confirmation → Completed/Rejected) im Alltag konsequent anwenden,
    inklusive der Regel, dass nur der Projekteigner final bestätigt.
  - Completion criteria: Mindestens ein Eintrag hat den vollständigen
    Lebenszyklus bis `Completed` oder `Rejected` durchlaufen.

- `EPIC-006` **Verifikationsnachweis & Umgang mit sensiblen Daten (Vorschlag)**
  - Type: Epic.
  - Status: Open.
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

- `STORY-015` **Verifikations-Nachweis-Format**
  - Type: Story.
  - Parent: `EPIC-006`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Sicherheit.
  - Priority: Prospective.
  - Dependencies: `STORY-011`.
  - Goal: Ein einfaches, lesbares Format festlegen, in dem ein Verify-Lauf
    protokolliert wird (Befehl, Ergebnis, Zeitpunkt, betroffener Scope).
  - Completion criteria: Nach einem Change liegt ein solcher Nachweis vor und
    lässt sich ohne Rückfrage nachvollziehen.

- `STORY-016` **Umgang mit Secrets/Credentials**
  - Type: Story.
  - Parent: `EPIC-006`.
  - Required for parent: No.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Sicherheit.
  - Priority: Prospective.
  - Dependencies: None.
  - Goal: Eine Regel festlegen, wie mit erkennbaren Zugangsdaten in
    Kommandozeilen-Output, Logs oder Dateien umgegangen wird (z. B. nie in
    Klartext in Dateien schreiben, vor dem Committen prüfen).
  - Completion criteria: Die Regel ist dokumentiert und deckt mindestens die
    Fälle Logging, Dateien und Git-Commits ab.

- `EPIC-007` **Plugin-Architektur**
  - Type: Epic.
  - Status: In progress.
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

- `STORY-019` **Ladestufen-Regel festlegen**
  - Type: Story.
  - Parent: `EPIC-007`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Architektur.
  - Priority: Important.
  - Dependencies: `STORY-018`.
  - Goal: Verbindlich festlegen, welche Inhalte in die Root-`CLAUDE.md`, in
    Skills, in Unterordner-`CLAUDE.md` und in Hooks gehören.
  - Completion criteria: Die Regel ist dokumentiert, und für jedes bestehende
    Modul ist nachvollziehbar, auf welcher Stufe es liegt und warum.

- `STORY-021` **Harness in Projekten initialisieren**
  - Type: Story.
  - Parent: `EPIC-007`.
  - Required for parent: No.
  - Status: In progress.
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
