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


class RemindNotesTest(NotesHookTest):
    def prompt(self, session="s1"):
        return self.run_hook("remind_notes.py", {"session_id": session, "hook_event_name": "UserPromptSubmit", "prompt": "weiter"})

    def prompts(self, count):
        return [self.prompt() for _ in range(count)]

    def test_the_reminder_comes_with_the_fifth_prompt_and_then_every_fifth(self):
        self.set_marks({("root", "TASK-002"): {"state": None, "turns": 0}})
        results = self.prompts(10)
        reminded = [i + 1 for i, r in enumerate(results) if r.stdout]
        self.assertEqual(reminded, [5, 10])
        self.assertIn("TASK-002", results[4].stdout)
        self.assertIn("5 turns", results[4].stdout)
        self.assertIn("10 turns", results[9].stdout)

    def test_the_reminder_never_blocks_and_writes_nothing_to_stderr(self):
        self.set_marks({("root", "TASK-002"): {"state": None, "turns": 4}})
        result = self.prompt()
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertTrue(result.stdout)

    def test_an_item_that_is_not_active_is_never_counted(self):
        self.set_marks({("root", "STORY-001"): {"state": "current", "turns": None}})
        self.assertEqual([r.stdout for r in self.prompts(6)], [""] * 6)
        self.assertEqual(self.marks(), {("root", "STORY-001"): {"state": "current", "turns": None}})

    def test_a_notes_entry_starts_counting_again(self):
        self.bash_done(f"{HELPER} doc TASK-002 TASK-002_spec.md", "[harness] active TASK-002\n")
        self.prompts(4)
        self.bash_done(f"{HELPER} note TASK-002", "[harness] notes-state TASK-002 current\n")
        self.assertEqual([r.stdout for r in self.prompts(4)], [""] * 4)
        self.assertTrue(self.prompt().stdout)

    def test_several_active_items_get_one_message(self):
        self.set_marks({("root", "TASK-002"): {"state": None, "turns": 4}, ("root", "TASK-003"): {"state": None, "turns": 4},
                        ("root", "TASK-004"): {"state": None, "turns": 1}})
        out = self.prompt().stdout
        self.assertIn("TASK-002", out)
        self.assertIn("TASK-003", out)
        self.assertNotIn("TASK-004", out)

    def test_a_subproject_is_named_by_its_item_only_when_it_is_not_the_root(self):
        self.write_subproject()
        self.set_marks({("Sub", "TASK-002"): {"state": None, "turns": 4}})
        self.assertIn("TASK-002 (Sub) (5 turns)", self.prompt().stdout)

    def test_a_switched_off_module_and_other_sessions_get_nothing(self):
        self.set_marks({("root", "TASK-002"): {"state": None, "turns": 4}})
        self.assertEqual(self.prompt(session="other").stdout, "")
        self.write_config(todo=False)
        self.assertEqual(self.prompt().stdout, "")

    def test_bad_input_does_nothing(self):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        for text in ("", "not json", "[]", '{"prompt": "x"}'):
            with self.subTest(text):
                result = subprocess.run([sys.executable, str(SCRIPTS / "remind_notes.py")], input=text,
                                        capture_output=True, text=True, env=env)
                self.assertEqual((result.returncode, result.stdout), (0, ""))


class FilesModeActiveItemTest(NotesHookTest):
    """With the files backend the marks come from file access: reading a spec, changing the notes."""

    def setUp(self):
        super().setUp()
        self.write_config(backend="files")
        self.items = self.project / "docs" / "todo" / "items"

    def read_file(self, path, session="s1"):
        return self.run_hook("mark_active_item.py", {"session_id": session, "tool_name": "Read", "tool_input": {"file_path": str(path)}})

    def edit_file(self, path, session="s1"):
        return self.run_hook("mark_backlog_dirty.py", {"session_id": session, "tool_name": "Edit", "tool_input": {"file_path": str(path)}})

    def test_reading_the_spec_makes_the_item_active(self):
        self.assertEqual(self.read_file(self.items / "TASK-002" / "TASK-002_spec.md").returncode, 0)
        self.assertEqual(self.marks(), {("root", "TASK-002"): {"state": None, "turns": 0}})

    def test_reading_the_spec_again_does_not_restart_the_counter(self):
        self.set_marks({("root", "TASK-002"): {"state": None, "turns": 3}})
        self.read_file(self.items / "TASK-002" / "TASK-002_spec.md")
        self.assertEqual(self.marks(), {("root", "TASK-002"): {"state": None, "turns": 3}})

    def test_other_files_do_not_activate_anything(self):
        for path in (self.items / "TASK-002" / "TASK-002_notes.md", self.items / "TASK-002" / "TASK-002_spec_topic.md",
                     self.items / "TASK-002" / "other.md", self.project / "docs" / "todo" / "TODO.md",
                     self.project / "README.md", self.items / "TASK-003" / "TASK-002_spec.md"):
            with self.subTest(path.name):
                self.read_file(path)
        self.assertEqual(self.marks(), {})

    def test_the_api_backend_and_a_switched_off_module_are_ignored(self):
        self.write_config(backend="api")
        self.read_file(self.items / "TASK-002" / "TASK-002_spec.md")
        self.write_config(todo=False)
        self.read_file(self.items / "TASK-002" / "TASK-002_spec.md")
        self.assertEqual(self.marks(), {})

    def test_changing_the_notes_of_an_active_item_restarts_the_counter(self):
        self.set_marks({("root", "TASK-002"): {"state": None, "turns": 4}})
        self.edit_file(self.items / "TASK-002" / "TASK-002_notes.md")
        self.assertEqual(self.marks(), {("root", "TASK-002"): {"state": None, "turns": 0}})

    def test_changing_notes_of_an_item_that_is_not_active_marks_nothing(self):
        self.edit_file(self.items / "TASK-002" / "TASK-002_notes.md")
        self.assertEqual(self.marks(), {})

    def test_the_reminder_runs_on_the_marks_of_the_files_backend_too(self):
        self.read_file(self.items / "TASK-002" / "TASK-002_spec.md")
        out = [self.run_hook("remind_notes.py", {"session_id": "s1", "prompt": "x"}).stdout for _ in range(5)]
        self.assertEqual([bool(o) for o in out], [False, False, False, False, True])


class RegistrationTest(unittest.TestCase):
    def test_the_hooks_are_registered_for_their_events(self):
        hooks = json.loads((SCRIPTS.parent / "hooks" / "hooks.json").read_text())["hooks"]

        def registered(event, matcher=None):
            return sorted(
                Path(h["command"].split("/")[-1].rstrip('"')).name
                for group in hooks[event] if group.get("matcher") == matcher
                for h in group["hooks"]
            )

        self.assertIn("mark_notes_state.py", registered("PostToolUse", "Bash"))
        self.assertIn("mark_active_item.py", registered("PostToolUse", "Read"))
        self.assertIn("check_notes_state.py", registered("Stop"))
        self.assertEqual(registered("UserPromptSubmit"), ["remind_notes.py"])

    def test_every_registered_script_exists(self):
        hooks = json.loads((SCRIPTS.parent / "hooks" / "hooks.json").read_text())["hooks"]
        for groups in hooks.values():
            for group in groups:
                for hook in group["hooks"]:
                    name = hook["command"].split("/scripts/")[1].rstrip('"')
                    self.assertTrue((SCRIPTS / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
