# STORY-051 — todo-Skill: Ort und Inhalt der Diskussionsprotokolle (Notes) festlegen

## State

- Goal/Status: Regeln für Ort, Inhalt, Zeitpunkt und Aufbau der Item-Notes festgelegt und mechanisch abgesichert. Alle Tasks Completed, Abschlusskriterien erfüllt, wartet auf Bestätigung.
- Next step: Owner bestätigt; echter Hook-Lauf in einer neuen Session; danach das Harness-Release.
- Open:
  - Echter Hook-Lauf in einer neuen Session (Block, Reminder, Form von tool_response)
  - Harness-Release (Vorschlag Patch 0.12.6) nach der Bestätigung
- Decided:
  - TASK-021 bis TASK-025 vom Owner bestätigt; Release des Harness erst am Ende der Story (2026-10-21, 2026-10-22)
  - Feste Überschriften von Kopf und Stempel auf Englisch (Regel 6), Inhalt in docs.language; der Viewer zeigt sie lokalisiert an (2026-10-21)
  - Notes: Kopf oben (wird ersetzt), darunter das Protokoll (wird nur angehängt); Marker Goal/Status, Next step, Open, Decided, References (2026-10-20)
  - Protokollregeln: spezifischstes Item, Kernfrage/Optionen/Entscheidung mit Begründung/Verworfenes, nach jeder geklärten Frage schreiben (2026-10-20)
  - Spec ist immer der aktuelle Stand; Besprechung endet mit der Spec; Umsetzungsplan erst beim Start, nicht gespeichert (2026-10-20)
  - Kopf wird nach jeder Änderung der Notes angepasst oder bestätigt; Stempel mit Prüfsumme, gesetzt von Server bzw. backlog.py; Hook am Turn-Ende blockiert bis dahin (2026-10-20)
  - Prüfidee A nur als Nachfrage, B als Reminder; C und D nicht (2026-10-20)
  - Langer Kopf nur Hinweis (ab 15 Beschlüssen); Umschreiben älterer Einträge nur Hinweis (2026-10-20)
  - Viewer hat Kopf und Protokoll getrennt und englische Überschriften; ältere Notes werden beim nächsten Bearbeiten migriert (2026-10-21)
  - Hooks im API-Modus ohne Netzwerk: PostToolUse-Hook liest die [harness]-Zeilen des Helfers (Weg A, TASK-024, 2026-10-22)
- References: Spec STORY-051_spec.md; TASK-021 Regeln und Format, TASK-022 Files-Modus, TASK-023 API-Helfer, TASK-024 Hooks, TASK-025 Nachfrage A, jeweils mit eigener Spec; Item im Backlog des ToDo-Viewers (vom Owner angelegt)

State confirmed after entry 2026-10-22 — Abnahmeprüfung nach TASK-024 (f7e0263cd2be)

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

## 2026-10-20 — Prüfidee E geschärft

### Discussed

- Einwand des Owners: E in der bisherigen Form prüft nur, ob ein Kopf vorhanden ist. Eine bestehende Notes-Datei kann per put-doc geändert werden, ohne dass der Kopf angepasst wird; auch bei note könnte der alte Kopf unverändert mitgeschickt werden.
- Grenze: Ob der Kopf inhaltlich stimmt, lässt sich mechanisch nicht prüfen (das wäre Prüfidee D, verworfen wegen Kosten und Unzuverlässigkeit). Mechanisch prüfbar ist, ob der Kopf nach der letzten Änderung bewusst neu geschrieben wurde.
- Vorschlag E1 – Stempel: Der Server schreibt in den Kopf selbst eine Zeile 'Stand nach Eintrag <Datum> — <Thema>'. Ist der neueste Protokolleintrag jünger als der Stempel, ist der Kopf veraltet; Helfer, Check und Viewer melden das.
- Vorschlag E2 – note: 'state' ist Pflicht, der Server ersetzt den Kopf und setzt den Stempel. Ist der neue Kopf identisch mit dem alten, gibt es eine Warnung ('Kopf unverändert, stimmt das?').
- Vorschlag E3 – put-doc auf Notes: Der Server vergleicht alt und neu. Protokoll geändert, Kopf aber nicht: Warnung. Ältere Protokolleinträge geändert: Warnung, weil das Protokoll nur angehängt wird (Korrekturen ausgenommen, aber bewusst).
- Empfehlung Claude: E1 bis E3 zusammen umsetzen; zusammen mit B ergibt das: Kopf wird bei jedem Schreiben erzwungen und gestempelt, Veralten ist sichtbar, und B erinnert, wenn gar nicht geschrieben wird.

