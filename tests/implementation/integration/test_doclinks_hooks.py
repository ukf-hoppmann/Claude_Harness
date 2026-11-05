import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS


class DoclinksHooksTest(unittest.TestCase):
    CONFIG = 'version = 1\n[docs]\nroot = "docs"\n[modules]\ntechdocs = true\ndevelopment = true\n'

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name).resolve()
        self.project = base / "project"
        self.data = base / "data"
        self.project.mkdir()
        self.write(".claude-harness/config.toml", self.CONFIG)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text=""):
        path = self.project / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def run_hook(self, script, payload, root=None):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(root or self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        env.pop("CLAUDE_CODE_REMOTE", None)
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script)], input=json.dumps(payload), capture_output=True, text=True, env=env
        )

    def edit(self, rel, session="s1", root=None):
        path = (root or self.project) / rel
        return self.run_hook(
            "mark_doclinks.py", {"session_id": session, "tool_input": {"file_path": str(path)}}, root
        )

    def stop(self, session="s1", active=False, root=None):
        return self.run_hook("check_doclinks.py", {"session_id": session, "stop_hook_active": active}, root)

    def start(self):
        return self.run_hook("session_start.py", {"session_id": "s1", "source": "startup"}).stdout


class SessionStartTest(DoclinksHooksTest):
    def test_silent_without_dead_links(self):
        self.write("README.md", "[a](docs/techdocs/a.md)\n")
        self.write("docs/techdocs/a.md", "# A\n")
        self.assertNotIn("Dead links", self.start())

    def test_reports_count_and_limited_list(self):
        self.write("README.md", "".join(f"[x](gone{i}.md)\n" for i in range(7)))
        out = self.start()
        self.assertIn("Dead links in docs: 7", out)
        self.assertIn("- README.md:1: gone0.md: target does not exist", out)
        self.assertIn("- … 2 more", out)

    def test_development_docs_are_checked(self):
        self.write("docs/development/architecture.md", "[x](interfaces/nope.md#a)\n")
        self.assertIn("Dead links in docs: 1", self.start())

    def test_modules_off(self):
        self.write(".claude-harness/config.toml", "version = 1\n")
        self.write("README.md", "[x](gone.md)\n")
        self.assertNotIn("Dead links", self.start())

    def test_subproject_names_project_and_folder(self):
        self.write(".claude-harness/config.toml", self.CONFIG + '[projects]\nsub = "sub"\n')
        self.write("sub/.claude-harness/config.toml", self.CONFIG)
        self.write("sub/README.md", "[x](gone.md)\n")
        out = self.start()
        self.assertIn("sub: Dead links in docs: 1", out)
        self.assertIn("sub/README.md:1: gone.md: target does not exist", out)


class StopHookTest(DoclinksHooksTest):
    def test_dead_link_in_changed_doc_blocks(self):
        self.write("docs/techdocs/a.md", "[x](gone.md)\n")
        self.assertEqual(self.edit("docs/techdocs/a.md").returncode, 0)
        result = self.stop()
        self.assertEqual(result.returncode, 2)
        self.assertIn("docs/techdocs/a.md:1: gone.md: target does not exist", result.stderr)

    def test_reported_again_until_fixed_then_silent(self):
        self.write("docs/techdocs/a.md", "[x](gone.md)\n")
        self.edit("docs/techdocs/a.md")
        self.assertEqual(self.stop().returncode, 2)
        self.assertEqual(self.stop().returncode, 2)
        self.write("docs/techdocs/a.md", "[x](b.md)\n")
        self.write("docs/techdocs/b.md")
        self.assertEqual(self.stop().returncode, 0)
        self.assertEqual(self.stop().stderr, "")

    def test_list_is_cleared_after_success(self):
        self.write("docs/techdocs/a.md", "ok\n")
        self.edit("docs/techdocs/a.md")
        self.assertEqual(self.stop().returncode, 0)
        self.write("docs/techdocs/a.md", "[x](gone.md)\n")  # changed without the marker hook
        self.assertEqual(self.stop().returncode, 0)

    def test_stop_hook_active_is_silent(self):
        self.write("README.md", "[x](gone.md)\n")
        self.edit("README.md")
        self.assertEqual(self.stop(active=True).returncode, 0)
        self.assertEqual(self.stop().returncode, 2)

    def test_only_changed_docs_are_checked(self):
        self.write("docs/techdocs/old.md", "[x](gone.md)\n")
        self.write("docs/techdocs/new.md", "ok\n")
        self.edit("docs/techdocs/new.md")
        self.assertEqual(self.stop().returncode, 0)

    def test_other_files_and_sessions_are_not_marked(self):
        self.write("src/code.md", "[x](gone.md)\n")
        self.write("docs/todo/x.md", "[x](gone.md)\n")
        self.edit("src/code.md")
        self.edit("docs/todo/x.md")
        self.assertEqual(self.stop().returncode, 0)
        self.write("README.md", "[x](gone.md)\n")
        self.edit("README.md", session="other")
        self.assertEqual(self.stop(session="s1").returncode, 0)

    def test_deleted_doc_is_silent(self):
        self.write("README.md", "[x](gone.md)\n")
        self.edit("README.md")
        (self.project / "README.md").unlink()
        self.assertEqual(self.stop().returncode, 0)

    def test_module_off(self):
        self.write("README.md", "[x](gone.md)\n")
        self.edit("README.md")
        self.write(".claude-harness/config.toml", "version = 1\n")
        result = self.stop()
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_marker_ignores_modules_off(self):
        self.write(".claude-harness/config.toml", "version = 1\n")
        self.write("README.md", "[x](gone.md)\n")
        self.edit("README.md")
        self.write(".claude-harness/config.toml", self.CONFIG)
        self.assertEqual(self.stop().returncode, 0)

    def test_subproject_message_names_folder(self):
        self.write(".claude-harness/config.toml", self.CONFIG + '[projects]\nsub = "sub"\n')
        self.write("sub/.claude-harness/config.toml", self.CONFIG)
        self.write("sub/docs/techdocs/a.md", "[x](gone.md)\n")
        self.edit("sub/docs/techdocs/a.md")
        result = self.stop()
        self.assertEqual(result.returncode, 2)
        self.assertIn("sub/docs/techdocs/a.md:1: gone.md", result.stderr)

    def test_invalid_input_and_config(self):
        self.assertEqual(self.run_hook("check_doclinks.py", {}).returncode, 0)
        self.write(".claude-harness/config.toml", "version = [\n")
        self.assertEqual(self.stop().returncode, 0)
        self.assertEqual(self.edit("README.md").returncode, 0)


if __name__ == "__main__":
    unittest.main()
