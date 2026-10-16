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


if __name__ == "__main__":
    unittest.main()
