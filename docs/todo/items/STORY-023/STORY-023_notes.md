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
