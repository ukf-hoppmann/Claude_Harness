---
name: worktree
description: Rules for running a change in its own git worktree and merging it back (development suite). Use when a plan was approved and implementation starts, when finishing or aborting a change made in a worktree, or when asked about leftover worktrees.
---

# Change workflow in a worktree

## Before you start

Read `.claude-harness/config.toml` of the project the work belongs to (with
subprojects, the session start lists each project and its folder; paths below
are relative to that folder). The rules apply only if `[modules].development`
is `true` and `[development].worktree` is not `false`; otherwise say so and
stop.

`worktree.py` below means
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py"`, run inside the
worktree. Its output format is described by the script itself; act on its
`error:` lines and on the findings of `check`.

## Why

A change with a plan runs isolated, so several sessions can work in parallel.
It starts from the branch the owner has checked out and goes back into that
branch, never into a default branch the owner did not choose. The owner
approves the plan; everything after that runs without further questions. A
merge commit can be undone with one `git revert -m 1`.

## Decide

- **A plan was approved** (plan mode, or a plan following the
  `decomposition` skill): work in a worktree as described below.
- **No plan:** work locally in the current checkout. Commit only when asked.
- **The session already runs in a worktree** (e.g. created by the app): this
  workflow does not apply. Treat that worktree as the local checkout: no
  further worktree, merge and removal only when the owner asks.
- **The session start reported that `worktree.baseRef` is not `"head"`:**
  propose adding `"worktree": {"baseRef": "head"}` to the project's
  `.claude/settings.json` and work locally until it is set. Without it a
  worktree branches from the default branch instead of the current one.

## Start

1. If the current checkout has uncommitted changes (ignored files do not
   count), ask the owner: continue without them, or commit them first? On
   "commit first", commit them on the current branch, then continue.
2. Call `EnterWorktree` with a name from the backlog ID or a short title.
3. Run `worktree.py start`. It records the base branch (the one checked out
   in the main checkout) and mirrors ignored files such as `.env` into the
   worktree. On an error, leave with `ExitWorktree` `action: "keep"` and ask.
4. If the plan changes dependencies, replace a linked dependency folder in
   the worktree with its own instead of changing the main checkout's.

## Work

Implement and commit in the worktree. Backlog and technical-doc changes of
the change belong in the same branch. Daily reports are written in the main
checkout after the merge, as the `daily` skill says.

## Finish (no questions)

1. Everything is committed and the affected tests pass. Failing tests: do not
   merge; report.
2. Run `worktree.py check`.
   - `base_moved: yes`: first run `git merge <base>` **in the worktree**.
     Resolve simple conflicts yourself and rerun the tests. On conflicts about
     content, stop and report. Conflicts never reach the owner's checkout.
   - Exit code 1: stop and report the findings.
3. Call `ExitWorktree` with `action: "keep"`. The session is back in the
   main checkout (`main` from `check`); Claude Code does not let a worktree
   session run git on the main checkout.
4. In the main checkout:
   `git merge --no-ff <worktree-branch> -m "<what the change does>"`.
   If git refuses because the owner's local changes would be overwritten,
   stop and report. Never stash, reset, or force anything there.
5. Do not push.
6. Remove what this change created: `git worktree remove <worktree-path>`,
   then `git branch -d <worktree-branch>`. Both refuse unmerged or unsaved
   work; then stop and report, never add `--force` or `-D`.
7. Report: base branch, merge commit, and how to undo it
   (`git revert -m 1 <merge-commit>`). If ignored files such as `.env` were
   changed in the worktree, say so: they do not travel with the merge and are
   gone with the worktree. Copy them back before removal only when the owner
   asks.

## Abort

If a step fails or the session ends before the finish, keep the worktree.
Report its path, its branch, and the base branch.

## Never

- Remove worktrees or branches that this session did not create, unless the
  owner explicitly asks. Another session may still need them.
- Pass `discard_changes: true` unless the owner explicitly asks.
- Push, force, rebase the base branch, or stash in the main checkout.
