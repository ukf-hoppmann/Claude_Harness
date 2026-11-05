# STORY-055 — Spec: Tote Verweise melden

Teil von EPIC-011. Unabhängig von STORY-053/054.

## Verweisformat (Entscheidung E3)

Normale relative Markdown-Links: `[Text](../interfaces/core/errors.md)` oder
`[Text](../interfaces/core/errors.md#report-error)` oder `[Text](#abschnitt)` (gleiche
Datei). Ziel relativ zur verweisenden Datei, wie GitHub und Editoren es auflösen.

Nicht geprüft: Links mit Schema (`http:`, `https:`, `mailto:` …), Links in Code-Blöcken
(```` ``` ````/`~~~`) und Inline-Code, Bilder dürfen mitgeprüft werden (nur Datei).
Referenz-Links (`[x][id]` mit `[id]: ziel`) mitprüfen, wenn einfach; sonst im Skill
erwähnen, dass Inline-Links zu verwenden sind.

## Prüfung (gemeinsamer Helfer `plugin/scripts/doclinks.py`)

- Fehler: Ziel liegt außerhalb des Projekts; Datei oder Ordner fehlt; Anker fehlt in
  einer `.md`-Zieldatei.
- Anker-Slug wie GitHub: Überschrift kleinschreiben, alles außer Buchstaben (inkl.
  Umlaute), Ziffern, `-`, `_` und Leerzeichen entfernen, Leerzeichen → `-`; doppelte
  Slugs bekommen `-1`, `-2`; Überschriften in Code-Blöcken zählen nicht; explizite
  `<a id="…">`/`<a name="…">` zählen als Anker.
- Geprüfte Dateien je Projekt: `README.md` und alle `.md` unter `techdocs.path`, wenn
  Modul techdocs aktiv; alle `.md` unter `development.path`, wenn Teil architecture
  aktiv. Der Helfer liegt in `plugin/scripts/` (Architekturregel 3).
- Meldung je Fehler: `<datei>:<zeile>: <ziel>: <grund>` (Englisch).

## Sitzungsstart

Je Projekt `Dead links in docs: <n>` plus gekürzte Liste (vorhandenes `_limited`),
analog zu den Scope-Tabellenfehlern. Laufzeit beachten (nur `.md` der genannten Ordner).

## Ende des Turns

- PostToolUse Write/Edit/MultiEdit merkt sich geänderte Dateien der geprüften Ordner je
  Session (über `state.py`; vorhandenes Muster von `mark_techdocs.py` oder neuer Marker).
- Stop-Hook (neues Skript oder Erweiterung eines bestehenden; eigener Eintrag in
  `hooks.json`): prüft nur diese Dateien; bei toten Links Meldung auf stderr und Exit 2,
  nichts bei `stop_hook_active`. Nach erfolgreicher Prüfung wird die Liste geleert.
- Auch Links in anderen Dateien, die auf eine geänderte oder gelöschte Datei zeigen,
  sind wünschenswert, aber optional; der Sitzungsstart fängt sie spätestens.

## Doku und Tests

Techdocs des Harness (interfaces: Hook und Meldung). Unit-Tests: Linkformen, Anker mit
Umlauten und Duplikaten, Code-Blöcke, externe Links, Ziel außerhalb, Sitzungsstart-Zeile,
Stop-Hook mit und ohne Fehler, `stop_hook_active`, abgeschaltete Module.
