"""The whole life of a cloud copy in a temporary project, with the real plugin."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import REPO_ROOT, SCRIPTS

CLOUD_EXPORT = SCRIPTS / "cloud_export.py"
PLUGIN_HOOKS = json.loads((REPO_ROOT / "plugin/hooks/hooks.json").read_text(encoding="utf-8"))
CONFIG = 'version = 1\n\n[modules]\ntodo = true\n\n[todo]\nbackend = "files"\n\n[cloud]\nexport = true\n'


def tree(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


class CloudCopyFlowTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        (self.project / ".claude-harness").mkdir()
        (self.project / ".claude-harness/config.toml").write_text(CONFIG, encoding="utf-8")
        (self.project / ".claude").mkdir()
        # A settings file in its own format, with a hook and a setting that must survive everything.
        (self.project / ".claude/settings.json").write_text(
            '{"worktree": { "baseRef": "head" },\n "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo mine"}]}]}}\n',
            encoding="utf-8",
        )
        (self.project / "README.md").write_text("readme\n", encoding="utf-8")
        self.before = tree(self.project)

    def cloud_export(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(CLOUD_EXPORT), str(self.project), *args], capture_output=True, text=True, timeout=60)

    def session_start_locally(self) -> str:
        env = {"PATH": os.environ["PATH"], "HOME": self.tmp.name, "CLAUDE_PROJECT_DIR": str(self.project), "CLAUDE_PLUGIN_DATA": self.tmp.name}
        result = subprocess.run([sys.executable, str(SCRIPTS / "session_start.py")], input="{}", env=env, capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def hook(self, command: str, remote: bool) -> subprocess.CompletedProcess:
        env = {"PATH": os.environ["PATH"], "HOME": self.tmp.name, "CLAUDE_PROJECT_DIR": str(self.project), "CLAUDE_PLUGIN_DATA": self.tmp.name}
        if remote:
            env["CLAUDE_CODE_REMOTE"] = "true"
        return subprocess.run(["sh", "-c", command], input="{}", env=env, cwd=self.project, capture_output=True, text=True, timeout=60)

    def test_create_use_update_and_take_out_again(self):
        # Switched on but not made yet: the local session start says so; the status agrees.
        self.assertIn("status: missing", self.cloud_export("--status").stdout)
        self.assertIn("Cloud copy: cloud.export is on but the project has no copy", self.session_start_locally())

        # Make it.
        written = self.cloud_export("--write")
        self.assertEqual(written.returncode, 0, written.stdout)
        self.assertNotIn("Cloud copy:", self.session_start_locally())
        self.assertIn("status: current", self.cloud_export("--status").stdout)
        self.assertEqual(self.cloud_export().stdout.count("changes: 0"), 1)

        # Own settings survive next to the copy's hooks.
        settings = json.loads((self.project / ".claude/settings.json").read_text(encoding="utf-8"))
        self.assertEqual(settings["worktree"], {"baseRef": "head"})
        self.assertEqual(settings["hooks"]["Stop"][0]["hooks"][0]["command"], "echo mine")
        self.assertTrue(set(PLUGIN_HOOKS["hooks"]) <= set(settings["hooks"]))

        # Every hook of the copy: nothing at all locally, the script in a cloud session.
        for event, groups in settings["hooks"].items():
            for group in groups:
                for hook in group["hooks"]:
                    if "runtime/scripts/" not in hook["command"]:
                        continue
                    with self.subTest(event=event, command=hook["command"][-40:]):
                        local = self.hook(hook["command"], remote=False)
                        self.assertEqual((local.returncode, local.stdout, local.stderr), (0, "", ""))
                        cloud = self.hook(hook["command"], remote=True)
                        self.assertIn(cloud.returncode, (0, 2), cloud.stderr)

        # A session start in the cloud reports the project, and no copy problem.
        start = [h["command"] for g in settings["hooks"]["SessionStart"] for h in g["hooks"] if "runtime/scripts/" in h["command"]][0]
        cloud_start = self.hook(start, remote=True)
        self.assertIn("Claude_Harness: modules todo=on", cloud_start.stdout)
        self.assertNotIn("Cloud copy:", cloud_start.stdout)

        # A hand-edited skill is noticed, and the removal leaves it alone.
        skill = self.project / ".claude/skills/harness-todo/SKILL.md"
        skill.write_text("mine\n", encoding="utf-8")
        self.assertIn("status: outdated", self.cloud_export("--status").stdout)
        removed = self.cloud_export("--remove", "--write")
        self.assertEqual(removed.returncode, 0, removed.stdout)
        self.assertIn("kept .claude/skills/harness-todo/SKILL.md (edited)", removed.stdout)
        self.assertEqual(skill.read_text(encoding="utf-8"), "mine\n")
        skill.unlink()

        # Back to where it started, byte for byte.
        self.assertEqual(tree(self.project), self.before)
        self.assertIn("Cloud copy: cloud.export is on but the project has no copy", self.session_start_locally())


if __name__ == "__main__":
    unittest.main()
