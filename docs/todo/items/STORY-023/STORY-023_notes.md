# STORY-023 — Notes

## 2026-09-24 — Grundentscheidungen

### Discussed

- Vorbild my_story_game: Wurzel `.harness/architecture-rules.md` mit
  MUST/SHOULD/MAY-Regeln, delegierte Teilbereiche unter `.harness/architecture/`,
  Änderungsverfahren mit Owner-Freigabe, eigene Architektur-Tests. Schwachstelle:
  Das Lesen hängt allein an einer Anweisung in `CLAUDE.md`.
- Eine inhaltliche Relevanzprüfung („betrifft diese Änderung die Architektur?“)
  ist nicht zuverlässig möglich; zuverlässig unterscheiden lässt sich nur nach
  Pfaden.
- Lange Chats sparen keine Tokens: Der ganze Verlauf wird bei jeder Nachricht
  verarbeitet und kann komprimiert werden. Ein Chat pro Thema mit erneutem
  Einlesen der Regeln ist günstiger.

### Decided

- Architektur wird Teilbereich einer Modul-Suite `development`: Schalter
  `[modules].development`, Teilbereiche einzeln unter `[development]`
  (zunächst nur `architecture`; weitere Teilbereiche aus `EPIC-004` folgen).
  Jeder Teilbereich bleibt ein eigener Skill mit eigenem Hook.
- Aufteilung wie bei den anderen Modulen: Der Plugin-Skill beschreibt den
  Umgang mit Architekturregeln; die Regeln selbst stehen im Projekt.
- Die Regeln liegen unter `docs/`, im Ordner der Suite `development`
  (Wurzel `architecture.md`, Teilbereiche `architecture/<bereich>.md`). Der Pfad
  steht in der Config und wird beim Session-Start genannt.
- Regeln sind immer englisch mit MUST/SHOULD/MAY (RFC 2119), unabhängig von
  `docs.language`.
- Die Wurzel listet Teilbereiche mit Pfadmustern.
- Laden: Skill für die Planung; ein Hook blockiert die erste Änderung an einer
  Projektdatei, bis die Wurzel in der Session gelesen wurde, und ebenso bei
  Dateien eines Teilbereichs, bis dessen Datei gelesen wurde. Nach einer
  Kontext-Komprimierung wird der Merker zurückgesetzt.
- Durchsetzung: Der Harness sorgt für das Lesen und die Regel, die Architektur
  zu befolgen. Bei jeder Regelerweiterung wird, wenn die Regel mechanisch
  prüfbar ist, ein Architektur-Test vorgeschlagen und in der Regel verwiesen.
- Umgang mit Regelverstößen und Regeländerungen wird eine eigene Story unter
  `EPIC-004` (`STORY-025`).

- Die Tagesberichte ziehen nach `docs/daily/` (neuer Standardpfad `daily`),
  damit `docs/development/` nur die Regeln der Suite enthält. Ein Ordner pro
  Modul direkt unter `docs/`; kein Zwischenordner.

### Open

- Keine.

## 2026-09-24 — Spec-Entscheidungen

### Decided

- Teilbereiche der Suite sind an, sobald die Suite an ist (Opt-out).
- Die Teilbereiche und ihre Pfadmuster stehen als Tabelle in der Wurzel
  `architecture.md`, nicht in der Config: Die Zuordnung ist selbst eine
  Architekturentscheidung; in der Config würde sie Aufgaben vermischen.
- Tests zählen als Projektdateien; der Mehraufwand ist ein einmaliges Lesen
  der Wurzel pro Session.

## 2026-09-24 — Umsetzung

### Discussed

- Umgesetzt nach Spec: Config-Suite `development`, Skill `architecture`,
  Vorlage, Hooks (PreToolUse-Ablehnung, PostToolUse-Lese-Merker, Reset bei
  `compact`/`clear`), `init`, Systemdoku. 81 Tests grün.
- Test in einer echten `claude -p`-Session in einem Wegwerfprojekt: Das
  Schreiben einer Datei in einem Scope wurde abgelehnt; die Session las
  Regeldatei und Scope-Datei und befolgte beide Regeln.
- Entwurf `docs/development/architecture.md` für dieses Repo; bindend erst nach
  Freigabe durch den Projektverantwortlichen.

### Decided

- Der Projektverantwortliche hat `docs/development/architecture.md` für dieses
  Repo freigegeben. Für die mechanisch prüfbaren Regeln 2 (nur
  Standardbibliothek) und 4 (jeder Config-Schlüssel dokumentiert) gibt es
  `tests/test_architecture_rules.py`; die Regeln verweisen darauf.
- Die Completion criteria sind erfüllt; die Story wartet auf Bestätigung.

## 2026-09-24 — Wiedereröffnet: Architektur schon beim Planen

### Discussed

- Der Hook greift erst bei der ersten Code-Änderung. Beim Planen und
  Besprechen hängt das Lesen der Architekturregeln nur am Skill, der nicht
  erzwungen wird. Dann entsteht ein Plan gegen die Regeln, und der Hook
  blockiert erst, wenn das Konzept schon steht.
- Ein Hook kann nicht erkennen, ob gerade Architektur geplant wird. Greifbar
  wird ein Plan an zwei Stellen: beim Schreiben einer Spec und beim Vorlegen
  eines Plans im Planungsmodus.
- Die Regeln bei jedem Session-Start vollständig zu laden wäre sicher, kostet
  aber in jedem Chat Tokens und widerspricht der Ladestufen-Regel.
- Ein Vermerk in der Root-`CLAUDE.md` würde die Startzeile des Hooks
  doppeln, die ohnehin in jedem Chat im Kontext ist.

### Decided

- Wiedereröffnet durch den Projektverantwortlichen am 2026-09-24, weil die
  Architektur schon beim Planen gelesen werden muss.
- Der Hook lehnt zusätzlich das Schreiben einer Spec im Backlog und das
  Verlassen des Planungsmodus ab, bis die Regeln gelesen sind.
- Die Skill-Beschreibung nennt ausdrücklich das Planen und Entwerfen.
- Umgesetzt: `check_architecture.py` prüft zusätzlich `ExitPlanMode` und
  Backlog-Specs; Startzeile und Skill-Beschreibung nennen das Planen. Tests
  für Spec (auch `_spec_<Thema>`), Notizen (nicht betroffen) und Plan.
- Eine eigenständige `claude -p`-Session kann `ExitPlanMode` nicht nutzen; die
  Plan-Sperre ist daher nur durch Tests belegt und in einer interaktiven
  Session noch zu beobachten. Der Versuch zeigte aber das Problem: Ohne Lesen
  der Regeln plante die Session gegen eine vorhandene Regel.
- Die Completion criteria sind weiterhin erfüllt; die Story wartet auf
  Bestätigung.

