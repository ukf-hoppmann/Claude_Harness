# TASK-017 — update-Skill: Projekt-Config mit dem aktuellen Harness-Stand abgleichen

## 2026-09-28 — Umfang: vollständiger Abgleich statt nur Backend-Wechsel

### Discussed

- Heute vergleicht `update` nur `version` mit `CONFIG_VERSION`. Weil `MIGRATIONS` leer ist, meldet es immer „aktuell“, obwohl ältere Configs Optionen wie `todo.backend`/`api_url`, die Teile unter `[development]`, `semver.file` oder die Kommentare der Vorlage nicht enthalten (z. B. die Config dieses Repos).
- Offen war, ob der Abgleich als Skript oder als reine Skill-Anleitung umgesetzt wird und ob fehlende Kommentare der Vorlage immer oder nur bei neuen Abschnitten nachgetragen werden.

### Decided

- Auf Wunsch des Owners gleicht `update` die Projekt-Config mit dem aktuellen Harness-Stand ab (Vorlage + bekannte Schlüssel) und trägt Fehlendes nach. Der zuerst geplante reine Backend-Wechsel ist ein Teil davon.
- Der Abgleich wird als Skript umgesetzt (testbar, gleiches Verhalten in jedem Projekt); der Skill ruft es auf, zeigt die Ergänzungen, fragt bei zu entscheidenden Werten und schreibt nach Freigabe.
- Fehlende Kommentare der Vorlage werden immer nachgetragen, auch in Abschnitten, die es in der Projekt-Config schon gibt. Eigene Kommentare des Projekts bleiben erhalten.

## 2026-09-29 — Umsetzungsplan und Entscheidungen zu Modulen und Kommentaren

### Discussed

- Plan: Vollständigkeitstest der Vorlage, Vergleich Projekt-Config gegen Vorlage, textbasiertes Ergänzen (die Standardbibliothek hat keinen TOML-Schreiber), CLI mit Vorschau/`--set`/`--write`, Skill und Doku, Integration an der Config dieses Repos.
- Nachgetragene Werte übernehmen den bisher wirksamen Standard, damit sich das Verhalten nicht ändert.

### Decided

- Fehlende Module: `update` fragt wie `init`, welche aktiviert werden sollen.
- Weicht ein vorhandener Kommentar an einer Stelle vom Vorlagentext ab, meldet `update` das und fragt, ob er bleibt oder durch den Vorlagentext ersetzt wird.
