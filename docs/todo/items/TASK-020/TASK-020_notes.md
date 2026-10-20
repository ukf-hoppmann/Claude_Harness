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
