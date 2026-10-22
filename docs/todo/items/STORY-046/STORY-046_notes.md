# STORY-046 — Doppelt vergebene IDs bei paralleler Arbeit in Cloud und lokal vermeiden

## State

- Goal/Status: Doppelt vergebene IDs bei paralleler Arbeit in Cloud und lokal vermeiden. Gelöst durch Platzhalter (Format Version 2); Regeltext und Techdoc angepasst, wartet auf Bestätigung.
- Next step: Owner bestätigt; danach Stand von EPIC-010 prüfen.
- Open:
  - Ein Item mit Platzhalter wurde nicht am echten Backlog synchronisiert (Beleg: Tests und Doku des Viewers)
- Decided:
  - Story gestartet, STORY-045 bestätigt (2026-10-22)
  - Befund: Der Viewer gleicht nach Uid ab, neue Einträge der Cloud tragen nur Platzhalter, Label und Uid vergibt der Viewer (2026-10-22)
  - Entscheidung (c): Platzhalter festschreiben statt Skill-Verbot oder Viewer-Erweiterung (2026-10-22)
  - sync-flow.md und interfaces.md angepasst (2026-10-22)
- References: Viewer-Doku neubau-server.md (Vergleich je Uid), interfaces.md (Neue Backlog-Einträge aus den Dateien); format.md (New entries); STORY-045 (sync-flow.md); EPIC-010

State confirmed after entry 2026-10-22 — Befund, Entscheidung und Umsetzung: Platzhalter statt Nummernvergabe (cb5018a370f1)

## 2026-10-22 — Befund, Entscheidung und Umsetzung: Platzhalter statt Nummernvergabe

### Discussed

- Ausgangslage: Die Story ging davon aus, dass die Cloud 'die nächste freie Nummer' vergibt und der lokale Viewer unabhängig davon dieselbe ID. STORY-045 ist bestätigt (Completed); STORY-046 gestartet (In progress).
- Kriterium 1, Verhalten des Viewers: Der Neubau gleicht je Uid ab (neubau-server.md, 'Vergleich je uid mit dem Hash beim letzten Sync'). Zwei unabhängig angelegte Einträge mit gleichem Label hätten verschiedene Uids; ein Eintrag aus den Dateien ohne Uid ist nach Format Version 2 nur als neuer Eintrag mit Platzhalter NEW-<kurzname> erlaubt (interfaces.md, 'Neue Backlog-Einträge aus den Dateien': 'Eine LLM erzeugt nie selbst eine Uid und nie ein Label'). Beim Sync vergibt die Datenbank Uid und das nächste freie Label, ersetzt den Platzhalter in allen Verweisen und benennt Ordner und Dokumente um. Ein Eintrag mit Label ohne Uid ist ein Formatfehler (missing_field), zwei gleiche Platzhalter ergeben invalid_placeholder. 'both_created' (beide Seiten neu mit verschiedenem Inhalt) betrifft Einträge mit gleicher Uid, die so nicht entstehen. Belege in den Tests des Viewers: test_a_new_item_has_a_placeholder_and_no_uid_label_or_created, test_placeholder_references_in_other_entries_are_rewritten, test_duplicate_placeholders_are_a_format_error, test_both_created_with_different_content_is_a_conflict.
- Im Harness gilt dasselbe schon: backlog.py verlangt für Einträge mit Label eine Uid und verbietet sie bei Platzhaltern (Tests in test_backlog.py: missing required field: Uid, must not contain Uid, uses the Uid of, invalid placeholder, Platzhalter eindeutig); der Stop-Hook prüft das im Dateimodus am Turn-Ende. format.md beschreibt die Platzhalter (Abschnitt New entries).
- Optionen: (a) Regel im Skill, lokal während einer Cloud-Sitzung keine Items gleichen Typs anzulegen; (b) Erweiterung des Viewers um vorläufige IDs wie bei den Notes; (c) vorhandene Platzhalter als Lösung festschreiben. (a) ist unnötig einschränkend und nicht prüfbar; (b) gibt es bereits, nämlich als Platzhalter des Formats Version 2, es wäre kein neues Item im Viewer nötig.

### Decided

- Entscheidung (c): Das Problem ist durch die Platzhalter des Formats Version 2 gelöst; die Cloud vergibt keine Labels und keine Uids. Es entfällt die Regel (a) und die Viewer-Erweiterung (b), weil sie schon vorhanden ist (Begründung oben). Der Owner bestätigt sie mit dem Abschluss der Story.
- Umgesetzt: sync-flow.md sagt ausdrücklich, dass die KI nie ein Label und keine Uid für einen neuen Eintrag schreibt und warum parallele Arbeit damit nicht kollidiert; die Aussage 'nicht gelöst, siehe STORY-046' ist entfernt. interfaces.md (Skript backlog.py) beschreibt die Wirkung. Ein Test sichert den Satz im Skill. 580 Tests grün.

### Open

- Nicht am echten Backlog durchgespielt: Ein neuer Backlog-Eintrag mit Platzhalter wurde nicht im echten Viewer synchronisiert (die Durchspielung in STORY-045 nutzte eine Note); der Beleg sind die Tests des Viewers und die Doku. Ein Eintrag im echten Backlog würde Daten anlegen, die nur der Owner endgültig löscht.
