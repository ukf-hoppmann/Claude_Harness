import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from helpers import REPO_ROOT
from cloud_export import RUNTIME_DIR, hook_entries

PLUGIN = REPO_ROOT / "plugin"
PLUGIN_HOOKS = json.loads((PLUGIN / "hooks/hooks.json").read_text(encoding="utf-8"))
CONFIG = 'version = 1\n\n[modules]\ntodo = true\n\n[todo]\nbackend = "files"\n'


def command_of(event: str) -> str:
    return hook_entries(PLUGIN_HOOKS)[event][0]["hooks"][0]["command"]


class CloudHookCommandTest(unittest.TestCase):
    """The exported hook commands, run through a shell in a project that holds a copy of the scripts."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        scripts = self.project / RUNTIME_DIR.as_posix() / "scripts"
        shutil.copytree(PLUGIN / "scripts", scripts, ignore=shutil.ignore_patterns("__pycache__"))
        (self.project / ".claude-harness/config.toml").write_text(CONFIG, encoding="utf-8")
        self.scripts = scripts

    def run_command(self, command: str, remote: bool, project_dir: bool = True):
        env = {"PATH": os.environ["PATH"], "HOME": self.tmp.name}
        if remote:
            env["CLAUDE_CODE_REMOTE"] = "true"
        if project_dir:
            env["CLAUDE_PROJECT_DIR"] = str(self.project)
        return subprocess.run(
            ["sh", "-c", command], input="{}", env=env, cwd=self.project, capture_output=True, text=True, timeout=30
        )

    def test_in_a_cloud_session_the_session_start_hook_runs(self):
        result = self.run_command(command_of("SessionStart"), remote=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Claude_Harness: modules todo=on", result.stdout)

    def test_without_the_cloud_variable_nothing_runs(self):
        result = self.run_command(command_of("SessionStart"), remote=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_a_variable_other_than_true_does_not_count(self):
        env = {"PATH": os.environ["PATH"], "HOME": self.tmp.name, "CLAUDE_CODE_REMOTE": "false"}
        result = subprocess.run(
            ["sh", "-c", command_of("SessionStart")], input="{}", env=env, cwd=self.project, capture_output=True, text=True
        )
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_without_the_project_dir_variable_the_working_directory_is_used(self):
        result = self.run_command(command_of("SessionStart"), remote=True, project_dir=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Claude_Harness: modules todo=on", result.stdout)

    def test_the_exit_code_of_a_blocking_hook_comes_through(self):
        (self.scripts / "check_architecture.py").write_text("import sys\nsys.exit(2)\n", encoding="utf-8")
        blocked = self.run_command(command_of("PreToolUse"), remote=True)
        self.assertEqual(blocked.returncode, 2)
        local = self.run_command(command_of("PreToolUse"), remote=False)
        self.assertEqual(local.returncode, 0)


GIT_ENV = {
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.invalid",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
}


class CloudSessionStartSyncTest(unittest.TestCase):
    """End to end: the exported SessionStart hook brings a stale cloud clone up to date before it reports."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.env = {"PATH": os.environ["PATH"], "HOME": self.tmp.name, **GIT_ENV}
        origin, self.upstream, self.clone = base / "origin.git", base / "upstream", base / "clone"
        self.git(base, "init", "-q", "--bare", str(origin))
        self.git(base, "init", "-q", str(self.upstream))
        shutil.copytree(
            PLUGIN / "scripts", self.upstream / RUNTIME_DIR.as_posix() / "scripts",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        self.write_config(self.upstream, "todo = true")
        self.git(self.upstream, "add", "-A")
        self.git(self.upstream, "commit", "-q", "-m", "copy")
        self.git(self.upstream, "remote", "add", "origin", str(origin))
        self.git(self.upstream, "push", "-q", "origin", "main")
        self.git(base, "clone", "-q", str(origin), str(self.clone))

    def git(self, cwd, *args):
        subprocess.run(["git", "-c", "init.defaultBranch=main", *args], cwd=cwd, env=self.env, check=True,
                       capture_output=True, text=True)

    @staticmethod
    def write_config(project: Path, modules: str):
        path = project / ".claude-harness/config.toml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'version = 1\n\n[modules]\n{modules}\n\n[todo]\nbackend = "files"\n', encoding="utf-8")

    def session_start(self, source: str):
        env = {**self.env, "CLAUDE_CODE_REMOTE": "true", "CLAUDE_PROJECT_DIR": str(self.clone)}
        return subprocess.run(
            ["sh", "-c", command_of("SessionStart")], input=json.dumps({"source": source, "cwd": str(self.clone)}),
            env=env, cwd=self.clone, capture_output=True, text=True, timeout=30,
        )

    def test_startup_fast_forwards_and_reports_the_new_state(self):
        self.write_config(self.upstream, "todo = true\ndaily = true")
        self.git(self.upstream, "commit", "-q", "-am", "daily on")
        self.git(self.upstream, "push", "-q", "origin", "main")
        result = self.session_start("startup")
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        self.assertIn("Git: fast-forwarded main", lines[0])
        self.assertIn("daily=on", lines[1])

    def test_resume_does_not_sync(self):
        self.write_config(self.upstream, "todo = true\ndaily = true")
        self.git(self.upstream, "commit", "-q", "-am", "daily on")
        self.git(self.upstream, "push", "-q", "origin", "main")
        result = self.session_start("resume")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Git:", result.stdout)
        self.assertNotIn("daily=on", result.stdout)


if __name__ == "__main__":
    unittest.main()
