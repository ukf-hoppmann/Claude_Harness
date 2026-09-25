import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath

from helpers import REPO_ROOT, SCRIPTS
from architecture import match_path, parse_scopes

RULES = """# Architecture rules

- Code MUST be tidy.

## Scopes

| Scope | Paths | Covers |
|---|---|---|
| llm | `src/llm/**`, `src/prompts/*.py` | Model calls |

## Changing these rules

Ask first.
"""


class ParseScopesTest(unittest.TestCase):
    def test_parses_table(self):
        scopes, errors = parse_scopes(RULES)
        self.assertEqual(errors, [])
        self.assertEqual(len(scopes), 1)
        self.assertEqual(scopes[0].name, "llm")
        self.assertEqual(scopes[0].patterns, ("src/llm/**", "src/prompts/*.py"))

    def test_no_section_or_empty_table(self):
        self.assertEqual(parse_scopes("# Rules\n"), ([], []))
        empty = "## Scopes\n\n| Scope | Paths | Covers |\n|---|---|---|\n\n## Other\n"
        self.assertEqual(parse_scopes(empty), ([], []))

    def test_invalid_rows(self):
        text = (
            "## Scopes\n\n| Scope | Paths | Covers |\n|---|---|---|\n"
            "| Bad Name | `src/**` | x |\n"
            "| nopaths | src/** | x |\n"
            "| short |\n"
            "| llm | `/abs/**` | x |\n"
        )
        scopes, errors = parse_scopes(text)
        self.assertEqual(scopes, [])
        self.assertEqual(len(errors), 4)

    def test_duplicate_scope(self):
        text = "## Scopes\n\n| Scope | Paths | Covers |\n|---|---|---|\n| a | `x/**` | |\n| a | `y/**` | |\n"
        scopes, errors = parse_scopes(text)
        self.assertEqual(len(scopes), 1)
        self.assertEqual(len(errors), 1)

    def test_template_is_valid(self):
        text = (REPO_ROOT / "plugin/templates/development/architecture.md").read_text()
        self.assertIn("## Scopes", text)
        self.assertEqual(parse_scopes(text)[1], [])


class MatchPathTest(unittest.TestCase):
    def test_patterns(self):
        cases = [
            ("src/llm/**", "src/llm/a.py", True),
            ("src/llm/**", "src/llm/deep/b.py", True),
            ("src/llm/**", "src/llmx/a.py", False),
            ("src/*.py", "src/a.py", True),
            ("src/*.py", "src/sub/a.py", False),
            ("**/models.py", "models.py", True),
            ("**/models.py", "a/b/models.py", True),
            ("src/?.py", "src/a.py", True),
        ]
        for pattern, path, expected in cases:
            with self.subTest(pattern=pattern, path=path):
                self.assertEqual(match_path(pattern, PurePosixPath(path)), expected)


class ArchitectureHookTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name).resolve()
        self.project = base / "project"
        self.data = base / "data"
        self.project.mkdir()
        self.write_config()
        self.rules = self.project / "docs/development/architecture.md"
        self.rules.parent.mkdir(parents=True)
        self.rules.write_text(RULES)
        self.scope = self.project / "docs/development/architecture/llm.md"
        self.scope.parent.mkdir()
        self.scope.write_text("# LLM\n\n- Prompts MUST be typed.\n")

    def tearDown(self):
        self._tmp.cleanup()

    def write_config(self, suite=True, architecture=None):
        config = self.project / ".claude-harness" / "config.toml"
        config.parent.mkdir(exist_ok=True)
        text = f'version = 1\n[modules]\ndevelopment = {"true" if suite else "false"}\n'
        if architecture is not None:
            text += f'[development]\narchitecture = {"true" if architecture else "false"}\n'
        config.write_text(text)

    def run_hook(self, script, payload):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            env=env,
        )

    def read(self, path, session="s1", **extra):
        return self.run_hook(
            "mark_architecture_read.py",
            {"session_id": session, "tool_name": "Read", "tool_input": {"file_path": str(path), **extra}},
        )

    def edit(self, rel_path, session="s1", tool="Edit"):
        key = "notebook_path" if tool == "NotebookEdit" else "file_path"
        result = self.run_hook(
            "check_architecture.py",
            {"session_id": session, "tool_name": tool, "tool_input": {key: str(self.project / rel_path)}},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        if not result.stdout.strip():
            return None
        output = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(output["permissionDecision"], "deny")
        return output["permissionDecisionReason"]

    def test_blocks_until_rules_are_read(self):
        reason = self.edit("src/app.py")
        self.assertIn("docs/development/architecture.md", reason)
        self.read(self.rules)
        self.assertIsNone(self.edit("src/app.py"))

    def test_worktree_files_need_the_same_rules(self):
        worktree = self.project / ".claude/worktrees/w1"
        for source in (self.project / ".claude-harness/config.toml", self.rules, self.scope):
            target = worktree / source.relative_to(self.project)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text())
        reason = self.edit(".claude/worktrees/w1/src/app.py")
        self.assertIn("docs/development/architecture.md", reason)
        self.assertNotIn(".claude/worktrees", reason)
        self.read(worktree / "docs/development/architecture.md")
        self.assertIsNone(self.edit(".claude/worktrees/w1/src/app.py"))

    def test_all_edit_tools_are_checked(self):
        for tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
            with self.subTest(tool=tool):
                self.assertIsNotNone(self.edit("src/app.py", session=tool, tool=tool))

    def test_partial_read_does_not_count(self):
        self.read(self.rules, offset=3)
        self.assertIsNotNone(self.edit("src/app.py"))
        self.read(self.rules, limit=2)
        self.assertIsNotNone(self.edit("src/app.py"))
        self.read(self.rules, offset=1, limit=2000)
        self.assertIsNone(self.edit("src/app.py"))

    def test_scope_file_required_only_for_matching_paths(self):
        self.read(self.rules)
        self.assertIsNone(self.edit("src/app.py"))
        reason = self.edit("src/llm/client.py")
        self.assertIn("docs/development/architecture/llm.md", reason)
        self.assertNotIn("architecture.md,", reason)
        self.read(self.scope)
        self.assertIsNone(self.edit("src/llm/client.py"))

    def test_rules_and_scope_named_together(self):
        reason = self.edit("src/prompts/story.py")
        self.assertIn("docs/development/architecture.md", reason)
        self.assertIn("docs/development/architecture/llm.md", reason)

    def test_tests_count_as_project_files(self):
        self.assertIsNotNone(self.edit("tests/test_app.py"))

    def test_ignored_paths(self):
        for path in (
            "README.md",
            "docs/development/architecture.md",
            "docs/todo/TODO.md",
            "docs/daily/2026-09-24_daily.md",
            "docs/techdocs/interfaces.md",
            ".claude-harness/config.toml",
        ):
            with self.subTest(path=path):
                self.assertIsNone(self.edit(path))

    def test_spec_needs_rules_but_other_backlog_files_do_not(self):
        for spec in ("docs/todo/items/STORY-001/STORY-001_spec.md", "docs/todo/items/STORY-001/STORY-001_spec_api.md"):
            with self.subTest(spec=spec):
                reason = self.edit(spec, session=spec)
                self.assertIn("docs/development/architecture.md", reason)
                self.assertIn("plan", reason)
        self.assertIsNone(self.edit("docs/todo/items/STORY-001/STORY-001_notes.md"))
        self.read(self.rules)
        self.assertIsNone(self.edit("docs/todo/items/STORY-001/STORY-001_spec.md"))

    def exit_plan_mode(self, session="s1"):
        result = self.run_hook(
            "check_architecture.py",
            {"session_id": session, "tool_name": "ExitPlanMode", "tool_input": {"plan": "Add a module."}},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        if not result.stdout.strip():
            return None
        return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecisionReason"]

    def test_plan_needs_rules(self):
        reason = self.exit_plan_mode()
        self.assertIn("docs/development/architecture.md", reason)
        self.assertIn("scope", reason)
        self.read(self.rules)
        self.assertIsNone(self.exit_plan_mode())

    def test_plan_without_rules_file_is_allowed(self):
        self.rules.unlink()
        self.assertIsNone(self.exit_plan_mode())

    def test_files_outside_project_are_ignored(self):
        result = self.run_hook(
            "check_architecture.py",
            {"session_id": "s1", "tool_name": "Write", "tool_input": {"file_path": "/elsewhere/x.py"}},
        )
        self.assertEqual(result.stdout.strip(), "")

    def test_sessions_are_independent(self):
        self.read(self.rules, session="s1")
        self.assertIsNotNone(self.edit("src/app.py", session="s2"))

    def test_missing_rules_file_blocks_nothing(self):
        self.rules.unlink()
        self.assertIsNone(self.edit("src/app.py"))

    def test_suite_or_part_off_blocks_nothing(self):
        for suite, part in ((False, None), (True, False)):
            with self.subTest(suite=suite, part=part):
                self.write_config(suite=suite, architecture=part)
                self.assertIsNone(self.edit("src/app.py"))

    def test_compact_resets_read_state(self):
        self.read(self.rules)
        self.run_hook("session_start.py", {"session_id": "s1", "source": "resume"})
        self.assertIsNone(self.edit("src/app.py"))
        self.run_hook("session_start.py", {"session_id": "s1", "source": "compact"})
        self.assertIsNotNone(self.edit("src/app.py"))

    def test_session_start_mentions_rules_and_scope_errors(self):
        out = self.run_hook("session_start.py", {"session_id": "s1", "source": "startup"}).stdout
        self.assertIn("docs/development/architecture.md", out)
        self.assertIn("claude-harness:architecture", out)
        self.assertIn("before planning", out)
        self.scope.unlink()
        out = self.run_hook("session_start.py", {"session_id": "s1", "source": "startup"}).stdout
        self.assertIn("architecture/llm.md", out)
        self.assertIn("missing", out)

    def test_session_start_mentions_decomposition(self):
        start = {"session_id": "s1", "source": "startup"}
        self.assertIn("claude-harness:decomposition", self.run_hook("session_start.py", start).stdout)
        config = self.project / ".claude-harness" / "config.toml"
        config.write_text('version = 1\n[modules]\ndevelopment = true\n[development]\ndecomposition = false\n')
        out = self.run_hook("session_start.py", start).stdout
        self.assertNotIn("claude-harness:decomposition", out)
        self.assertIn("claude-harness:architecture", out)
        self.write_config(suite=False)
        self.assertNotIn("claude-harness:decomposition", self.run_hook("session_start.py", start).stdout)

    def test_session_start_missing_rules(self):
        self.rules.unlink()
        out = self.run_hook("session_start.py", {"session_id": "s1", "source": "startup"}).stdout
        self.assertIn("does not exist", out)


class SubprojectArchitectureTest(unittest.TestCase):
    """Root project (core) plus subproject Plugins/A, each with its own rules."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name).resolve()
        self.project = base / "project"
        self.data = base / "data"
        self.plugin = self.project / "Plugins/A"
        self.write(self.project / ".claude-harness/config.toml",
                   'version = 1\n[modules]\ndevelopment = true\n[projects]\nA = "Plugins/A"\n')
        self.write(self.plugin / ".claude-harness/config.toml", "version = 1\n[modules]\ndevelopment = true\n")
        self.root_rules = self.write(self.project / "docs/development/architecture.md", RULES)
        self.write(self.project / "docs/development/architecture/llm.md", "# LLM\n")
        self.plugin_rules = self.write(self.plugin / "docs/development/architecture.md", "# Plugin rules\n")

    def tearDown(self):
        self._tmp.cleanup()

    @staticmethod
    def write(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def run_hook(self, script, payload):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script)], input=json.dumps(payload), capture_output=True, text=True, env=env
        )

    def read(self, path):
        self.run_hook("mark_architecture_read.py",
                      {"session_id": "s1", "tool_name": "Read", "tool_input": {"file_path": str(path)}})

    def deny_reason(self, tool, tool_input):
        result = self.run_hook("check_architecture.py", {"session_id": "s1", "tool_name": tool, "tool_input": tool_input})
        self.assertEqual(result.returncode, 0, result.stderr)
        if not result.stdout.strip():
            return None
        return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecisionReason"]

    def edit(self, rel_path):
        return self.deny_reason("Edit", {"file_path": str(self.project / rel_path)})

    def plan(self, text):
        return self.deny_reason("ExitPlanMode", {"plan": text})

    def test_plugin_file_needs_plugin_rules_only(self):
        reason = self.edit("Plugins/A/src/filter.py")
        self.assertIn("Plugins/A/docs/development/architecture.md", reason)
        self.read(self.plugin_rules)
        self.assertIsNone(self.edit("Plugins/A/src/filter.py"))
        # Root scopes do not apply inside the plugin, even with matching patterns.
        self.assertIsNone(self.edit("Plugins/A/src/llm/client.py"))

    def test_core_file_needs_root_rules(self):
        self.read(self.plugin_rules)
        reason = self.edit("src/app.py")
        self.assertIn("docs/development/architecture.md", reason)
        self.assertNotIn("Plugins/A", reason)
        self.read(self.root_rules)
        self.assertIsNone(self.edit("src/app.py"))

    def test_same_named_rules_are_not_confused(self):
        self.read(self.root_rules)
        self.assertIsNotNone(self.edit("Plugins/A/src/filter.py"))

    def test_plugin_harness_files_are_not_checked(self):
        for path in ("Plugins/A/README.md", "Plugins/A/docs/todo/TODO.md", "Plugins/A/.claude-harness/config.toml"):
            with self.subTest(path=path):
                self.assertIsNone(self.edit(path))

    def test_spec_in_plugin_backlog_needs_plugin_rules(self):
        reason = self.edit("Plugins/A/docs/todo/items/STORY-001/STORY-001_spec.md")
        self.assertIn("Plugins/A/docs/development/architecture.md", reason)
        self.read(self.plugin_rules)
        self.assertIsNone(self.edit("Plugins/A/docs/todo/items/STORY-001/STORY-001_spec.md"))

    def test_plan_needs_rules_of_mentioned_projects(self):
        reason = self.plan("Change Plugins/A/src/filter.py and src/app.py.")
        self.assertIn("Plugins/A/docs/development/architecture.md", reason)
        self.read(self.plugin_rules)
        self.assertIsNone(self.plan("Change Plugins/A/src/filter.py."))
        reason = self.plan("Add a module to the core.")
        self.assertIn("docs/development/architecture.md", reason)
        self.assertNotIn("Plugins/A", reason)

    def test_unusable_subproject_is_not_checked(self):
        (self.plugin / ".claude-harness/config.toml").unlink()
        self.assertIsNone(self.edit("Plugins/A/src/filter.py"))


if __name__ == "__main__":
    unittest.main()
