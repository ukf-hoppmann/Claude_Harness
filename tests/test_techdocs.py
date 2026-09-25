import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS


class TechdocsHookTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name).resolve()
        self.project = base / "project"
        self.data = base / "data"
        self.project.mkdir()
        self.write_config()

    def tearDown(self):
        self._tmp.cleanup()

    def write_config(self, enabled=True):
        config = self.project / ".claude-harness" / "config.toml"
        config.parent.mkdir(exist_ok=True)
        config.write_text(
            'version = 1\n[docs]\nroot = "docs"\n'
            f'[modules]\ntechdocs = {"true" if enabled else "false"}\n'
        )

    def run_hook(self, script, payload):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            env=env,
        )

    def edit(self, rel_path, session="s1"):
        return self.run_hook(
            "mark_techdocs.py",
            {"session_id": session, "tool_name": "Edit", "tool_input": {"file_path": str(self.project / rel_path)}},
        )

    def stop(self, session="s1", active=False):
        return self.run_hook("check_techdocs.py", {"session_id": session, "stop_hook_active": active})

    def test_code_change_without_docs_reminds_once_per_session(self):
        self.edit("src/app.py")
        first = self.stop()
        self.assertEqual(first.returncode, 2)
        self.assertIn("claude-harness:techdocs", first.stderr)
        self.edit("src/other.py")
        self.assertEqual(self.stop().returncode, 0)

    def test_docs_change_in_worktree_counts_as_docs(self):
        worktree = self.project / ".claude/worktrees/w1"
        (worktree / ".claude-harness").mkdir(parents=True)
        (worktree / ".claude-harness/config.toml").write_text(
            (self.project / ".claude-harness/config.toml").read_text()
        )
        for rel in ("src/app.py", "docs/techdocs/interfaces.md"):
            self.run_hook("mark_techdocs.py", {
                "session_id": "s1", "cwd": str(worktree), "tool_name": "Edit",
                "tool_input": {"file_path": str(worktree / rel)},
            })
        result = self.run_hook("check_techdocs.py", {"session_id": "s1", "cwd": str(worktree)})
        self.assertEqual(result.returncode, 0, result.stderr)

    def write_subproject(self):
        (self.project / ".claude-harness/config.toml").write_text(
            'version = 1\n[modules]\ntechdocs = true\n[projects]\nA = "Plugins/A"\n'
        )
        config = self.project / "Plugins/A/.claude-harness/config.toml"
        config.parent.mkdir(parents=True)
        config.write_text("version = 1\n[modules]\ntechdocs = true\n")

    def test_docs_count_only_for_their_own_project(self):
        self.write_subproject()
        self.edit("Plugins/A/src/filter.py")
        self.edit("docs/techdocs/interfaces.md")
        result = self.stop()
        self.assertEqual(result.returncode, 2)
        self.assertIn("A (Plugins/A/README.md, Plugins/A/docs/techdocs/)", result.stderr)
        self.assertNotIn("root (", result.stderr)

    def test_plugin_docs_satisfy_plugin_changes(self):
        self.write_subproject()
        self.edit("Plugins/A/src/filter.py")
        self.edit("Plugins/A/README.md")
        self.assertEqual(self.stop().returncode, 0)

    def test_reminds_once_per_project(self):
        self.write_subproject()
        self.edit("Plugins/A/src/filter.py")
        self.assertEqual(self.stop().returncode, 2)
        self.assertEqual(self.stop().returncode, 0)
        self.edit("src/core.py")
        result = self.stop()
        self.assertEqual(result.returncode, 2)
        self.assertIn("root (README.md, docs/techdocs/)", result.stderr)
        self.assertNotIn("Plugins/A", result.stderr)

    def test_sessions_are_independent(self):
        self.edit("src/app.py", session="s1")
        self.assertEqual(self.stop(session="s2").returncode, 0)
        self.assertEqual(self.stop(session="s1").returncode, 2)

    def test_docs_change_in_same_session_suppresses_reminder(self):
        for doc in ("README.md", "docs/techdocs/architecture.md"):
            with self.subTest(doc=doc):
                session = f"s-{doc}"
                self.edit("src/app.py", session=session)
                self.edit(doc, session=session)
                self.assertEqual(self.stop(session=session).returncode, 0)

    def test_ignored_paths_do_not_remind(self):
        ignored = [
            "tests/test_app.py",
            "src/app_test.go",
            "web/app.test.ts",
            "docs/todo/TODO.md",
            "docs/daily/2026-09-23_daily.md",
            "docs/techdocs/interfaces.md",
            ".claude-harness/config.toml",
        ]
        for index, path in enumerate(ignored):
            with self.subTest(path=path):
                session = f"s{index}"
                self.edit(path, session=session)
                self.assertEqual(self.stop(session=session).returncode, 0)

    def test_files_outside_project_are_ignored(self):
        self.run_hook(
            "mark_techdocs.py",
            {"session_id": "s1", "tool_name": "Write", "tool_input": {"file_path": "/elsewhere/notes.md"}},
        )
        self.assertEqual(self.stop().returncode, 0)

    def test_stop_hook_active_is_silent(self):
        self.edit("src/app.py")
        self.assertEqual(self.stop(active=True).returncode, 0)

    def test_module_off_is_silent(self):
        self.write_config(enabled=False)
        self.edit("src/app.py")
        self.assertEqual(self.stop().returncode, 0)

    def test_session_start_lists_missing_documents(self):
        result = self.run_hook("session_start.py", {})
        self.assertIn("Missing technical docs: README.md, docs/techdocs/architecture.md", result.stdout)
        (self.project / "README.md").write_text("# P\n")
        self.assertNotIn("README.md,", self.run_hook("session_start.py", {}).stdout)


if __name__ == "__main__":
    unittest.main()
