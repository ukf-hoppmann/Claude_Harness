# STORY-051 — Spec: Aufbau und Absicherung der Item-Notes

Diese Spec ist immer der aktuelle Stand; der Weg zu den Entscheidungen steht
in den Notes.

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
- **Spec:** immer der aktuelle technische Stand, aus dem eine neue Session
  ohne Rückfragen einen Plan erstellen kann; ohne Schrittfolge und ohne
  Entscheidungsfindung. Wird aktualisiert, sobald etwas entschieden ist oder
  sich ändert, und am Ende der Klärung noch einmal geprüft.
- **Umsetzungsplan:** entsteht erst beim Start der Umsetzung aus Spec,
  Architektur- und Zerlegungsregeln, wird dem Owner zur Freigabe vorgelegt und
  nicht im Backlog gespeichert. Die Besprechung endet mit der Spec; ist ein
  Item zu groß, wird es in Kinder-Items zerlegt.

## Wo und wie protokolliert wird

- **Ort:** in das spezifischste Item, um das es geht. Läuft die Klärung im
  Rahmen von Task X, gehört sie zu Task X. Story-Notes nur für Entscheidungen,
  die mehrere Kinder betreffen oder Ziel und Umfang der Story ändern; das
  betroffene Kind bekommt einen Verweis. Bewusste Ausnahmen sind erlaubt.
- **Inhalt:** Protokoll statt Ergebnisliste. Je Thema: Kernfrage, geprüfte
  Optionen mit Vor- und Nachteilen, Empfehlung, Entscheidung des Owners mit
  Begründung, verworfene Optionen mit Grund. Unentschiedenes sofort unter
  Open. Bei mehreren Themen zuerst ein Themenplan.
- **Zeitpunkt:** nach jeder beantworteten Frage, bevor die nächste kommt.

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
- Keine feste Längengrenze; ab 15 Punkten unter Beschlossen gibt es einen
  Hinweis (Spec schreiben oder Item teilen?), nie eine Ablehnung.

Regeln für das Protokoll:

- Erledigte Open-Punkte früherer Einträge werden im neuen Eintrag
  ausdrücklich geschlossen ("Open vom <Datum> (X) erledigt: …").
- Das Protokoll wird nur angehängt. Werden ältere Einträge umgeschrieben,
  gibt es einen Hinweis (Korrekturen bleiben möglich).

## Absicherung des Kopfs

- Stempelzeile am Ende des Kopfs:
  `Stand bestätigt nach Eintrag <YYYY-MM-DD> — <Thema> (<Prüfsumme>)`.
  Prüfsumme: SHA-256 über das Protokoll in kanonischer Form (alle Einträge
  ab der ersten Zeile `## YYYY-MM-DD — `, LF, ohne Leerzeichen am
  Zeilenende, genau ein Zeilenumbruch am Ende), davon die ersten 12
  Hex-Zeichen. Die Definition steht in `format.md` und gilt gleich für
  ToDo-Viewer und `backlog.py`.
- Der Stempel enthält die Prüfsumme des Protokolls zum Zeitpunkt der
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
- Ein fehlender Kopf (Zustand `missing`) zählt für den Hook wie ein
  veralteter.
- Reminder (Prüfidee B): Aktives Item ist eines, das in der Session auf
  `In progress` gesetzt oder dessen Spec gelesen wurde. Nach 5 Turns ohne
  Notes-Eintrag zu diesem Item erinnert ein Hook daran (kein Blocker).
