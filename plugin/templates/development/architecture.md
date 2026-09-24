# Architecture rules

<!-- Binding architecture of this project. Always English; MUST, SHOULD, and
MAY have their RFC 2119 meaning. Keep this file short: rules that apply to the
whole project only. Rules for one area go into a scope file. A rule that can
be checked mechanically names its test, e.g. "Enforced by:
tests/architecture/test_layers.py". -->

## Rules

<!-- Numbered sections of rules, e.g. "## 1. Dependency direction". -->

## Scopes

<!-- Areas with additional rules in architecture/<Scope>.md. A scope applies
in addition to this file, never instead of it. Paths: patterns relative to
the project root in backticks, comma-separated; `*` stays within one path
part, `**` spans any number of parts. Example row:
| llm-integration | `src/llm/**`, `src/prompts/*.py` | Model calls and prompts | -->

| Scope | Paths | Covers |
|---|---|---|

## Changing these rules

If a requirement does not fit these rules, do not add a local exception or
bypass them. Stop before changing code, name the requirement and the
conflicting rule, and propose the smallest change to these rules. A change to
this file or a scope file becomes binding only after the project owner
approves it.
