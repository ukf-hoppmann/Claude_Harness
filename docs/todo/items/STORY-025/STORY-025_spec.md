# STORY-025 — Spec: Konflikte mit Regeln und Harness-Vorgaben

## Goal

Passt eine Anforderung, eine gestaltete Architektur oder ein Wunsch des
Projektverantwortlichen nicht zu den dokumentierten Regeln oder zu den
Vorgaben des Harness, handelt die AI nicht selbst. Sie benennt den Konflikt,
schlägt Lösungen vor, und der Projektverantwortliche entscheidet. Gewünschte
Änderungen am Harness landen über eine Übergabe im Harness-Backlog.

## Begriffe

- **Projektregeln:** die Regeldateien der Suite `development` im Projekt
  (heute `architecture.md` und ihre Scopes; künftige Teilbereiche ebenso).
  Der Projektverantwortliche besitzt sie.
- **Harness-Vorgaben:** was das Plugin festlegt: Skills, Hooks, Formate und
  Vorlagen der Module (z. B. Backlog-Format, Sprache der Regeln, Sperre vor
  dem Lesen der Architektur). Sie lassen sich nur im Harness-Repo ändern.
- **Konflikt:** Eine Regel oder Vorgabe müsste gebrochen oder geändert werden,
  oder das Ergebnis ändert sich für den Projektverantwortlichen. Eine
  regelkonforme Umsetzung, die das gewünschte Ergebnis nicht verändert, ist
  kein Konflikt; die AI wählt sie ohne Nachfrage.

## Verfahren

1. **Anhalten.** Die AI setzt den betroffenen Teil nicht um, auch nicht
   vorläufig. Nicht betroffene Teile darf sie fortsetzen.
2. **Benennen, kurz:** was gewünscht ist, welche Regel oder Vorgabe
   entgegensteht (Datei und Abschnitt bzw. Skill), und warum sie nicht passt.
3. **Lösungen vorschlagen**, soweit sinnvoll:
   - einmalige Ausnahme;
   - kleinste Änderung der Projektregel;
   - Anforderung anders umsetzen;
   - bei Harness-Vorgaben zusätzlich: Modul oder Teilbereich abschalten,
     oder eine Änderung am Harness vorschlagen.
4. **Der Projektverantwortliche entscheidet; die AI folgt.** Regeln sind
   Leitlinien, die er gezielt durchbrechen darf.

Folgen der Entscheidung:

| Entscheidung | Was die AI tut |
|---|---|
| Einmalige Ausnahme | Umsetzen. Nicht eigens festhalten; der Tagesbericht erwähnt sie nur, wenn sie ohnehin berichtenswert ist. |
| Projektregel ändern | Regeldatei ändern, den Vorschlag vorher zeigen. Bindend ab der Freigabe. |
| Harness ändern | Übergabe an den Harness-Backlog (siehe unten). |

Grenze: Hooks setzen Harness-Vorgaben mechanisch durch; eine Ausnahme kann
die AI dort nicht gewähren. Dann nennt sie den Schalter in der Config, der
das Modul oder den Teilbereich abschaltet.

Probleme mit dem Harness selbst (Fehler, unpassende Vorgaben, störende Hooks)
spricht die AI von sich aus an und bietet die Übergabe an.

## Übergabe an den Harness-Backlog

Nur nach Zustimmung des Projektverantwortlichen.

1. **Repo finden:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_repo.py"`
   im Projekt-Root gibt den ersten Pfad aus `[harness].repo` aus, der auf
   diesem Rechner existiert und das Harness-Repo ist (Datei
   `plugin/.claude-plugin/plugin.json` mit `"name": "claude-harness"`).
   Sonst gibt es nichts aus.
2. **Auftrag formulieren** (Englisch, eigenständig verständlich): Wunsch des
   Projektverantwortlichen, Anlass im Projekt, betroffene Vorgabe, bereits
   besprochene Lösungen. Die Empfänger-Session lädt den Skill
   `claude-harness:todo` und ordnet den Punkt nach dessen Regeln ein; neue
   Items legt sie erst nach Freigabe an.