- Nachfrage beim Ort (Prüfidee A): Ein Notes-Eintrag an eine Story, während
  eines ihrer Kinder `In progress` ist, ergibt einen Hinweis ("TASK-x ist in
  Arbeit, gehört das dorthin?"). Nur Nachfrage, nie Ablehnung, weil es
  berechtigte Ausnahmen gibt.
- Nicht umgesetzt: Prüfung auf fehlende Begründungen (C) und Prüfung durch ein
  zweites Modell (D).

## Umstellung

1. ToDo-Viewer zuerst, abwärtskompatibel: neue Endpunkte zusätzlich, alte
   unverändert; Notes ohne Kopf sind `missing`, kein Fehler.
2. Danach das Harness-Release mit Skill, Helfer und Hooks. Der Harness prüft
   vor Nutzung, ob der Viewer Köpfe unterstützt; sonst ein klarer Hinweis
   statt Blockade.
3. Bestehende Notes bekommen den Kopf beim nächsten Bearbeiten (erzwungen
   durch den Hook); kein Massenlauf, archivierte Items bleiben ohne Kopf.

## Schnittstelle zum ToDo-Viewer (API-Modus)

Umsetzung im ToDo-Viewer (Neubau, `server/`) ist eigene Arbeit dort. Heute
liegt jede Notes-Datei als ein Text in `backlog_documents`; `POST
/items/{ref}/notes` hängt einen Eintrag an. Der Harness erwartet:

1. **Datenmodell:** Kopf 1:1 zum Item (Inhalt, Prüfsumme und Eintrag, gegen
   den bestätigt wurde, Revision), Protokolleinträge 1:n (Datum, Thema,
   Markdown-Text des Eintrags, Reihenfolge). Der Text wird verlustfrei
   gespeichert, nicht nur als Listen, weil Einträge auch per `put-doc`
   entstehen. Migration: bestehende Notes an `## YYYY-MM-DD — ` in Einträge
   zerlegen; ein vorhandener Abschnitt `## Stand` wird Kopf, sonst bleibt der
   Kopf leer.
2. **Prüfsumme:** über das Protokoll in kanonischer Form (alle Einträge, LF,
   ohne Leerzeichen am Zeilenende, ein Zeilenumbruch am Ende), gleich
   berechnet wie in `backlog.py`; die Definition steht in `format.md` und ist
   der gemeinsame Vertrag.
3. **Endpunkte:**
   - Kopf lesen ohne Protokoll (z. B. `GET /items/{ref}/notes/state`).
   - Kopf ersetzen (`PUT …/notes/state`, mit Version); setzt den Stempel.
   - Kopf bestätigen (`POST …/notes/state/confirm`, mit Version); setzt den
     Stempel, ohne den Inhalt zu ändern.
   - `POST /items/{ref}/notes` nimmt optional `state` mit (Kopf ersetzen im
     selben Schritt).
   - Optional: einzelne oder die letzten N Einträge lesen.
   - `GET/PUT …/documents/<ID>_notes.md` bleiben und arbeiten auf der
     zusammengesetzten Datei; `PUT` zerlegt sie wieder.
4. **Zustand melden:** Item (`show`, `index`) trägt einen Zustand des Kopfs:
   `current`, `stale` oder `missing`. Schreibende Antworten auf Notes
   enthalten einen Hinweis, wenn der Kopf danach veraltet ist.
5. **Spiegel:** Encode setzt die Datei zusammen (Titelzeile aus dem aktuellen
   Label und Titel, `## Stand`, Stempelzeile, Protokoll); Decode zerlegt sie
   und übernimmt den Stempel aus der Datei (Files-Modus bestätigt per
   `backlog.py`). Die Titelzeile wird immer aus dem Item erzeugt; damit
   folgt sie auch einem Typwechsel (heute bleibt sie beim alten Label).
6. **Oberfläche:** Kopf oben anzeigen, veralteten Kopf markieren, Protokoll
   einklappbar.
7. **Tests:** Vertragstests für Endpunkte, Prüfsumme (gleiches Ergebnis wie
   `backlog.py`), Migration und Spiegel in beide Richtungen.

## Betroffen

- `plugin/skills/todo/SKILL.md`, `format.md`, `api.md`
- `plugin/scripts/backlog_api.py`, `backlog.py`, `check_backlog.py`
- Hook-Konfiguration des Plugins (Turn-Ende, Reminder)
- ToDo-Viewer (separates Projekt)

## Abnahme

- Neue und bearbeitete Notes haben einen Kopf nach obigem Aufbau mit gültigem
  Stempel; ein veralteter oder fehlender Kopf blockiert das Turn-Ende, bis er
  angepasst oder bestätigt ist.
- Gleiche Prüfsumme in ToDo-Viewer und `backlog.py` für dasselbe Protokoll.
- Ein Harness gegen einen Viewer ohne Köpfe arbeitet weiter und meldet das.
- Reminder B und Nachfrage A erscheinen in den beschriebenen Fällen und
  blockieren nicht.
- Regeln stehen in `SKILL.md`, `format.md`, `api.md`; Tests laufen.
