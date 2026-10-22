import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from helpers import SCRIPTS  # noqa: F401  (puts plugin/scripts on the path)
import state


class NotesMarksTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        patcher = mock.patch.dict(os.environ, {"CLAUDE_PLUGIN_DATA": self._tmp.name})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self._tmp.cleanup)

    def test_no_file_means_no_marks(self):
        self.assertEqual(state.read_notes_marks("s1"), {})

    def test_marks_round_trip_per_project_and_item(self):
        marks = {
            ("root", "TASK-001"): {"state": "stale", "turns": 3},
            ("Plugins/A", "STORY-002"): {"state": None, "turns": 0},
            ("root", "STORY-003"): {"state": "current", "turns": None},
        }
        state.write_notes_marks("s1", marks)
        self.assertEqual(state.read_notes_marks("s1"), marks)

    def test_sessions_do_not_share_marks(self):
        state.write_notes_marks("s1", {("root", "TASK-001"): {"state": "stale", "turns": None}})
        self.assertEqual(state.read_notes_marks("s2"), {})

    def test_the_file_lives_in_the_data_folder_of_the_hooks(self):
        state.write_notes_marks("s1", {("root", "TASK-001"): {"state": "stale", "turns": None}})
        self.assertEqual(state.notes_marks_file("s1").parent, Path(self._tmp.name))

    def test_a_broken_file_is_read_as_empty(self):
        state.notes_marks_file("s1").write_text("{not json")
        self.assertEqual(state.read_notes_marks("s1"), {})

    def test_entries_of_the_wrong_shape_are_dropped(self):
        state.notes_marks_file("s1").write_text('{"root\\tTASK-001": "stale", "no-tab": {"state": "stale"}, "root\\tTASK-002": {"state": "stale", "turns": 1}}')
        self.assertEqual(state.read_notes_marks("s1"), {("root", "TASK-002"): {"state": "stale", "turns": 1}})

    def test_an_empty_dict_removes_the_file(self):
        state.write_notes_marks("s1", {("root", "TASK-001"): {"state": "stale", "turns": None}})
        state.write_notes_marks("s1", {})
        self.assertFalse(state.notes_marks_file("s1").exists())

    def test_the_session_id_is_made_safe_for_a_file_name(self):
        self.assertEqual(state.notes_marks_file("a/b c").parent, Path(self._tmp.name))


class EditNotesMarksTest(unittest.TestCase):
    """Hooks of parallel tool calls run at the same time; every update must survive (found in the first real run)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        patcher = mock.patch.dict(os.environ, {"CLAUDE_PLUGIN_DATA": self._tmp.name})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self._tmp.cleanup)

    def test_the_changes_are_stored_when_the_block_ends(self):
        with state.edit_notes_marks("s1") as marks:
            marks[("root", "TASK-001")] = {"state": "stale", "turns": None}
        with state.edit_notes_marks("s1") as marks:
            marks[("root", "TASK-001")]["turns"] = 0
        self.assertEqual(state.read_notes_marks("s1"), {("root", "TASK-001"): {"state": "stale", "turns": 0}})

    def test_an_error_in_the_block_stores_nothing(self):
        state.write_notes_marks("s1", {("root", "TASK-001"): {"state": "stale", "turns": None}})
        with self.assertRaises(RuntimeError):
            with state.edit_notes_marks("s1") as marks:
                marks.clear()
                raise RuntimeError
        self.assertEqual(state.read_notes_marks("s1"), {("root", "TASK-001"): {"state": "stale", "turns": None}})

    def test_emptying_the_marks_removes_the_file(self):
        state.write_notes_marks("s1", {("root", "TASK-001"): {"state": "stale", "turns": None}})
        with state.edit_notes_marks("s1") as marks:
            marks.clear()
        self.assertFalse(state.notes_marks_file("s1").exists())

    def test_writing_leaves_no_temporary_files(self):
        state.write_notes_marks("s1", {("root", "TASK-001"): {"state": "stale", "turns": None}})
        self.assertEqual(sorted(p.name for p in Path(self._tmp.name).iterdir() if p.suffix != ".lock"), ["notes-marks-s1.json"])

    def test_parallel_processes_lose_no_update(self):
        code = (
            "import sys, time; sys.path.insert(0, sys.argv[1]); import state; "
            "i = sys.argv[2]\n"
            "with state.edit_notes_marks('s1') as marks:\n"
            "    time.sleep(0.02)\n"
            "    marks[('root', 'TASK-' + i)] = {'state': 'stale', 'turns': None}\n"
        )
        env = dict(os.environ, CLAUDE_PLUGIN_DATA=self._tmp.name)
        procs = [subprocess.Popen([sys.executable, "-c", code, str(SCRIPTS), str(n)], env=env) for n in range(12)]
        for proc in procs:
            self.assertEqual(proc.wait(), 0)
        self.assertEqual(sorted(i for _, i in state.read_notes_marks("s1")), sorted(f"TASK-{n}" for n in range(12)))


if __name__ == "__main__":
    unittest.main()
