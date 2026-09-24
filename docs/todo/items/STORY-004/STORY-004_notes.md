# STORY-004 — Notes

## 2026-09-24 — Auslegung

### Discussed

- Vorlage Agent_Harness (`rules/modules/task-decomposition.md`): Zerlegung
  nach beobachtbaren Ergebnissen, Abwägung Nutzen gegen Kontextverlust und
  Koordinationsaufwand, Integrationsschritt am Ende. Nur Ideenquelle.
- Der Projektverantwortliche meint vor allem: Beim Planen sollen möglichst
  kleine, gut kontrollierbare Schritte entstehen, die die AI auch mit
  einfachen Modellen umsetzen kann.
- Heutiges Verhalten der AI: Pläne haben Schritte, aber deren Größe schwankt,
  und sie setzen oft den Kontext der planenden Session voraus. Ohne diesen
  Kontext kann ein einfaches Modell einen Schritt nicht sicher umsetzen.

### Decided

- Die Kriterien kommen in einen neuen Skill der Suite `development`
  (Arbeitsname `decomposition`), fest im Plugin.

### Open

- Ob ein Hook die Anwendung erzwingt.
- Ob Goal und Completion criteria an die Auslegung „kleine Schritte für
  einfache Modelle“ angepasst werden.

## 2026-09-24 — Zerlegung nach logischen Abschnitten

### Discussed

- Beispiel des Projektverantwortlichen (my_story_game): ein Button löst eine
  Funktion aus, die im Backend verarbeitet, persistiert, neu geladen und in
  die UI zurückgegeben wird. Statt einer großen Aufgabe entstehen
  Teilaufgaben: Persistenz, Laden, Backend-Verarbeitung, API-Eintrag,
  Frontend-Button mit `await` auf die Antwort. Jede ist für sich testbar.
- Erwarteter Nutzen: weniger Fehler, weniger Rechenaufwand. Tokens sinken
  spürbar erst, wenn Abschnitte in frischem Kontext (Subagent, einfacheres
  Modell) umgesetzt werden; das wäre ein eigenes Item.
- Überschneidung mit `STORY-005`: Die Abschnitte entsprechen den Dimensionen;
  die Checkliste könnte später Teil desselben Skills werden.

### Decided

- Zwei Ebenen: Im Backlog grob (Tasks nur mit eigenständigem Ergebnis), beim
  Planen fein (logische Abschnitte entlang des Datenflusses, von unten nach
  oben, je mit eigenem Test, Schnittstellen im Plan festgelegt, abschließender
  Integrationsschritt).

### Open

- Freigabe der angepassten Goal und Completion criteria.
- Hook weiterhin offen.

## 2026-09-24 — Reihenfolge, STORY-005, neue Ziele

### Decided

- Keine feste Reihenfolge „von unten nach oben“. Abschnitte werden in der
  Reihenfolge ihrer Abhängigkeiten umgesetzt, sodass jeder einzeln
  integrierbar ist (im Beispiel: ohne Daten keine Verarbeitung).
- `STORY-005` (Dimensions-Checkliste) wird zusammen mit dieser Story geplant
  und kommt in denselben Skill.
- Goal und Completion criteria sind an die Auslegung angepasst (Freigabe des
  Projektverantwortlichen).

### Open

- Hook weiterhin offen.

## 2026-09-24 — Spec freigegeben

### Decided

- Spec `STORY-004_spec.md` freigegeben; Umsetzung beginnt. Die Umsetzung
  selbst wird als erste Erprobung nach dem neuen Skill zerlegt.
- Danach wird geklärt, was die Arbeit mit Subagenten bräuchte (eigenes Item).

## 2026-09-24 — Umsetzung

### Discussed

- Umgesetzt nach Spec: Teilbereich `development.decomposition` (Validierung,
  Test, `configuration.md`, Vorlage), Startzeile in `session_start.py` mit
  Test, Skill `plugin/skills/decomposition/SKILL.md`, Doku (`interfaces.md`,
  `architecture.md`, README) und `init`. 96 Tests grün.
- Die Umsetzung lief bereits in Abschnitten mit je eigenem Test: 1. Config,
  2. Startzeile, 3. Skill, 4. Doku und `init`, 5. Integration (alle Tests,
  Startzeile in diesem Repo). Dimensionen: Konfiguration §1, Schnittstellen
  §2/§3, Tests je Abschnitt, Doku §4; nicht betroffen: Persistenz, Laden,
  UI, Sicherheit, Migration.

### Open

- Erprobung an einem realen Feature nach dem Skill (Plan mit Abschnitten
  vorab vorgelegt) und Vergleich zweier ähnlicher Aufgaben. Bis dahin bleiben
  `STORY-004` und `STORY-005` in Arbeit.

## 2026-09-24 — Erprobung an STORY-022

### Discussed

- Der Umsetzungsplan zu `STORY-022` (Session „Story22 native
  implementation“) wurde nach dem Skill erstellt und vorab vorgelegt: sieben
  Abschnitte mit Ziel, Dateien, eigenem Test, Test-zuerst-Angabe,
  „nicht anfassen“ und „nachfragen, wenn“; Schnittstellen vorab festgelegt;
  Integration am Schluss; Dimensions-Zeile am Ende (erfüllt `STORY-005`).

### Decided

- Der Projektverantwortliche akzeptiert als Vergleich zweier ähnlicher
  Aufgaben den Plan zu `STORY-022` und die Umsetzung dieser Story (gleiches
  Muster: Config, Startzeile, Skill, Doku, Integration).
- Sobald `STORY-022` nach diesem Plan umgesetzt ist, gehen `STORY-004` und
  `STORY-005` auf `Awaiting confirmation`.

### Open

- Abschluss der Umsetzung von `STORY-022`.
