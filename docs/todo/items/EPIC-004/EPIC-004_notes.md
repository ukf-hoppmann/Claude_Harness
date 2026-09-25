# EPIC-004 – Notizen

## Summary
Legt fest, wie entwickelt wird: Architekturregeln, Zerlegung, Change-Ablauf
im Worktree, Tests und Versionierung. Ein eigenes Prinzipien-Dokument gehört
nicht mehr dazu.

## 2026-09-25 — STORY-009 verworfen

### Discussed
- STORY-009 (Entwicklungsprinzipien-Dokument) mit Agent_Harness
  (`rules/core/development.md`) verglichen. Die genannten Prinzipien (keine
  unnötigen Abstraktionen, keine spekulativen Features, kommentarsparsam,
  fremde Arbeit erhalten) sind natives Verhalten von Claude. Ein Dokument
  dazu würde nur Tokens kosten.
- Projektspezifische Regeln landen ohnehin als Abschnitte in
  `docs/development/architecture.md` (siehe Secrets, Pfade).

### Decided
- Der Owner hat STORY-009 verworfen. Goal und Completion criteria von
  EPIC-004 sind angepasst: „Entwicklungsprinzipien“ wurde gestrichen.
- Neues Pflicht-Kind STORY-029 (SemVer-Versionierung) angelegt.
