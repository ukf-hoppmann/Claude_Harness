# STORY-052 — Spec: Branch-Stand beim Start einer Cloud-Session abgleichen

## Anlass

In ezf-ui (Branch `modularRefactor`, Kopie 0.12.7, `cloud.export = true`) startete
eine Cloud-Session auf `0f5fc36` (2026-11-02), während `origin/modularRefactor` auf
`d389b49` (2026-11-04) stand. Das Repo war ein Shallow Clone, beide Stände hatten
keinen gemeinsamen Vorfahren („ahead 85, behind 86“), der manuelle Fetch lief als
„forced update“. Backlog, Specs und Tagesberichte waren veraltet, ohne dass es
auffiel. Der Session-Start der Kopie gleicht den Branch heute nicht ab.

Vermutete Ursache: ein gecachter Container-Stand von vor einem Rebase oder
Force-Push auf origin. Prüfbar in einer betroffenen Session: gleiche Commit-Texte
mit verschiedenen Hashes in `git log --oneline -5` beider Stände.

## Ort

- Neues Modul `plugin/scripts/cloud_sync.py` mit der ganzen Git-Logik.
- `session_start.py` ruft es als ersten Schritt in `main()` auf, nur bei
  `CLAUDE_CODE_REMOTE=true` und Quelle `startup`. Kein eigener Eintrag in
  `hooks.json`: Claude Code führt passende Hooks parallel aus, die Reihenfolge
  vor dem Session-Start wäre nicht gesichert.
- Der Export (`cloud_export.py`) kopiert Skripte und SessionStart-Hook schon
  heute; dort ändert sich nichts.

## Konfiguration

`cloud.sync` (Boolean, Standard `true`, nur im Root-Projekt wie `[cloud]`), wirkt
nur in Cloud-Sessions. `false` schaltet den Abgleich ab.

## Ablauf

1. Branch per `git symbolic-ref`; detached HEAD oder kein Remote `origin`: nichts tun.
2. `git fetch --no-tags origin +refs/heads/<b>:refs/remotes/origin/<b>`, ohne
   `--unshallow`, Zeitlimit etwa 15 s (Hook-Zeitlimit 30 s).
3. Fälle:

| Fall | Aktion | Meldung (Englisch, eine Zeile) |
|---|---|---|
| Gleicher Stand | keine | keine |
| HEAD Vorfahr von origin, Baum sauber | `git merge --ff-only` | `Git: fast-forwarded <b> <alt>..<neu> (+n from origin).` |
| HEAD Vorfahr, Baum unsauber | keine | Abstand und `git stash && git merge --ff-only origin/<b>` |
| Nur lokal voraus | keine | keine (normaler Zustand vor einem Push) |
| Beidseitige Commits | keine | `+a / -b` und `git rebase origin/<b>`; `git reset --hard` nur nach Rückfrage |
| Kein gemeinsamer Vorfahr | keine | siehe unten |
| Fetch scheitert / Zeitlimit | keine | `Git: could not fetch origin/<b> (<reason>); checkout may be stale.` |

Meldung ohne gemeinsamen Vorfahren (Zahlen sind im Shallow Clone nicht verlässlich,
deshalb Hash und Datum):

> `Git: <b> shares no history with origin/<b> in this shallow clone (local <sha>, <date>; origin <sha>, <date>). Nothing changed. Likely a stale cached clone or a force-push. Tell the user before working; reset only on request: git reset --hard origin/<b>.`

## Architektur

Ausnahme von Regel 2 (Hooks ohne Netz) und Regel 5 (Hooks schreiben nicht ins
Projekt), vom Besitzer am 2026-11-04 freigegeben, in `architecture.md` eng gefasst:
nur Cloud-Session, nur bei `cloud.sync`, nur Fetch des aktuellen Branches und
Fast-Forward.

## Tests und Doku

- `tests/implementation/unit/test_cloud_sync.py`: temporäres Bare-Repo als origin;
  alle Fälle der Tabelle, Shallow Clone ohne gemeinsamen Vorfahren, Zeitlimit,
  `CLAUDE_CODE_REMOTE` ungesetzt.
- `test_session_start.py`: Abgleich läuft vor den übrigen Zeilen, nur bei `startup`.
- `test_config.py`: `cloud.sync`.
- Techdocs: `interfaces.md` (Skript), `configuration.md` (`cloud.sync`).
- Funktionstest in einer echten Cloud-Session von ezf-ui.

## Rollout

Minor-Release. Jedes Projekt mit `cloud.export` braucht danach
`/claude-harness:update` und einen Commit; der lokale Session-Start meldet die
Kopie bereits als veraltet.
