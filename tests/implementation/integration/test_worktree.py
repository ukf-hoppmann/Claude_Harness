import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS
from worktree import base_ref_setting


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def write_settings(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data if isinstance(data, str) else json.dumps(data))


class BaseRefSettingTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.root = base / "project"
        self.home = base / "home"
        self.root.mkdir()
        self.home.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def test_unset(self):
        self.assertIsNone(base_ref_setting(self.root, self.home))

    def test_precedence(self):
        write_settings(self.home / ".claude/settings.json", {"worktree": {"baseRef": "fresh"}})
        self.assertEqual(base_ref_setting(self.root, self.home), "fresh")
        write_settings(self.root / ".claude/settings.json", {"worktree": {"baseRef": "head"}})
        self.assertEqual(base_ref_setting(self.root, self.home), "head")
        write_settings(self.root / ".claude/settings.local.json", {"worktree": {"baseRef": "fresh"}})
        self.assertEqual(base_ref_setting(self.root, self.home), "fresh")

    def test_file_without_value_falls_through(self):
        write_settings(self.root / ".claude/settings.local.json", {"permissions": {}})
        write_settings(self.root / ".claude/settings.json", {"worktree": {}})
        write_settings(self.home / ".claude/settings.json", {"worktree": {"baseRef": "head"}})
        self.assertEqual(base_ref_setting(self.root, self.home), "head")

    def test_broken_file_counts_as_unset(self):
        write_settings(self.root / ".claude/settings.json", "{not json")
        write_settings(self.home / ".claude/settings.json", ["list"])
        self.assertIsNone(base_ref_setting(self.root, self.home))
        write_settings(self.root / ".claude/settings.local.json", {"worktree": "head"})
        self.assertIsNone(base_ref_setting(self.root, self.home))


class SessionStartTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name).resolve()
        self.project = base / "project"
        self.home = base / "home"
        self.data = base / "data"
        self.project.mkdir()
        self.home.mkdir()
        git(self.project, "init", "-q")
        self.write_config("")

    def tearDown(self):
        self._tmp.cleanup()

    def write_config(self, development):
        config = self.project / ".claude-harness/config.toml"
        config.parent.mkdir(exist_ok=True)
        config.write_text(f"version = 1\n[modules]\ndevelopment = true\n[development]\narchitecture = false\n{development}")

    def session_start(self):
        env = dict(
            os.environ,
            HOME=str(self.home),
            CLAUDE_PROJECT_DIR=str(self.project),
            CLAUDE_PLUGIN_DATA=str(self.data),
        )
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "session_start.py")],
            input=json.dumps({"session_id": "s1", "source": "startup"}),
            capture_output=True,
            text=True,
            env=env,
        ).stdout

    def test_skill_line_and_missing_base_ref(self):
        out = self.session_start()
        self.assertIn("claude-harness:worktree", out)
        self.assertIn("worktree.baseRef", out)

    def test_head_is_silent(self):
        write_settings(self.project / ".claude/settings.json", {"worktree": {"baseRef": "head"}})
        out = self.session_start()
        self.assertIn("claude-harness:worktree", out)
        self.assertNotIn("worktree.baseRef", out)

    def test_broken_settings_do_not_break_start(self):
        write_settings(self.project / ".claude/settings.json", "{not json")
        out = self.session_start()
        self.assertIn("worktree.baseRef", out)
        self.assertIn("Claude_Harness: modules", out)

    def test_switched_off(self):
        self.write_config("worktree = false\n")
        out = self.session_start()
        self.assertNotIn("claude-harness:worktree", out)
        self.assertNotIn("worktree.baseRef", out)

    def test_no_check_outside_git(self):
        shutil.rmtree(self.project / ".git")
        out = self.session_start()
        self.assertIn("claude-harness:worktree", out)
        self.assertNotIn("worktree.baseRef", out)


