# EPIC-007 — Notes

## 2026-09-23 — Plugin-Architektur und Ladestufen

### Discussed

- Agent_Harness hat die Projektregeln per Python-Tool aus einer Policy in
  `CLAUDE.md` gerendert. Claude_Harness soll Regeln anwenden, ohne dass die AI
  bei jeder Aufgabe alles einliest; Regeln wie der Backlog sind nur relevant,
  wenn damit gearbeitet wird.
- Claude Code lädt Inhalte gestuft:
  1. Root-`CLAUDE.md`: immer, daher sehr kurz halten (fast nur Verweise).
  2. Skills: immer nur die einzeilige Beschreibung, der Inhalt erst beim Thema.
  3. `CLAUDE.md` in Unterordnern: erst beim Arbeiten in diesem Ordner.
  4. Hooks: Skripte ohne Token-Kosten, die nicht vergessen werden können.
- Ob ein Skill automatisch geladen wird, hängt davon ab, wie gut seine
  Beschreibung zur Aufgabe passt. Das ist zuverlässig, aber nicht garantiert.

### Decided

- Claude_Harness wird als Claude-Code-Plugin gebaut (Skills, Hooks, Befehle).
  Die Module aus Agent_Harness werden zu Skills. Kein Renderer für `CLAUDE.md`.
- Faustregel: Was immer gelten muss, wird ein Hook; was themenbezogen ist, wird
  ein Skill; die Root-`CLAUDE.md` enthält fast nur Verweise.
- Das Plugin wird in diesem Repo selbst genutzt.
- Ein Plugin für alle Module, mit Schalterliste in der Projektkonfiguration
  (Details in `EPIC-001`).

### Open

- Genaue Ordnerstruktur des Plugins und ob es im Repo-Root oder in einem
  Unterordner liegt.
- Wie das Plugin in diesem Repo aktiviert wird (lokale Installation oder
  Marketplace).

## 2026-09-23 — Grundgerüst umgesetzt

### Decided

- Das Plugin liegt in `plugin/`, nicht im Repo-Root. Andere Projekte bekommen
  so nur das Plugin, nicht Backlog und Tests dieses Repos.
- Dogfooding über einen lokalen Marketplace (`.claude-plugin/marketplace.json`
  im Root) und `.claude/settings.json`. Ersatzweg: `claude --plugin-dir ./plugin`.
- Hooks:
  - SessionStart: eine kurze Zeile zu Modulen und Backlog in den Kontext.
  - PostToolUse (Write/Edit): markiert, dass der Backlog geändert wurde.
  - Stop: prüft den Backlog nur, wenn er geändert wurde; bei Fehlern arbeitet
    die AI weiter und korrigiert.
- Geprüft wird erst beim Stop, nicht nach jedem Edit, weil das Archivieren
  zwei Edits braucht und der Stand dazwischen kurz ungültig ist.
- Die Hook-Skripte sind in Python (nur Standardbibliothek).

### Open

- ~~Ob der Marketplace-Pfad `./` in `.claude/settings.json` funktioniert.~~
  Am 2026-09-23 geprüft: Eine neue Session lädt das Plugin, der
  SessionStart-Hook liefert seine Zeile, und der Skill `claude-harness:todo`
  ist sichtbar. Der Stop-Hook meldete in einem Testprojekt einen ungültigen
  Wert zurück an die Session.
- `/claude-harness:init` ist noch nicht in einer interaktiven Session
  ausprobiert (`STORY-021`).
