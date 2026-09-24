---
name: init
description: Set up Claude_Harness in the current project by creating .claude-harness/config.toml from the template.
disable-model-invocation: true
---

# Initialize Claude_Harness in this project

1. If `.claude-harness/config.toml` already exists, show its content, say the
   project is already initialized, and stop. Do not overwrite it.
2. Show the user the template `${CLAUDE_PLUGIN_ROOT}/templates/config.toml` and
   ask:
   - which language generated documents use (`docs.language`, default `en`);
   - which folder holds all harness documents (`docs.root`, default `docs`);
   - which modules to enable (currently: `todo`, `daily`, `techdocs`,
     `development`);
   - for `todo`: the backlog folder relative to `docs.root` (default `todo`);
   - for `daily`: the report folder relative to `docs.root` (default
     `daily`);
   - for `techdocs`: the folder relative to `docs.root` (default `techdocs`)
     and which documents the project keeps (`architecture`, `interfaces`,
     `configuration`, `operations`);
   - for `development`: the folder relative to `docs.root` (default
     `development`) and which parts to switch off (all parts are on by
     default; currently `architecture`, `decomposition`, and `worktree`);
   - the path of the Claude_Harness repository on this machine
     (`harness.repo`, optional; used to hand harness wishes over to its
     backlog). Propose the output of
     `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_repo.py" --suggest`.
3. Before proposing a backlog folder, search the project for existing backlog
   files (e.g. `TODO.md`, `todo.md`, `BACKLOG.md`) and mention what you find.
4. Write `.claude-harness/config.toml` only after the user approved the final
   content.
5. If `todo` is enabled and `TODO.md` does not exist in the chosen folder, ask
   separately whether to create `TODO.md` and `archive.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/todo/`. Translate the prose into
   `docs.language`, but keep the `## Work items` heading and all field names
   in English; the backlog check needs them. Never convert or overwrite an
   existing backlog without explicit approval.
6. If `techdocs` is enabled, look for existing documentation (README,
   architecture or API docs) and mention it. Ask separately whether to create
   missing documents (`README.md` and the chosen ones) from
   `${CLAUDE_PLUGIN_ROOT}/templates/techdocs/`. Never overwrite existing files.
7. If the `architecture` part is active, look for existing architecture rules
   (e.g. `.harness/architecture-rules.md`, `ARCHITECTURE.md`) and mention
   them. Ask separately whether to create `architecture.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/development/architecture.md`. It stays in
   English regardless of `docs.language`. Never overwrite existing files.
8. Validate the result:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py" <docs.root>/<todo.path>`
   and report the outcome.