### Decided

- Prüfidee B (Reminder bei aktivem Item ohne aktuellen Notes-Eintrag) wird umgesetzt.

### Open

- Ob E in der geschärften Form (E1–E3) umgesetzt wird.
- Plan speichern oder mit der Spec enden; Maßstab des Längenhinweises; Umgang mit bestehenden Notes-Dateien; Regeln 1–4 und Prüfideen A, C, D.

## 2026-10-20 — Kopf-Absicherung: Stempel plus Hook statt Pflicht-Kopf

### Discussed

- Owner-Vorschlag: Nicht bei jedem Eintrag muss ein neuer Kopf mit. Wurden die Notes angefasst, muss der Kopf entweder geändert oder bewusst unverändert bestätigt werden. Umsetzung: Kopf trägt einen Stempel (wie E1); weicht der Stempel vom letzten Stand der Notes ab, fragt ein Hook, ob der Kopf aktuell ist; die LLM prüft den Kopf und passt ihn an oder bestätigt ihn, womit der Stempel nachgezogen wird.
- Ergänzungen Claude: (1) Den Stempel setzt der Server, nicht die LLM per Hand: ein neuer Befehl, z. B. 'confirm-state <ID>' (Kopf unverändert bestätigt) bzw. ein optionales 'state' bei note/put-doc (Kopf geändert); beides setzt den Stempel. Vermeidet falsch abgetippte Zeitstempel. (2) Der Stempel verweist auf die Version bzw. den Eintrag, gegen den bestätigt wurde, damit das Setzen des Stempels selbst die Notes nicht wieder 'veraltet' erscheinen lässt. (3) Hook am Stop statt direkt nach dem Schreiben, weil Eintrag und Kopf oft in zwei Aufrufen kommen; geprüft werden nur Items, deren Notes in dieser Session geändert wurden. (4) Der Stop-Hook kann das Turn-Ende blockieren, bis Kopf geändert oder bestätigt ist; Endlosschleife ausgeschlossen, weil Bestätigen ihn immer auflöst.
- Damit entfallen E2 (Pflicht-Kopf bei note) und die Kopf-Warnung aus E3; die Warnung beim Umschreiben älterer Protokolleinträge (E3) bleibt als eigener Vorschlag.

### Decided

- Kein Pflicht-Kopf bei jedem Eintrag. Nach jeder Änderung der Notes wird der Kopf entweder angepasst oder bewusst als aktuell bestätigt; abgesichert über einen Stempel im Kopf und einen Hook, der bei veraltetem Stempel nachfragt.

### Open

- Ergänzungen (1)–(4) bestätigen, insbesondere ob der Hook das Turn-Ende blockiert oder nur erinnert.
- Warnung beim Umschreiben älterer Protokolleinträge (Rest von E3).
- Plan speichern oder mit der Spec enden; Maßstab des Längenhinweises; Umgang mit bestehenden Notes-Dateien; Regeln 1–4 und Prüfideen A, C, D.

## 2026-10-20 — Stempel im Files-Modus, Kopf und Protokoll in der API getrennt

### Discussed

