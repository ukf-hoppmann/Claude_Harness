# Probelauf: Harness in der Cloud (STORY-047, Weg B)

Dieser Lauf klärt, ob der Harness einmal im Cloud-Environment eingerichtet werden
kann (Weg B), statt in jedes Projekt kopiert zu werden (Weg A). Er ändert nichts
am Harness und nichts an deinen Projekten. Zusammenhang und Begründung: Notes
von `STORY-047` und `EPIC-010`.

## Was geprüft wird

| # | Frage | Wo steht die Antwort |
|---|---|---|
| Q1 | Darf das Setup-Script ein Repository klonen, das der Sitzung nicht zugeordnet ist (hier: den Harness)? | `setup.log`: Zeilen `git ls-remote`, `git clone`, `raw file`, `archive` |
| Q2 | Wirken Hooks aus `~/.claude/settings.json` der Maschine in der Sitzung? | `hook.log`, `session_start.out`, Kontext der Sitzung |
| Q3 | Sind Skills aus `~/.claude/skills` der Maschine in der Sitzung sichtbar, und stimmen die Pfade im Skilltext? | Skill-Liste, Skilltext |
| Q4 | Läuft `claude plugin install` im Setup-Script, und wirkt das Plugin dann wie lokal? | `setup.log` (Modus `plugin`), Skill-Liste |
| Q5 | Wie verhält sich der Harness als zweites Repository der Sitzung: Pfad, was wird geladen, lesen und schreiben? | Sitzung B |
| Q6 | Grunddaten: Python-Version, `CLAUDE_CODE_REMOTE`, `CLAUDE_PROJECT_DIR`, `claude` im Setup-Script | `setup.log` |

## Dateien

| Datei | Zweck |
|---|---|
| `setup.sh` | Probe-Setup-Script für ein eigenes Cloud-Environment. Protokolliert nach `/root/harness-probe/` und endet immer mit Exit 0. |
| `target/` | Inhalt eines kleinen Wegwerf-Repositories (`.claude-harness/config.toml`, `CLAUDE.md`) als Zielprojekt. |

## Vorbereitung

1. Wegwerf-Repository auf GitHub anlegen (z. B. `harness-probe-target`, privat) und den Inhalt von `target/`
   hineinkopieren, committen, pushen. Warum nicht `ezf-ui`: Der Stand auf GitHub ist dort 79 Commits hinter
   lokal, und der Probelauf soll kein echtes Projekt berühren. Die Config nutzt den Dateimodus, so sieht der
   Sitzungsstart-Hinweis wie später in der Cloud aus.
2. Prüfen, dass das Repository für Claude auf claude.ai/code auswählbar ist (GitHub-Verbindung deines Kontos).
   Dasselbe gilt für `Claude_Harness` (Sitzung B).
3. In claude.ai/code ein **neues Environment** anlegen (Name z. B. `Harness-Probe`, nicht das Default-Environment),
   Netzwerk **Trusted**, Inhalt von `setup.sh` ins Feld „Setup script“. Die Repository-URL oben im Script prüfen.
4. Wichtig: Nach der ersten Sitzung speichert die Plattform das Ergebnis des Scripts zwischen (Cache, etwa sieben
   Tage). Ändert sich das Script, läuft es neu. Eine Sitzung mit gecachtem Environment führt das Script nicht noch
   einmal aus; die Protokolle von `/root/harness-probe/` bleiben aber erhalten.

## Lauf 1: Sitzung A (ein Repository)

Neue Sitzung im Environment `Harness-Probe`, **nur** das Wegwerf-Repository auswählen. Diesen Text als erste
Nachricht einfügen:

