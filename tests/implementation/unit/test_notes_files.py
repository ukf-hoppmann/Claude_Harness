import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from helpers import REPO_ROOT
import notes_files
from cloud_export import runtime_files, skill_files

BACKLOG = REPO_ROOT / "tests" / "fixtures" / "notes-files"
HEADER = "File | Status | Review | Topic | Summary"
DUE_HEADER = "File | Status | Reason | Review | Topic | Summary"


def run(*args: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = notes_files.main(["notes_files.py", *args])
    return code, out.getvalue(), err.getvalue()


class IndexTest(unittest.TestCase):
    def test_lists_notes_with_head_fields_sorted_by_file_name(self):
        code, out, _ = run(str(BACKLOG), "--index")
        self.assertEqual(code, 0)
        self.assertEqual(
            out.splitlines(),
            [
                HEADER,
                "NOTE-001.md | waiting | 2026-11-07T08:00:00Z | Performance | Check the performance when the database fills up",
                "NOTE-002.md | snoozed | 2027-01-01T08:00:00Z | Sprint 12 \\| Release | Ask the team about the release date",
                "NOTE-005.md | done | 2026-01-01T08:00:00Z | - | Finished long ago, review date is past",
                "new-idee.md | waiting | - | Ideen | An idea written in the cloud",
            ],
        )

    def test_leaves_out_trash_archive_documents_and_topics(self):
        _, out, _ = run(str(BACKLOG), "--index")
        for name in ("NOTE-003", "NOTE-004", "NOTE-001_notes", "topics"):
            self.assertNotIn(name, out)

    def test_index_is_the_default(self):
        self.assertEqual(run(str(BACKLOG)), run(str(BACKLOG), "--index"))

    def test_missing_notes_folder_gives_empty_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run(tmp, "--index"), (0, "", ""))

    def test_unreadable_note_is_reported_and_the_rest_listed(self):
        with tempfile.TemporaryDirectory() as tmp:
            notes = Path(tmp) / "notes"
            notes.mkdir()
            (notes / "NOTE-001.md").write_bytes(b"# NOTE-001\nSummary: ok\nStatus: waiting\n")
            (notes / "NOTE-002.md").write_bytes(b"\xff\xfe not text")
            code, out, err = run(tmp)
        self.assertEqual(code, 1)
        self.assertIn("NOTE-001.md | waiting | - | - | ok", out)
        self.assertIn("NOTE-002.md", err)

    def test_missing_summary_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            notes = Path(tmp) / "notes"
            notes.mkdir()
            (notes / "NOTE-001.md").write_text("# NOTE-001\nStatus: waiting\n")
            code, _, err = run(tmp)
        self.assertEqual(code, 1)
        self.assertIn("NOTE-001.md: no Summary line", err)


class DueTest(unittest.TestCase):
    def test_topic_date_makes_a_snoozed_note_due(self):
        code, out, _ = run(str(BACKLOG), "--due", "--today", "2026-10-22")
        self.assertEqual(code, 0)
        self.assertEqual(
            out.splitlines(),
            [
                DUE_HEADER,
                "NOTE-002.md | snoozed | topic due 2026-10-10 | 2027-01-01T08:00:00Z | Sprint 12 \\| Release | Ask the team about the release date",
            ],
        )

    def test_review_date_on_the_day_counts(self):
        _, out, _ = run(str(BACKLOG), "--due", "--today", "2026-11-07")
        self.assertIn("NOTE-001.md | waiting | review 2026-11-07 |", out)

    def test_both_reasons_are_named_and_finished_notes_never_are_due(self):
        _, out, _ = run(str(BACKLOG), "--due", "--today", "2027-02-01")
        self.assertIn("NOTE-002.md | snoozed | review 2027-01-01, topic due 2026-10-10 |", out)
        self.assertIn("new-idee.md | waiting | topic due 2026-12-01 |", out)
        self.assertNotIn("NOTE-005", out)

    def test_nothing_due_prints_nothing(self):
        self.assertEqual(run(str(BACKLOG), "--due", "--today", "2026-01-01"), (0, "", ""))

    def test_today_defaults_to_the_current_date(self):
        # The fixtures are all in the past or near future; with the real date the old topic date is always due.
        _, out, _ = run(str(BACKLOG), "--due")
        self.assertIn("NOTE-002.md", out)


