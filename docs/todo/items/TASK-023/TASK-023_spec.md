# TASK-023 — Spec: Kopf-Befehle im API-Helfer

Grundlage: STORY-051_spec.md (Schnittstelle zum ToDo-Viewer, Umstellung).
Voraussetzung: die abwärtskompatible Erweiterung im ToDo-Viewer (Item im
Backlog des ToDo-Viewers). Ist sie noch nicht da, gegen einen Mock entwickeln
und die Endpunkte mit dem Viewer abstimmen.

## Umfang

- `plugin/scripts/backlog_api.py` neue Befehle:
  - `state <ID>`: Kopf und Zustand lesen, ohne Protokoll.
  - `put-state <ID> <version>`: Kopf ersetzen (Text von stdin).
  - `confirm-state <ID> <version>`: Kopf unverändert bestätigen.
  - `note <ID>`: optionales Feld `state` im stdin-JSON.
  - Hinweise des Servers (Kopf veraltet, Kopf lang, ältere Einträge
    geändert) sichtbar ausgeben.
- Fähigkeitsprüfung: Unterstützt der Viewer keine Köpfe (fehlender
  Endpunkt oder zu alte Version), geben die neuen Befehle eine klare Meldung
  aus; alte Befehle funktionieren unverändert.
- Session-State (`state.py`): Items merken, deren Notes in der Session über
  den Helfer geändert wurden, und Items, die aktiv sind (auf `In progress`
  gesetzt oder Spec per `doc` gelesen), für TASK-024.
- `plugin/skills/todo/api.md`: Befehle beschreiben; Lesereihenfolge
  "zuerst `state`, Protokoll mit `doc` nur bei Bedarf".

## Abnahme

- Unit-Tests gegen einen Test-Server bzw. Mock: alle Befehle, Versionen,
  Fähigkeitsprüfung, Session-State.
- Mit dem echten Viewer abgeglichen, sobald er die Erweiterung hat.