3. **Übergeben**, erste passende Möglichkeit:
   - Das Projekt ist selbst das Harness-Repo: direkt nach den Regeln des
     `todo`-Skills arbeiten, keine Übergabe.
   - Die Umgebung kann eine Session in einem anderen Verzeichnis anbieten
     (z. B. Aufgabenkarte in der Desktop-App): damit übergeben.
   - Sonst ein fertiges Kommando zum selbst Ausführen:
     `cd <repo> && claude "<Auftrag>"`.
   - Kein Repo gefunden: den Auftrag als fertigen Text ausgeben, und
     anbieten, den Pfad dieses Rechners in `[harness].repo` einzutragen
     (Vorschlag über `harness_repo.py --suggest`).

## Config

Neue, optionale Tabelle (bleibt `version = 1`):

```toml
[harness]
repo = [
  "/Users/me/Documents/GitHub/Claude_Harness",   # MacBook
  "/Users/me/Code/Claude_Harness",                # iMac
]
```

- Liste von Strings, absolute Pfade oder mit `~` beginnend. Leere Liste
  erlaubt. Andere Schlüssel in `[harness]` sind Fehler (Architekturregel 4).
- Kein Modul und kein Schalter: Das Verfahren gilt immer; ohne Pfad entfällt
  nur die Übergabe.

## Skript `harness_repo.py`

Nur Standardbibliothek; liest die Config über `harness_config.py`.

- `harness_repo.py` (im Projekt-Root oder mit `CLAUDE_PROJECT_DIR`, wie
  `daily.py`): erster gültiger Pfad aus der Config,
  sonst keine Ausgabe. Exit 0 auch bei fehlender oder ungültiger Config.
- `harness_repo.py --suggest`: Kandidat für diesen Rechner aus
  `~/.claude/plugins/known_marketplaces.json`: nur Marketplaces mit
  Quelle `directory`, deren Verzeichnis das Harness-Repo ist. Die Datei gehört
  Claude Code; fehlt sie oder ändert sich ihr Format, gibt es keinen Vorschlag.
  Nur für Vorschläge, nie zur Laufzeit.

## Wo die Regeln stehen (Ladestufen, Architekturregel 7)

- Kein Hook: Konflikte lassen sich nicht mechanisch erkennen.
- **Neuer Skill `claude-harness:conflicts`** mit dem Verfahren und der
  Übergabe. Beschreibung in einem Satz, nur wann er geladen wird, sinngemäß:
  „Use when a requirement or a wish of the project owner conflicts with the
  project's binding rules or with a Claude_Harness rule, or when the harness
  itself causes a problem.“ Gilt für alle Teilbereiche der Suite und alle
  Module.
- Skill `architecture`: Der Absatz zu Konflikten wird ein kurzer Verweis auf
  `claude-harness:conflicts`.
- Vorlage `templates/development/architecture.md`, Abschnitt
  `## Changing these rules`: kurz: Regeln sind Leitlinien; bei einem Konflikt
  benennt die AI ihn und der Projektverantwortliche entscheidet (Verweis auf
  den Skill); Änderungen an dieser Datei gelten ab seiner Freigabe.
- Die übrigen Modul-Skills bekommen keinen Verweis; die Skill-Beschreibung
  genügt.

## Other modules

- `init`: neuer Schritt: Pfad zum Harness-Repo abfragen, Vorschlag über
  `harness_repo.py --suggest`; leer lassen ist erlaubt.
- Techdocs: `configuration.md` (`[harness]`), `interfaces.md` (Skill
  `conflicts`, Skript `harness_repo.py`).

## Application in this repo

- `.claude-harness/config.toml`: `[harness].repo` mit dem Pfad dieses Repos.
- `docs/development/architecture.md`, Abschnitt `## Changing these rules`,
  an die neue Vorlage anpassen (nach Freigabe).

## Tests

- Config: `[harness].repo` gültig, kein String, relativer Pfad, unbekannter
  Schlüssel, Tabelle fehlt.
- `harness_repo.py`: erster existierender gültiger Pfad gewinnt; nicht
  existierende Pfade und Ordner ohne passende `plugin.json` werden
  übersprungen; `~` wird aufgelöst; keine Config → keine Ausgabe.
- `--suggest`: `directory`-Marketplace mit Harness-Repo wird vorgeschlagen,
  `github`-Marketplace nicht, fehlende oder kaputte Datei → keine Ausgabe.

## Nicht umgesetzt

- Kein Hinweis-Hook bei direkten Änderungen an Regeldateien: Regeländerungen
  folgen nach dem Verfahren ohnehin einer Entscheidung im Chat.
