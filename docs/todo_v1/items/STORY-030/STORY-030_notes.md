## 2026-09-25 — Update-Schritt und Config-Versionierung

### Discussed

- Ausgangspunkt: Andere Projekte sollen per "Update den Harness" prüfen
  lassen, ob sich am Harness etwas geändert hat, und das nachziehen — i. d. R.
  betrifft das nur `.claude-harness/config.toml`.
- Frage, ob die Config dafür statt der einfachen Zahl (`version = 1`) eine
  SemVer-Version bekommen sollte.

### Decided

- Keine SemVer für das Config-Schema. Begründung: SemVer lohnt sich bei
  mehreren unabhängigen Konsumenten, die selbst zwischen "minor sicher
  automatisch ziehen" und "major erst prüfen" unterscheiden müssen. Hier gibt
  es genau einen Konsumenten (den Harness selbst), und Schema plus
  Migrationslogik werden immer zusammen mit dem Plugin ausgeliefert.
  Zusätzlich brauchen additive Änderungen (z. B. ein neues Modul in
  `KNOWN_MODULES`) schon jetzt keinen Versionsbump, da alte Configs den
  Default bekommen (siehe `harness_config.py`); ein Bump ist nur bei
  echten Breaking Changes nötig.
- Stattdessen: `CONFIG_VERSION` bleibt ein hochzählender Integer, ergänzt um
  eine Migrationsliste (`from_version → to_version` mit einer kurzen
  Beschreibung und ggf. einer Funktion, die alte Werte in neue überführt),
  ähnlich wie Datenbank-Schema-Migrationen.
- Neuer `update`-Skill als Pendant zu `init`: liest die Config, vergleicht
  `version` mit `CONFIG_VERSION`, wendet bei Rückstand die fehlenden
  Migrationen nacheinander an (Rückfrage nur bei neuen, echten
  Entscheidungen), zeigt das Ergebnis vor dem Schreiben und validiert danach
  mit dem bestehenden Config-Parser.

### Open

- ~~Genaues Format der Migrationsliste in `harness_config.py`.~~ Entschieden
  und umgesetzt: `Migration`-Dataclass (`from_version`, `to_version`,
  `description`, `upgrade`), `MIGRATIONS`-Tupel, `_migration_chain`,
  `migrate_data`, Exception `ConfigOutdated`.
- ~~Ob der `update`-Skill auch für registrierte Subprojekte (`[projects]`)
  automatisch mitläuft.~~ Entschieden: nein, ein Aufruf aktualisiert genau
  ein Projekt; Teilprojekte werden einzeln aufgerufen (wie bei `init`).
- ~~Ob/wie der Session-Start-Hook auf eine veraltete Config hinweisen
  soll.~~ Umgesetzt: eigener `ConfigOutdated`-Zweig in `session_start.py`
  (`outdated_message`), verweist auf `/claude-harness:update`.

## 2026-09-25 — Umsetzung

### Decided

- Plan umgesetzt in Worktree `worktree-STORY-030`: Migrationsrahmen in
  `plugin/scripts/harness_config.py` (test-first, `tests/test_config.py`),
  eigene Hook-Meldung in `plugin/scripts/session_start.py` (test-first,
  neues `tests/test_session_start.py`), neuer Skill
  `plugin/skills/update/SKILL.md` analog `init`, Doku in
  `docs/techdocs/interfaces.md` und `docs/techdocs/configuration.md`
  ergänzt.
- `CONFIG_VERSION` bleibt `1`, `MIGRATIONS` bleibt leer — kein echter
  Schema-Bruch für diese Story. Der Rahmen ist über Tests mit einer
  gemockten synthetischen Migration abgedeckt (`mock.patch.object` auf
  `CONFIG_VERSION`/`MIGRATIONS`).
- Alle Acceptance criteria aus `STORY-030_spec.md` erfüllt: 188 Tests grün,
  Backlog-Check fehlerfrei, `update`-Skill würde gegen die eigene Config
  dieses Repos "bereits aktuell" melden.
