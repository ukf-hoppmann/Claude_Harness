# Project Backlog

Active project work: open, in progress, or awaiting a project-owner decision.
Completed and rejected items are moved to `archive.md`; per-item notes and
specs live in `items/<ID>/`.

Format: Claude_Harness backlog format version 1. The rules are defined in the
`todo` skill of the claude-harness plugin (`skills/todo/format.md`).

## Work items

- `EPIC-009` **Notes und Topics: Erinnerungen neben dem Backlog**
  - Type: Epic.
  - Status: In progress.
  - Created: 2026-10-06.
  - Area: Dokumentation.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Der Harness kennt ein zweites Pflegegebiet neben dem Backlog:
    Notes und Topics im ToDo-Viewer (dort EPIC-005). Ein Modul `notes` mit
    eigenem Skill legt fest, wie Claude Notes erkennt, anlegt, pflegt und
    liest. Die Technik (Datenbank, Auslöser, Fälligkeit, Index) liefert
    allein der Viewer über seine API; der Harness spricht nur diese API an,
    hat keinen Dateizugriff und prüft keine Fälligkeiten.
  - Completion criteria: Alle Pflicht-Stories sind abgeschlossen; ein
    Projekt mit `[modules].notes = true` bekommt den Skill
    `claude-harness:notes` und eine Zeile im Session-Start; Claude kann über
    den Helfer Topics und Notes lesen, anlegen, ändern, verlinken,
    zurückstellen, erledigen, verwerfen und befördern; bei nicht
    erreichbarem Server fragt er nach; es gibt kein Markdown-Backend für
    Notes.
  - Summary: Der Harness bringt Claude bei, Erinnerungen, Fragen und Ideen
    als Notes im ToDo-Viewer zu pflegen, getrennt von der Arbeit im Backlog.
    Der Viewer baut die Technik, der Harness die Regeln dazu.
  - Notes: `items/EPIC-009/EPIC-009_notes.md`.
  - Spec: `items/EPIC-009/EPIC-009_spec.md`.

- `STORY-038` **Modulschalter notes in Config und Session-Start**
  - Type: Story.
  - Parent: `EPIC-009`.
  - Required for parent: Yes.
  - Status: Awaiting confirmation.
  - Created: 2026-10-06.
  - Area: Konfiguration.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: `[modules].notes` ist ein gültiger Schlüssel der Harness-Config
    (Standard aus). Bei aktivem Modul gibt der Session-Start eine statische
    Zeile mit Skill-Hinweis aus (ohne Netzwerk und ohne Abfrage von
    Fälligem), bei mehreren Projekten einmal je Hinweis. `init`, `update`
    und die Vorlage kennen den Schalter. Das Modul braucht keine eigenen
    Config-Schlüssel (kein Prüf-Intervall, keine Uhrzeit für relative
    Angaben).
  - Completion criteria: Unbekannte Modulnamen bleiben Fehler, `notes` wird
    akzeptiert; `session_start.py` zeigt die Zeile nur bei aktivem Modul,
    einfach und mit Teilprojekten; `plugin/templates/config.toml`,
    `docs/techdocs/configuration.md` und die Tests in `test_config.py` und
    den Session-Start-Tests sind angepasst; `init` und `update` erwähnen das
    Modul; die Tests laufen grün.
  - Spec: `items/STORY-038/STORY-038_spec.md`.
  - Notes: `items/STORY-038/STORY-038_notes.md`.
  - Summary: Das Modul notes lässt sich wie die anderen Module in der Config
    einschalten; der Session-Start nennt es nur mit einer Zeile.

