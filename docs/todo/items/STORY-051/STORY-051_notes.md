# STORY-051 — todo-Skill: Ort und Inhalt der Diskussionsprotokolle (Notes) festlegen

## Stand

- Ziel/Status: Regeln für Ort, Inhalt, Zeitpunkt und Aufbau der Item-Notes festlegen und mechanisch absichern; Klärung läuft, Spec wird fortlaufend geschrieben. Am 2026-10-20 von TASK-020 zur Story STORY-051 umgewandelt.
- Nächster Schritt: Zerlegung in Tasks mit dem Owner abstimmen; offene Punkte klären.
- Offen:
  - Plan speichern oder mit der Spec enden; Empfehlung: mit der Spec enden, Zerlegung über Kinder-Items (2026-10-20)
  - Maßstab und Schwellwert des Längenhinweises; Empfehlung: Anzahl Punkte unter Beschlossen (2026-10-20)
  - Warnung beim Umschreiben älterer Protokolleinträge (2026-10-20)
  - Umgang mit bestehenden Notes-Dateien: Kopf nachträglich oder beim nächsten Eintrag (2026-10-20)
  - Regeln 1–4 (Ort, Inhalt, Zeitpunkt, Spec/Notes) und Prüfideen A, C, D; Empfehlung: 1–4 und A umsetzen, C schwach, D nicht (2026-10-19)
- Beschlossen:
  - Notes bekommen einen Kopf „Stand“ über dem Protokoll; der Kopf wird ersetzt, das Protokoll nur angehängt (2026-10-20)
  - Reihenfolge des Kopfs: Ziel/Status, Nächster Schritt, Offen, Beschlossen, Verweise (2026-10-20)
  - Keine feste Längengrenze, ein langer Kopf ergibt nur einen Hinweis (2026-10-20)
  - Spec wird fortlaufend geschrieben und am Ende geprüft (2026-10-20)
  - Nach jeder Änderung der Notes wird der Kopf angepasst oder bewusst bestätigt; Hook am Turn-Ende blockiert bis dahin (2026-10-20)
  - Stempel als Prüfsumme des Protokolls, in API und Files-Modus; gesetzt vom Server bzw. von backlog.py, nie von Hand (2026-10-20)
  - Kopf und Protokoll in der API getrennt gespeichert, nach außen eine Markdown-Datei (2026-10-20)
  - Reminder B bei aktivem Item ohne aktuellen Notes-Eintrag (2026-10-20)
- Verweise: Spec STORY-051_spec.md; ToDo-Viewer (separates Projekt) für die Schnittstelle

Stand bestätigt nach Eintrag 2026-10-20 — Prüfsumme und Trennung beschlossen (Prüfsumme folgt, Mechanismus noch nicht gebaut)

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
