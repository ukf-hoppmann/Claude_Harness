"""Integrationstest fuer human-scripts/branch_cleanup.py (echte Git-Repos, lokale Remotes)."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.helpers import REPO_ROOT

SCRIPT = REPO_ROOT / "human-scripts" / "branch_cleanup.py"
ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
       "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t", "GIT_CONFIG_GLOBAL": "/dev/null"}


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, env=ENV, capture_output=True, text=True, check=True).stdout.strip()


class BranchCleanupTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        self.a, self.b, self.w = t / "a.git", t / "b.git", t / "work"
        for r in (self.a, self.b):
            git(t, "init", "--bare", "-b", "main", str(r))
        git(t, "init", "-b", "main", str(self.w))
        git(self.w, "remote", "add", "origin", str(self.a))
        git(self.w, "remote", "set-url", "--push", "origin", str(self.a))
        git(self.w, "remote", "set-url", "--add", "--push", "origin", str(self.b))
        self.commit("base")
        git(self.w, "push", "origin", "main")
        git(self.w, "remote", "set-head", "origin", "main")

    def tearDown(self):
        self.tmp.cleanup()

    def commit(self, msg):
        (self.w / "f.txt").write_text(msg + os.urandom(4).hex())
        git(self.w, "add", "-A")
        git(self.w, "commit", "-m", msg)

    def branch(self, name, merged):
        git(self.w, "checkout", "-b", name, "main")
        self.commit(name)
        git(self.w, "push", "origin", name)
        git(self.w, "checkout", "main")
        if merged:
            git(self.w, "merge", "--no-ff", "-m", "m", name)
            git(self.w, "push", "origin", "main")

    def run_script(self, cwd=None, *args):
        return subprocess.run(["python3", "-I", str(SCRIPT), *args],
                              cwd=cwd or self.w, env=ENV, capture_output=True, text=True)

    @staticmethod
    def single_cmds(out):
        """Einzelbefehle, ohne den Sammelabschnitt."""
        return [l for l in out.split("Alle auf einmal")[0].splitlines() if l.startswith("git push")]

    def test_merged_unmerged_protected(self):
        self.branch("claude/done", merged=True)
        self.branch("claude/open", merged=False)
        git(self.w, "push", "origin", "main:master")  # geschuetzt trotz Muster
        p = self.run_script(self.w / ".git" / "..", "--pattern", "*")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = p.stdout
        cmds = self.single_cmds(out)
        self.assertEqual(len(cmds), 2)  # beide Push-Ziele, nur claude/done
        self.assertTrue(all(":refs/heads/claude/done" in c for c in cmds))
        self.assertIn(str(self.a), cmds[0] + cmds[1])
        self.assertIn(str(self.b), cmds[0] + cmds[1])
        self.assertRegex(out, r"claude/open\s+NOT MERGED")
        self.assertRegex(out, r"master\s+PROTECTED")
        self.assertRegex(out, r"main\s+PROTECTED")
        self.assertNotIn(":refs/heads/main", out)
        self.assertNotIn(":refs/heads/master", out)

    def test_never_deletes_and_commands_work(self):
        self.branch("claude/done", merged=True)
        before = git(self.w, "ls-remote", "--heads", str(self.a))
        p = self.run_script()
        self.assertEqual(git(self.w, "ls-remote", "--heads", str(self.a)), before)
        for c in self.single_cmds(p.stdout):
            subprocess.run(c, shell=True, cwd=self.w, env=ENV, check=True, capture_output=True)
        self.assertNotIn("claude/done", git(self.w, "ls-remote", "--heads", str(self.a)))
        self.assertNotIn("claude/done", git(self.w, "ls-remote", "--heads", str(self.b)))

    def test_all_in_one_command_per_target(self):
        self.branch("claude/one", merged=True)
        self.branch("claude/two", merged=True)
        p = self.run_script()
        marker = p.stdout.index("Alle auf einmal")
        cmds = [l for l in p.stdout[marker:].splitlines() if l.startswith("git push")]
        self.assertEqual(len(cmds), 2)
        for c in cmds:
            subprocess.run(c, shell=True, cwd=self.w, env=ENV, check=True, capture_output=True)
        for r in (self.a, self.b):
            heads = git(self.w, "ls-remote", "--heads", str(r))
            self.assertNotIn("claude/", heads)

    def test_lease_blocks_changed_branch(self):
        self.branch("claude/done", merged=True)
        p = self.run_script()
        cmds = self.single_cmds(p.stdout)
        git(self.w, "checkout", "claude/done")
        self.commit("late")
        git(self.w, "push", "origin", "claude/done")
        git(self.w, "checkout", "main")
        r = subprocess.run(cmds[0], shell=True, cwd=self.w, env=ENV, capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)

    def test_other_target_differs_gives_no_command_there(self):
        self.branch("claude/done", merged=True)
        git(self.w, "push", str(self.b), "--delete", "claude/done")
        git(self.w, "checkout", "-b", "tmp", "main")
        self.commit("other")
        git(self.w, "push", str(self.b), "tmp:claude/done")
        git(self.w, "checkout", "main")
        p = self.run_script()
        cmds = self.single_cmds(p.stdout)
        self.assertEqual(len(cmds), 1)
        self.assertIn(str(self.a), cmds[0])
        self.assertIn("anderem Commit", p.stdout)

    def test_current_branch_protected(self):
        self.branch("claude/done", merged=True)
        git(self.w, "checkout", "claude/done")
        p = self.run_script()
        self.assertRegex(p.stdout, r"claude/done\s+PROTECTED")
        self.assertNotIn("git push", p.stdout)

    def write_config(self, body):
        d = self.w / ".claude-harness"
        d.mkdir(exist_ok=True)
        (d / "config.toml").write_text("version = 1\n" + body)

    def test_config_from_project_harness_toml(self):
        self.branch("claude/done", merged=True)
        self.branch("codex/done", merged=True)
        self.write_config('[branch_cleanup]\ncoding_patterns = ["codex/*"]\nprotected = ["codex/keep"]\n')
        out = self.run_script().stdout
        self.assertIn(":refs/heads/codex/done", out)
        self.assertNotIn("claude/done", out)
        self.write_config('[branch_cleanup]\ncoding_patterns = ["codex/*"]\nprotected = ["codex/*"]\n')
        self.assertNotIn("git push", self.run_script().stdout)

    def test_invalid_config_fails(self):
        self.write_config('[branch_cleanup]\ncoding_patterns = []\n')
        p = self.run_script()
        self.assertEqual(p.returncode, 2)
        self.assertIn("coding_patterns", p.stderr)

    def test_outside_repo_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.run_script(d)
        self.assertEqual(p.returncode, 2)
        self.assertIn("Nicht in einem Git-Repository", p.stderr)


if __name__ == "__main__":
    unittest.main()