- Owner: Ergänzung 1 (Server setzt den Stempel) gilt nur für die API. Im Files-Modus, relevant für das Arbeiten online (Cloud), gibt es keinen Server.
- Vorschlag Claude: Stempel als Prüfsumme des Protokolls statt Zeitstempel, z. B. 'Stand bestätigt nach Eintrag <Datum> — <Thema> (<Hash>)'. Veraltet heißt: Prüfsumme des aktuellen Protokolls weicht vom Stempel ab. Funktioniert in beiden Modi gleich, ist unabhängig von Dateizeiten (git checkout, Kopieren) und löst Ergänzung 2 von selbst, weil das Setzen des Stempels das Protokoll nicht ändert. Files-Modus: backlog.py bekommt einen Befehl zum Bestätigen, der den Stempel schreibt; die vorhandene Backlog-Prüfung am Turn-Ende meldet veraltete Köpfe. API-Modus: der Server rechnet und setzt ihn.
- Kopf und Protokoll in der API getrennt oder am Stück? Empfehlung Claude: in der API getrennt (Kopf 1:1 zum Item, Protokolleinträge 1:n), mit eigenen Befehlen zum Lesen des Kopfs, zum Ersetzen und zum Bestätigen. Hauptnutzen: Die LLM liest zuerst nur den Kopf, das Protokoll nur bei Bedarf; spart Kontext. Veraltet ist im Datenmodell direkt ablesbar (Kopf bestätigt gegen Eintrag X, neuester Eintrag Y). Nach außen bleibt es eine Markdown-Datei (Kopf oben, Protokoll darunter), damit Files-Modus, Spiegel und Git gleich aussehen; der Server zerlegt und setzt beim Sync zusammen.
- Betroffen ist dann auch der ToDo-Viewer (eigenes Projekt, nicht in diesem Repo): Datenmodell, Endpunkte, Sync. Das ist eigene Arbeit dort; dieser Task beschreibt die Schnittstelle, die der Harness erwartet.
- Der Hook soll die LLM zwingen, den Kopf anzusehen und ihn bewusst zu lassen oder zu ändern; er blockiert also das Turn-Ende (Ergänzung 4).

### Decided

- Ergänzungen 2–4 übernommen: Stempel verweist auf den bestätigten Stand; Hook am Turn-Ende, nur für in der Session geänderte Notes; Hook blockiert, bis der Kopf angepasst oder bewusst bestätigt ist. Open vom 2026-10-20 (Ergänzungen 1–4) damit bis auf 1 erledigt.

### Open

- Stempel als Prüfsumme in beiden Modi (statt vom Server gesetzter Zeit).
- Kopf und Protokoll in der API getrennt speichern und lesen, nach außen eine Datei; Abstimmung mit dem ToDo-Viewer.
- Warnung beim Umschreiben älterer Protokolleinträge; Plan speichern oder mit der Spec enden; Maßstab des Längenhinweises; Umgang mit bestehenden Notes-Dateien; Regeln 1–4 und Prüfideen A, C, D.

## 2026-10-20 — Prüfsumme und Trennung beschlossen

### Decided

- Stempel als Prüfsumme des Protokolls in beiden Modi (API: Server berechnet; Files: Bestätigungsbefehl in backlog.py, Meldung über die Backlog-Prüfung am Turn-Ende). Open vom 2026-10-20 (Prüfsumme) erledigt.
- In der API werden Kopf und Protokoll getrennt gespeichert (Kopf 1:1, Einträge 1:n) mit eigenen Befehlen zum Lesen, Ersetzen und Bestätigen des Kopfs; nach außen bleibt es eine Markdown-Datei. Die Umsetzung im ToDo-Viewer ist eigene Arbeit dort; TASK-020 beschreibt die erwartete Schnittstelle. Open vom 2026-10-20 (Trennung) erledigt.

### Open

- Plan speichern oder mit der Spec enden (Empfehlung Claude: mit der Spec enden, Zerlegung über Kinder-Items).
- Maßstab des Längenhinweises (Empfehlung Claude: Anzahl Punkte unter Beschlossen) und Schwellwert.
- Warnung beim Umschreiben älterer Protokolleinträge.
- Umgang mit bestehenden Notes-Dateien (Kopf nachträglich oder beim nächsten Eintrag).
- Regeln 1–4 und Prüfideen A, C, D.

## 2026-10-20 — Umwandlung in Story, Kopf ergänzt

### Discussed

- Der Umfang reicht inzwischen über eine Session hinaus: Skill-Regeln und Format, Helfer und Prüfung, Hooks, Schnittstelle zum ToDo-Viewer. Nach den Zerlegungsregeln ist das eine Story mit Tasks.

