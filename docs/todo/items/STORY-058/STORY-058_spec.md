# STORY-058 — Spec: Schnittstellen-Doku, Vorlagen und Skill-Regeln

Teil von EPIC-011. Zuletzt umsetzen: beschreibt die Mechanismen aus STORY-053 bis 057.

## Zielgruppen (Entscheidung in EPIC-011)

- `development` (`docs/development/`): verbindliche Doku für die AI, Englisch.
  `architecture.md` + `architecture/**`: was wohin gehört, was Pflicht ist, nie das Wie.
  `interfaces.md` + `interfaces/**`: wie es geht (Schnittstellen, Kataloge).
- `techdocs`: Doku für Menschen in `docs.language`. Duplikate zu development sind
  vorerst erlaubt (Abbau in STORY-059). Keine Umbenennung der Module.

## Schnittstellen-Doku

- Ort: `<development.path>/interfaces.md` (Index: eine Zeile je Datei mit Link) und
  `<development.path>/interfaces/**`. Konvention E1: Datei `X.md` neben Ordner `X/`.
- Gehört zum Teil `architecture` des development-Moduls; keine neue Config.
  Optional: fehlt `interfaces.md`, keine Warnung.
- Katalog wiederverwendbarer Bausteine: je Besitzer (Schicht) eine Datei, eine Zeile je
  Baustein: `| Building block | Purpose | Use when | Details |` (Details = Link).
- Inhalt: aktueller Stand, Englisch, die spezifischste Datei pflegen, Index nachziehen.

## Vorlagen (`plugin/templates/development/`)

- `architecture.md`: Spalte Required reading, Hinweis auf Unterordner-Scopes, Links statt
  Text für das Wie, Abschnitt `## Required on use` als Kommentar.
- `scope.md` (neu): Bereichs-Scope mit `## Responsibilities`
  `| Concern | Owner | Others do | Others don't | Details |`, `## Rules`,
  `## Required on use`.
- `interfaces.md` (neu, Index), `interface.md` (neu, eine Schnittstelle),
  `catalog.md` (neu).

## Skills

- Neuer Skill `plugin/skills/interfaces/SKILL.md` (`claude-harness:interfaces`):
  Beschreibung ein Satz, wann laden (Schnittstelle oder geteilten Baustein entwerfen,
  nutzen, ändern; Katalog pflegen; Pflege-Erinnerung aus STORY-056). Regeln wie oben.
- Skill architecture: Pflichtlektüre (Pfade, Nutzung) gegen Nachschlagen (Links);
  Architektur ohne Wie, nur Links; Pflichtdateien kurz; höchstens zwei Ebenen; die
  Scope-Tabelle ist die einzige Liste der Pflicht. Nicht mit dem Skill interfaces
  duplizieren (Architekturregel 9).
- Skill decomposition: vor einem neuen Baustein die Kataloge prüfen und im Plan nennen,
  was wiederverwendet wird; was mehrere Besitzer brauchen, in die geteilte Schicht, die
  die Architektur nennt; gibt es keine, nachfragen.
- Skill techdocs und Sitzungsstart: Zielgruppe nennen („Technical docs (for people)“,
  Hinweis auf interfaces für die AI). Skill-Beschreibungen anpassen.
- Prüfen: Skills `init` und `update` (Vorlagen anbieten), Cloud-Export (neuer Skill und
  Vorlagen werden mit exportiert; Test).

## Harness selbst

- `docs/development/architecture.md` Regel 6: development-Dokumente (Architektur,
  Schnittstellen) sind Englisch. Änderung im Plan zur Freigabe vorlegen.
- Techdocs des Harness nachziehen.

## Tests

Bestehende Tests für Sitzungsstart und Cloud-Export anpassen; Test, dass die Vorlagen
existieren und der neue Skill exportiert wird.
