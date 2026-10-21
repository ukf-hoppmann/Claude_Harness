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

    def test_notes_and_spec_fields_are_unknown(self):
        report = self.check([item(
            "STORY-001", Summary="Kurz.",
            Notes="`items/STORY-001/STORY-001_notes.md`", Spec="`items/STORY-001/STORY-001_spec.md`",
        )])
        self.assertError(report, "STORY-001 has unknown fields: Notes, Spec")

    def test_format_line_is_required(self):
        self.dir.mkdir(parents=True)
        (self.dir / "TODO.md").write_text("# Backlog\n\n## Work items\n\nNo entries.\n")
        self.assertError(validate_backlog(self.dir), "TODO.md has no format line")

    def test_format_version_1_is_rejected(self):
        self.dir.mkdir(parents=True)
        (self.dir / "TODO.md").write_text(
            "# Backlog\n\nFormat: Claude_Harness backlog format version 1. The rules are\n"
            "defined elsewhere.\n\n## Work items\n\nNo entries.\n"
        )
        self.assertError(validate_backlog(self.dir), "TODO.md uses an unsupported backlog format")

    def test_format_line_may_span_lines(self):
        self.dir.mkdir(parents=True)
        (self.dir / "TODO.md").write_text(
            "# Backlog\n\nFormat: Claude_Harness backlog\nformat version 2. The rules are elsewhere.\n"
            "\n## Work items\n\nNo entries.\n"
        )
        self.assertEqual(validate_backlog(self.dir).errors, [])

    def test_archive_needs_format_version_2(self):
        write_backlog(self.dir, [])
        (self.dir / "archive.md").write_text("# Archive\n\n## Work items\n\nNo entries.\n")
        self.assertError(validate_backlog(self.dir), "archive.md has no format line")

    def test_uid_is_required(self):
        self.assertError(self.check([item("STORY-001", Uid=None)]), "STORY-001 is missing required field: Uid")

    def test_uid_must_be_a_uuid(self):
        self.assertError(self.check([item("STORY-001", Uid="1234.")]), "STORY-001 Uid must be a UUID")

    def test_uid_is_unique_across_files(self):
        uid = "3f0c2a9e-6b1d-4c57-9a8e-2d4b7c1e5f60."
        report = self.check(
            [item("STORY-001", Uid=uid)],
            [item("STORY-002", Status="Completed", Resolution="Confirmed.", Uid=uid)],
        )
        self.assertError(report, "STORY-002 uses the Uid of STORY-001")

    def test_uid_is_stored(self):
        report = self.check([item("STORY-001", Uid="3F0C2A9E-6B1D-4C57-9A8E-2D4B7C1E5F60.")])
        self.assertEqual(report.errors, [])
        self.assertEqual(report.items[0].uid, "3f0c2a9e-6b1d-4c57-9a8e-2d4b7c1e5f60")

    def test_placeholder_without_uid_and_created(self):
        report = self.check([
            item("EPIC-001", Type="Epic"),
            item("NEW-login-dialog", Type="Story", Parent="`EPIC-001`", Required_for_parent="Yes",
                 Created=None),
            item("NEW-2fa", Type="Task", Parent="`NEW-login-dialog`", Required_for_parent="No",
                 Dependencies="`STORY-001`"),
            item("STORY-001", Dependencies="None"),
            item("STORY-002", Dependencies="`NEW-2fa`"),
        ])
        self.assertEqual(report.errors, [])
        placeholder = next(i for i in report.items if i.identifier == "NEW-login-dialog")
        self.assertIsNone(placeholder.uid)
        self.assertIsNone(placeholder.created)

    def test_placeholder_must_not_have_uid(self):
        report = self.check([item("NEW-login", Uid="3f0c2a9e-6b1d-4c57-9a8e-2d4b7c1e5f60.")])
        self.assertError(report, "NEW-login is a new entry and must not contain Uid")

    def test_placeholder_name_rules(self):
        report = self.check([item("NEW-Login_Dialog")])
        self.assertError(report, "invalid placeholder: NEW-Login_Dialog")

    def test_placeholder_is_unique(self):
        self.assertError(self.check([item("NEW-login"), item("NEW-login")]), "NEW-login is defined twice")

    def test_reference_to_missing_placeholder(self):
        self.assertError(
            self.check([item("STORY-001", Dependencies="`NEW-gibts-nicht`")]),
            "references missing dependency: NEW-gibts-nicht",
        )

    def test_show_placeholder(self):
        from backlog import main
        write_backlog(self.dir, [item("NEW-login")])
        self.assertEqual(main(["backlog.py", str(self.dir), "--show", "NEW-login"]), 0)

    def test_duplicate_id_across_files(self):
        closed = item("STORY-001", Status="Completed", Resolution="Confirmed.")
        report = self.check([item("STORY-001")], [closed])
        self.assertError(report, "defined twice")

    def test_active_item_in_archive_is_notice(self):
        # Format 2: the file an entry is in carries no information; the ToDo-Viewer moves it.
        report = self.check([], [item("STORY-001")])
        self.assertTrue(report.ok)
        self.assertTrue(any("STORY-001 is Open; move it to TODO.md" in n for n in report.notices))

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
            "EPIC-001 | Epic | Completed | Test | Alt | -",
            "STORY-001 | Story | Completed | Test | Kind | EPIC-001",
            "STORY-002 | Story | Open | Test | Neu | -",
        ])

    def test_resolution_only_when_closed(self):
        self.assertError(self.check([item("STORY-001", Resolution="x")]), "must not contain Resolution")
        self.assertError(self.check([item("STORY-001", Status="Rejected")]), "requires Resolution")

    def test_unknown_field(self):
        self.assertError(self.check([item("STORY-001", Owner="me")]), "unknown fields: Owner")

    def test_only_english_empty_marker(self):
        self.dir.mkdir(parents=True)
        (self.dir / "TODO.md").write_text("# Backlog\n\n## Work items\n\nKeine Einträge.\n")
        self.assertError(validate_backlog(self.dir), "invalid backlog content: Keine Einträge.")

    def test_deleted_item_in_archive_keeps_active_status(self):
        report = self.check([], [item("STORY-001", Status="In progress", Deleted="2026-09-28.")])
        self.assertEqual(report.errors, [])
        self.assertEqual(report.items[0].deleted.isoformat(), "2026-09-28")

    def test_deleted_item_in_todo_is_notice(self):
        report = self.check([item("STORY-001", Deleted="2026-09-28.")], [])
        self.assertTrue(report.ok)
        self.assertTrue(any("STORY-001 is Deleted; move it to archive.md" in n for n in report.notices))

    def test_deleted_requires_date(self):
        self.assertError(
            self.check([], [item("STORY-001", Deleted="gestern")]), "STORY-001 Deleted must use YYYY-MM-DD"
        )

    def test_deleted_children_do_not_count_for_parent_rules(self):
        report = self.check(
            [item("EPIC-001", Type="Epic", Status="In progress")],
            [item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes", Deleted="2026-09-28.")],
        )
        self.assertError(report, "EPIC-001 Epic with Status In progress requires at least one required child")
        report = self.check(
            [],
            [
                item("EPIC-001", Type="Epic", Status="Completed", Resolution="Confirmed."),
                item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes",
                     Status="Completed", Resolution="Confirmed."),
                item("STORY-002", Parent="`EPIC-001`", Required_for_parent="No", Deleted="2026-09-28."),
            ],
        )
        self.assertEqual(report.errors, [])

    def test_deleted_parent_is_not_checked(self):
        report = self.check([], [
            item("EPIC-001", Type="Epic", Status="In progress", Deleted="2026-09-28."),
            item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes", Deleted="2026-09-28."),
        ])
        self.assertEqual(report.errors, [])

    def test_index_marks_deleted_items(self):
        from backlog import format_index
        report = self.check([], [item("STORY-001", "Weg", Deleted="2026-09-28.")])
        self.assertEqual(format_index(report).splitlines()[1:], [
            "STORY-001 | Story | Open (deleted 2026-09-28) | Test | Weg | -",
        ])

    def test_unknown_parent(self):
        self.assertError(
            self.check([item("STORY-001", Parent="`EPIC-099`", Required_for_parent="Yes")]),
            "references missing parent: EPIC-099",
        )

    def test_empty_epic_may_be_rejected(self):
        report = self.check([], [item("EPIC-001", Type="Epic", Status="Rejected", Resolution="Abgelehnt.")])
        self.assertEqual(report.errors, [])

    def test_show_item_from_todo(self):
        from backlog import show_items
        write_backlog(self.dir, [item("STORY-001", "Eins"), item("STORY-002", "Zwei")])
        output, missing = show_items(self.dir, ["STORY-001"])
        self.assertEqual(missing, [])
        self.assertEqual(output.splitlines()[:2], ["Source: TODO.md", "- `STORY-001` **Eins**"])
        self.assertIn("  - Type: Story", output.splitlines())
        self.assertNotIn("STORY-002", output)

    def test_show_archived_item_with_continuation_lines(self):
        from backlog import show_items
        archived = item(
            "STORY-003", "Alt", Status="Completed",
            Goal="Erste Zeile\n    zweite Zeile.", Resolution="Confirmed.",
        )
        write_backlog(self.dir, [item("STORY-001")], [archived, item("STORY-004", Status="Rejected",
                                                                     Resolution="Abgelehnt.")])
        output, missing = show_items(self.dir, ["STORY-003"])
        self.assertEqual(missing, [])
        self.assertEqual(output.splitlines(), [
            "Source: archive.md",
            *archived.rstrip("\n").splitlines(),
        ])

    def test_show_several_items_in_requested_order(self):
        from backlog import show_items
        write_backlog(self.dir, [item("STORY-001", "Eins")],
                      [item("STORY-002", "Zwei", Status="Completed", Resolution="Confirmed.")])
        output, missing = show_items(self.dir, ["STORY-002", "STORY-001"])
        self.assertEqual(missing, [])
        blocks = output.split("\n\n")
        self.assertEqual([b.splitlines()[:2] for b in blocks], [
            ["Source: archive.md", "- `STORY-002` **Zwei**"],
            ["Source: TODO.md", "- `STORY-001` **Eins**"],
        ])

    def test_show_missing_item(self):
        from backlog import main
        write_backlog(self.dir, [item("STORY-001")], [])
        self.assertEqual(main(["backlog.py", str(self.dir), "--show", "STORY-001"]), 0)
        self.assertEqual(main(["backlog.py", str(self.dir), "--show", "STORY-001", "STORY-099"]), 1)

    def test_show_usage_errors(self):
        from backlog import main
        write_backlog(self.dir, [item("STORY-001")])
        self.assertEqual(main(["backlog.py", str(self.dir), "--show"]), 2)
        self.assertEqual(main(["backlog.py", str(self.dir), "--show", "kein-id"]), 2)
        self.assertEqual(main(["backlog.py", str(self.dir), "--index", "--show", "STORY-001"]), 2)

    def write_notes(self, identifier, text):
        path = self.dir / "items" / identifier / f"{identifier}_notes.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def test_confirm_state(self):
        import contextlib
        import io

        from backlog import main
        from notes_head import CURRENT, state_of
        write_backlog(self.dir, [item("STORY-001")])
        path = self.write_notes(
            "STORY-001",
            "# STORY-001 — Title\n\n## State\n\n- Goal/Status: g\n\n## 2026-10-01 — Topic\n\n### Decided\n\n- a\n",
        )
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(["backlog.py", str(self.dir), "--confirm-state", "STORY-001"]), 0)
        self.assertEqual(state_of(path.read_text()), CURRENT)
        self.assertRegex(out.getvalue(), r"^confirmed STORY-001: 2026-10-01 — Topic \([0-9a-f]{12}\)\n$")

    def test_confirm_state_errors(self):
        import contextlib
        import io

        from backlog import USAGE, main
        self.assertIn("--confirm-state", USAGE)
        write_backlog(self.dir, [item("STORY-001")])
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["backlog.py", str(self.dir), "--confirm-state", "STORY-001"]), 1)
            self.write_notes("STORY-001", "# STORY-001 — Title\n\n## 2026-10-01 — Topic\n\n- a\n")
            self.assertEqual(main(["backlog.py", str(self.dir), "--confirm-state", "STORY-001"]), 1)
            self.assertEqual(main(["backlog.py", str(self.dir), "--confirm-state", "kein-id"]), 2)
            self.assertEqual(main(["backlog.py", str(self.dir), "--confirm-state"]), 2)

    def test_repository_backlog_is_valid(self):
        report = validate_backlog(REPO_ROOT / "docs" / "todo")
        self.assertEqual(report.errors, [])


if __name__ == "__main__":
    unittest.main()
