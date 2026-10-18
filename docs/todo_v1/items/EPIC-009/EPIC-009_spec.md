# Spec: Notes und Topics im Harness

## Was und warum

Neben dem Backlog (Arbeit mit Fertig-Definition) gibt es Notes: Erinnerungen,
Fragen, Beobachtungen und Ideen, die einen Auslöser oder ein Wiedersehen haben
statt einer Fertig-Definition. Der ToDo-Viewer baut die Technik (EPIC-005 in
seinem Backlog) und stellt sie über seine API bereit. Der Harness bringt
Claude bei, damit zu arbeiten. Quelle der Anforderungen:
`docs/notes-harness-prompt.md` im ToDo-Viewer-Repo.

## Was der Viewer liefert (Voraussetzung, nicht Teil des Harness)

- **Topic**: nur zum Sortieren; Baum der Tiefe 2, ausnahmsweise 3; optionaler
  Termin. Eine Note liegt in genau einem Topic.
- **Note**: Kurzfassung (eine Zeile, Pflicht), optionaler Langtext, Prüf-Datum
  (Standard 30 Tage), optionale Auslöser (Zeitpunkt, Ereignis an verlinktem
  Item, Topic-Termin; der früheste feuert).
- **Link** zwischen Note und Item, Topic oder Note, abfragbar in beide
  Richtungen; Rollen `reference`, `trigger`, `origin`.
- **IDs**: intern `uid`, nach außen stabiles `label` (`NOTE-001`,
  `TOPIC-001`, pro Projekt und Typ). Claude adressiert nur über das Label.
- **Zustände**: `waiting`, `due`, `snoozed`, `done`, `dropped`, `promoted`.
  `due` heißt nur "schau hin". `done`, `dropped`, `promoted` gehen ins Archiv,
  Löschen in den Papierkorb; endgültig löschen nur der Besitzer.
- **Hinweise bei Änderungen** an verlinkten Items oder Notes; sie bleiben, bis
  jemand entscheidet (behalten, abkoppeln, verwerfen, befördern).
- **Schlanker Index** je Topic und Note (Label, Status, Fälligkeit,
  Kurzfassung, optional Mini-Zusammenfassung je Topic).
- Alle Keys, Feldnamen, Status, Rollen und API-Namen sind englisch; Texte in
  `[docs].language`.
- Notes liegen ausschließlich in der Datenbank des Viewers. Kein
  Markdown-Backend, nichts zu committen.

## Was der Harness festlegt

1. **Modul**: `[modules].notes`, eigener Skill `claude-harness:notes`, eine
   statische Zeile im Session-Start. Keine weiteren Config-Schlüssel, kein
   weiterer Hook, kein Netzwerkzugriff in Hooks (Architekturregel 2 bleibt
   unberührt).
2. **Erkennung** (Note, Backlog-Eintrag oder Wecker):
   - Backlog-Eintrag: Arbeit mit klarer Fertig-Definition.
   - Note: "merke dir", "erinnere mich" mit längerem Horizont, offene Frage
     an Dritte, Beobachtung ("prüfe, wenn ..."), Idee ohne Auftrag.
   - Wecker: Minuten bis wenige Stunden; Claude erinnert innerhalb der
     Session mit den vorhandenen Scheduling-Werkzeugen von Claude Code.
   - Eindeutig: handeln. Fraglich: einmal kurz nachfragen. Der Zeitaspekt ist
     der wichtigste Marker.
3. **Befugnisse**: ohne Rückfrage anlegen, ändern, Links setzen,
   zurückstellen, erledigen; mit Rückfrage verwerfen und befördern; endgültig
   löschen nie. Eine Rückstufung Item zu Note ist eine Typänderung und braucht
   wie im Backlog Rückfrage.
4. **Lesereihenfolge**: zuerst nur der Index, nach Relevanz filtern, den
   Langtext nur laden, wenn eine Note passt oder bearbeitet wird.
5. **Fälligkeit**: Claude prüft sie nie und spricht sie nicht von sich aus an.
   Er liest den Zustand `due` und die Hinweise, wenn der Besitzer ihn dazu
   auffordert. Danach: zurückstellen, erledigen, verwerfen oder befördern; die
   Aktionen mit Rückfrage richten sich nach Punkt 3.
6. **Relative Zeitangaben**: Claude löst sie in einen festen Zeitpunkt auf und
   nennt ihn beim Anlegen zur Bestätigung. Bei Unklarheit (z. B. "früh" kann
   6 Uhr oder 9 Uhr heißen) fragt er nach. Keine feste Uhrzeit in der Config.
7. **Prüf-Datum**: der Standard des Viewers gilt. Claude ändert ihn nur auf
   ausdrücklichen Wunsch.
8. **Sprint-Merker**: "Merke für den nächsten Sprint" wird eine Note in einem
   Topic mit Termin. Ist der Termin abgelaufen, fragt Claude nach dem nächsten
   und setzt ihn nach Bestätigung.
9. **Umwandlung**: Note zu Task, Story oder Epic (Kurzfassung wird Titel und
   Kurzfassung, Langtext wird die Notiz, die Note gilt als `promoted`, Link
   `origin`) und Item zu Note (nur ohne Kinder und Fortschritt, Resolution
   "zur Notiz zurückgestuft"). Beides läuft über die API des Viewers.
10. **Privatsphäre**: Notes sind privat, solange sie nur in der Datenbank
    liegen. Claude behandelt sie nicht als Teamwissen und kopiert ihren Inhalt
    nicht in eingecheckte Dateien (Backlog, Daily, Doku).
11. **Server nicht erreichbar**: wie beim Backlog (Exit 3): dem Besitzer
    sagen und nachfragen; nicht auf Dateien ausweichen (es gibt keine).
12. **Daily und Techdocs**: Notes kommen nicht in den Tagesbericht. Die
    Techdocs beschreiben Modul, Helfer und Skill und verweisen für das
    Notes-Modell auf die Doku des Viewers.

## Nicht Teil dieser Stufe

Wiederkehrende Notes, Popups, Benachrichtigung außerhalb des Viewers,
Cloud-Sync, Mindmap-Ansicht, Notes mit Parent, Abhängigkeiten oder Priorität,
automatisches Aufgreifen von Fälligem.

## Reihenfolge

STORY-038 (Config, Session-Start) kann sofort umgesetzt werden. STORY-039
(Helfer) und STORY-040 (Skill) brauchen die API des Viewers. STORY-041 (Abgrenzung,
Doku, Release) kommt zuletzt.
