import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import REPO_ROOT, SCRIPTS

SCRIPT = SCRIPTS / "cloud_export.py"
VERSION = json.loads((REPO_ROOT / "plugin/.claude-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
CONFIG = 'version = 1\n\n[modules]\ntodo = true\n\n[todo]\nbackend = "files"\n'


def tree(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


class CliTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        (self.project / ".claude-harness").mkdir()
        (self.project / ".claude-harness/config.toml").write_text(CONFIG, encoding="utf-8")

    def run_cli(self, *args: str, folder: Path | None = None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(folder or self.project), *args], capture_output=True, text=True, timeout=60
        )

    def lines(self, result, prefix: str) -> list[str]:
        return [line for line in result.stdout.splitlines() if line.startswith(prefix)]


class PreviewTest(CliTestCase):
    def test_preview_lists_the_changes_and_writes_nothing(self):
        before = tree(self.project)
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"plugin: {VERSION}", result.stdout)
        self.assertIn("copy: none", result.stdout)
        creates = self.lines(result, "create ")
        self.assertIn("create .claude/settings.json", creates)
        self.assertIn("create .claude/skills/harness-todo/SKILL.md", creates)
        self.assertIn("create .claude-harness/runtime/scripts/cloud_export.py", creates)
        self.assertIn("create .claude-harness/runtime/manifest.json", creates)
        self.assertEqual(self.lines(result, "changes: "), [f"changes: {len(creates)}"])
        self.assertEqual(tree(self.project), before)


class WriteTest(CliTestCase):
    def test_write_creates_the_copy_and_a_second_run_has_nothing_to_do(self):
        first = self.run_cli("--write")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        written = int(re.search(r"^written: (\d+)$", first.stdout, re.MULTILINE).group(1))
        self.assertEqual(written, len(self.lines(first, "create ")))
        self.assertTrue((self.project / ".claude/skills/harness-todo/SKILL.md").is_file())
        second = self.run_cli()
        self.assertIn("copy: " + VERSION, second.stdout)
        self.assertEqual(self.lines(second, "changes: "), ["changes: 0"])

    def test_the_written_session_start_hook_runs_in_a_cloud_session(self):
        self.run_cli("--write")
        settings = json.loads((self.project / ".claude/settings.json").read_text(encoding="utf-8"))
        command = settings["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        env = {"PATH": os.environ["PATH"], "HOME": self.tmp.name, "CLAUDE_CODE_REMOTE": "true", "CLAUDE_PROJECT_DIR": str(self.project)}
        result = subprocess.run(["sh", "-c", command], input="{}", env=env, cwd=self.project, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Claude_Harness: modules todo=on", result.stdout)

    def test_a_copy_edited_by_hand_is_shown_with_a_diff_and_marked(self):
        self.run_cli("--write")
        edited = self.project / ".claude-harness/runtime/scripts/cloud_export.py"
        edited.write_text("# mine\n", encoding="utf-8")
        result = self.run_cli()
        self.assertIn("update .claude-harness/runtime/scripts/cloud_export.py (edited)", result.stdout)
        self.assertIn("--- .claude-harness/runtime/scripts/cloud_export.py", result.stdout)
        self.run_cli("--write")
        self.assertNotEqual(edited.read_text(encoding="utf-8"), "# mine\n")


class StatusTest(CliTestCase):
    def test_status_missing_current_and_outdated(self):
        self.assertIn("status: missing", self.run_cli("--status").stdout)
        self.run_cli("--write")
        self.assertIn("status: current", self.run_cli("--status").stdout)
        (self.project / ".claude/skills/harness-todo/SKILL.md").write_text("changed\n", encoding="utf-8")
        self.assertIn("status: outdated", self.run_cli("--status").stdout)

    def test_status_writes_nothing(self):
        before = tree(self.project)
        self.run_cli("--status")
        self.assertEqual(tree(self.project), before)


class RemoveTest(CliTestCase):
    def test_removal_preview_lists_the_deletions_and_writes_nothing(self):
        self.run_cli("--write")
        before = tree(self.project)
        result = self.run_cli("--remove")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("delete .claude/skills/harness-todo/SKILL.md", result.stdout)
        self.assertIn("delete .claude-harness/runtime/manifest.json", result.stdout)
        self.assertEqual(self.lines(result, "changes: "), [f"changes: {len(self.lines(result, 'delete '))}"])
        self.assertEqual(tree(self.project), before)

    def test_export_then_removal_brings_back_the_project_as_it_was(self):
        (self.project / ".claude").mkdir()
        (self.project / ".claude/settings.json").write_text('{"worktree": { "baseRef": "head" }}\n', encoding="utf-8")
        (self.project / "README.md").write_text("readme\n", encoding="utf-8")
        before = tree(self.project)
        self.run_cli("--write")
        self.assertNotEqual(tree(self.project), before)
        result = self.run_cli("--remove", "--write")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertRegex(result.stdout, r"(?m)^written: \d+$")
        self.assertEqual(tree(self.project), before)

    def test_a_file_edited_by_hand_stays_and_is_listed(self):
        self.run_cli("--write")
        edited = self.project / ".claude/skills/harness-todo/SKILL.md"
        edited.write_text("mine\n", encoding="utf-8")
        result = self.run_cli("--remove", "--write")
        self.assertIn("kept .claude/skills/harness-todo/SKILL.md (edited)", result.stdout)
        self.assertEqual(edited.read_text(encoding="utf-8"), "mine\n")

    def test_without_a_copy_it_is_an_error(self):
        result = self.run_cli("--remove")
        self.assertEqual(result.returncode, 1)
        self.assertIn("error: no copy to remove", result.stdout)

    def test_removal_and_status_do_not_go_together(self):
        self.assertEqual(self.run_cli("--remove", "--status").returncode, 2)


class ErrorTest(CliTestCase):
    def test_a_project_without_a_config_is_refused(self):
        (self.project / ".claude-harness/config.toml").unlink()
        result = self.run_cli("--write")
        self.assertEqual(result.returncode, 1)
        self.assertIn("error:", result.stdout)
        self.assertIn("config.toml", result.stdout)
        self.assertEqual(list(tree(self.project)), [])

    def test_invalid_settings_stop_everything_before_a_file_is_written(self):
        (self.project / ".claude").mkdir()
        (self.project / ".claude/settings.json").write_text("{broken", encoding="utf-8")
        before = tree(self.project)
        result = self.run_cli("--write")
        self.assertEqual(result.returncode, 1)
        self.assertIn("error:", result.stdout)
        self.assertIn("settings.json", result.stdout)
        self.assertEqual(tree(self.project), before)

    def test_usage_errors_exit_with_2(self):
        for args in (["--bogus"], ["--status", "--write"]):
            self.assertEqual(self.run_cli(*args).returncode, 2, args)
        self.assertEqual(subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
