# STORY-004 — Spec: Zerlegung von Aufgaben (mit STORY-005)

## Goal

Aufgaben werden so zerlegt, dass kleine, gut kontrollierbare Schritte
entstehen. Jeder Schritt lässt sich einzeln testen und kann ohne den Kontext
der planenden Session umgesetzt werden, auch von einem einfacheren Modell.
Das senkt Fehler und Rechenaufwand. Eine Dimensions-Checkliste (`STORY-005`)
stellt sicher, dass kein Abschnitt vergessen wird.

## Begriffe

- **Abschnitt:** ein Schritt eines Umsetzungsplans mit genau einer logischen
  Aufgabe entlang des Datenflusses, z. B. Persistenz, Laden, Verarbeitung,
  API-Eintrag, UI.
- **Task im Backlog:** ein Kind-Item mit eigenständigem Ergebnis. Es ist
  deutlich gröber als ein Abschnitt.
- **Dimension:** ein technischer Aspekt, den eine Aufgabe berühren kann
  (Liste unten).

## Zwei Ebenen

### Backlog (grob)

Eine Story bekommt Tasks nur, wenn alle drei Punkte zutreffen:

1. Jeder Task liefert für sich ein Ergebnis, das der Projektverantwortliche
   nutzen oder prüfen kann.
2. Jeder Task lässt sich in einer eigenen Session abschließen.
3. Die Story passt nicht sinnvoll in einen einzigen Umsetzungsplan.

Die Schichten eines einzelnen Features werden keine Tasks, sondern Abschnitte
im Plan. Tasks legt die AI nach den Regeln des `todo`-Skills nur nach
Freigabe an.

### Plan (fein)

Ein Umsetzungsplan besteht aus Abschnitten. Ein Abschnitt ist richtig
geschnitten, wenn alle Punkte zutreffen:

- **Eine Aufgabe:** Er lässt sich ohne „und außerdem“ beschreiben.
- **Einzeln testbar:** Er hat einen eigenen Test oder eine beobachtbare
  Prüfung mit einem Befehl und einem erwarteten Ergebnis.
- **Einzeln integrierbar:** Nach dem Abschnitt baut das Projekt, und alle
  Tests sind grün. Es gibt keinen kaputten Zwischenstand.
- **Selbsterklärend:** Er nennt das Ziel, die betroffenen Dateien oder
  Symbole, die Schnittstelle zu den Nachbarabschnitten, was nicht angefasst
  wird, den Test und wann angehalten und gefragt wird.
- **Entschieden:** Er enthält keine offene Entscheidung. Schnittstellen
  zwischen Abschnitten (Datenformate, Signaturen, Namen) legt der Plan fest,
  nicht der Abschnitt.

Reihenfolge: nach Abhängigkeiten. Jeder Abschnitt nutzt nur Abschnitte, die
schon umgesetzt und getestet sind. Eine feste Richtung (etwa „von unten nach
oben“) gibt es nicht.

Der letzte Abschnitt ist immer die **Integration**: Der ganze Ablauf wird
gegen das ursprüngliche Ziel geprüft.

Nicht zerlegen oder zusammenlegen, wenn:

- die Aufgabe nur eine Aufgabe und einen Test hat (z. B. Bugfix,
  Config-Anpassung). Dann gibt es einen Abschnitt;
- ein Abschnitt nicht für sich testbar wäre. Dann wird er mit dem Nachbarn
  zusammengelegt, dessen Test ihn abdeckt;
- die Änderung mechanisch viele Dateien gleich betrifft (z. B. eine
  Umbenennung). Das ist ein einziger Abschnitt;
- eine Aufteilung einen Zwischenstand erzeugen würde, der nicht baut oder
  dessen Tests fehlschlagen.

Beispiel (my_story_game, Button löst Verarbeitung mit Speichern und Neuladen
aus): 1. Persistenz, 2. Laden, 3. Backend-Verarbeitung, 4. API-Eintrag,
5. Frontend-Button mit `await` auf die Antwort, 6. Integration.

