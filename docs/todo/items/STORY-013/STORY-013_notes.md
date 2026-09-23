# STORY-013 — Notes

## 2026-09-23 — Daily-Report: Grundentscheidungen

Vorlage aus Agent_Harness: Modul `DOC-DAILY`
(`rules/modules/daily-development.md`, `templates/daily-development.md`). Die
Repo-interne Variante `HDOC-001` (`docs/development/README.md`) dient nur als
Ideenquelle.

### Discussed

- Ziel: nachvollziehbar festhalten, was an einem Tag geändert wurde, damit
  Änderungen transparent sind und sich später beantworten lässt, wann was
  passiert ist. Nicht jede Kleinigkeit, nur relevante Ergebnisse.
- Tokenverbrauch (grobe Schätzung, nicht gemessen):
  - Kontinuierlich nach jeder Implementierung: ca. 2–5k je Aktualisierung,
    15–50k pro Tag; beste Qualität, weil der Kontext noch da ist.
  - Nur auf Trigger (Session-Ende, auf Zuruf): ca. 5–15k einmalig, aber
    Rekonstruktion aus Git verliert Begründungen und wird leicht vergessen.
  - Mittelweg per Hook: ca. 10–25k pro Arbeitstag; bei nicht relevanten
    Änderungen nur ca. 200 Tokens für die Erinnerung.
- Links auf Backlog-Einträge sind stabil: Item-Ordner bleiben beim Archivieren
  in `items/` liegen. Links auf Stellen in `TODO.md` wären es nicht.

### Decided

- Das Modul `daily` bleibt optional (Schalter in `[modules]`).
- Pfad: `<docs>/development/daily/<YYYY-MM-DD>_daily.md`, ein Bericht pro
  Kalendertag mit relevanter Arbeit; kein Bericht für Tage ohne relevante
  Arbeit; mehrere Sessions ergänzen denselben Bericht.
- Config: gemeinsame Doku-Wurzel (Variante A), z. B. `[paths] docs = "docs"`;
  Modulpfade werden relativ dazu angegeben (`todo`, `development/daily`).
  Betrifft das Schema aus `STORY-001`.
- Sprache wird allgemein in der Config gesetzt und gilt für alle erzeugten
  Dokumente (Standard hier: Deutsch). Sie betrifft Fließtext und Überschriften
  der Berichte, nicht die maschinell geprüften Feldnamen (z. B. `Status:` im
  Backlog). Ein Sprachwechsel übersetzt bestehende Dokumente nicht.
- Relevanzkriterium wie in Agent_Harness: ergebnisorientiert, zusammenhängende
  Schritte bündeln; Erkundungen, Zwischenentwürfe, kleine Formulierungs- und
  Formatänderungen und Wiederholungen zählen nicht. Planung zählt, wenn sie
  eine Entscheidung, ein umsetzungsreifes Ziel, eine Abgrenzung, ein Risiko
  oder einen wichtigen nächsten Schritt festlegt oder ändert.
- Inhalt: Zusammenfassung als schlanker Fließtext; danach nah am
  Agent_Harness-Format mit Tabellen: Features (neu, geändert,
  entfernt/abgelehnt/zurückgestellt), Bugfixes, technische/Doku-/
  Betriebsänderungen, Entscheidungen mit Alternativen, Verifikation, offene
  Punkte und nächste Schritte, Referenzen. Weggelassen werden die Aufteilung
  der Arbeit zwischen Mensch und KI, SemVer-Einschätzung und
  Präsentationsbeobachtungen.
- Referenzen: In der Evidence-Spalte stehen Backlog-ID (bei aktivem
  `todo`-Modul als relativer Link auf `items/<ID>/`, sonst nur die ID) und
  Commit-Hash. Die Uhrzeit liefert Git; keine eigene Uhrzeitspalte.
- Wahrhaftigkeit wird übernommen: keine behauptete Verifikation, gemessen vs.
  vermutet trennen, beim Nachtragen nichts erfinden und als nachträglich
  kennzeichnen, Unfertiges sichtbar lassen.
- Aktualisierung per Hook: Der `Stop`-Hook erinnert nur, wenn Projektdateien
  geändert wurden (ohne Daily und Backlog); Claude entscheidet anhand der
  Relevanzkriterien, ob und was eingetragen wird.

