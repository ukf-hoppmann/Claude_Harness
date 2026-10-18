# Spec: API-Helfer für Notes und Topics

## Was und warum

Claude arbeitet an Notes nur über die API des Viewers, wie beim Backlog über
`backlog_api.py`. Ein eigener Helfer `notes_api.py` kapselt Aufruf, Fehler und
Projektwahl. Die Befehle sind erst festlegbar, wenn der Viewer seine API
(Notes-API-Story im Viewer-Backlog) beschrieben hat.

## Voraussetzung

API-Beschreibung des Viewers: Pfade, Felder, Index-Format, Fehlercodes,
Versions-Token, wie ein Projekt gewählt wird. Ohne sie nicht beginnen.

## Umfang

1. **Refactoring zuerst**: `Api`, `ApiError`, Exit-Codes, `find_project`,
   Quellenfindung und HTTP-Fehlertext aus `plugin/scripts/backlog_api.py` in ein
   gemeinsames Modul (z. B. `viewer_api.py`) ziehen. `backlog_api.py` darf sich
   nach außen nicht ändern; die vorhandenen Tests sind der Nachweis.
2. **`notes_api.py`**: voraussichtliche Befehle (Namen folgen der Viewer-API):
   `index` (Topics und Notes, schlank), `show <LABEL>` (mit Langtext), `create`
   (Note oder Topic), `update`, `link`/`unlink`, `status` (snooze, done, drop),
   `promote`, `demote`, `trash`/`restore`, Hinweise lesen und entscheiden.
3. Projektwahl wie im Backlog (`--project`), URL aus der Config. Modul `notes`
   muss an sein, sonst Fehler mit Exit 2.
4. Kein Löschen für immer, keine Dateipfade.

## Tests

Stub-HTTP-Server in den Tests: Erfolg, Versionskonflikt, Fehlercodes,
Unerreichbarkeit (Exit 3), ungültiges JSON (Exit 2). Test zuerst, wo die
Schnittstelle schon fest ist (Refactoring: vorhandene Tests; neue Befehle:
nach der API-Beschreibung).

## Abnahme

Alle Tests grün; `notes_api.py` ohne Argumente zeigt die Befehlsliste;
`api.md` des Skills (STORY-040) stimmt mit dem Helfer überein.
