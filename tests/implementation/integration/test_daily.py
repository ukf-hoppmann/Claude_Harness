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
        self.assertIn("docs/daily/", pending.stdout)
        self.assertEqual(self.run_script("daily.py", "ack").returncode, 0)
        self.assertIn("No pending commits", self.run_script("daily.py", "pending").stdout)
        self.assertEqual(self.stop().returncode, 0)

    def test_daily_only_commit_is_ignored(self):
        self.baseline()
        self.commit("docs/daily/2026-09-23_daily.md", "daily report")
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
        self.git("checkout", "-q", "main")
        self.git("merge", "-q", "--no-ff", "-m", "merge feature", "feature")
        self.assertEqual(self.stop().returncode, 2)

    def test_any_checked_out_branch_triggers(self):
        # No main or master and no remote origin: the checked-out branch is where reports go.
        self.git("branch", "-m", "modularRefactor")
        self.git("remote", "add", "ezf-ui", "https://example.com/repo.git")
        self.baseline()
        self.commit("src/app.py", "feature")
        self.assertEqual(self.stop().returncode, 2)
        self.assertIn("feature", self.run_script("daily.py", "pending").stdout)

    def test_detached_head_is_silent(self):
        self.baseline()
        self.git("checkout", "-q", "--detach")
        self.commit("src/app.py", "detached")
        self.assertEqual(self.stop().returncode, 0)
        self.assertEqual(self.run_script("daily.py", "pending").returncode, 1)

    def test_branch_of_a_change_is_silent(self):
        self.baseline()
        self.git("checkout", "-q", "-b", "change")
        self.git("config", "branch.change.harnessBase", "main")
        self.commit("src/app.py", "change work")
        self.assertEqual(self.stop().returncode, 0)
        self.assertEqual(self.run_script("daily.py", "pending").returncode, 1)

    def test_acknowledged_branch_is_not_reported_again_after_merge(self):
        self.baseline()
        self.git("checkout", "-q", "-b", "feature")
        self.commit("src/other.py", "on branch")
        self.assertEqual(self.run_script("daily.py", "ack").returncode, 0)
        self.git("checkout", "-q", "main")
        self.git("merge", "-q", "--no-ff", "-m", "merge feature", "feature")
        self.assertEqual(self.stop().returncode, 0)
        self.assertIn("No pending commits", self.run_script("daily.py", "pending").stdout)

    def test_switching_branches_keeps_pending_commits(self):
        self.baseline()
        self.git("checkout", "-q", "-b", "feature")
        self.commit("src/other.py", "on branch")
        self.assertEqual(self.run_script("daily.py", "ack").returncode, 0)
        self.git("checkout", "-q", "main")
        self.commit("src/app.py", "on main")
        pending = self.run_script("daily.py", "pending").stdout
        self.assertIn("on main", pending)
        self.assertNotIn("on branch", pending)

    def test_single_sha_ack_file_still_counts(self):
        self.commit("src/app.py", "acknowledged before")
        head = subprocess.run(
            ["git", "-C", str(self.project), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
        ack = self.project / ".git/claude-harness/daily-ack"
        ack.parent.mkdir(parents=True)
        ack.write_text(head)
        self.commit("src/app.py", "added after")
        pending = self.run_script("daily.py", "pending").stdout
        self.assertIn("added after", pending)
        self.assertNotIn("acknowledged before", pending)

    def test_linked_worktree_is_silent(self):
        self.baseline()
        worktree = self.project.parent / "wt"
        self.git("worktree", "add", "-q", "-b", "wt-branch", str(worktree))
        self.commit("src/wt.py", "in worktree", cwd=worktree)
        self.assertEqual(self.stop(cwd=worktree).returncode, 0)
        self.assertNotEqual(self.run_script("daily.py", "pending", cwd=worktree).returncode, 0)

    def test_worktree_merging_back_into_its_base_reports_there(self):
        # The owner switched the main checkout away; the change is merged in its worktree.
        self.baseline()
        worktree = self.project.parent / "wt"
        self.git("worktree", "add", "-q", "-b", "wt-branch", str(worktree))
        self.git("config", "branch.wt-branch.harnessBase", "main")
        self.git("checkout", "-q", "-b", "other")
        self.commit("src/wt.py", "in worktree", cwd=worktree)
        self.assertEqual(self.stop(cwd=worktree).returncode, 0)
        self.git("checkout", "-q", "main", cwd=worktree)
        self.git("merge", "-q", "--no-ff", "-m", "merge change", "wt-branch", cwd=worktree)
        self.assertEqual(self.stop(cwd=worktree).returncode, 2)
        pending = self.run_script("daily.py", "pending", cwd=worktree)
        self.assertEqual(pending.returncode, 0, pending.stderr)
        self.assertIn("in worktree", pending.stdout)

    def write_subproject(self, root_daily=True):
        (self.project / ".claude-harness/config.toml").write_text(
            f'version = 1\n[modules]\ndaily = {"true" if root_daily else "false"}\n[projects]\nA = "Plugins/A"\n'
        )
        config = self.project / "Plugins/A/.claude-harness/config.toml"
        config.parent.mkdir(parents=True)
        config.write_text("version = 1\n[modules]\ndaily = true\n")
        self.commit("src/app.py", "set up subproject")

    def test_plugin_commit_counts_only_for_plugin(self):
        self.write_subproject()
        self.baseline()
        self.commit("Plugins/A/src/filter.py", "plugin feature")
        result = self.stop()
        self.assertEqual(result.returncode, 2)
        self.assertIn("A (1, Plugins/A/docs/daily/)", result.stderr)
        self.assertIn("--project A", result.stderr)
        self.assertNotIn("root (", result.stderr)
        self.assertIn("No pending commits", self.run_script("daily.py", "pending").stdout)
        pending = self.run_script("daily.py", "pending", "--project", "A").stdout
        self.assertIn("plugin feature", pending)
        self.assertIn("Plugins/A/docs/daily/", pending)

    def test_core_commit_counts_only_for_root(self):
        self.write_subproject()
        self.baseline()
        self.commit("src/core.py", "core feature")
        result = self.stop()
        self.assertIn("root (1, docs/daily/)", result.stderr)
        self.assertIn("No pending commits", self.run_script("daily.py", "pending", "--project", "A").stdout)

    def test_plugin_backlog_only_commit_counts_nowhere(self):
        self.write_subproject()
        self.baseline()
        self.commit("Plugins/A/docs/todo/TODO.md", "plugin backlog")
        self.commit("Plugins/A/docs/daily/2026-09-25_daily.md", "plugin daily")
        self.assertEqual(self.stop().returncode, 0)

    def test_acknowledged_states_are_separate(self):
        self.write_subproject()
        self.baseline()
        self.commit("Plugins/A/src/filter.py", "plugin feature")
        self.commit("src/core.py", "core feature")
        self.assertEqual(self.run_script("daily.py", "ack", "--project", "A").returncode, 0)
        self.assertIn("No pending commits", self.run_script("daily.py", "pending", "--project", "A").stdout)
        self.assertIn("core feature", self.run_script("daily.py", "pending").stdout)

    def test_project_selection_errors(self):
        self.write_subproject(root_daily=False)
        unknown = self.run_script("daily.py", "pending", "--project", "Nope")
        self.assertEqual(unknown.returncode, 1)
        self.assertIn("A", unknown.stderr)
        missing = self.run_script("daily.py", "pending")
        self.assertEqual(missing.returncode, 1)
        self.assertIn("--project A", missing.stderr)
        self.assertEqual(self.run_script("daily.py", "pending", "--project").returncode, 2)

    def test_session_in_subproject_below_git_root(self):
        plugin = self.project / "Plugins/A"
        (plugin / ".claude-harness").mkdir(parents=True)
        (plugin / ".claude-harness/config.toml").write_text("version = 1\n[modules]\ndaily = true\n")
        self.commit("Plugins/A/src/filter.py", "plugin set up")
        self.assertEqual(self.stop(cwd=plugin).returncode, 0)
        self.commit("src/core.py", "outside the plugin")
        self.commit("Plugins/A/docs/todo/TODO.md", "plugin backlog")
        self.assertEqual(self.stop(cwd=plugin).returncode, 0)
        self.commit("Plugins/A/src/filter.py", "plugin feature")
        self.assertEqual(self.stop(cwd=plugin).returncode, 2)

    def test_module_off_is_silent(self):
        self.write_config(daily=False)
        self.baseline()
        self.commit("src/app.py", "feature")
        self.assertEqual(self.stop().returncode, 0)


if __name__ == "__main__":
    unittest.main()