### Decided

- Owner: TASK-020 wird zur Story; neue ID STORY-051 (retype). Überschriften von Notes und Spec auf STORY-051 angepasst; ältere Protokolleinträge nennen weiter TASK-020.
- Owner: Diese Notes bekommen schon jetzt einen Kopf nach dem beschlossenen Aufbau, von Hand und ohne Prüfsumme, bis der Mechanismus gebaut ist.

### Open

- Zerlegung in Tasks (Vorschlag folgt).
- Goal und Completion criteria der Story decken Aufbau und Absicherung der Notes noch nicht ab; Anpassung braucht Owner-Freigabe.

## 2026-10-20 — Goal angepasst, Zerlegung in Tasks, Liste für den ToDo-Viewer

### Discussed

- Owner wünscht eine Liste, was im ToDo-Viewer anzupassen ist. Grundlage: Neubau in server/ (Port 5411); Notes liegen heute als ein Text in backlog_documents, POST /items/{ref}/notes hängt Einträge an, der Spiegel arbeitet in beide Richtungen. Liste steht in der Spec (Abschnitt Schnittstelle zum ToDo-Viewer): Datenmodell mit Migration, Prüfsumme als gemeinsamer Vertrag mit backlog.py, Endpunkte für Kopf lesen/ersetzen/bestätigen, Zustand current/stale/missing, Spiegel zusammensetzen/zerlegen, Oberfläche, Vertragstests.
- Beobachtung: Beim Typwechsel blieb die Titelzeile der Notes beim alten Label (TASK-020); wird mit der aus dem Item erzeugten Titelzeile behoben.

### Decided

- Owner: Goal, Completion criteria und Summary der Story erweitert um Aufbau und Absicherung der Notes. Open vom 2026-10-20 (Goal anpassen) erledigt.
- Owner: Zerlegung in TASK-021 (Regeln und Format im todo-Skill), TASK-022 (Kopf-Prüfsumme im Files-Modus), TASK-023 (Kopf-Befehle im API-Helfer), TASK-024 (Hooks: Kopf-Pflicht am Turn-Ende, Reminder B). TASK-022 und TASK-023 hängen von TASK-021 ab, TASK-024 von beiden. Prüfidee A bekommt keinen Task, solange sie nicht beschlossen ist. Open vom 2026-10-20 (Zerlegung) erledigt.

### Open

- Item im Backlog des ToDo-Viewers anlegen (braucht ausdrückliche Freigabe für dieses Projekt).

## 2026-10-20 — ToDo-Viewer-Item angelegt, Umstellung synchron

### Discussed

- Owner: Die Umstellung muss weitgehend synchron erfolgen, damit alle Projekte wissen, wie sie mit der neuen Struktur umgehen.
- Vorschlag Claude zur Reihenfolge: ToDo-Viewer zuerst und abwärtskompatibel (neue Endpunkte zusätzlich, alte unverändert, fehlender Kopf ist Zustand 'missing', kein Fehler). Danach Harness-Release, das die neuen Befehle nutzt; der Helfer prüft beim Start, ob der Viewer Köpfe unterstützt (Fähigkeit oder Mindestversion), und der Hook greift nur dann; sonst ein klarer Hinweis statt Blockade. So muss nicht auf die Minute synchron umgestellt werden, und kein Projekt bricht.
- Bestehende Notes: Kopf erst beim nächsten Anfassen anlegen, erzwungen durch den Hook (Zustand 'missing' zählt wie 'stale'); kein Massenlauf über alle Items, archivierte bleiben ohne Kopf.

### Decided

- Owner hat das Item im Backlog des ToDo-Viewers selbst angelegt. Open vom 2026-10-20 (Item im ToDo-Viewer anlegen) erledigt.

### Open

- Reihenfolge und Kompatibilität der Umstellung (Vorschlag oben).
- Format der Stempelzeile und Definition der Prüfsumme (Vorschlag: SHA-256, erste 12 Hex-Zeichen).
- Reminder B: was als aktives Item gilt und nach wie vielen Turns er erinnert.

## 2026-10-20 — Entscheidungen zu Prüfideen, Protokollregeln, Plan, Umstellung

