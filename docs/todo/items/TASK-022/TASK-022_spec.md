# TASK-022 — Spec: Kopf-Prüfsumme im Files-Modus

Grundlage: STORY-051_spec.md (Absicherung des Kopfs), Definition der
Prüfsumme in `format.md` (TASK-021).

## Umfang

- Gemeinsame Funktionen (neues Modul oder in `backlog.py`, nach
  Architekturregeln): Notes-Datei in Titel, Kopf, Stempel und Protokoll
  zerlegen; kanonische Form und Prüfsumme berechnen; Zustand ermitteln
  (`current`, `stale`, `missing`). TASK-023 und TASK-024 nutzen sie wieder.
- `backlog.py <folder> --confirm-state <ID>`: schreibt bzw. ersetzt die
  Stempelzeile mit aktuellem letzten Eintrag und Prüfsumme; ändert weder Kopf
  noch Protokoll. Fehlt der Kopf, Fehlermeldung mit Hinweis, ihn zuerst zu
  schreiben.
- `check_backlog.py` (Stop-Hook, Files-Modus): für Notes-Dateien, die in der
  Session geändert wurden, Zustand `stale` oder `missing` als Fehler melden
  (blockiert das Turn-Ende) mit der Anweisung: Kopf prüfen, anpassen oder
  bestätigen, dann `--confirm-state`. Nicht geänderte alte Notes ohne Kopf
  werden nicht gemeldet.
- Hinweis (kein Fehler): Kopf mit mehr als 15 Punkten unter Beschlossen;
  ältere Protokolleinträge geändert (Vergleich mit dem Stand vor der Session,
  falls verfügbar, sonst über Git).
- `cloud_export.py`: prüfen, dass Kopf und Stempel beim Export erhalten
  bleiben.

## Abnahme

- Unit-Tests: Zerlegen (mit/ohne Kopf, ohne Einträge), Prüfsumme gegen feste
  Testvektoren (die auch der ToDo-Viewer nutzt), Zustände, Bestätigen ändert
  nur die Stempelzeile, Check meldet nur geänderte Notes, Hinweise blockieren
  nicht.
- format.md bzw. Techdocs beschreiben den Befehl.