### Open

- Zusätzliche Regeln gegen Fehlerquellen (Vorschlag):
  - Datum: das lokale Systemdatum zum Zeitpunkt des Eintrags, nicht geschätzt.
  - Vor dem Schreiben den bestehenden Bericht lesen und vorhandene Zeilen
    aktualisieren statt doppelt einzutragen (wichtig nach Komprimierung).
  - Commit-Hash erst eintragen, wenn der Commit existiert; bis dahin
    „nicht committet“.
  - Nur den heutigen Bericht ändern; frühere Tage nur als gekennzeichnete
    Korrektur.
  - Keine Geheimnisse und keine rohen Logs in den Bericht (Bezug `STORY-016`).
  - Hook-Schleife vermeiden: Das Schreiben des Daily löst keine neue
    Erinnerung aus.
- Konkrete Schlüsselnamen für Doku-Wurzel und Sprache im Schema.

## 2026-09-23 — Ort und Zeitpunkt der Aktualisierung

### Discussed

- Schreiben im Worktree würde beim Mergen Konflikte in denselben Tabellen
  erzeugen, sobald mehrere Sessions am selben Tag arbeiten.
- „Nur den heutigen Bericht ändern“ heißt: Fehler in früheren Berichten werden
  nicht still überschrieben, sondern als datierte Korrektur ergänzt, damit
  frühere Aussagen nachvollziehbar bleiben.

### Decided

- Das Daily wird nur im Haupt-Checkout geschrieben und erst, nachdem die
  Änderung dort angekommen ist (nach dem Merge bzw. bei lokaler Arbeit nach dem
  Commit). Damit existiert der Commit-Hash beim Schreiben immer.

### Open

- Auslöser des Hooks anpassen (Vorschlag): Statt nach Dateiänderungen erinnert
  der `Stop`-Hook, wenn auf dem Hauptzweig Commits liegen, die seit der letzten
  Daily-Aktualisierung noch nicht erfasst sind.
- Datum bei spätem Merge (Vorschlag): Es zählt der Tag, an dem die Änderung auf
  dem Hauptzweig ankommt.
- Schlüsselnamen (Vorschlag, Config `version = 2`): `[docs] root = "docs"`,
  `[docs] language = "de"`; `[todo] path` und `[daily] path` relativ zu
  `docs.root` (`todo`, `development/daily`); Modulschalter `daily`.

## 2026-09-23 — Offene Punkte geschlossen

### Decided

- Hook-Auslöser: Der `Stop`-Hook erinnert im Haupt-Checkout, wenn auf dem
  Hauptzweig Commits liegen, die seit dem zuletzt bestätigten Stand noch nicht
  erfasst sind. Commits, die nur den Daily-Ordner ändern, zählen nicht.
- Datum: Es zählt der Tag, an dem die Änderung auf dem Hauptzweig ankommt
  (lokales Systemdatum beim Schreiben).
- Schlüsselnamen: `[docs] root`, `[docs] language`, `[daily] path`,
  Modulschalter `daily`; `[todo] path` und `[daily] path` relativ zu
  `docs.root`. Die Config bleibt bei `version = 1`, weil das Projekt noch am
  Anfang steht.
- Regeln gegen Fehlerquellen: Systemdatum statt Schätzung; bestehenden
  Bericht vorher lesen und Zeilen aktualisieren statt doppeln; nur den
  heutigen Bericht ändern, frühere nur per datierter Korrektur; keine
  Geheimnisse und keine rohen Logs; das Schreiben des Daily löst keine neue
  Erinnerung aus. Die Regel „bis zum Commit ‚nicht committet‘ eintragen“
  entfällt, weil erst nach dem Merge geschrieben wird.
- Der bestätigte Stand liegt pro Klon im Git-Verzeichnis
  (`.git/claude-harness/daily-ack`) und wird von Claude mit `daily.py ack`
  gesetzt, auch wenn nichts relevant war. Der Plugin-Datenordner scheidet
  aus, weil `daily.py` per Bash aufgerufen wird und dort
  `CLAUDE_PLUGIN_DATA` fehlen kann.
- Details: `STORY-013_spec.md`.
