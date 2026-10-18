# STORY-022 — Spec: Change-Workflow im Worktree (Suite `development`)

## Goal

Changes mit freigegebenem Plan laufen isoliert in einem eigenen Worktree, damit
mehrere Sessions parallel arbeiten können. Der Worktree zweigt vom aktuell
ausgecheckten Branch ab und wird nach Abschluss selbstständig dorthin
zurückgemerged und gelöscht. Der Eigner gibt nur den Plan frei; danach läuft
alles bis zum Aufräumen ohne weitere Rückfrage.

## Warum ein Teilbereich nötig ist

- `EnterWorktree` wird nur benutzt, wenn der Nutzer es sagt oder
  Projektanweisungen es vorschreiben. Die Regel des Harness ist diese
  Anweisung.
- Ohne `worktree.baseRef = "head"` zweigt ein Worktree von
  `origin/<default-branch>` ab, in EZF-Backend also vom Produktivstand.
- Das Zurückmergen in den Ausgangsbranch ist nativ nicht geregelt.

## Config

Neuer Teilbereich der Suite `development` (bleibt `version = 1`):

```toml
[development]
worktree = true   # Standard: an, wenn die Suite an ist
```

Semantik und Validierung wie bei `architecture` und `decomposition`
(`DEVELOPMENT_PARTS` in `harness_config.py`), dokumentiert in
`configuration.md`, getestet in `tests/test_config.py` (Architekturregel 4).

## Verteilung nach Ladestufen (Architekturregel 7)

| Teil | Stufe | Begründung |
|---|---|---|
| `baseRef`-Prüfung | Hook (Session-Start) | per Skript prüfbar, darf nie vergessen werden |
| Ablauf, Entscheidung, Verbote | Skill `claude-harness:worktree` | gilt nur beim Thema Change-Workflow |
| Ausgangsbranch merken, Vorprüfung vor dem Merge | Skript `worktree.py` | deterministische Git-Auswertung |

## Session-Start

Ist der Teilbereich aktiv:

1. Eine Zeile mit Verweis auf den Skill `claude-harness:worktree` (laden, wenn
   ein Plan freigegeben wurde oder ein Worktree zurückgeführt werden soll).
2. **Prüfung `worktree.baseRef`:** gelesen aus
   `.claude/settings.local.json`, `.claude/settings.json` (Projekt) und
   `~/.claude/settings.json`, in dieser Rangfolge; der erste gesetzte Wert
   gilt. Ist er nicht `"head"`, eine kurze Fehlerzeile: Worktrees würden vom
   Default-Branch abzweigen; Verweis auf den Skill. Ungültige oder unlesbare
   Settings-Dateien gelten als „nicht gesetzt“ und brechen den Session-Start
   nicht ab.

Weitere Zeilen gibt es nicht (Architekturregel 7: nur Ort/Skill, fehlende
Dateien, Fehler).

## Skript `plugin/scripts/worktree.py`

Nur Standardbibliothek, ruft `git` auf. Schreibt nur den Git-Config-Eintrag
und die übernommenen ignorierten Dateien im Worktree. Aufruf durch die AI laut
Skill, nicht durch einen Hook.

- `start` (im frisch angelegten Worktree):
  1. Ermittelt den Ausgangsbranch als den Branch, der im Haupt-Checkout
     ausgecheckt ist, und speichert ihn als
     `branch.<worktree-branch>.harnessBase`. Fehler, wenn der Haupt-Checkout
     detached ist oder die Session nicht in einem Worktree läuft.
  2. Spiegelt die ignorierten Dateien des Haupt-Checkouts in den Worktree
     (Liste aus `git ls-files --others --ignored --exclude-standard
     --directory`), damit der Worktree dem aktuellen Stand entspricht, z. B.
     `.env`, lokale Configs, `.claude/settings.local.json`.
     - Nie übernommen: `.claude/worktrees/` (andere Worktrees) und `.git`.
     - Abhängigkeitsordner (`node_modules`, `.venv`, `venv`) werden verlinkt
       statt kopiert, weil sie groß sind und virtuelle Umgebungen beim
       Kopieren brechen. Caches und Build-Ausgaben (`__pycache__`,
       `.pytest_cache`, `.mypy_cache`, `dist`, `build`) werden weggelassen.
     - Bereits vorhandene Dateien im Worktree werden nicht überschrieben.
     - Ausgabe: Anzahl kopierter Dateien, verlinkte und ausgelassene Ordner.
- `check` (vor dem Merge): gibt Ausgangsbranch, Pfad des Haupt-Checkouts und
  diese Befunde aus: Worktree sauber ja/nein; Ausgangsbranch seit Abzweigung
  bewegt ja/nein; im Haupt-Checkout noch der Ausgangsbranch ausgecheckt
  ja/nein. Exit-Code ≠ 0, wenn ein Befund den Merge verbietet.

Die Ausgabe ist kurz und maschinenlesbar genug, damit die AI sie ohne
weitere Git-Befehle bewerten kann.

## Skill `claude-harness:worktree`

Englisch (Architekturregel 6). Beschreibung ein Satz, wann laden.

### Entscheidung

- Ein Plan wurde freigegeben (Plan-Modus oder Plan nach Skill
  `claude-harness:decomposition`) → Worktree.
- Kein Plan → lokal im aktuellen Checkout, Committen wie bisher nur auf
  Wunsch.
