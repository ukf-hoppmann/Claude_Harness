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

- `STORY-004` **Zerlegungs-Heuristik definieren**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: Yes.
  - Status: In progress.
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

- `STORY-005` **Dimensions-Checkliste je Teilaufgabe**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: No.
  - Status: In progress.
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

- `STORY-026` **Abschnitte an Subagenten übergeben**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Required for parent: No.
  - Status: Open.
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
