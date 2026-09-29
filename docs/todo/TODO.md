# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `STORY-037` **Testkonventionen: Ablage, Gliederung, Test-Arten**
  - Type: Story.
  - Parent: `EPIC-004`.
  - Status: Open.
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
  - Notes: `items/STORY-037/STORY-037_notes.md`.
  - Required for parent: Yes.

- `EPIC-004` **Entwicklungsprozess & Prinzipien**
  - Type: Epic.
  - Status: Open.
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

- `TASK-018` **todo-Skill: Lücken beim Wiedereröffnen und bei geschlossenen Parents**
  - Type: Task.
  - Parent: None.
  - Status: Open.
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
  - Notes: `items/TASK-018/TASK-018_notes.md`.
