# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `EPIC-004` **Entwicklungsprozess & Prinzipien**
  - Type: Epic.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Verbindlich festlegen, wie in einem Projekt entwickelt wird:
    Entwicklungsprinzipien, projektweite Architektur-Definitionen, Heuristik
    zur Task-Zerlegung, Change-Ablauf (Workspace, Ablauf, Cleanup), TDD-Ritual
    und einheitliche Testebenen (Unit/Integration/System), damit Qualität
    nicht vom Zufall abhängt.
  - Completion criteria: Prinzipien, Architektur-Definitionen,
    Zerlegungs-Heuristik, Change-Ablauf und Testkommando sind dokumentiert und
    werden bei mindestens einem Change sichtbar angewendet.

- `STORY-023` **Architektur-Definitionen**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Awaiting confirmation.
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

- `STORY-025` **Regelverstöße und Regeländerungen**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-24.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `STORY-023`.
  - Goal: Festlegen, was geschieht, wenn eine Anforderung nicht zu den
    verbindlichen Regeln der Suite `development` passt (keine lokalen
    Ausnahmen, sondern stoppen und die kleinste Regeländerung vorschlagen) und
    wie Änderungen an den Regeldateien erst mit Freigabe des
    Projektverantwortlichen bindend werden.
  - Completion criteria: Das Verfahren ist im Plugin festgelegt, gilt für alle
    Teilbereiche der Suite, und direkte Änderungen an Regeldateien lösen einen
    Hinweis auf die nötige Freigabe aus.

- `STORY-004` **Zerlegungs-Heuristik definieren**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Kriterien festlegen (Umfang, Kopplung, Unterbrechbarkeit,
    Integrationsrisiko), nach denen entschieden wird, ob eine Aufgabe zerlegt
    wird.
  - Completion criteria: Die Kriterien sind so konkret, dass zwei ähnliche
    Aufgaben nachvollziehbar gleich behandelt werden.

- `STORY-005` **Dimensions-Checkliste je Teilaufgabe**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: No.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Prospective.
  - Dependencies: `STORY-004`.
  - Goal: Eine Prüfliste relevanter Dimensionen (Persistenz, Schnittstellen,
    Sicherheit, Tests, Dokumentation) für jede zerlegte Teilaufgabe
    bereitstellen, damit nichts vergessen wird.
  - Completion criteria: Die Checkliste wird bei einer zerlegten Aufgabe
    sichtbar durchlaufen und im Ergebnis referenziert.

- `STORY-022` **Change-Workflow (Workspace, Ablauf, Cleanup)**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-24.
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
  - Summary: Ersetzt EPIC-003. Die bisherigen Stories STORY-006, STORY-007 und
    STORY-008 sowie TASK-001 sind jetzt Tasks dieser Story.

- `STORY-006` **Workspace-Entscheidung formalisieren**
  - Type: Task.
  - Parent: `STORY-022`.
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
    konfigurierbar gemacht wird. Wird sie konfigurierbar, sind die Felder in
    `configuration.md` dokumentiert und ihre Validierung ist getestet.

- `STORY-007` **Verbindlicher Change-Ablauf**
  - Type: Task.
  - Parent: `STORY-022`.
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
  - Type: Task.
  - Parent: `STORY-022`.
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
  - Parent: `STORY-022`.
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

- `STORY-024` **Testdisziplin & Verifikation**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-24.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: None.
  - Goal: Festlegen, wie in einem Projekt getestet und verifiziert wird:
    einheitliche Testebenen mit einem Verify-Kommando, TDD für passende
    Änderungen und ein nachvollziehbarer Nachweis von Verify-Läufen.
  - Completion criteria: Das Verify-Kommando führt alle konfigurierten
    Testebenen aus und ist dokumentiert; die Regeln zu TDD und
    Verifikationsnachweis sind entschieden (umgesetzt oder bewusst
    zurückgestellt).
  - Summary: Bündelt alles zum Testen: Verify-Kommando (STORY-011), TDD
    (STORY-010) und Verifikationsnachweis (STORY-015) sind Tasks dieser Story.

- `STORY-011` **Test-Ebenen & einheitliches Verify-Kommando**
  - Type: Task.
  - Parent: `STORY-024`.
  - Required for parent: Yes.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Important.
  - Dependencies: `STORY-001`.
  - Goal: Unit-, Integrations- und Systemtests über einen einzigen,
    konsistenten Aufrufpunkt (Verify-Skript) statt ad-hoc-Befehlen ausführen.
  - Completion criteria: Ein Befehl führt alle konfigurierten Testebenen aus
    und liefert ein lesbares Ergebnis (bestanden/fehlgeschlagen je Ebene). Die
    Testbefehle je Ebene stehen in der Projektkonfiguration; die Felder sind in
    `configuration.md` dokumentiert und ihre Validierung ist getestet.

- `STORY-010` **TDD-Ritual (Red/Green/Refactor)**
  - Type: Task.
  - Parent: `STORY-024`.
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

- `STORY-015` **Verifikations-Nachweis-Format**
  - Type: Task.
  - Parent: `STORY-024`.
  - Required for parent: No.
  - Status: Open.
  - Created: 2026-09-23.
  - Area: Entwicklung.
  - Priority: Prospective.
  - Dependencies: `STORY-011`.
  - Goal: Ein einfaches, lesbares Format festlegen, in dem ein Verify-Lauf
    protokolliert wird (Befehl, Ergebnis, Zeitpunkt, betroffener Scope).
  - Completion criteria: Nach einem Change liegt ein solcher Nachweis vor und
    lässt sich ohne Rückfrage nachvollziehen.

- `STORY-016` **Umgang mit Secrets/Credentials**
  - Type: Story.
  - Parent: `EPIC-004`.
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
  - Dependencies: `STORY-018`, `STORY-023`.
  - Goal: Verbindlich festlegen, welche Inhalte in die Root-`CLAUDE.md`, in
    Skills, in Unterordner-`CLAUDE.md` und in Hooks gehören.
  - Completion criteria: Die Regel ist dokumentiert, und für jedes bestehende
    Modul ist nachvollziehbar, auf welcher Stufe es liegt und warum.