- Läuft die Session schon in einem Worktree (z. B. von der App angelegt),
  gilt dieser Ablauf nicht: Der Worktree ist dann der lokale Checkout, es
  wird dort gearbeitet wie ohne Plan; kein weiterer Worktree, Merge und
  Löschen nur auf Wunsch.
- Meldet der Session-Start ein falsches `baseRef`: dem Eigner vorschlagen,
  `"worktree": {"baseRef": "head"}` in `.claude/settings.json` des Projekts
  einzutragen, und bis dahin lokal arbeiten.

### Start

1. Hat der Haupt-Checkout nicht committete Änderungen (ohne ignorierte
   Dateien), den Eigner fragen: ohne sie weitermachen oder erst committen?
   Bei „erst committen“ committet die AI sie auf dem Ausgangsbranch, dann
   geht es weiter.
2. `EnterWorktree` mit einem Namen aus Item-ID oder Kurztitel.
3. `worktree.py start` (Ausgangsbranch merken, ignorierte Dateien
   spiegeln). Scheitert es, Worktree verlassen (`keep`) und nachfragen.
4. Ändert der Plan Abhängigkeiten, verlinkte Abhängigkeitsordner im Worktree
   durch eigene ersetzen, statt die des Haupt-Checkouts zu verändern.

### Arbeiten

Coden und committen im Worktree. Backlog- und Techdocs-Änderungen des
Changes gehören in denselben Branch. Tagesberichte entstehen wie bisher nach
dem Merge im Haupt-Checkout (Skill `daily`).

### Abschluss (ohne Rückfrage)

1. Alles committet, Tests grün. Rote Tests → kein Merge, melden.
2. `worktree.py check`. Hat sich der Ausgangsbranch bewegt, zuerst
   `git merge <ausgangsbranch>` **im Worktree**; einfache Konflikte selbst
   lösen, Tests erneut; inhaltliche Konflikte → abbrechen und melden. So
   entstehen Konflikte nie im Checkout des Eigners.
3. `ExitWorktree` mit `action: "keep"`: Die Session ist wieder im
   Haupt-Checkout. Aus einer Worktree-Session heraus lässt Claude Code keine
   Git-Befehle auf den Haupt-Checkout zu (geändert am 2026-09-25,
   `TASK-013`).
4. Im Haupt-Checkout: `git merge --no-ff <worktree-branch>` mit einer
   Nachricht, die den Change benennt. Verweigert git den Merge (lokale
   Änderungen des Eigners würden überschrieben), abbrechen und melden.
5. Kein Push.
6. `git worktree remove <pfad>` und `git branch -d <worktree-branch>`.
   Verweigert git (ungesicherte oder nicht gemergte Arbeit), abbrechen und
   melden; nie `--force` oder `-D`.
7. Abschlussmeldung: Ausgangsbranch, Merge-Commit und der Befehl zum
   Zurücknehmen (`git revert -m 1 <merge-commit>`). Wurden im Worktree
   ignorierte Dateien geändert (z. B. `.env`), wird das genannt: Sie laufen
   nicht über den Merge zurück und wären mit dem Worktree weg. Die AI
   überträgt sie vor dem Löschen nur auf Bitte des Eigners.

### Abbruch

Scheitert ein Schritt oder endet die Session vorher, bleibt der Worktree
stehen. Die AI meldet Pfad, Branch und Ausgangsbranch.

### Verboten

- Worktrees oder Branches löschen, die nicht in dieser Session angelegt
  wurden, außer der Eigner bittet ausdrücklich darum.
- `discard_changes: true` ohne ausdrückliche Bitte des Eigners.
- Push, Force, Rebase des Ausgangsbranches, Stash im Haupt-Checkout.

## Betroffene Dateien

- `plugin/scripts/harness_config.py` — Teilbereich `worktree`.
- `plugin/scripts/session_start.py` — Skill-Zeile, `baseRef`-Prüfung.
- `plugin/scripts/worktree.py` — neu.
- `plugin/skills/worktree/SKILL.md` — neu.
- `plugin/templates/config.toml` — Schlüssel.
- `docs/techdocs/configuration.md`, `interfaces.md`, `architecture.md`,
  `README.md` — nachziehen.
- `tests/` — Config, Session-Start, `worktree.py` gegen ein temporäres
  Git-Repo mit Worktree.

## Acceptance criteria

- `development.worktree` wird validiert wie die anderen Teilbereiche; `false`
  schaltet Zeile, Prüfung und Skill-Regel ab.
- Session-Start meldet fehlendes oder falsches `baseRef` und bleibt bei
  korrektem Wert still; getestet inklusive defekter Settings-Datei.
- `worktree.py start/check` sind gegen ein temporäres Repo getestet:
  Ausgangsbranch gespeichert, detached HEAD abgelehnt, ignorierte Dateien
  gespiegelt (`.env` kopiert, `.venv` verlinkt, Caches und
  `.claude/worktrees/` ausgelassen, vorhandene Dateien nicht überschrieben),
  bewegter Ausgangsbranch und gewechselter Haupt-Checkout erkannt.
- Ein realer Change mit Plan ist in einem Projekt, dessen aktueller Branch
  nicht der Default-Branch ist, vollständig durchgelaufen: Worktree vom
  aktuellen Branch, Merge-Commit dorthin, Worktree gelöscht, kein Push,
  fremde Worktrees unverändert.
