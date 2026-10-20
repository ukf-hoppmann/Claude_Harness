# TASK-020 — todo-Skill: Ort und Inhalt der Diskussionsprotokolle (Notes) festlegen

## 2026-10-19 — Ausgangslage und Vorschläge zur Prüfung durch den Owner

### Discussed

- Anlass: In einer anderen Session (anderes Projekt) landeten die Klärungen zu einem Task fast vollständig in den Notes der übergeordneten Story; der Task bekam nur eine Zeile. Zudem waren die Einträge zu knapp: Themenliste ohne Kernfragen, abgewogene Optionen und verworfene Varianten fehlten, ein noch unentschiedenes Thema war gar nicht notiert.
- Ist-Stand im Harness: SKILL.md sagt nur 'Record decisions in the item's notes as they happen, dated, under Discussed / Decided / Open'. format.md beschreibt Notes als 'Discussions and decisions' und die Spec als technische Zusammenfassung ohne Schritt-für-Schritt-Plan; Richtungsänderungen gehören in die Notes. Nicht geregelt: welches Item (Story oder Task), Mindestinhalt, Zeitpunkt.
- Regelvorschlag 1 – Ort: Notes ins spezifischste Item, um das es geht. Läuft die Klärung im Rahmen von Task X, gehören sie zu Task X. Story-Notes nur für Entscheidungen, die mehrere Kinder betreffen oder Ziel/Umfang der Story ändern; das betroffene Kind bekommt einen Verweis. Faustregel: Wer nur das Task-Item öffnet, findet dort alles zu diesem Task.
- Regelvorschlag 2 – Inhalt: Protokoll statt Ergebnisliste. Je Thema: Kernfrage, geprüfte Optionen mit Vor- und Nachteilen, Empfehlung, Entscheidung des Owners mit Begründung, verworfene Optionen mit Grund. Unentschiedene Vorschläge sofort unter Open. Bei mehreren Themen ist der erste Eintrag ein Themenplan mit Stand je Thema.
- Regelvorschlag 3 – Zeitpunkt: nach jeder beantworteten Frage schreiben, bevor die nächste Frage kommt, nicht am Ende.
- Regelvorschlag 4 – Spec und Notes: Sobald etwas entschieden ist, kommt das technische Ergebnis in die Spec; die Notes behalten den Weg dorthin (bisher nur implizit geregelt, soll ausdrücklich werden).
- Prüfidee A – Warnung im note-Befehl von backlog_api.py: Notes an eine Story, während eines ihrer Kinder In progress ist, ergeben den Hinweis 'TASK-x ist in Arbeit, gehört das dorthin?'. Billig, verlässlich, trifft genau den beobachteten Fehler.
- Prüfidee B – Reminder 'aktives Item': Der State merkt sich das Item, an dem die Session arbeitet (Status gesetzt, Spec gelesen). Ein UserPromptSubmit- oder Stop-Hook erinnert: 'Aktives Item TASK-x, letzter Notes-Eintrag vor N Turns'. Reminder, kein Blocker; Muster wie bei daily/techdocs.
- Prüfidee C – Strukturprüfung im note-Befehl: decided-Einträge ohne Begründung werden abgelehnt oder bekommen eine Warnung. Eher schwach und leicht zu umgehen.
- Prüfidee D – Prompt-Hook am Stop: Ein kleines Modell prüft, ob im Turn etwas entschieden oder abgewogen wurde, das nicht protokolliert ist. Semantisch, aber teuer, kostet bei jedem Turn Zeit und ist unzuverlässig.

### Decided

- Item angelegt als Task ohne Parent, Priorität Urgent (Owner: dringend). Ohne Parent wie die vergleichbaren TASK-014 und TASK-018; der thematisch nächste Parent EPIC-005 ist abgeschlossen.

### Open

- Owner liest die Vorschläge und entscheidet später (ausdrücklich nicht sofort), welche Regeln (1–4) und Prüfungen (A–D) umgesetzt werden.
- Empfehlung von Claude: Regeln 1–4 in den Skill, dazu Prüfidee A; B optional; C schwach; D nicht umsetzen.

## 2026-10-20 — Aufbau der Notes-Datei: Kopf mit Stand plus Protokoll (Regelvorschlag 5)

### Discussed

- Anlass: Der Owner findet lange Notes unübersichtlich (z. B. STORY-027_notes.md mit 277 Zeilen, 13 Einträgen). Die Datei ist ein reines Protokoll zum Anhängen; der aktuelle Stand muss aus allen Einträgen rekonstruiert werden. Früher offene Punkte werden später erledigt, ohne dass das vermerkt wird; Entscheidungen sind über Einträge verstreut und teils überholt. Das Summary im TODO.md-Eintrag ist eine stabile, laienverständliche Beschreibung, kein Stand.
- Regelvorschlag 5 – Aufbau: Oben ein Kopf (Abschnitt 'Stand'), der bei jedem neuen Eintrag ersetzt statt ergänzt wird, mit Ziel/Status (sehr kurz), Offen, Beschlossen, Nächster Schritt, Verweise (Spec, Kinder, verwandte Items). Darunter das bisherige Protokoll (Discussed/Decided/Open), nur angehängt. Reihenfolge der Kopf-Abschnitte noch nicht fix.
- Nutzen für die LLM: Für den Arbeitsstand reichen Kopf und Spec; das Protokoll wird nur gelesen, wenn eine Begründung nachvollzogen werden muss. Spart Kontext und vermeidet Fehldeutungen (z. B. erledigtes Open für offen halten).
- Länge des Kopfs (Empfehlung Claude): keine feste Grenze von 10–15 Zeilen, weil lange Klärungen dann keinen Platz finden. Stattdessen Regeln statt Zeilenlimit: ein Punkt pro Zeile mit Datum als Verweis ins Protokoll; nur geltender Stand, überholte Entscheidungen fallen aus dem Kopf (bleiben im Protokoll); technische Details in die Spec, im Kopf nur ein Satz und Verweis. Ein sehr langer Kopf ist ein Signal, das Item zu teilen oder Inhalt in die Spec zu verschieben.
- Ergänzungen: Erledigte Open-Punkte werden im neuen Eintrag ausdrücklich geschlossen ('Open vom <Datum> (X) erledigt: …'). Reine Fortschrittsmeldungen ('TASK-x umgesetzt') gehören nicht als eigener Eintrag in die Notes, sondern in Status, Daily Report oder eine Zeile im Kopf.
- Prüfidee E: Der note-Befehl von backlog_api.py bekommt ein Feld 'state' und ersetzt damit den Kopf bei jedem Eintrag; fehlt es, gibt es eine Warnung. Damit kann der Kopf nicht vergessen werden und veraltet nicht.

### Decided

- Owner stimmt der Idee Kopf (Stand) plus Protokoll grundsätzlich zu: Übersicht oben, Entscheidungsweg bleibt protokolliert.

### Open

- Ob der Kopf eine weiche Längengrenze bekommt (z. B. Warnung ab etwa 40 Zeilen) oder gar keine.
- Reihenfolge der Kopf-Abschnitte (Vorschlag Claude: Ziel/Status, Nächster Schritt, Offen, Beschlossen, Verweise).
- Ob Prüfidee E umgesetzt wird und wie bestehende Notes-Dateien einen Kopf bekommen (nachträglich oder erst beim nächsten Eintrag).
- Weiterhin offen: Entscheidung des Owners zu Regeln 1–4 und Prüfideen A–D.