### Discussed

- Claude hat die Prüfideen und den Reminder B in einfacher Sprache erklärt und die offenen Fragen auf vier Owner-Entscheidungen reduziert; rein technische Punkte entscheidet Claude selbst.
- Owner zu A: Es gibt berechtigte Fälle, in denen etwas im Rahmen eines Tasks besprochen, aber in der Story oder einem anderen Task protokolliert wird. A darf deshalb nur nachfragen, nie verhindern.
- Owner zu Plan und Spec: Die Spec wird regelmäßig aktualisiert, sobald Neues dazukommt. Sie ist immer der aktuelle Stand und kein Element der Entscheidungsfindung; die Entscheidungsfindung steht in den Notes.

### Decided

- Prüfidee A umsetzen, nur als Nachfrage (Hinweis), nie als Blockade.
- Prüfidee B umsetzen (bestätigt).
- Prüfideen C und D werden nicht umgesetzt.
- Regeln 1–4 vom 2026-10-19 übernommen: Ort (spezifischstes Item), Inhalt (Kernfrage, Optionen, Entscheidung mit Begründung, Verworfenes), Zeitpunkt (nach jeder geklärten Frage), Spec und Notes getrennt.
- Die Besprechung endet mit der Spec; der Umsetzungsplan entsteht erst beim Start der Umsetzung, wird zur Freigabe vorgelegt und nicht dauerhaft gespeichert. Die Spec ist immer der aktuelle Stand.
- Umstellung: zuerst ToDo-Viewer abwärtskompatibel, danach das Harness-Release; bestehende Notes bekommen den Kopf beim nächsten Bearbeiten, kein Massenlauf.
- Technisch von Claude festgelegt (Owner: muss nicht entscheiden): Prüfsumme SHA-256, erste 12 Hex-Zeichen; Stempelzeile 'Stand bestätigt nach Eintrag <Datum> — <Thema> (<Prüfsumme>)'; Längenhinweis ab 15 Punkten unter Beschlossen; Hinweis beim Umschreiben älterer Protokolleinträge; Reminder B: aktives Item = in der Session auf In progress gesetzt oder Spec gelesen, Erinnerung nach 5 Turns ohne Notes-Eintrag; Harness prüft vor Nutzung, ob der Viewer Köpfe unterstützt.
- Damit alle bisher offenen Punkte erledigt.

### Open

- Prüfidee A braucht einen eigenen Task (Vorschlag folgt).

## 2026-10-20 — TASK-025 angelegt, Specs für alle Tasks

### Discussed

- Owner möchte nur noch 'umsetzen' sagen können. Dafür hat jeder Task TASK-021 bis TASK-025 eine eigene Spec bekommen, die auf die Story-Spec verweist und Umfang, Abgrenzung und Abnahme festlegt.
- Reihenfolge: TASK-021 zuerst; danach TASK-022 und TASK-025 (unabhängig vom ToDo-Viewer); TASK-023 braucht die Erweiterung im ToDo-Viewer (sonst gegen Mock); TASK-024 zuletzt. Die Abhängigkeit von TASK-023 zum ToDo-Viewer-Item ist projektübergreifend und nur in der Spec vermerkt.

### Decided

- Owner: TASK-025 (Nachfrage bei Notes an eine Story mit Kind in Arbeit) angelegt, abhängig von TASK-021, für die Story erforderlich. Open vom 2026-10-20 (Task für Prüfidee A) erledigt.

## 2026-10-21 — ToDo-Viewer umgesetzt, Abgleich mit dem Harness

### Discussed

