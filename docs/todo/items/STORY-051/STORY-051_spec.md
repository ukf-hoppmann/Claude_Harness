# STORY-051 — Spec: Aufbau und Absicherung der Item-Notes

Stand: fortlaufend; enthält nur Beschlossenes. Offene Punkte stehen am Ende
und in den Notes.

## Was und warum

Item-Notes (`<ID>_notes.md`) sind heute ein reines Protokoll zum Anhängen.
Der aktuelle Stand eines Items muss aus allen Einträgen rekonstruiert werden;
das ist für den Owner unübersichtlich und kostet die LLM Kontext und
Fehldeutungen. Künftig hat jede Notes-Datei einen Kopf mit dem geltenden
Stand und darunter das Protokoll. Ein Mechanismus stellt sicher, dass der Kopf
nach jeder Änderung der Notes bewusst geprüft wird.

## Rollen der Dokumente

- **Notes, Kopf:** geltender Stand des Items. Wird ersetzt, nicht ergänzt.
- **Notes, Protokoll:** Weg zu den Entscheidungen (Discussed/Decided/Open),
  nur angehängt.
- **Spec:** geregelte technische Darstellung, aus der eine neue Session ohne
  Rückfragen einen Plan erstellen kann; ohne Schrittfolge. Wird fortlaufend
  geschrieben, sobald Entscheidungen stabil sind, und am Ende der Klärung
  noch einmal geprüft.

## Aufbau der Notes-Datei

```markdown
# <ID> — <Titel>

## Stand

- Ziel/Status: <ein Satz>
- Nächster Schritt: …
- Offen:
  - … (<Datum des Protokolleintrags>)
- Beschlossen:
  - … (<Datum>)
- Verweise: Spec, Kinder-Items, verwandte Items

Stand bestätigt nach Eintrag <Datum> — <Thema> (<Prüfsumme>)

## <YYYY-MM-DD> — <Thema>

### Discussed
### Decided
### Open
```

Regeln für den Kopf:

- Reihenfolge: Ziel/Status, Nächster Schritt, Offen, Beschlossen, Verweise.
- Ein Punkt pro Zeile, mit Datum als Verweis ins Protokoll.
- Nur was jetzt gilt; überholte Entscheidungen fallen aus dem Kopf und
  bleiben im Protokoll.
- Technisches steht im Kopf in einem Satz mit Verweis auf die Spec.
- Keine feste Längengrenze; ein langer Kopf ergibt nur einen Hinweis, nie
  eine Ablehnung.

Regeln für das Protokoll:

- Erledigte Open-Punkte früherer Einträge werden im neuen Eintrag
  ausdrücklich geschlossen ("Open vom <Datum> (X) erledigt: …").

## Absicherung des Kopfs

- Der Stempel im Kopf enthält die Prüfsumme des Protokolls zum Zeitpunkt der
  Bestätigung. Der Kopf ist veraltet, wenn die Prüfsumme des aktuellen
  Protokolls abweicht. Das Setzen des Stempels ändert das Protokoll nicht.
- Nicht jeder Eintrag braucht einen neuen Kopf. Nach jeder Änderung der Notes
  wird der Kopf entweder angepasst oder bewusst als aktuell bestätigt; beides
  setzt den Stempel.
- Den Stempel schreibt nie die LLM von Hand:
  - API-Modus: der Server (beim Ersetzen oder Bestätigen des Kopfs).
  - Files-Modus: ein Bestätigungsbefehl in `backlog.py`.
- Hook am Turn-Ende: Für Items, deren Notes in dieser Session geändert wurden
  und deren Stempel veraltet ist, blockiert er das Turn-Ende, bis der Kopf
  angesehen und angepasst oder bestätigt ist. Im Files-Modus läuft das über
  die vorhandene Backlog-Prüfung am Turn-Ende.
- Reminder (Prüfidee B): Gibt es ein aktives Item der Session und seit
  mehreren Turns keinen Notes-Eintrag, erinnert ein Hook daran (kein
  Blocker).

## Schnittstelle zum ToDo-Viewer (API-Modus)

Umsetzung im ToDo-Viewer ist eigene Arbeit dort; der Harness erwartet:

- Kopf und Protokoll getrennt gespeichert: Kopf 1:1 zum Item, Einträge 1:n.
- Befehle bzw. Endpunkte: Kopf lesen (ohne Protokoll), Kopf ersetzen,
  Kopf bestätigen; `note` hängt weiter Einträge an und kann optional einen
  neuen Kopf mitnehmen.
- Der Server berechnet Prüfsumme und Stempel und meldet veraltete Köpfe.
- Nach außen (Spiegel, Git, Files-Modus) bleibt es eine Markdown-Datei im
  obigen Aufbau; der Sync zerlegt und setzt zusammen.

## Betroffen

- `plugin/skills/todo/SKILL.md`, `format.md`, `api.md`
- `plugin/scripts/backlog_api.py`, `backlog.py`, `check_backlog.py`
- Hook-Konfiguration des Plugins (Turn-Ende, Reminder)
- ToDo-Viewer (separates Projekt)

## Noch offen (siehe Notes)

- Plan speichern oder mit der Spec enden.
- Maßstab und Schwellwert des Längenhinweises.
- Warnung beim Umschreiben älterer Protokolleinträge.
- Umgang mit bestehenden Notes-Dateien.
- Regeln 1–4 (Ort, Inhalt, Zeitpunkt, Spec/Notes) und Prüfideen A, C, D.
- Abnahmekriterien.
