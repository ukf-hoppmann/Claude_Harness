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
