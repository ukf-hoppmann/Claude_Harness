# STORY-022 — Notizen

## 2026-09-24 — Was Claude Code nativ macht, Zuschnitt der Story

### Discussed

- Arbeitsort heute: Claude Code arbeitet standardmäßig im aktuellen
  Checkout. `EnterWorktree` wird nur benutzt, wenn der Nutzer „Worktree“
  ausdrücklich sagt oder CLAUDE.md/Memory es vorschreibt. Die Desktop-App kann
  eine Session schon in einem Worktree starten. Die Basis eines neuen
  Worktrees steuert die Claude-Code-Einstellung `worktree.baseRef`: `fresh`
  (Standard, `origin/<default-branch>`) oder `head` (lokaler HEAD).
- Cleanup heute: `ExitWorktree remove` verweigert das Löschen bei nicht
  committeten Dateien oder Commits, die nicht auf dem Ausgangsbranch liegen,
  gilt aber nur für Worktrees, die in der eigenen Session angelegt wurden.
- Merge zurück: nativ nicht geregelt. `sync_with_base_branch` der App merged
  nur in die Gegenrichtung (Basis → Worktree).
- Scope-Tracking (früher TASK-004): Im Worktree ist der Branch der Scope
  (`git diff <basis>...HEAD`); eine eigene Pfadliste wäre doppelt.
- Beispiel EZF-Backend: `main` ist produktiv, der Mitarbeiter arbeitet in
  `Development`, der Eigner mit der AI in `ansTest`. Die Basis muss deshalb
  der aktuell ausgecheckte Branch sein, nicht `main`.

### Decided

- Plan freigegeben = großer Change → Worktree. Kein Plan = kleiner Change →
  lokal im aktuellen Checkout.
- Der Worktree zweigt vom aktuell ausgecheckten Branch ab; dieser
  Ausgangsbranch wird am Worktree-Branch gespeichert und ist das Merge-Ziel.
- Nach Abschluss committet die AI und merged selbstständig, ohne Rückfrage,
  mit Merge-Commit (`--no-ff`), damit ein `git revert -m 1` den ganzen Change
  zurücknimmt. Danach wird der Worktree gelöscht. Damit ist der Change fertig.
- Kein Push, nur lokaler Merge.
- Tests müssen vor dem Merge grün sein.
- Worktrees aus anderen Sessions werden nie automatisch gelöscht, nur auf
  ausdrückliche Bitte des Eigners.
- Bei Abbruch bleibt der Worktree stehen; die AI meldet Pfad, Branch und
  Ausgangsbranch.
- TASK-001 bis TASK-004 werden abgelehnt; ihr Inhalt geht in die Spec dieser
  Story auf.

### Open

- Keine (siehe Nachtrag unten).

## 2026-09-24 — Nachtrag: Start, App-Worktree, ignorierte Dateien

### Discussed

- Der Worktree soll ein Spiegel des aktuellen Stands sein. Da nichts gepusht
  wird und `.env` und Ähnliches relevant sein können, reicht der letzte
  Commit nicht.

### Decided

- Nicht committete Änderungen im Haupt-Checkout: Die AI fragt, ob ohne sie
  weitergemacht oder erst committet wird.
- Startet die Session schon in einem Worktree, wird der Ablauf ignoriert und
  dort lokal gearbeitet.
- Ignorierte Dateien werden beim Start in den Worktree gespiegelt.
  Abhängigkeitsordner (`node_modules`, `.venv`) werden verlinkt statt
  kopiert, Caches und Build-Ausgaben ausgelassen, `.claude/worktrees/` nie
  übernommen. Das erledigt `worktree.py start`; damit ist die Frage nach
  einem eingebauten Mechanismus von Claude Code hinfällig.