class CheckTest(unittest.TestCase):
    FORMAT = REPO_ROOT / "tests" / "fixtures" / "notes-format"

    def test_valid_notes_have_no_findings(self):
        self.assertEqual(run(str(self.FORMAT / "valid"), "--check"), (0, "", ""))

    def test_an_error_is_printed_with_file_line_and_code_and_fails(self):
        code, out, _ = run(str(self.FORMAT / "invalid" / "unknown_trigger"), "--check")
        self.assertEqual(code, 1)
        self.assertRegex(out, r"^notes/NOTE-001\.md:15: unknown_trigger: .+\n$")

    def test_notices_are_printed_but_do_not_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            notes = Path(tmp) / "notes"
            notes.mkdir()
            (notes / "readme.md").write_text("x\n")
            code, out, _ = run(tmp, "--check")
        self.assertEqual(code, 0)
        self.assertRegex(out, r"^notes/readme\.md:1: ignored_file: ")

    def test_errors_come_before_notices(self):
        with tempfile.TemporaryDirectory() as tmp:
            notes = Path(tmp) / "notes"
            notes.mkdir()
            (notes / "NOTE-001.md").write_text("# NOTE-002\n")
            (notes / "readme.md").write_text("x\n")
            _, out, _ = run(tmp, "--check")
        self.assertEqual([line.split(": ")[1] for line in out.splitlines()], ["file_label_mismatch", "ignored_file"])

    def test_no_notes_folder_is_not_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run(tmp, "--check"), (0, "", ""))

    def test_new_notes_with_capital_letters_are_listed_and_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            notes = Path(tmp) / "notes"
            notes.mkdir()
            (notes / "new-Idee.md").write_text("# NEW\nSummary: s\nStatus: waiting\n")
            _, index, _ = run(tmp, "--index")
            code, out, _ = run(tmp, "--check")
        self.assertIn("new-Idee.md | waiting | - | - | s", index)
        self.assertEqual(code, 1)
        self.assertIn("invalid_placeholder", out)


class CloudCopyTest(unittest.TestCase):
    def test_the_cloud_copy_carries_the_helper_and_the_rules_with_a_working_path(self):
        plugin = REPO_ROOT / "plugin"
        self.assertIn(".claude-harness/runtime/scripts/notes_files.py", runtime_files(plugin))
        rules = skill_files(plugin)[".claude/skills/harness-todo/notes-files.md"].decode("utf-8")
        self.assertIn(".claude-harness/runtime/scripts/notes_files.py", rules)
        self.assertNotIn("CLAUDE_PLUGIN_ROOT", rules)


class SyncFlowTest(unittest.TestCase):
    SKILL = REPO_ROOT / "plugin" / "skills" / "todo"

    def test_the_flow_rules_reach_the_cloud_copy(self):
        self.assertIn(".claude/skills/harness-todo/sync-flow.md", skill_files(REPO_ROOT / "plugin"))

    def test_the_skill_files_point_to_the_flow_rules(self):
        for name in ("SKILL.md", "notes.md", "notes-files.md"):
            with self.subTest(name):
                self.assertIn("(sync-flow.md)", (self.SKILL / name).read_text(encoding="utf-8"))

    def test_notes_are_not_called_database_only_without_naming_the_mirror(self):
        text = (self.SKILL / "notes.md").read_text(encoding="utf-8")
        self.assertNotIn("there are no note files, so nothing is committed", text)
        self.assertIn("mirror", text)


class UsageTest(unittest.TestCase):
    def test_wrong_calls_exit_2(self):
        for args in ([], ["a", "b"], [str(BACKLOG), "--bogus"], [str(BACKLOG), "--today", "x"],
                     [str(BACKLOG), "--due", "--today", "22.10.2026"], [str(BACKLOG), "--index", "--due"],
                     [str(BACKLOG), "--check", "--index"], [str(BACKLOG), "--check", "--due"],
                     [str(BACKLOG), "--check", "--today", "2026-01-01"]):
            with self.subTest(args=args):
                code, _, err = run(*args)
                self.assertEqual(code, 2)
                self.assertIn("usage:", err)


if __name__ == "__main__":
    unittest.main()
