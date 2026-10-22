"""Hooks for the notes head and the notes reminder in the API backend (TASK-024).

The helper backlog_api.py prints `[harness]` lines on stderr; the PostToolUse hook mark_notes_state.py reads them from the
Bash answer and stores the marks; check_notes_state.py (Stop) and remind_notes.py (UserPromptSubmit) use them.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from helpers import SCRIPTS
import state

HELPER = f'python3 "/plugins/claude-harness/scripts/backlog_api.py"'


class NotesHookTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.project = base / "project"
        self.data = base / "data"
        self.project.mkdir()
        self.addCleanup(self._tmp.cleanup)
        self.write_config()

    def write_config(self, todo=True, backend="api", root=None):
        config = (root or self.project) / ".claude-harness" / "config.toml"
        config.parent.mkdir(parents=True, exist_ok=True)
        extra = '[projects]\nSub = "Plugins/Sub"\n' if root is None else ""
        config.write_text(
            f'version = 1\n[docs]\nroot = "docs"\n[modules]\ntodo = {"true" if todo else "false"}\n'
            f'[todo]\nbackend = "{backend}"\n{extra}'
        )

    def write_subproject(self, backend="api"):
        sub = self.project / "Plugins" / "Sub"
        self.write_config(root=sub, backend=backend)

    def run_hook(self, script, payload, extra_env=None):
        env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CODE_REMOTE", "CLAUDE_HARNESS_TODO_BACKEND")}
        env.update(CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data), **(extra_env or {}))
        return subprocess.run([sys.executable, str(SCRIPTS / script)], input=json.dumps(payload),
                              capture_output=True, text=True, env=env)

    def bash_done(self, command, stderr="", stdout="", session="s1"):
        """The PostToolUse hook after a successful Bash call."""
        response = {"stdout": stdout, "stderr": stderr, "interrupted": False, "isImage": False}
        return self.run_hook("mark_notes_state.py", {
            "session_id": session, "hook_event_name": "PostToolUse", "tool_name": "Bash",
            "tool_input": {"command": command}, "tool_response": response,
        })

    def marks(self, session="s1"):
        with mock.patch.dict(os.environ, {"CLAUDE_PLUGIN_DATA": str(self.data)}):
            return state.read_notes_marks(session)

    def set_marks(self, marks, session="s1"):
        with mock.patch.dict(os.environ, {"CLAUDE_PLUGIN_DATA": str(self.data)}):
            state.write_notes_marks(session, marks)


class MarkNotesStateTest(NotesHookTest):
    def test_a_notes_write_marks_the_state_of_the_head(self):
        for reported in ("current", "stale", "missing"):
            with self.subTest(reported):
                result = self.bash_done(f"{HELPER} note STORY-001 <<'EOF'\n{{}}\nEOF", f"[harness] notes-state STORY-001 {reported}\n")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.marks(), {("root", "STORY-001"): {"state": reported, "turns": None}})

    def test_an_active_item_starts_its_counter(self):
        self.bash_done(f"{HELPER} update TASK-002 1", "[harness] active TASK-002\n")
        self.assertEqual(self.marks(), {("root", "TASK-002"): {"state": None, "turns": 0}})

    def test_both_lines_for_one_item_are_kept_together(self):
        self.bash_done(f"{HELPER} doc TASK-002 TASK-002_spec.md", "[harness] active TASK-002\n")
        self.bash_done(f"{HELPER} note TASK-002", "[harness] notes-state TASK-002 stale\n")
        self.assertEqual(self.marks(), {("root", "TASK-002"): {"state": "stale", "turns": 0}})

    def test_a_notes_write_resets_the_counter_of_an_active_item(self):
        self.set_marks({("root", "TASK-002"): {"state": None, "turns": 4}})
        self.bash_done(f"{HELPER} note TASK-002", "[harness] notes-state TASK-002 current\n")
        self.assertEqual(self.marks(), {("root", "TASK-002"): {"state": "current", "turns": 0}})

    def test_becoming_active_again_does_not_reset_a_running_counter(self):
        self.set_marks({("root", "TASK-002"): {"state": "current", "turns": 3}})
        self.bash_done(f"{HELPER} doc TASK-002 TASK-002_spec.md", "[harness] active TASK-002\n")
        self.assertEqual(self.marks(), {("root", "TASK-002"): {"state": "current", "turns": 3}})

    def test_the_lines_may_stand_in_stdout_too(self):
        self.bash_done(f"{HELPER} note STORY-001", stdout="{}\n[harness] notes-state STORY-001 stale\n")
        self.assertEqual(self.marks(), {("root", "STORY-001"): {"state": "stale", "turns": None}})

    def test_the_project_option_names_the_project(self):
        self.write_subproject()
        self.bash_done(f"{HELPER} --project Sub note STORY-001", "[harness] notes-state STORY-001 stale\n")
        self.assertEqual(self.marks(), {("Sub", "STORY-001"): {"state": "stale", "turns": None}})

    def test_an_unknown_project_is_ignored(self):
        self.bash_done(f"{HELPER} --project Nope note STORY-001", "[harness] notes-state STORY-001 stale\n")
        self.assertEqual(self.marks(), {})

    def test_another_projects_backlog_is_ignored(self):
        self.bash_done(f"{HELPER} --source Misc note STORY-001", "[harness] notes-state STORY-001 stale\n")
        self.assertEqual(self.marks(), {})

    def test_other_commands_are_ignored(self):
        self.bash_done("echo '[harness] notes-state STORY-001 stale'", "[harness] notes-state STORY-001 stale\n")
        self.bash_done(f"{HELPER} state STORY-001", "")
        self.assertEqual(self.marks(), {})

    def test_other_tools_are_ignored(self):
        payload = {"session_id": "s1", "tool_name": "Edit", "tool_input": {"file_path": "x"},
                   "tool_response": {"stderr": "[harness] notes-state STORY-001 stale"}}
        self.assertEqual(self.run_hook("mark_notes_state.py", payload).returncode, 0)
        self.assertEqual(self.marks(), {})

    def test_the_files_backend_and_a_switched_off_module_are_ignored(self):
        self.write_config(backend="files")
        self.bash_done(f"{HELPER} note STORY-001", "[harness] notes-state STORY-001 stale\n")
        self.write_config(todo=False)
        self.bash_done(f"{HELPER} note STORY-001", "[harness] notes-state STORY-001 stale\n")
        self.assertEqual(self.marks(), {})

    def test_marks_belong_to_the_session(self):
        self.bash_done(f"{HELPER} note STORY-001", "[harness] notes-state STORY-001 stale\n", session="s1")
        self.assertEqual(self.marks("s2"), {})

    def test_bad_input_does_nothing(self):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        for text in ("", "not json", "[]", '{"session_id": "s1"}'):
            with self.subTest(text):
                result = subprocess.run([sys.executable, str(SCRIPTS / "mark_notes_state.py")], input=text,
                                        capture_output=True, text=True, env=env)
                self.assertEqual(result.returncode, 0)
        self.assertEqual(self.marks(), {})

    def test_a_tool_response_as_plain_text_is_read(self):
        payload = {"session_id": "s1", "tool_name": "Bash", "tool_input": {"command": f"{HELPER} note STORY-001"},
                   "tool_response": "{}\n[harness] notes-state STORY-001 stale\n"}
        self.assertEqual(self.run_hook("mark_notes_state.py", payload).returncode, 0)
        self.assertEqual(self.marks(), {("root", "STORY-001"): {"state": "stale", "turns": None}})


class CheckNotesStateTest(NotesHookTest):
    def stop(self, active=False, session="s1"):
        return self.run_hook("check_notes_state.py", {"session_id": session, "stop_hook_active": active})

    def test_a_stale_or_missing_head_blocks_the_end_of_the_turn(self):
        for reported in ("stale", "missing"):
            with self.subTest(reported):
                self.set_marks({("root", "STORY-001"): {"state": reported, "turns": None}})
                result = self.stop()
                self.assertEqual(result.returncode, 2)
                self.assertIn("STORY-001", result.stderr)
                self.assertIn(reported, result.stderr)
                self.assertIn("put-state", result.stderr)
                self.assertIn("confirm-state", result.stderr)
                self.assertIn("format.md", result.stderr)

    def test_a_current_head_and_an_item_only_known_as_active_do_not_block(self):
        self.set_marks({("root", "STORY-001"): {"state": "current", "turns": None},
                        ("root", "TASK-002"): {"state": None, "turns": 0}})
        result = self.stop()
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_no_marks_do_not_block(self):
        self.assertEqual(self.stop().returncode, 0)

    def test_the_hook_does_not_block_again_while_it_is_already_continuing(self):
        self.set_marks({("root", "STORY-001"): {"state": "stale", "turns": None}})
        self.assertEqual(self.stop(active=True).returncode, 0)

    def test_confirming_releases_the_block(self):
        self.bash_done(f"{HELPER} note STORY-001", "[harness] notes-state STORY-001 stale\n")
        self.assertEqual(self.stop().returncode, 2)
        self.assertEqual(self.stop().returncode, 2)
        self.bash_done(f"{HELPER} confirm-state STORY-001 4", "[harness] notes-state STORY-001 current\n")
        self.assertEqual(self.stop().returncode, 0)

    def test_every_stale_item_is_named_and_a_subproject_gets_its_option(self):
        self.write_subproject()
        self.set_marks({("root", "STORY-001"): {"state": "stale", "turns": None},
                        ("Sub", "TASK-005"): {"state": "missing", "turns": None}})
        result = self.stop()
        self.assertEqual(result.returncode, 2)
        self.assertIn("STORY-001", result.stderr)
        self.assertIn("--project Sub", result.stderr)
        self.assertIn("TASK-005", result.stderr)

    def test_the_files_backend_a_switched_off_module_and_other_sessions_are_left_alone(self):
        self.set_marks({("root", "STORY-001"): {"state": "stale", "turns": None}})
        self.assertEqual(self.stop(session="other").returncode, 0)
        self.write_config(backend="files")
        self.assertEqual(self.stop().returncode, 0)
        self.write_config(todo=False)
        self.assertEqual(self.stop().returncode, 0)

    def test_bad_input_does_not_block(self):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        for text in ("", "not json", "[]", '{"stop_hook_active": false}'):
            with self.subTest(text):
                result = subprocess.run([sys.executable, str(SCRIPTS / "check_notes_state.py")], input=text,
                                        capture_output=True, text=True, env=env)
                self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
