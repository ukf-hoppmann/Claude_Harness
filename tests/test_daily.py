import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS


class DailyHookTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name).resolve()
        self.project = base / "project"
        self.data = base / "data"
        self.project.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.write_config()
        self.commit("src/app.py", "initial")

    def tearDown(self):
        self._tmp.cleanup()

    def git(self, *args, cwd=None):
        subprocess.run(["git", "-C", str(cwd or self.project), *args], check=True, capture_output=True)

    def write_config(self, daily=True):
        config = self.project / ".claude-harness" / "config.toml"
        config.parent.mkdir(exist_ok=True)
        config.write_text(
            f'version = 1\n[docs]\nroot = "docs"\n[modules]\ndaily = {"true" if daily else "false"}\n'
        )

    def commit(self, path, message, cwd=None):
        root = cwd or self.project
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(target.read_text() + "x\n" if target.exists() else "x\n")
        self.git("add", "-A", cwd=root)
        self.git("commit", "-q", "-m", message, cwd=root)

    def run_script(self, script, *args, payload=None, cwd=None):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(cwd or self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script), *args],
            input=json.dumps(payload or {}),
            capture_output=True,
            text=True,
            env=env,
        )

    def stop(self, session="s1", active=False, cwd=None):
        return self.run_script(
            "check_daily.py", payload={"session_id": session, "stop_hook_active": active}, cwd=cwd
        )

    def baseline(self):
        # The first run sets HEAD as the silent starting point.
        self.assertEqual(self.stop().returncode, 0)

    def test_new_commit_triggers_reminder_once_per_head(self):
        self.baseline()
        self.commit("src/app.py", "feature")
        first = self.stop()
        self.assertEqual(first.returncode, 2)
        self.assertIn("1 commit(s)", first.stderr)
        self.assertIn("claude-harness:daily", first.stderr)
        self.assertEqual(self.stop().returncode, 0)
        self.assertEqual(self.stop(session="s2").returncode, 2)

    def test_stop_hook_active_is_silent(self):
        self.baseline()
        self.commit("src/app.py", "feature")
        self.assertEqual(self.stop(active=True).returncode, 0)

    def test_ack_clears_pending(self):
        self.baseline()
        self.commit("src/app.py", "feature")
        pending = self.run_script("daily.py", "pending")
        self.assertEqual(pending.returncode, 0)
        self.assertIn("feature", pending.stdout)
        self.assertIn("docs/development/daily/", pending.stdout)
        self.assertEqual(self.run_script("daily.py", "ack").returncode, 0)
        self.assertIn("No pending commits", self.run_script("daily.py", "pending").stdout)
        self.assertEqual(self.stop().returncode, 0)

    def test_daily_only_commit_is_ignored(self):
        self.baseline()
        self.commit("docs/development/daily/2026-09-23_daily.md", "daily report")
        self.assertEqual(self.stop().returncode, 0)

    def test_backlog_only_commit_is_ignored(self):
        self.baseline()
        self.commit("docs/todo/TODO.md", "backlog change")
        self.commit("docs/todo/items/STORY-001/STORY-001_notes.md", "notes")
        self.assertEqual(self.stop().returncode, 0)

    def test_mixed_commit_with_backlog_triggers(self):
        self.baseline()
        (self.project / "docs/todo").mkdir(parents=True)
        (self.project / "docs/todo/TODO.md").write_text("x\n")
        self.commit("src/app.py", "code and backlog")
        self.assertEqual(self.stop().returncode, 2)

    def test_merge_of_feature_branch_triggers(self):
        self.baseline()
        self.git("checkout", "-q", "-b", "feature")
        self.commit("src/other.py", "on branch")
        self.assertEqual(self.stop().returncode, 0)
        self.git("checkout", "-q", "main")
        self.git("merge", "-q", "--no-ff", "-m", "merge feature", "feature")
        self.assertEqual(self.stop().returncode, 2)

    def test_linked_worktree_is_silent(self):
        self.baseline()
        worktree = self.project.parent / "wt"
        self.git("worktree", "add", "-q", "-b", "wt-branch", str(worktree))
        self.commit("src/wt.py", "in worktree", cwd=worktree)
        self.assertEqual(self.stop(cwd=worktree).returncode, 0)
        self.assertNotEqual(self.run_script("daily.py", "pending", cwd=worktree).returncode, 0)

    def test_module_off_is_silent(self):
        self.write_config(daily=False)
        self.baseline()
        self.commit("src/app.py", "feature")
        self.assertEqual(self.stop().returncode, 0)


if __name__ == "__main__":
    unittest.main()
