# Claude_Harness

Claude_Harness is a Claude Code plugin that provides project rules as
switchable modules. It replaces the older Agent_Harness; that project is only a
source of ideas, not a binding reference.

- `plugin/` is the product that other projects install. Everything else in
  this repo is for developing it.
- This repo uses its own plugin (see `.claude/settings.json` and
  `.claude-harness/config.toml`).
- Backlog: `docs/todo/`. Its rules live in the `todo` skill; load it only when
  working with the backlog.
- Tests: `python3 -m unittest discover -s tests/implementation -t tests`
  (Python 3.11+, stdlib only); layout and functional tests: `tests/README.md`.
