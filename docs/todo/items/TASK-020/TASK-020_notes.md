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

## 2026-10-20 — Kopf: Reihenfolge, Längenhinweis, Abgrenzung zur Spec

### Discussed

- Abgrenzung Notes/Spec: Laut format.md ist die Spec eine technische Zusammenfassung (Was und Warum, Randbedingungen, Schnittstellen, betroffene Dateien, Abnahmekriterien), aus der ohne weiteres Zutun des Owners ein Plan entstehen kann; sie enthält selbst keinen Schritt-für-Schritt-Plan. Nicht geregelt ist, wann sie geschrieben wird (am Ende oder fortlaufend). Owner-Verständnis: Notes sind das Gesprächsprotokoll, in dem auch technisch entschieden wird; die Spec entsteht am Ende.
- Klarstellung zum Kopf: 'Technische Details in die Spec' heißt nicht, dass die Spec eine Sammlung von Details ist. Gemeint: Der Kopf nennt jede Entscheidung in einer Zeile; die vollständige, planfähige Beschreibung steht in der Spec, sobald es sie gibt. Vorher stehen die Einzelheiten im Protokoll.
- Empfehlung Claude: Spec fortlaufend schreiben, sobald Entscheidungen stabil sind (wie Regelvorschlag 4), damit bei langen Items der Kopf nicht alles tragen muss und am Ende kein großer Übertragungsschritt nötig ist.
- Längenhinweis: nach Zeilen (misst Kontextkosten, aber umgehbar durch lange Zeilen) oder nach Anzahl beschlossener Punkte (misst, ob das Item zu groß ist oder in Spec bzw. Kinder gehört). Empfehlung Claude: Anzahl der Punkte unter Beschlossen, Hinweis mit Vorschlag 'Spec schreiben oder Item teilen'. Owner nennt als Beispiel Task 6 in ezf-ui, wo alle Elemente geplant und später getrennt umgesetzt werden; so ein langer Kopf kann sinnvoll sein.

### Decided

- Reihenfolge des Kopfs: Ziel/Status, Nächster Schritt, Offen, Beschlossen, Verweise.
- Ein langer Kopf ergibt nur einen Hinweis, nie eine Ablehnung, weil manche Items bewusst lang werden.
- Open vom 2026-10-20 (Reihenfolge der Kopf-Abschnitte) damit erledigt; Open (weiche Längengrenze) teilweise erledigt: nur Hinweis, Maßstab noch offen.

### Open

- Maßstab des Hinweises: Zeilen oder Anzahl beschlossener Punkte, und ab welchem Wert.
- Wann die Spec geschrieben wird: am Ende der Klärung oder fortlaufend.
- Prüfidee E und Umgang mit bestehenden Notes-Dateien weiterhin offen.

## 2026-10-20 — Spec fortlaufend, Plan speichern, Absicherung des Kopfs

### Discussed

- Plan speichern? Ist-Stand: Die decomposition-Regeln trennen zwei Ebenen. Grob: Stories und Tasks im Backlog, ein Task passt in eine Session. Fein: Abschnitte des Umsetzungsplans, die in Plan Mode oder im Chat entstehen; die Spec bleibt ohne Schrittfolge. Nach Freigabe des Plans läuft die Umsetzung im Worktree ohne Rückfragen.
- Empfehlung Claude: Den Feinplan nicht im Backlog speichern. Er hängt vom Codestand beim Start der Umsetzung ab, veraltet schnell und ist aus Spec, Architekturregeln und decomposition-Regeln jederzeit neu ableitbar. Der dauerhafte Plan ist die Zerlegung in Kinder-Items (jedes mit eigener Spec bzw. eigenem Ziel), die eine neue Session ohne Rückfragen umsetzen kann. In die Notes kommt nur eine Zeile, dass der Plan freigegeben wurde, sowie Abweichungen vom Plan, die sich bei der Umsetzung ergeben.
- Prüfstein für eine fertige Spec: Eine neue Session ohne den Kontext der Diskussion kann daraus ohne Rückfragen einen Plan erstellen.
- Hook für den Kopf: Ein Hook, der in jedem Turn nachfragt, ob der Kopf angepasst wurde, wäre Rauschen und würde bald ignoriert. Zwei gezielte Absicherungen decken die beiden Fehlerfälle ab: (1) Notes geschrieben, Kopf nicht angepasst: Prüfidee E im Helfer, deterministisch beim Schreiben (note ohne 'state' ergibt eine Warnung; put-doc auf Notes ohne Abschnitt Stand ebenso). (2) Diskutiert, aber gar nichts notiert: Prüfidee B, Stop-Hook-Reminder nur, wenn ein aktives Item existiert und seit N Turns kein Notes-Eintrag erfolgte.
- Empfehlung Claude: E umsetzen (billig, verlässlich), B als Reminder dazu; einen Hook bei jedem Turn nicht.

### Decided

- Die Spec wird fortlaufend geschrieben, sobald Entscheidungen stabil sind; sie ist die geregelte technische Darstellung und wird am Ende der Klärung noch einmal geprüft, statt erst am Ende zu entstehen. Open vom 2026-10-20 (Zeitpunkt der Spec) damit erledigt.
- Owner: Die Absicherung, dass der Kopf aktuell ist, ist sehr wichtig.

### Open

- Plan speichern oder mit der Spec enden (Empfehlung Claude: mit der Spec enden, Zerlegung über Kinder-Items).
- Absicherung des Kopfs: E und B wie empfohlen oder ein anderer Hook.
- Maßstab des Längenhinweises; Umgang mit bestehenden Notes-Dateien; Regeln 1–4 und Prüfideen A, C, D.
