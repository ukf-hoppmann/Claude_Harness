# Project Backlog Archive

Completed and rejected work items, moved unchanged from `TODO.md` after the
project owner's decision.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

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
  - Resolution: Rejected by the project owner on 2026-09-24: merged into `EPIC-004` as `STORY-022`; STORY-006, STORY-007, STORY-008 and TASK-001 became its tasks.

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
  - Resolution: Confirmed by the project owner on 2026-09-24.
