# STORY-012 — Spec: Technische Systemdokumentation

## Goal

Ein Modul `techdocs` legt fest, welche Dokumente beschreiben, wie ein Projekt
aktuell aufgebaut ist und benutzt wird, welche Art von Änderung welches
Dokument betrifft und wann eine Anpassung entfällt. Es erinnert daran, die
Dokumente im selben Change mitzupflegen.

Abgrenzung: Anforderungen stehen im Backlog (Goal, Kriterien, Specs), der
Verlauf im Daily (`STORY-013`). Die Systemdoku beschreibt nur den aktuellen
Zustand.

## Config

```toml
[modules]
techdocs = true              # in der Vorlage an; Standard ohne Eintrag: aus

[techdocs]
path = "techdocs"            # relativ zu docs.root; Standard "techdocs"
documents = ["architecture", "interfaces", "configuration"]   # Standard
```

- Erlaubte Arten in `documents`: `architecture`, `interfaces`,
  `configuration`, `operations`. Unbekannte Arten und Doppelungen sind
  Fehler; eine leere Liste ist erlaubt (dann nur die README).
- Dateiname je Art: `<docs.root>/<techdocs.path>/<Art>.md`.
- `README.md` im Projekt-Root gehört immer dazu und ist nicht konfigurierbar.
- Sprache: `docs.language`.

## Documents

| Art | Inhalt |
|---|---|
| `readme` | Zweck, Voraussetzungen, Installation, Schnellstart, Verweise auf die übrigen Dokumente |
| `architecture` | Komponenten und ihr Zusammenspiel, Datenfluss, wo Zustand liegt, wichtige Entscheidungen kurz mit Verweis auf die Backlog-Notizen |
| `interfaces` | Öffentliche Schnittstellen: API, CLI, Dateiformate, Hooks, Ereignisse |
| `configuration` | Jede Einstellung mit Typ, Standardwert, Pflicht/optional und Wirkung |
| `operations` | Deployment, Betrieb, Überwachung, Fehlerbilder und Behebung |

Vorlagen: `plugin/templates/techdocs/<Art>.md` und
`plugin/templates/techdocs/readme.md`. Kein Verlauf, keine Changelogs in
diesen Dokumenten.

## Rules

Zuordnung (ein Change kann mehrere Dokumente betreffen):

| Art der Änderung | Dokument |
|---|---|
| Nutzung, Installation, Voraussetzungen | `readme` |
| Komponente neu/entfernt, Datenfluss, neue Abhängigkeit, Architekturentscheidung | `architecture` |
| API, CLI, Dateiformat, Hook | `interfaces` |
| Einstellung neu, geändert, entfernt | `configuration` |
| Deployment, Betrieb, Fehlerbilder | `operations` |

- Backlog-Änderungen (Einträge, Notizen, Specs) und Tagesberichte brauchen
  keine Systemdoku; der Backlog dokumentiert sich selbst.
- Keine Anpassung nötig, wenn sich nichts von außen Sichtbares ändert:
  Refactoring ohne Verhaltensänderung, nur Tests, Tippfehler, Formatierung,
  interne Umbenennungen, Abhängigkeits-Updates ohne Verhaltensänderung.
- Im Zweifel das betroffene Dokument lesen und prüfen.
- Betrifft eine Änderung eine Art, die das Projekt nicht führt, wird das
  genannt und das Anlegen vorgeschlagen, nicht stillschweigend übergangen.
- Veraltete Aussagen werden korrigiert oder entfernt, nicht ergänzt.
- Die Doku-Anpassung gehört in denselben Change (auch im Worktree).
- Der Abschlussbericht eines Changes nennt die Doku-Änderungen oder kurz den
  Grund, warum keine nötig waren.
- Fehlende Dokumente aus `documents` werden nur nach Freigabe aus den
  Vorlagen angelegt.

## Hook

- `PostToolUse` (Write/Edit/MultiEdit) merkt pro Session:
  - „Projekt geändert“, wenn die Datei im Projekt liegt und nicht zu
    Backlog-Ordner, Daily-Ordner, Systemdoku oder Tests gehört (Pfadteil
    `test`/`tests`, Dateiname `test_*`, `*_test.*` oder `*.test.*`);
  - „Doku geändert“, wenn die Datei `README.md` oder im techdocs-Ordner liegt.
- `Stop`: Ist „Projekt geändert“ gesetzt, „Doku geändert“ nicht, und wurde in
  dieser Session noch nicht erinnert, erinnert er einmal (Exit 2) mit Verweis
  auf den Skill `claude-harness:techdocs`. `stop_hook_active` → still.
- Modul aus oder Config ungültig → Hooks tun nichts.

## Session start

Bei aktivem Modul eine Zeile mit Ordner und Skill; fehlende Dokumente aus
`documents` (und eine fehlende README) werden genannt.

## Init

`/claude-harness:init` fragt, ob `techdocs` aktiv sein soll und welche Arten
das Projekt führt, und legt fehlende Dokumente nach Freigabe aus den Vorlagen
an, ohne Bestehendes zu überschreiben.

## Application in this repo

`README.md`, `docs/techdocs/architecture.md`, `interfaces.md`,
`configuration.md` beschreiben den aktuellen Stand von Claude_Harness;
`operations` wird nicht geführt.

## Affected files

- `plugin/scripts/harness_config.py`, `plugin/templates/config.toml`,
  `.claude-harness/config.toml`
- `plugin/scripts/techdocs.py` (Pfadklassifikation, Marker),
  `plugin/scripts/mark_techdocs.py`, `plugin/scripts/check_techdocs.py`,
  `plugin/scripts/state.py`, `plugin/scripts/session_start.py`,
  `plugin/hooks/hooks.json`
- `plugin/skills/techdocs/SKILL.md`, `plugin/templates/techdocs/*.md`,
  `plugin/skills/init/SKILL.md`
- `README.md`, `docs/techdocs/*.md`
- `tests/test_config.py`, `tests/test_techdocs.py`

## Acceptance criteria

- Eine Codeänderung ohne Doku-Änderung führt beim Stop zu genau einer
  Erinnerung pro Session.
- Keine Erinnerung, wenn nur Tests, Backlog, Daily oder Systemdoku geändert
  wurden, wenn die Doku in derselben Session geändert wurde, oder bei
  abgeschaltetem Modul.
- Die Config lehnt unbekannte oder doppelte Dokumentarten ab.
- Dieses Repo hat README und die drei konfigurierten Dokumente, und sie
  beschreiben den aktuellen Stand.
