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

## 2026-09-24 — Umsetzung

### Decided

- Tagesberichte gehören nicht in den Worktree-Branch, sondern entstehen wie
  bisher nach dem Merge im Haupt-Checkout (Skill `daily`); die Spec war hier
  ungenau und ist korrigiert.
- Dieses Repo setzt `worktree.baseRef = "head"` in `.claude/settings.json`.

## 2026-09-25 — Befunde beim ersten Worktree-Change von STORY-027

### Discussed

- Abschluss laut Skill: `git -C <main> merge` aus der Worktree-Session. Claude
  Code blockiert Git-Befehle, die aus einer isolierten Worktree-Session auf
  den Haupt-Checkout zielen. Umweg bei `TASK-007`: `ExitWorktree` mit
  `keep`, Merge im Haupt-Checkout, dann `git worktree remove` und
  `git branch -d`.
- Hook-Pfade: `CLAUDE_PROJECT_DIR` bleibt im Worktree der Haupt-Checkout.
  Dateien liegen aber unter `.claude/worktrees/<Name>/`. Der techdocs-Hook
  zählte deshalb Doku-Änderungen im Worktree nicht als Doku und meldete
  fälschlich fehlende Doku.

### Decided

- Der Owner hat einen Eintrag für beide Befunde freigegeben: `TASK-013`.

## 2026-09-25 — TASK-013 umgesetzt

### Decided

- Neuer Abschluss:
  1. `worktree.py check`
  2. `ExitWorktree keep`
  3. Merge im Haupt-Checkout
  4. `git worktree remove` und `git branch -d`

  Spec und Skill sind angepasst.
- Hooks erkennen einen Worktree von Claude Code am `cwd` der Hook-Eingabe
  oder am Pfad der bearbeiteten Datei und nutzen ihn als Projekt-Root
  (`project_root` in `harness_config.py`). Dafür ist kein Git-Aufruf nötig.

### Discussed

- Der reale Durchlauf ist der Abschluss von `TASK-013` selbst.

## 2026-09-25 — Abschlussprüfung

### Discussed

- `TASK-013` ist bestätigt. Die übrigen Tasks sind abgelehnt, die Story hat
  also keine offenen Kinder mehr.
- Der reale Durchlauf ist erfüllt: `TASK-007` bis `TASK-013` liefen jeweils
  mit freigegebenem Plan durch den ganzen Ablauf ohne Rückfrage:
  - Worktree vom Ausgangsbranch `main`
  - Merge-Commit mit `--no-ff`
  - Worktree und Branch gelöscht

  Andere Worktrees wurden nicht angefasst.
- Blockiert: `TASK-001` bis `TASK-003` sind Pflicht-Tasks mit Status
  `Rejected`, ihr Inhalt ging 2026-09-24 in die Spec über. Laut
  Backlog-Format braucht eine Story aber für `Completed` alle Pflicht-Tasks
  als `Completed`. Status bleibt `In progress`, bis der Owner entscheidet,
  z. B. diese Tasks auf `Required for parent: No` zu setzen.

### Open

- Wie werden abgelehnte Pflicht-Tasks behandelt, deren Inhalt in der Story
  aufgegangen ist?
