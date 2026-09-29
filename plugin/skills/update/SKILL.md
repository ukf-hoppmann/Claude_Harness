---
name: update
description: Bring an already-initialized project's .claude-harness/config.toml up to the current Claude_Harness state: schema version, missing options, modules, and template comments.
disable-model-invocation: true
---

# Update Claude_Harness in this project

The **target folder** is the folder whose configuration gets updated: the
project root, or a registered subproject's folder. All paths below are
relative to it. `config_update.py` below means
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/config_update.py" <target folder>`,
with `--subproject` added for a subproject. Its output format is described by
the script itself.

1. Ask what to update, the same way `init` asks what to set up:
   - **This project** (default): the target folder is the project root.
   - **A subproject**: ask which registered name (from `[projects]` of the
     root config).
2. If `.claude-harness/config.toml` does not exist in the target folder, say
   so and point to `/claude-harness:init` instead. Do not create anything
   here.
3. Schema version: read the target's `version` and compare it to
   `CONFIG_VERSION` in `${CLAUDE_PLUGIN_ROOT}/scripts/harness_config.py`.
   - **Greater, or lower without a known migration path**: this is not
     something `update` fixes; say so (the same "invalid configuration" case
     `init` and the session-start hook report) and stop.
   - **Lower, with a migration path**: show each pending migration's
     description in plain language, ask for a new value only when the
     description names no default, show the concrete edits, and write them
     plus the new `version` after approval. Keep every comment, ordering,
     and untouched value.
   - **Equal**: continue.
4. Run `config_update.py`. On an `error:` line, report it and stop. With
   `changes: 0` and no decision line, tell the user the config is up to date
   and stop.
5. Ask for every pending decision, the way `init` asks:
   - `modules.<name>`: a module the config does not list yet (currently
     off). Explain what it does and ask whether to enable it.
   - `todo.backend`: whether the AI works through the ToDo-Viewer API
     (`api`) or on the files directly (`files`).
   - `harness.repo` (project root only): propose the output of
     `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_repo.py" --suggest`;
     it may stay empty.
   - `comment:<place>`: a comment differs from the template. Show both texts
     and ask whether to keep it or replace it with the template text.

   Run `config_update.py` again with one `--set <key>=<value>` per answer.
   Answers can bring up new decisions (enabling `todo` asks for
   `todo.backend`); ask those too, until none is pending.
6. Show the diff and write it after approval: the same call plus `--write`.
7. Afterwards:
   - If `todo` is on with backend `api`, check the server with
     `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog_api.py" [--project <name>] health`
     and report the result. If `todo` is on with backend `files`, run
     `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py" <target folder>/<docs.root>/<todo.path>`
     and report the result.
   - For each module enabled in step 5, offer the documents `init` would set
     up for it (its steps 7 to 10), with the same rules: ask first, never
     overwrite.
8. For the project root with registered subprojects, mention that each
   subproject is updated separately by re-running this skill with that
   subproject chosen in step 1. One `update` call never touches more than
   one project's config.
