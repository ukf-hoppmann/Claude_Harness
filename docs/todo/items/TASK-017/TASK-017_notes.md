# TASK-017 — update-Skill: Projekt-Config mit dem aktuellen Harness-Stand abgleichen

## 2026-09-28 — Umfang: vollständiger Abgleich statt nur Backend-Wechsel

### Discussed

- Heute vergleicht `update` nur `version` mit `CONFIG_VERSION`. Weil `MIGRATIONS` leer ist, meldet es immer „aktuell“, obwohl ältere Configs Optionen wie `todo.backend`/`api_url`, die Teile unter `[development]`, `semver.file` oder die Kommentare der Vorlage nicht enthalten (z. B. die Config dieses Repos).

### Decided

- Auf Wunsch des Owners gleicht `update` die Projekt-Config mit dem aktuellen Harness-Stand ab (Vorlage + bekannte Schlüssel) und trägt Fehlendes nach. Der zuerst geplante reine Backend-Wechsel ist ein Teil davon.

### Open

- Wie wird der Abgleich umgesetzt: als Skript (z. B. in `harness_config.py`, testbar) oder als reine Skill-Anleitung?
- Sollen fehlende Kommentare der Vorlage immer nachgetragen werden oder nur bei neu eingefügten Abschnitten?