class WorktreeScriptTest(unittest.TestCase):
    """worktree.py start/check against a real repository with a linked worktree."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name).resolve()
        self.main = base / "main"
        self.wt = base / "main/.claude/worktrees/feature"
        self.main.mkdir()
        git(self.main, "init", "-q", "-b", "main")
        git(self.main, "config", "user.email", "t@example.com")
        git(self.main, "config", "user.name", "Test")
        (self.main / ".gitignore").write_text(".env\n.venv/\n__pycache__/\n.claude/worktrees/\nlocal/\n*.secret\n")
        (self.main / "app.py").write_text("x = 1\n")
        git(self.main, "add", ".")
        git(self.main, "commit", "-q", "-m", "init")
        git(self.main, "checkout", "-q", "-b", "ansTest")
        git(self.main, "worktree", "add", "-q", "-b", "feature", str(self.wt))

    def tearDown(self):
        self._tmp.cleanup()

    def run_script(self, command, cwd=None):
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "worktree.py"), command],
            cwd=cwd or self.wt,
            capture_output=True,
            text=True,
            env=env,
        )

    @staticmethod
    def fields(result):
        return dict(line.split(": ", 1) for line in result.stdout.splitlines() if ": " in line)

    def test_start_records_base(self):
        result = self.run_script("start")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.fields(result)["base"], "ansTest")
        self.assertEqual(git(self.main, "config", "branch.feature.harnessBase"), "ansTest")

    def test_start_rejects_detached_main(self):
        git(self.main, "checkout", "-q", "--detach")
        result = self.run_script("start")
        self.assertEqual(result.returncode, 1)
        self.assertIn("error:", result.stdout)

    def test_start_rejects_main_checkout(self):
        result = self.run_script("start", cwd=self.main)
        self.assertEqual(result.returncode, 1)
        self.assertIn("error:", result.stdout)

    def test_start_mirrors_ignored_files(self):
        (self.main / ".env").write_text("SECRET=1\n")
        (self.main / ".venv/bin").mkdir(parents=True)
        (self.main / ".venv/bin/python").write_text("")
        (self.main / "__pycache__").mkdir()
        (self.main / "__pycache__/app.pyc").write_text("")
        (self.main / "local/__pycache__").mkdir(parents=True)
        (self.main / "local/settings.json").write_text("{}")
        (self.main / "local/__pycache__/x.pyc").write_text("")
        (self.main / "Größe.secret").write_text("ä")
        (self.main / ".claude/worktrees/other").mkdir(parents=True)
        (self.main / ".claude/worktrees/other/file").write_text("")
        result = self.run_script("start")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.wt / ".env").read_text(), "SECRET=1\n")
        self.assertEqual((self.wt / "local/settings.json").read_text(), "{}")
        self.assertEqual((self.wt / "Größe.secret").read_text(), "ä")
        self.assertTrue((self.wt / ".venv").is_symlink())
        self.assertEqual((self.wt / ".venv").resolve(), (self.main / ".venv").resolve())
        self.assertFalse((self.wt / "__pycache__").exists())
        self.assertFalse((self.wt / "local/__pycache__").exists())
        self.assertFalse((self.wt / ".claude/worktrees").exists())
        fields = self.fields(result)
        self.assertEqual(fields["copied"], "3 files")
        self.assertEqual(fields["linked"], ".venv")
        self.assertEqual(fields["skipped"], "__pycache__, local/__pycache__")

    def test_start_mirrors_ignored_harness_configs_of_subprojects(self):
        with (self.main / ".gitignore").open("a") as gitignore:
            gitignore.write(".claude-harness/\n")
        for folder in (self.main, self.main / "Plugins/A"):
            (folder / ".claude-harness").mkdir(parents=True)
            (folder / ".claude-harness/config.toml").write_text(f"version = 1 # {folder.name}\n")
        result = self.run_script("start")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.wt / ".claude-harness/config.toml").read_text(), "version = 1 # main\n")
        self.assertEqual((self.wt / "Plugins/A/.claude-harness/config.toml").read_text(), "version = 1 # A\n")

    def test_start_keeps_existing_files(self):
        (self.main / ".env").write_text("main\n")
        (self.wt / ".env").write_text("worktree\n")
        result = self.run_script("start")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.wt / ".env").read_text(), "worktree\n")
        fields = self.fields(result)
        self.assertEqual(fields["copied"], "0 files")
        self.assertEqual(fields["linked"], "none")
        self.assertEqual(fields["skipped"], "none")

    def commit_in_worktree(self):
        (self.wt / "feature.py").write_text("y = 2\n")
        git(self.wt, "add", ".")
        git(self.wt, "commit", "-q", "-m", "feature")

    def test_check_clean(self):
        self.run_script("start")
        self.commit_in_worktree()
        (self.wt / ".env").write_text("ignored\n")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.fields(result), {
            "base": "ansTest",
            "main": str(self.main),
            "clean": "yes",
            "base_moved": "no",
            "main_on_base": "yes",
            "merge_in": "main",
        })

    def test_check_dirty_worktree(self):
        self.run_script("start")
        (self.wt / "app.py").write_text("x = 3\n")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.fields(result)["clean"], "no")
        (self.wt / "app.py").write_text("x = 1\n")
        (self.wt / "new.py").write_text("")
        self.assertEqual(self.fields(self.run_script("check"))["clean"], "no")

    def test_check_base_moved(self):
        self.run_script("start")
        self.commit_in_worktree()
        (self.main / "other.py").write_text("")
        git(self.main, "add", ".")
        git(self.main, "commit", "-q", "-m", "other")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.fields(result)["base_moved"], "yes")

    def test_check_main_switched(self):
        self.run_script("start")
        git(self.main, "checkout", "-q", "main")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.fields(result)["main_on_base"], "no")
        self.assertEqual(self.fields(result)["merge_in"], "worktree")

    def test_check_base_checked_out_elsewhere(self):
        self.run_script("start")
        git(self.main, "checkout", "-q", "main")
        git(self.main, "worktree", "add", "-q", str(self.main.parent / "other"), "ansTest")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.fields(result)["merge_in"], "none")

    def test_check_without_start(self):
        result = self.run_script("check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("error:", result.stdout)

    def test_invalid_call(self):
        self.assertEqual(self.run_script("unknown").returncode, 2)


if __name__ == "__main__":
    unittest.main()
