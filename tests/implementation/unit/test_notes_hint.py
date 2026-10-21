import unittest

import notes_hint


class ChildInProgressHintTest(unittest.TestCase):
    def test_names_children_in_progress(self):
        hint = notes_hint.child_in_progress_hint("STORY-001", "Story", ["TASK-002", "TASK-003"])
        self.assertIn("TASK-002, TASK-003 are in progress", hint)
        self.assertIn("STORY-001", hint)

    def test_single_child_uses_singular(self):
        self.assertIn("TASK-002 is in progress", notes_hint.child_in_progress_hint("EPIC-001", "Epic", ["TASK-002"]))

    def test_no_hint_without_children_in_progress(self):
        self.assertIsNone(notes_hint.child_in_progress_hint("STORY-001", "Story", []))

    def test_no_hint_for_tasks(self):
        self.assertIsNone(notes_hint.child_in_progress_hint("TASK-001", "Task", ["TASK-002"]))
