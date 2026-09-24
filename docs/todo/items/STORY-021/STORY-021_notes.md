# STORY-021 — Notes

## 2026-09-24 — Testlauf in my_story_game

### Discussed

- Test in einem temporären, abgekoppelten Worktree von my_story_game
  (Stand `57ba94a`), mit eigenständigen `claude -p`-Sessions, Plugin per
  `--plugin-dir` geladen. Das Projekt hat bereits das Altsystem `.harness/`,
  ein `docs/TODO.md` im alten Format und `docs/development/daily/`.
- Ablauf: `/claude-harness:init` → Fragen beantwortet (de, `docs`, alle
  Module, techdocs inkl. `operations`) → Config, Backlog, README und vier
  techdocs aus den Vorlagen angelegt → Validierung: 0 Fehler.
- Beobachtet:
  - Vor jeder Freigabe wurde nichts geschrieben. `.harness/`, das bestehende
    `docs/TODO.md` und der bestehende Daily-Ordner wurden erkannt und
    angesprochen, aber nicht verändert.
  - Beim Anlegen des Backlogs wurde auch `## Work items` ins Deutsche
    übersetzt. Der Stop-Hook meldete den Fehler, die Session korrigierte ihn
    selbst.
  - Der techdocs-Stop-Hook schlug nach dem Schreiben von
    `.claude-harness/config.toml` an. Die Session entschied zu Recht, dass
    keine Aktualisierung nötig ist.
  - Mit `--plugin-dir` außerhalb des Projekts blockiert die Sandbox den
    Lesezugriff auf die Vorlagen. Das kommt vom Testaufbau; im Test half
    `--add-dir`.
  - Zweiter Aufruf in dem eingerichteten Projekt: „bereits initialisiert“,
    Prüfsummen aller angelegten Dateien unverändert.
- Worktree und Test-Transkripte wurden danach entfernt; my_story_game ist
  unverändert.

### Decided

- Die Completion criteria sind erfüllt; die Story wartet auf Bestätigung.

### Open

- Keine.

## 2026-09-24 — Verbesserungen aus dem Testlauf

### Decided

- `init` sagt beim Anlegen des Backlogs ausdrücklich, dass `## Work items` und
  die Feldnamen englisch bleiben.
- Der techdocs-Hook ignoriert Änderungen unter `.claude-harness/`
  (Test ergänzt, `interfaces.md` angepasst).
