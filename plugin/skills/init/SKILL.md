---
name: init
description: Set up Claude_Harness in the current project or in a subproject by creating .claude-harness/config.toml from the template, and optionally the copy of the plugin for cloud sessions.
disable-model-invocation: true
---

# Initialize Claude_Harness in this project

The **target folder** is the folder that gets the configuration. All paths
below (`.claude-harness/config.toml`, `docs.root`, `README.md`, the documents)
are relative to it.

1. Ask what to set up:
   - **This project** (default): the target folder is the project root.
   - **A subproject**, e.g. one plugin of an application whose own rules and
     documents should live in its folder: ask for its folder relative to the
     project root and a name (a letter, then letters, digits, `_`, `-`; not
     `root`). The target folder is that folder.
2. If `.claude-harness/config.toml` already exists in the target folder, show
   its content, say it is already initialized, and stop. Do not overwrite it.
3. Show the user the template `${CLAUDE_PLUGIN_ROOT}/templates/config.toml` and
   ask:
   - which language generated documents use (`docs.language`, default `en`);
   - which folder holds all harness documents (`docs.root`, default `docs`);
   - which modules to enable (currently: `todo`, `daily`, `techdocs`,
     `development`, `semver`; `semver` is off unless the user wants it);
   - for `todo`: the backlog folder relative to `docs.root` (default `todo`),
     and whether the AI works through the ToDo-Viewer API (`backend = "api"`,
     default; `api_url` defaults to `http://localhost:5411/api`) or on
     the files directly (`backend = "files"`; notes need the API);
   - for `daily`: the report folder relative to `docs.root` (default
     `daily`);
   - for `techdocs`: the folder relative to `docs.root` (default `techdocs`)
     and which documents the project keeps (`architecture`, `interfaces`,
     `configuration`, `operations`);
   - for `development`: the folder relative to `docs.root` (default
     `development`), which parts to switch off (all parts are on by
     default; currently `architecture`, `decomposition`, `worktree`, and
     `testing`), and the test folder relative to the project root (`tests`,
     default `tests` next to the source folder);
   - only for the project root: the path of the Claude_Harness repository on
     this machine (`harness.repo`, optional; used to hand harness wishes over
     to its backlog). Propose the output of
     `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_repo.py" --suggest`. A
     subproject config must not contain `[harness]` or `[projects]`;
   - only for the project root: whether Claude Code cloud sessions
     (claude.ai/code) work on this project (`cloud.export`, default `false`).
     Explain that a cloud session loads the repository but not the plugin, so
     with `true` the project holds a committed copy of the plugin (step 11).
     A subproject config must not contain `[cloud]`.
4. Before proposing a backlog folder, search the target folder for existing
   backlog files (e.g. `TODO.md`, `todo.md`, `BACKLOG.md`) and mention what
   you find.
5. Write `.claude-harness/config.toml` in the target folder only after the
   user approved the final content.
6. For a subproject, register it in the root config: add
   `<name> = "<folder>"` to `[projects]` of the project root's
   `.claude-harness/config.toml`, after showing the change. If the project
   root has no config yet, propose one that only registers subprojects
   (`version = 1` plus `[projects]`, no modules) and write it only after
   approval.
7. If `todo` is enabled with `backend = "files"` and `TODO.md` does not exist in the chosen folder, ask
   separately whether to create `TODO.md` and `archive.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/todo/`. Translate the prose into
   `docs.language`, but keep the `## Work items` heading, the format line
   (`Claude_Harness backlog format version 1`), `No entries.`, and all field
   names in English; the backlog check and the ToDo-Viewer need them. Never convert or overwrite an
   existing backlog without explicit approval.
8. If `techdocs` is enabled, look for existing documentation (README,
   architecture or API docs) and mention it. Ask separately whether to create
   missing documents (`README.md` and the chosen ones) from
   `${CLAUDE_PLUGIN_ROOT}/templates/techdocs/`. Never overwrite existing files.
9. If the `architecture` part is active, look for existing architecture rules
   (e.g. `.harness/architecture-rules.md`, `ARCHITECTURE.md`) and mention
   them. Ask separately whether to create `architecture.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/development/architecture.md`. It stays in
   English regardless of `docs.language`. Never overwrite existing files. For
   a subproject, ask whether rules of the root project should apply as well;
   if so, list them under `## Inherited rules`.
10. If `semver` is enabled, set it up as described under "Setup" in skill
    `claude-harness:semver`.
11. If `cloud.export` is `true` (project root only), create the copy for cloud
    sessions: run
    `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cloud_export.py" <target folder>`
    and show the preview (one line per file, the diff of every update; files
    marked `(edited)` are not what an earlier copy wrote). Run it again with
    `--write` only after approval. Then tell the user:
    - The copy consists of the skills `harness-*` in `.claude/skills/`, the
      scripts and templates in `.claude-harness/runtime/`, the hooks in
      `.claude/settings.json`, and the manifest
      `.claude-harness/runtime/manifest.json`. It must be committed, best in
      a commit of its own, so that `git revert` takes it out again.
    - The hooks run only in cloud sessions with one repository; locally the
      plugin applies. `/claude-harness:update` keeps the copy current and can
      remove it again.
    - A cloud session cannot reach the ToDo-Viewer API: the backlog there
      needs `todo.backend = "files"` in the config.
12. Ask whether the harness configs should stay out of Git (e.g. when
    colleagues should not see them): propose adding `.claude-harness/` to
    `.gitignore` and change it only after approval. Do not propose it when
    `cloud.export` is `true`: the copy and the config must be committed for
    cloud sessions. The documents under `docs.root` are normally committed.
    Mention that the plugin can be enabled in `.claude/settings.local.json`
    instead of the committed `.claude/settings.json`.
13. Validate the result:
    `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py" <target folder>/<docs.root>/<todo.path>`
    and report the outcome. For a subproject, the next session start lists it
    among the projects.
