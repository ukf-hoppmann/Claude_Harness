import tempfile
import unittest
from pathlib import Path

from helpers import REPO_ROOT, item, write_backlog
from backlog import validate_backlog


class BacklogTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name) / "todo"

    def tearDown(self):
        self._tmp.cleanup()

    def check(self, todo_items, archive_items=None):
        write_backlog(self.dir, todo_items, archive_items)
        return validate_backlog(self.dir)

    def assertError(self, report, fragment):
        self.assertTrue(
            any(fragment in e for e in report.errors),
            f"expected error containing {fragment!r}, got {report.errors}",
        )

    def test_valid_hierarchy(self):
        report = self.check([
            item("EPIC-001", Type="Epic", Status="In progress"),
            item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes", Status="In progress"),
            item("TASK-001", Type="Task", Parent="`STORY-001`", Required_for_parent="No"),
        ])
        self.assertEqual(report.errors, [])
        self.assertEqual(len(report.items), 3)

    def test_empty_backlog_and_templates(self):
        self.assertTrue(self.check([], []).ok)
        self.assertTrue(validate_backlog(REPO_ROOT / "plugin/templates/todo").ok)

    def test_missing_todo_file(self):
        self.assertError(validate_backlog(self.dir), "TODO.md not found")

    def test_missing_required_field(self):
        self.assertError(self.check([item("STORY-001", Goal=None)]), "missing required fields: Goal")

    def test_invalid_priority(self):
        self.assertError(self.check([item("STORY-001", Priority="Wichtig")]), "Priority must be one of")

    def test_notes_require_summary_and_existing_file(self):
        report = self.check([item("STORY-001", Notes="`items/STORY-001/STORY-001_notes.md`")])
        self.assertError(report, "file does not exist")
        self.assertError(report, "requires Summary")

    def test_notes_with_summary_and_file(self):
        notes = self.dir / "items" / "STORY-001" / "STORY-001_notes.md"
        notes.parent.mkdir(parents=True)
        notes.write_text("# Notes\n")
        report = self.check([item(
            "STORY-001",
            Summary="Kurz.",
            Notes="`items/STORY-001/STORY-001_notes.md`",
        )])
        self.assertEqual(report.errors, [])

    def test_notes_path_must_stay_inside(self):
        report = self.check([item("STORY-001", Summary="x", Notes="`../secret.md`")])
        self.assertError(report, "must stay inside")

    def test_duplicate_id_across_files(self):
        closed = item("STORY-001", Status="Completed", Resolution="Confirmed.")
        report = self.check([item("STORY-001")], [closed])
        self.assertError(report, "defined twice")

    def test_active_item_in_archive(self):
        self.assertError(self.check([], [item("STORY-001")]), "must be Completed or Rejected")

    def test_closed_item_in_todo_is_notice(self):
        report = self.check([item("STORY-001", Status="Completed", Resolution="Confirmed.")])
        self.assertTrue(report.ok)
        self.assertTrue(any("move it to archive.md" in n for n in report.notices))

    def test_references_across_files(self):
        report = self.check(
            [item("STORY-002", Dependencies="`STORY-001`")],
            [item("STORY-001", Status="Completed", Resolution="Confirmed.")],
        )
        self.assertEqual(report.errors, [])

    def test_missing_reference(self):
        self.assertError(self.check([item("STORY-001", Dependencies="`STORY-099`")]), "missing dependency")

    def test_dependency_cycle(self):
        report = self.check([
            item("STORY-001", Dependencies="`STORY-002`"),
            item("STORY-002", Dependencies="`STORY-001`"),
        ])
        self.assertError(report, "dependency cycle")

    def test_story_cannot_have_story_parent(self):
        report = self.check([
            item("STORY-001"),
            item("STORY-002", Parent="`STORY-001`", Required_for_parent="Yes"),
        ])
        self.assertError(report, "cannot use Story STORY-001 as Parent")

    def test_epic_in_progress_needs_required_child(self):
        self.assertError(
            self.check([item("EPIC-001", Type="Epic", Status="In progress")]),
            "requires at least one required child",
        )

    def test_completed_parent_with_open_required_child(self):
        report = self.check([
            item("EPIC-001", Type="Epic", Status="Completed", Resolution="Confirmed."),
            item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes"),
        ])
        self.assertError(report, "cannot be Completed")

    def test_completed_parent_with_active_optional_child(self):
        report = self.check([
            item("EPIC-001", Type="Epic", Status="Completed", Resolution="Confirmed."),
            item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes",
                 Status="Completed", Resolution="Confirmed."),
            item("STORY-002", Parent="`EPIC-001`", Required_for_parent="No"),
        ])
        self.assertError(report, "children are still active: STORY-002")

    def test_completed_parent_with_closed_children(self):
        report = self.check([
            item("EPIC-001", Type="Epic", Status="Completed", Resolution="Confirmed."),
            item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes",
                 Status="Completed", Resolution="Confirmed."),
            item("STORY-002", Parent="`EPIC-001`", Required_for_parent="No",
                 Status="Rejected", Resolution="Rejected."),
        ])
        self.assertEqual(report.errors, [])

    def test_ready_parent_notice(self):
        report = self.check(
            [
                item("EPIC-001", Type="Epic", Status="In progress"),
                item("STORY-002", Parent="`EPIC-001`", Required_for_parent="No"),
            ],
            [item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes",
                  Status="Completed", Resolution="Confirmed.")],
        )
        self.assertTrue(report.ok)
        ready = [n for n in report.notices if n.startswith("EPIC-001: all required children")]
        self.assertEqual(len(ready), 1)
        self.assertIn("children still active: STORY-002", ready[0])

    def test_no_ready_notice_while_required_child_active(self):
        report = self.check([
            item("EPIC-001", Type="Epic", Status="In progress"),
            item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes", Status="In progress"),
        ])
        self.assertEqual(report.notices, [])

    def rejected_required(self, parent_status, **parent_fields):
        return self.check(
            [item("EPIC-001", Type="Epic", Status=parent_status, **parent_fields)],
            [
                item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes",
                     Status="Completed", Resolution="Confirmed."),
                item("STORY-002", Parent="`EPIC-001`", Required_for_parent="Yes",
                     Status="Rejected", Resolution="Rejected."),
            ],
        )

    def test_rejected_required_child_blocks_with_hint(self):
        for status, extra in (("Awaiting confirmation", {}), ("Completed", {"Resolution": "Confirmed."})):
            with self.subTest(status=status):
                report = self.rejected_required(status, **extra)
                self.assertError(report, "STORY-002 (Rejected)")
                self.assertError(report, "Required for parent: No")
                self.assertFalse(any("children are active" in e for e in report.errors), report.errors)

    def test_rejected_required_child_notice_when_others_are_done(self):
        report = self.rejected_required("In progress")
        self.assertTrue(report.ok)
        self.assertFalse(any("all required children are Completed" in n for n in report.notices))
        notice = [n for n in report.notices if n.startswith("EPIC-001:")]
        self.assertEqual(len(notice), 1)
        self.assertIn("STORY-002 (Rejected)", notice[0])
        self.assertIn("ask the owner", notice[0])

    def test_open_required_child_message_names_status(self):
        report = self.check([
            item("EPIC-001", Type="Epic", Status="Awaiting confirmation"),
            item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes", Status="In progress"),
        ])
        self.assertError(report, "STORY-001 (In progress)")

    def test_index_lists_both_files(self):
        from backlog import format_index
        report = self.check(
            [item("STORY-002", "Neu")],
            [
                item("EPIC-001", "Alt", Type="Epic", Status="Completed", Resolution="Confirmed."),
                item("STORY-001", "Kind", Parent="`EPIC-001`", Required_for_parent="Yes",
                     Status="Completed", Resolution="Confirmed."),
            ],
        )
        self.assertEqual(report.errors, [])
        self.assertEqual(format_index(report).splitlines()[1:], [
            "EPIC-001 | Epic | Completed | Alt | -",
            "STORY-001 | Story | Completed | Kind | EPIC-001",
            "STORY-002 | Story | Open | Neu | -",
        ])

    def test_resolution_only_when_closed(self):
        self.assertError(self.check([item("STORY-001", Resolution="x")]), "must not contain Resolution")
        self.assertError(self.check([item("STORY-001", Status="Rejected")]), "requires Resolution")

    def test_unknown_field(self):
        self.assertError(self.check([item("STORY-001", Owner="me")]), "unknown fields: Owner")

    def test_repository_backlog_is_valid(self):
        report = validate_backlog(REPO_ROOT / "docs" / "todo")
        self.assertEqual(report.errors, [])


if __name__ == "__main__":
    unittest.main()
