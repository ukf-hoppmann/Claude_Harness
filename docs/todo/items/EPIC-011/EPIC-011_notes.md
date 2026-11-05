# EPIC-011 — Hierarchische Architektur- und Schnittstellen-Doku für die AI

## State

- Goal/Status: Alle Pflicht-Stories abgeschlossen (v0.13.0); Epic wartet auf Bestätigung (2026-11-05)
- Next step: Über STORY-059 entscheiden, dann Epic schließen; ezf-ui auf den neuen Harness umstellen (2026-11-05)
- Open: STORY-059 offen, blockiert das Schließen des Epics (2026-11-05)
- Decided: development für die AI, techdocs für Menschen; Schnittstellen-Doku und Katalog in development (2026-11-05)
- Decided: E1 X.md neben X/, E2 Pfade ab Projekt-Root, E3 Markdown-Links, E4 nur public_api (2026-11-05)
- Decided: keine Umbenennung der Module; Pflicht über Nutzung statt Rückfrage-Hook (2026-11-05)
- References: STORY-053 bis STORY-059; Release v0.13.0 (2026-11-05)

State confirmed after entry 2026-11-05 — Umsetzung abgeschlossen (47f30b2b6b3b)

## 2026-11-05 — Entwurf aus ezf-ui gegen den Harness geprüft

### Discussed

- Vorschlag aus ezf-ui (harness-prompt.md): Architektur und Schnittstellen als Baum, Pflichtlektüre, Linkprüfung, Pflege-Erinnerung, Katalog, Vorlagen.
- Befund im Code: Scopes flach (_SCOPE_NAME, scope_path; mark_architecture_read markiert nur direkte Kinder von architecture/). Techdocs kommen schon mit Unterordnern zurecht (classify zählt alles unter techdocs_path). Pflichtlektüre außerhalb der Architektur gibt es nicht.
- Konflikte mit Grundsätzen: Architektur englisch (Zuständigkeitstabellen englisch), architecture.md kurz (Zuständigkeiten in Bereichs-Scopes), Lade-Stufen (Pflichtdateien kurz halten). Projektspezifisches (Schichtnamen, Zeilen, ESLint) bleibt in ezf-ui.
- Ladestufen: Vorschlag des Besitzers, nach dem Lesen per Hook zu fragen, ob alles Relevante gelesen ist, und index.md bei Ordnerzugriff automatisch einzuspielen. Empfehlung: allgemeine Rückfrage wird abgenickt und wirkt nicht; der eigentliche Fehler (modals.alert statt reportError) entsteht beim Schreiben, nicht beim Lesen. Stattdessen Pflicht über Nutzung (Bezeichner im neuen Code erzwingen Doku).

### Decided

- Zielgruppen: development = verbindliche Doku für die AI (englisch), techdocs = Doku für Menschen (docs.language). Die Schnittstellen-Doku und der Katalog, gegen die programmiert wird, liegen in development (interfaces.md + interfaces/**), nicht in techdocs. Duplikate zu techdocs sind erlaubt; Abbau später in STORY-059.
- Keine Umbenennung der Module (development_ai/techdocs_human): Migrationsaufwand zu hoch; stattdessen Zielgruppe in Sitzungsstart und Skills nennen.
- E1: Index-Datei X.md liegt neben Ordner X/ (interfaces.md + interfaces/, architecture/plugins.md + architecture/plugins/patient.md); kein index.md.
- E2: Pfade in Required reading relativ zum Projekt-Root, wie die Spalte Paths.
- E3: Verweise sind normale relative Markdown-Links, optional mit #anker.
- E4: Pflege-Erinnerung nur über [development].public_api; umbenannte oder gelöschte Ziele findet die Linkprüfung.
- E5: Katalog liegt in der Doku für die AI (development/interfaces).
- Pflichtlektüre wird aus der einen Scope-Tabelle berechnet, nicht über Verweisketten; höchstens zwei Ebenen unter der Wurzel empfohlen. Kein automatisches Einspielen von index.md bei Ordnerzugriff.
- Pflicht über Nutzung wird als STORY-057 umgesetzt.
- Umsetzung mit Sonnet in eigenen Sessions, je Story ein Worktree.

## 2026-11-05 — Umsetzung abgeschlossen

### Discussed

- STORY-053 bis 058 in Sonnet-Sessions umgesetzt und in main gemergt (v0.12.9 bis v0.13.0); 788 Tests grün; Gesamtablauf in einem Testprojekt nach dem Muster von ezf-ui geprüft (Pflichtlektüre, Unterordner-Scope, Required on use, tote Links, Pflege-Erinnerung).

### Decided

- Besitzer hat STORY-053 bis 058 am 2026-11-05 bestätigt.

### Open

- STORY-059 (optional) ist noch offen und verhindert das Schließen des Epics: aus dem Epic lösen oder hier lassen.