- Owner: Die Aufteilung in Kopf und Protokoll ist im ToDo-Viewer schon umgesetzt (dort TASK-044, v0.8.14, läuft auf Port 5411).
- Abgleich Claude mit dem Code und interfaces.md des Viewers: Endpunkte state (lesen), put-state, confirm-state, entries; note mit optionalem state und state_version; notes_state in show/list und Spalte Notes im index; Hinweise notes_state_stale, notes_state_long (ab 15 Beschlüssen), notes_history_rewritten; Prüfsumme und Stempelzeile genau wie in der Spec; Testvektoren in tests/fixtures/notes-state/checksum.json. Die Titelzeile kommt jetzt aus dem Item.
- Abweichung: /core/health meldet keine Version. Claude legt fest: Der Harness erkennt die Unterstützung am Feld notes_state in show bzw. an einer 404 auf notes/state.
- Probe: Der Kopf dieser Notes war stale (handgeschriebene Stempelzeile ohne Prüfsumme) und wurde über put-state ersetzt; der Server hat gestempelt, Zustand current.

### Decided

- TASK-023-Spec an die tatsächliche Schnittstelle angepasst; die Entwicklung gegen eine Attrappe entfällt. Testvektoren werden in die Harness-Tests kopiert.

## 2026-10-21 — Konflikt mit Architekturregel 6 (Sprache der Überschriften)

### Discussed

- Beim Start der Umsetzung geprüft: Architekturregel 6 verlangt, dass maschinell geprüfte Feldnamen und Überschriften Englisch bleiben (wie Discussed/Decided/Open). Kopf und Stempel sind aber deutsch und werden maschinell geprüft: '## Stand', '- Beschlossen:' (Zählung für den Längenhinweis), 'Stand bestätigt nach Eintrag …'. Im ToDo-Viewer v0.8.14 fest so eingebaut. Projekte mit docs.language = en bekämen deutsche Überschriften.
- Optionen: (1) Englisch: '## State', '- Goal/Status:', '- Next step:', '- Open:', '- Decided:', '- References:', Stempel 'State confirmed after entry <Datum> — <Thema> (<Prüfsumme>)'; braucht eine kleine Änderung im ToDo-Viewer (Konstanten, Tests, Migration der schon gestempelten Köpfe, bisher nur STORY-051). (2) Ausnahme von Regel 6: Deutsch bleibt fest für alle Projekte. (3) Sprachabhängig nach docs.language: Viewer und Harness müssten beide Sprachen erkennen; mehr Aufwand, fehleranfällig.
- Empfehlung Claude: Option 1, einheitlich mit Discussed/Decided/Open; der Inhalt des Kopfs bleibt in docs.language.
- Kein Konflikt: Architekturregel 2 (Hooks ohne Netzwerk). Der Hook aus TASK-024 fragt den Viewer nicht selbst; der Helfer merkt sich den Zustand des Kopfs aus den Antworten des Servers im Session-State, der Hook liest nur diesen.

### Open

- Sprache der Überschriften: Option 1, 2 oder 3.

## 2026-10-21 — Englische Überschriften beschlossen

### Discussed

- Unverändert bleiben Titelzeile '# <ID> — <Titel>', Eintragsüberschrift '## YYYY-MM-DD — <Thema>' und '### Discussed/Decided/Open'. Hinweise des Servers: der Harness wertet nur die stabilen Codes aus; Meldungstexte, die die LLM liest, sollten wie alle Hook-Meldungen Englisch sein (Regel 6).

### Decided

- Owner: Option 1. Die festen Überschriften und Marker von Kopf und Stempel sind Englisch: '## State', '- Goal/Status:', '- Next step:', '- Open:', '- Decided:', '- References:', Stempel 'State confirmed after entry <YYYY-MM-DD> — <Thema> (<Prüfsumme>)'. Der Inhalt bleibt in docs.language. Weil die Überschriften fest sind, kann der Viewer sie in seiner Oberfläche lokalisiert anzeigen. Open vom 2026-10-21 (Sprache der Überschriften) erledigt.
- Owner passt den ToDo-Viewer an; Claude stellt danach den Kopf dieser Notes um und schreibt die englischen Überschriften in Spec und todo-Skill.

## 2026-10-21 — Release zurückgehalten, weiter mit TASK-022

### Discussed

- Nach dem Merge von TASK-021 verlangt der semver-Skill ein Release (patch 0.12.1). Das widerspricht der vereinbarten Reihenfolge (Viewer zuerst, dann Harness), solange der Viewer noch ## Stand schreibt.

### Decided