- `STORY-039` **API-Helfer für Notes und Topics**
  - Type: Story.
  - Parent: `EPIC-009`.
  - Required for parent: Yes.
  - Status: Awaiting confirmation.
  - Created: 2026-10-06.
  - Area: Entwicklung.
  - Priority: Normal.
  - Dependencies: None.
  - Goal: Ein Helfer `notes_api.py` spricht die Notes-API des ToDo-Viewers
    an (Topics und Notes lesen, anlegen, ändern, verlinken, Status wechseln,
    befördern, zurückstufen, Papierkorb) nach dem Muster von
    `backlog_api.py`. HTTP-Client, Projektwahl, Fehlerbehandlung und
    Exit-Codes liegen in einem gemeinsamen Modul statt doppelt. Er nutzt nur
    die Standardbibliothek, liest die API-URL aus der Config und kennt
    keinen Dateizugriff auf Notes. Die genauen Befehle richten sich nach der
    API-Story im Backlog des ToDo-Viewers (EPIC-005 dort); Umsetzung erst
    nach deren Festlegung.
  - Completion criteria: Der gemeinsame Client ist aus `backlog_api.py`
    herausgelöst und die bestehenden Backlog-Tests laufen unverändert grün;
    `notes_api.py` deckt alle in der Notes-Spec genannten Befehle ab; Exit 3
    bei nicht erreichbarem Server; Tests mit einem Stub-Server für Erfolg,
    Konflikt, Fehlercodes und Unerreichbarkeit.
  - Spec: `items/STORY-039/STORY-039_spec.md`.
  - Notes: `items/STORY-039/STORY-039_notes.md`.
  - Summary: Ein Helfer-Skript, über das Claude Notes im Viewer liest und
    ändert, wie beim Backlog.

- `STORY-040` **Skill notes: Regeln für Notes und Topics**
  - Type: Story.
  - Parent: `EPIC-009`.
  - Required for parent: Yes.
  - Status: In progress.
  - Created: 2026-10-06.
  - Area: Dokumentation.
  - Priority: Normal.
  - Dependencies: `STORY-039`.
  - Goal: Der Skill `claude-harness:notes` (mit `api.md`) legt fest, wie
    Claude Notes erkennt (Note oder Backlog-Eintrag oder Wecker), anlegt,
    pflegt, liest, verlinkt, befördert und zurückstuft, was er ohne
    Rückfrage darf, wie er relative Zeitangaben in feste Zeitpunkte auflöst,
    und dass Notes privat sind. Der Skill nennt Fälligkeit nur als Zustand,
    den der Viewer setzt; Claude prüft nichts und spricht Fälliges nicht von
    sich aus an, sondern liest es nur auf Zuruf.
  - Completion criteria: `plugin/skills/notes/SKILL.md` und `api.md`
    enthalten alle in der Spec (STORY-040) genannten Regeln, die
    Beschreibung ist ein Satz ohne Regeln (Architekturregel 9), alle Texte
    sind englisch; `api.md` stimmt mit den Befehlen von `notes_api.py`
    überein; ein Funktionstest oder eine dokumentierte Probe zeigt
    Erkennung, Anlegen mit Bestätigung des aufgelösten Zeitpunkts und Lesen
    über den Index vor dem Langtext.
  - Spec: `items/STORY-040/STORY-040_spec.md`.
  - Notes: `items/STORY-040/STORY-040_notes.md`.
  - Summary: Der Skill, der Claude beibringt, wann etwas eine Note ist und
    wie er sie anlegt, liest und pflegt.

- `STORY-041` **Abgrenzung im todo-Skill und Techdocs zu Notes**
  - Type: Story.
  - Parent: `EPIC-009`.
  - Required for parent: Yes.
  - Status: In progress.
  - Created: 2026-10-06.
  - Area: Dokumentation.
  - Priority: Normal.
  - Dependencies: `STORY-040`.
  - Goal: Der todo-Skill grenzt das Backlog von Notes ab und verweist auf
    `claude-harness:notes`, inklusive Umwandlung Item zu Note und Note zu
    Item. Die Techdocs (Interfaces, Architektur, README) beschreiben das
    Modul und verweisen für das Notes-Modell auf die Dokumentation des
    Viewers. Notes kommen nicht in den Tagesbericht; das steht im
    daily-Skill nur dann, wenn es Missverständnisse gibt. Danach folgt das
    Release (SemVer, Minor).
  - Completion criteria: `plugin/skills/todo/SKILL.md` nennt die Abgrenzung
    in höchstens einem kurzen Abschnitt; `docs/techdocs/interfaces.md`,
    `architecture.md` und `README.md` nennen Modul, Helfer und Skill; kein
    Notes-Inhalt wird in Repository-Dateien geschrieben; Release mit
    passender Version und Tag.
  - Spec: `items/STORY-041/STORY-041_spec.md`.
  - Notes: `items/STORY-041/STORY-041_notes.md`.
  - Summary: Kleine Querverweise im todo-Skill, Anpassung der Dokumentation
    und das Release.