```text
Das ist ein Diagnoselauf. Ändere keine Dateien im Repository, committe und pushe nichts. Führe die Schritte aus und gib zu jedem das Ergebnis wörtlich oder knapp zusammengefasst an:

1. cat /root/harness-probe/setup.log
2. cat /root/harness-probe/hook.log und /root/harness-probe/session_start.out (falls vorhanden)
3. Steht in deinem Kontext vom Sitzungsstart eine Zeile, die mit "Claude_Harness:" beginnt? Zitiere sie. Kennst du außerdem den Probelauf-Marker aus der CLAUDE.md des Repositorys? Nenne ihn.
4. Welche Skills siehst du in deiner Skill-Liste (nur Namen)? Sind todo, daily, techdocs, testing, worktree dabei?
5. Lade den Skill "todo" (falls vorhanden): steht im Text noch das Platzhalterwort ${CLAUDE_PLUGIN_ROOT} oder ein echter Pfad?
6. echo "$CLAUDE_CODE_REMOTE $CLAUDE_PROJECT_DIR"; python3 --version; pwd
7. ls -la ~/.claude ~/.claude/skills; cat ~/.claude/settings.json
8. Führe /context aus und nenne die geladenen Memory-Dateien und Skills.
9. Wenn /opt/claude-harness existiert: git -C /opt/claude-harness log -1 --oneline

Schließe mit einer Tabelle: Schritt | Ergebnis (ja / nein / teilweise) | Beleg.
```

## Lauf 2: Sitzung B (zwei Repositories)

Neue Sitzung im selben Environment mit dem Wegwerf-Repository **und** `Claude_Harness`. Erste Nachricht:

```text
Diagnoselauf mit zwei Repositories. Ändere nichts, committe und pushe nichts.

1. pwd; ls -la. Wo liegen die beiden Repositories (Pfade)?
2. cat /root/harness-probe/hook.log. Gibt es eine neue SessionStart-Zeile für diese Sitzung?
3. Steht in deinem Kontext vom Sitzungsstart eine Zeile, die mit "Claude_Harness:" beginnt?
4. Führe /context aus: Welche CLAUDE.md-Dateien (aus welchem Repository) und welche Skills sind geladen?
5. Im Harness-Repository: python3 plugin/scripts/backlog.py docs/todo --index | head -5 (Lesezugriff auf das Backlog im Dateimodus)
6. git -C <Pfad des Harness-Repositories> remote -v; git -C <Pfad> status -sb
7. Trockenlauf, schreibt nichts: git -C <Pfad> push --dry-run origin HEAD:refs/heads/probe-dry-run

Schließe mit einer Tabelle: Schritt | Ergebnis (ja / nein / teilweise) | Beleg.
```

## Lauf 3 (optional): Plugin im Setup-Script (Q4)

In `setup.sh` `MODE="manual"` auf `MODE="plugin"` stellen (das Script läuft dann neu) und Sitzung A wiederholen. Der
Modus installiert das Plugin mit `claude plugin install`, schreibt aber keine eigenen Hooks. Wichtig sind dann
Schritt 1 (Zeilen `plugin marketplace add`, `plugin install`, `plugin list`) und die Skill-Liste.

## Auswertung

Beide Tabellen (und ggf. die von Lauf 3) in die Sitzung zurückkopieren. Daraus folgt:

| Befund | Folge |
|---|---|
| Q1 nein (Clone scheitert, auch `raw` nicht) | Weg B scheidet aus. Weg A (Kopie im Projekt). |
| Q1 ja, Q2 ja, Q3 ja | Weg B trägt. Zu klären bleiben Namensraum und Pfadplatzhalter in den Skilltexten. |
| Q1 ja, Q2 nein | Hooks nur über die eingecheckte `.claude/settings.json` des Projekts (Weg A für die Hooks). |
| Q3 nein | Skills über `.claude/skills` des Projekts (Weg A für die Skills). |
| Q4 ja | Einfachste Lösung: Plugin wie lokal, nur das Setup-Script nötig. |
| Q5: Harness-Skills und Hooks fehlen, Lesen und Schreiben gehen | Das zweite Repository taugt als Datenquelle (Backlog, Wünsche), nicht als Quelle der Regeln. |

## Aufräumen

- Environment `Harness-Probe` archivieren, Wegwerf-Repository löschen oder archivieren.
- Es wird nichts in `Claude_Harness` oder in ein Projekt gepusht; Schritt 7 in Sitzung B ist ein Trockenlauf.
- Stand: Das lokale `main` von `Claude_Harness` liegt fünf Commits vor GitHub. Der Clone in der Cloud zeigt den
  älteren Stand. Für den Probelauf ist das ohne Bedeutung, vor dem echten Einsatz muss gepusht sein.