- Owner: Release zurückhalten bis zum Ende der Story; dann ein Release mit allen Änderungen, einschließlich 7e7e8b1 (nummerierte Completion criteria).
- Owner: weiter mit TASK-022.

## 2026-10-21 — Viewer auf englische Überschriften umgestellt, Migration nur teilweise

### Discussed

- Der Owner hat den ToDo-Viewer auf die englischen Überschriften umgestellt. Migriert wurden nur die Notes, die der Viewer selbst braucht; alle anderen werden nicht gesammelt umgestellt.

### Decided

- Ältere Notes werden beim nächsten Bearbeiten migriert, nicht auf Vorrat (Owner, 2026-10-21). Begründung: Aufwand fällt nur dort an, wo die Notes ohnehin angefasst werden.
- TASK-021 und TASK-022 vom Owner bestätigt (Completed). Weiter mit TASK-025.

## 2026-10-22 — Abnahmeprüfung nach TASK-024

### Discussed

- Alle fünf Tasks sind Completed (TASK-021 bis TASK-025); TASK-024 hat der Owner am 2026-10-22 bestätigt. Geprüft wurden die Abschlusskriterien und der Abschnitt Abnahme der Spec gegen den Stand.
- Kriterium 1, Regeln in Skill und format.md: erfüllt (TASK-021; Kopf, Marker, Protokollregeln, Abgrenzung der Notes). Ergänzt: api.md und SKILL.md nennen die [harness]-Zeilen, die Blockade und den Reminder (TASK-024).
- Kriterium 2, Prüfsumme in API- und Files-Modus gesetzt und geprüft: erfüllt. Files-Modus: backlog.py, notes_head.py, Stop-Hook check_backlog.py (TASK-022). API-Modus: Der Server setzt den Stempel; der Helfer hat state, put-state, confirm-state, entries (TASK-023). Die Testvektoren sind mit dem Viewer geteilt (tests/fixtures/notes-state/checksum.json).
- Kriterium 3, Hook am Turn-Ende und Reminder B umgesetzt und getestet: erfüllt (TASK-024: mark_notes_state.py, check_notes_state.py, remind_notes.py, mark_active_item.py; 636 Tests grün). Nachfrage A ist als Hinweis des Helfers und des Hooks im Files-Modus umgesetzt (TASK-025). Nicht belegt: ein Lauf mit den echten, geladenen Hooks in einer neuen Session; die Form der Bash-Antwort stammt aus der Doku von Claude Code.
- Kriterium 4, Schnittstelle zum Viewer beschrieben und dort umgesetzt: erfüllt (interfaces.md; der Viewer liefert Kopf, Stempel und notes_state; der Handlauf gegen den echten Viewer mit state, confirm-state und note lief). Der Viewer ist der Neubau.
- Abnahme der Spec: Gleiche Prüfsumme in Viewer und backlog.py (geteilte Vektoren); ein Harness gegen einen Viewer ohne Köpfe arbeitet weiter und meldet das (404-Meldung des Helfers, kein Merker, keine Blockade); Reminder und Nachfrage blockieren nicht; Regeln und Tests vorhanden. Offen bleibt die Wirkung der neuen Hooks im echten Betrieb.
- Umstellung nach Spec: Der Viewer ist zuerst umgestellt, der Harness erkennt die Unterstützung am Feld notes_state, bestehende Notes bekommen den Kopf beim nächsten Bearbeiten (kein Massenlauf). Das Harness-Release mit Skill, Helfer und Hooks steht aus: Es wurde bis zum Ende der Story zurückgehalten (Eintrag vom 2026-10-21). Unveröffentlicht seit v0.12.5 sind die Änderungen von TASK-024 und STORY-046.

### Decided

- Die Story steht auf Awaiting confirmation; der Owner bestätigt sie. Das Harness-Release (Vorschlag: Patch 0.12.6) wartet auf seine Freigabe und idealerweise auf den echten Hook-Lauf in einer neuen Session.

### Open

- Echter Hook-Lauf in einer neuen Session: Block am Turn-Ende bei veraltetem Kopf, Reminder nach 5 Prompts als Kontext, Form von tool_response bei Bash.
- Harness-Release nach der Bestätigung.
