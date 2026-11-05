import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS

PATTERNS = '["src/core/index.ts", "src/plugins/*/index.ts"]'


class PublicApiHookTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name).resolve()
        self.project = base / "project"
        self.data = base / "data"
        self.project.mkdir()
        self.write_config()

    def tearDown(self):
        self._tmp.cleanup()

    def write_config(self, patterns=PATTERNS, development="true", extra="", path=None):
        config = (path or self.project) / ".claude-harness" / "config.toml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(
            f"version = 1\n[modules]\ndevelopment = {development}\n"
            f"[development]\npublic_api = {patterns}\n{extra}"
        )

    def run_hook(self, script, payload):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script)],
            input=json.dumps(payload), capture_output=True, text=True, env=env,
        )

    def edit(self, rel_path, session="s1", base=None, **extra):
        file_path = (base or self.project) / rel_path
        return self.run_hook("mark_public_api.py", {
            "session_id": session, "tool_name": "Edit", "tool_input": {"file_path": str(file_path)}, **extra,
        })

    def stop(self, session="s1", **extra):
        return self.run_hook("check_public_api.py", {"session_id": session, **extra})

    def test_matching_change_reminds_once_per_session(self):
        self.edit("src/core/index.ts")
        first = self.stop()
        self.assertEqual(first.returncode, 2)
        self.assertIn("claude-harness:architecture", first.stderr)
        self.assertIn("claude-harness:interfaces", first.stderr)
        self.assertIn("1 file", first.stderr)
        self.assertIn("src/core/index.ts", first.stderr)
        self.edit("src/plugins/a/index.ts")
        self.assertEqual(self.stop().returncode, 0)

    def test_other_session_is_reminded_separately(self):
        self.edit("src/core/index.ts")
        self.assertEqual(self.stop().returncode, 2)
        self.edit("src/core/index.ts", session="s2")
        self.assertEqual(self.stop(session="s2").returncode, 2)

    def test_message_counts_files(self):
        self.edit("src/core/index.ts")
        self.edit("src/plugins/a/index.ts")
        self.edit("src/plugins/a/index.ts")
        self.assertIn("2 files", self.stop().stderr)

    def test_non_matching_change_is_not_marked(self):
        self.edit("src/other.ts")
        self.edit("src/plugins/a/deep/index.ts")
        self.assertEqual(self.stop().returncode, 0)

    def test_no_reminder_without_change(self):
        self.assertEqual(self.stop().returncode, 0)

    def test_no_patterns_does_nothing(self):
        self.write_config(patterns="[]")
        self.edit("src/core/index.ts")
        self.assertEqual(self.stop().returncode, 0)

    def test_architecture_part_off_does_nothing(self):
        self.write_config(extra="architecture = false\n")
        self.edit("src/core/index.ts")
        self.assertEqual(self.stop().returncode, 0)

    def test_development_off_does_nothing(self):
        self.write_config(development="false")
        self.edit("src/core/index.ts")
        self.assertEqual(self.stop().returncode, 0)

    def test_invalid_config_does_nothing(self):
        self.edit("src/core/index.ts")
        self.write_config(patterns='["/abs"]')
        self.assertEqual(self.stop().returncode, 0)
        self.assertEqual(self.edit("src/core/index.ts").returncode, 0)

    def test_stop_hook_active_does_nothing(self):
        self.edit("src/core/index.ts")
        self.assertEqual(self.stop(stop_hook_active=True).returncode, 0)
        self.assertEqual(self.stop().returncode, 2)

    def test_change_in_worktree_counts(self):
        worktree = self.project / ".claude/worktrees/w1"
        self.write_config(path=worktree)
        self.edit("src/core/index.ts", base=worktree, cwd=str(worktree))
        result = self.stop(cwd=str(worktree))
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_subprojects_give_one_message_naming_each(self):
        (self.project / ".claude-harness/config.toml").write_text(
            'version = 1\n[projects]\nA = "Plugins/A"\nB = "Plugins/B"\n'
        )
        for name in ("A", "B"):
            self.write_config(path=self.project / "Plugins" / name)
        self.edit("Plugins/A/src/core/index.ts")
        self.edit("Plugins/B/src/plugins/x/index.ts")
        result = self.stop()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("A (", result.stderr)
        self.assertIn("B (", result.stderr)
        self.assertEqual(self.stop().returncode, 0)

    def test_subproject_without_patterns_is_skipped(self):
        (self.project / ".claude-harness/config.toml").write_text(
            'version = 1\n[projects]\nA = "Plugins/A"\nB = "Plugins/B"\n'
        )
        self.write_config(path=self.project / "Plugins" / "A")
        self.write_config(patterns="[]", path=self.project / "Plugins" / "B")
        self.edit("Plugins/A/src/core/index.ts")
        self.edit("Plugins/B/src/core/index.ts")
        result = self.stop()
        self.assertIn("A (", result.stderr)
        self.assertNotIn("B (", result.stderr)


if __name__ == "__main__":
    unittest.main()
