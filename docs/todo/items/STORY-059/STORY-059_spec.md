# STORY-059 — Spec: Techdocs als Zusammenfassung der development-Doku

Teil von EPIC-011. Entscheidungen in den Notes von STORY-059.

## Ziel

Eine allgemeine Regel für alle Projekte, nicht die Überarbeitung der Techdocs dieses Repos.
Bisher laufen Techdocs (Menschen, `docs.language`) und development-Doku (AI, Englisch)
parallel und duplizieren Inhalte. Künftig sind die Techdocs eine Übersicht, die für konkrete
Elemente auf die development-Doku verlinkt.

## Regel

- Ein Element (Schnittstelle, Baustein, Bereichsregel), das die development-Doku beschreibt,
  bekommt in den Techdocs einen zusammenfassenden Satz in `docs.language` und einen relativen
  Markdown-Link auf die development-Datei. Gibt es keine development-Doku dazu, beschreiben die
  Techdocs es vollständig (Projekte ohne development-Doku arbeiten wie bisher).
- Die Zusammenfassung muss für einen Überblick ohne den Link reichen; Links von Doku in
  `docs.language` auf englische Dateien sind in Ordnung.

| Dokument | Rolle |
|---|---|
| `README.md` | vollständig (Einstieg, Installation, Benutzung); verweist auf jedes vorhandene Techdoc, damit z. B. die Konfiguration auffindbar ist |
| `architecture` | Überblick über Komponenten, Datenfluss, Entscheidungen; für verbindliche Regeln Links auf `development/architecture.md` und die Scopes |
| `interfaces` | Übersicht: eine Zeile je Schnittstelle oder Bereich (Zweck + Link auf die development-Datei); Einzelheiten nur ohne development-Doku |
| `configuration` | vollständig (Einstellungen setzen Menschen) |
| `operations` | vollständig |

- Bestehende Projekte: nichts wird erzwungen. Wer einen Abschnitt bearbeitet, der die
  development-Doku dupliziert, ersetzt ihn durch Zusammenfassung und Link.
- Sprache: `docs.language` (schon konfigurierbar, im Skill `init` abgefragt); keine Änderung.

## Änderungen

- `plugin/skills/techdocs/SKILL.md`: Regel und Tabelle oben; Satz „duplicates are allowed for
  now“ ersetzen. Nicht mit Skill `interfaces` duplizieren (Architekturregel 9); dort ggf. ein
  kurzer Verweis, dass die Techdocs auf die Schnittstellen-Doku verlinken.
- Vorlagen `plugin/templates/techdocs/`: `readme.md` (Links auf alle Techdocs als Pflichtteil),
  `architecture.md` (Hinweis auf Links zu den Regeln), `interfaces.md` (Übersichtstabelle
  `| Schnittstelle | Zweck | Details |` mit Link; Abschnitt für vollständige Beschreibung nur ohne
  development-Doku). Vorlagen bleiben Englisch in Kommentaren, Überschriften wie bisher.
- `plugin/scripts/techdocs.py` (`classify`): eine geänderte Datei unter
  `<development.path>/interfaces.md` oder `<development.path>/interfaces/**` zählt als `docs`, wenn
  der Teil architecture des development-Moduls aktiv ist. Die Erinnerung in `check_techdocs.py`
  schweigt dann. `development/architecture*` zählt nicht (Regeländerungen brauchen weiter einen
  Blick auf die Techdocs). Architekturregel 3 beachten: nur Konfig-Werte lesen, keine Dokumente
  des anderen Moduls.
- Techdocs des Harness (`docs/techdocs/interfaces.md`): Verhalten der Erinnerung nachziehen. Die
  Techdocs dieses Repos werden sonst nicht umgebaut.

## Tests

Unit-Tests für `classify` und die Erinnerung: Änderung unter `development/interfaces/**` schweigt
die Erinnerung, Änderung unter `development/architecture*` nicht, abgeschalteter Teil
architecture zählt nicht. Bestehende Tests bleiben grün.