## Dimensions-Checkliste (STORY-005)

Beim Zerlegen geht die AI für die Aufgabe diese Dimensionen durch:

Persistenz · Laden/Zustand · Fachlogik · Schnittstellen (API, CLI,
Dateiformate, Hooks) · UI · Konfiguration · Sicherheit · Fehlerbehandlung ·
Migration/Betrieb · Tests · Dokumentation.

- Jede berührte Dimension wird einem Abschnitt zugeordnet oder bekommt einen
  eigenen.
- Der Plan endet mit einer Zeile, die das Ergebnis referenziert, z. B.
  „Dimensionen: Persistenz §1, Laden §2, Fachlogik §3, Schnittstellen §4,
  UI §5, Tests je Abschnitt, Doku §6; nicht betroffen: Sicherheit,
  Migration.“
- Tests und Dokumentation gehören normalerweise in den Abschnitt, der die
  Änderung macht, nicht in einen eigenen.

## Wo die Regeln stehen (Ladestufen, Architekturregel 7)

- **Kein Hook** vorerst: Ob gut zerlegt wurde, kann ein Skript nicht prüfen.
  Offen, ob später ein Hinweis nötig ist (Beobachtung beim Erproben).
- **Neuer Skill `claude-harness:decomposition`** (Teilbereich der Suite
  `development`) mit beiden Ebenen und der Checkliste. Beschreibung in einem
  Satz, nur wann er geladen wird, sinngemäß: „Use when planning how to
  implement a change, presenting an implementation plan, or considering
  whether a backlog item should get child tasks.“
- Der Skill legt fest, dass der Plan (im Planungsmodus oder im Chat) die
  Abschnitte enthält, nicht die Spec. Specs bleiben ohne Schrittfolge
  (`todo`-Regeln).
- Skills `todo` und `architecture` bekommen keinen Verweis; die
  Skill-Beschreibung genügt.

## Config

Neuer Teilbereich der Suite (bleibt `version = 1`):

```toml
[development]
decomposition = true   # Standard; false schaltet ihn ab
```

- `DEVELOPMENT_PARTS` in `harness_config.py` wird um `decomposition`
  ergänzt; Validierung wie bei `architecture` (nur Boolean).
- Keine Projektdatei: Die Kriterien stehen fest im Plugin.

## Session-Start

Ist der Teilbereich an, gibt `session_start.py` eine Zeile aus, sinngemäß:
„Decomposition: rules in skill claude-harness:decomposition (load it when
planning an implementation or splitting backlog items).“

## Other modules

- `init`: Der Teilbereich wird bei der Auswahl der Teilbereiche genannt.
- Techdocs: `configuration.md` (`development.decomposition`),
  `interfaces.md` (Skill `decomposition`, Startzeile), README falls die Suite
  dort beschrieben ist.

## Tests

- Config: `development.decomposition` gültig (`true`/`false`), kein Boolean
  ist ein Fehler, fehlt → an.
- Session-Start: Zeile erscheint, wenn Suite und Teilbereich an sind; fehlt
  bei abgeschalteter Suite oder `decomposition = false`.
- `tests/test_architecture_rules.py` deckt die Dokumentation des neuen
  Schlüssels ab.

## Erprobung (Completion criteria)

- Das nächste reale Feature (hier oder in my_story_game) wird nach dem Skill
  geplant: Abschnitte mit je eigenem Test, Checklisten-Zeile im Plan, und
  so umgesetzt.
- Zwei ähnliche Aufgaben werden nach denselben Kriterien zerlegt, und das
  Ergebnis ist vergleichbar.

## Nicht umgesetzt

- Übergabe von Abschnitten an Subagenten oder günstigere Modelle. Erst damit
  sinken die Tokens deutlich; das wäre ein eigenes Item.
- Hook zur Durchsetzung (siehe oben).
