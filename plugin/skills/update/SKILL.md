---
name: update
description: Bring an already-initialized project's .claude-harness/config.toml up to the current Claude_Harness schema.
disable-model-invocation: true
---

# Update Claude_Harness in this project

The **target folder** is the folder whose configuration gets updated: the
project root, or a registered subproject's folder. All paths below are
relative to it.

1. Ask what to update, the same way `init` asks what to set up:
   - **This project** (default): the target folder is the project root.
   - **A subproject**: ask which registered name (from `[projects]` of the
     root config).
2. If `.claude-harness/config.toml` does not exist in the target folder, say
   so and point to `/claude-harness:init` instead. Do not create anything
   here.
3. Read the target's `version` and compare it to `CONFIG_VERSION` in
   `plugin/scripts/harness_config.py` (the plugin's own copy at
   `${CLAUDE_PLUGIN_ROOT}/scripts/harness_config.py`).
   - **Equal**: tell the user the config is already up to date and stop.
     Do not change the file.
   - **Greater, or no known migration path from it**: this is not something
     `update` fixes; say so (the same "invalid configuration" case `init`
     and the session-start hook already report) and stop.
   - **Lower, with a migration path**: continue with step 4. The
     session-start hook message ("config is version X, current is Y; run
     `/claude-harness:update`") is what leads here.
4. For each pending migration, in order, show its description in plain
   language. When a step introduces a new value that has no documented
   default (rare while `MIGRATIONS` is empty; check the migration's own
   description for what it needs), ask for it exactly as `init` asks for
   template values. Otherwise fill in the value the migration's description
   states, without asking.
5. Show the resulting `.claude-harness/config.toml` (the concrete edits, not
   just the new version number) before writing anything. Preserve every
   existing comment, ordering, and untouched value — write only the lines
   the migrations actually change plus the new `version`. Write the file
   only after the user approves it.
6. Validate the result the same way `init` does at the end of its setup:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py" <target folder>/<docs.root>/<todo.path>`
   if `todo` is enabled, and confirm the config itself now parses (no
   `ConfigError` reported at the next session start). Report the outcome.
7. For the project root with registered subprojects, mention that each
   subproject is updated separately by re-running this skill with that
   subproject chosen in step 1 — one `update` call never touches more than
   one project's config.
