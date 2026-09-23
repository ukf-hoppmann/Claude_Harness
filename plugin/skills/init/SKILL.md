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
   - which modules to enable (currently: `todo`);
   - for `todo`: which folder holds the backlog (default `docs/todo`).
3. Before proposing a backlog folder, search the project for existing backlog
   files (e.g. `TODO.md`, `todo.md`, `BACKLOG.md`) and mention what you find.
4. Write `.claude-harness/config.toml` only after the user approved the final
   content.
5. If `todo` is enabled and `TODO.md` does not exist in the chosen folder, ask
   separately whether to create `TODO.md` and `archive.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/todo/`. Never convert or overwrite an
   existing backlog without explicit approval.
6. Validate the result:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py" <backlog folder>`
   and report the outcome.
