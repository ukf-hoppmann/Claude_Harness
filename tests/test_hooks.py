import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS, item, write_backlog


class HookTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.project = base / "project"
        self.data = base / "data"
        self.project.mkdir()
        self.todo_dir = self.project / "docs" / "todo"

    def tearDown(self):
        self._tmp.cleanup()

    def write_config(self, todo=True, path="todo", daily=False):
        config = self.project / ".claude-harness" / "config.toml"
        config.parent.mkdir(exist_ok=True)
        config.write_text(
            'version = 1\n[docs]\nroot = "docs"\n'
            f'[modules]\ntodo = {"true" if todo else "false"}\ndaily = {"true" if daily else "false"}\n'
            f'[todo]\npath = "{path}"\n'
        )

    def run_hook(self, script, payload):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            env=env,
        )

    def edit(self, file_path, session="s1"):
        return self.run_hook(
            "mark_backlog_dirty.py",
            {"session_id": session, "tool_name": "Edit", "tool_input": {"file_path": str(file_path)}},
        )

    def stop(self, session="s1", active=False):
        return self.run_hook("check_backlog.py", {"session_id": session, "stop_hook_active": active})

    def test_session_start_without_config(self):
        result = self.run_hook("session_start.py", {})
        self.assertEqual(result.returncode, 0)
        self.assertIn("/claude-harness:init", result.stdout)

    def test_session_start_reports_missing_backlog(self):
        self.write_config()
        result = self.run_hook("session_start.py", {})
        self.assertIn("does not exist", result.stdout)
        self.assertIn("ask for permission", result.stdout)
        self.assertFalse(self.todo_dir.exists())

    def test_session_start_reports_module_off(self):
        self.write_config(todo=False)
        result = self.run_hook("session_start.py", {})
        self.assertIn("todo=off", result.stdout)
        self.assertNotIn("Backlog", result.stdout)

    def test_session_start_reports_invalid_config(self):
        config = self.project / ".claude-harness" / "config.toml"
        config.parent.mkdir()
        config.write_text("version = 7\n")
        self.assertIn("invalid configuration", self.run_hook("session_start.py", {}).stdout)

    def test_session_start_reports_backlog_errors(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.assertIn("1 errors", self.run_hook("session_start.py", {}).stdout)

    def test_stop_without_backlog_edit_does_nothing(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.edit(self.project / "src" / "main.py")
        self.assertEqual(self.stop().returncode, 0)

    def test_stop_blocks_invalid_backlog_once(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.edit(self.todo_dir / "TODO.md")
        first = self.stop()
        self.assertEqual(first.returncode, 2)
        self.assertIn("Priority must be one of", first.stderr)
        self.assertEqual(self.stop(active=True).returncode, 0)

    def test_stop_clears_marker_when_valid(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.edit(self.todo_dir / "TODO.md")
        self.assertEqual(self.stop().returncode, 2)
        write_backlog(self.todo_dir, [item("STORY-001")])
        self.assertEqual(self.stop().returncode, 0)
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.assertEqual(self.stop().returncode, 0)

    def test_stop_delivers_new_notice_once_per_session(self):
        self.write_config()
        write_backlog(self.todo_dir, [
            item("EPIC-001", Type="Epic", Status="In progress"),
            item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes",
                 Status="Completed", Resolution="Confirmed."),
        ])
        self.edit(self.todo_dir / "TODO.md")
        first = self.stop()
        self.assertEqual(first.returncode, 2)
        self.assertIn("EPIC-001: all required children are Completed", first.stderr)
        self.edit(self.todo_dir / "TODO.md")
        self.assertEqual(self.stop().returncode, 0)
        self.edit(self.todo_dir / "TODO.md", session="s2")
        self.assertEqual(self.stop(session="s2").returncode, 2)

    def test_module_off_skips_check(self):
        self.write_config(todo=False)
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.edit(self.todo_dir / "TODO.md")
        self.assertEqual(self.stop().returncode, 0)

    def test_custom_todo_path(self):
        self.write_config(path="planning")
        planning = self.project / "docs" / "planning"
        write_backlog(planning, [item("STORY-001", Priority="Wrong")])
        self.edit(planning / "TODO.md")
        self.assertEqual(self.stop().returncode, 2)


if __name__ == "__main__":
    unittest.main()
