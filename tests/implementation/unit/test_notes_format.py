import json
import tempfile
import unittest
from pathlib import Path

from helpers import REPO_ROOT
from notes_format import Finding, check_notes_folder

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "notes-format"

NOTE = "# NOTE-001\nUid: u-1\nSummary: s\nStatus: waiting\n"
NEW = "# NEW\nSummary: s\nStatus: waiting\n"
TOPIC = "- TOPIC-001 | Name | uid=t-1"


def check(files: dict[str, str | bytes]) -> list[Finding]:
    """The findings for a notes folder holding exactly these files."""
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp) / "notes"
        folder.mkdir()
        for name, content in files.items():
            data = content if isinstance(content, bytes) else content.encode("utf-8")
            (folder / name).write_bytes(data)
        return check_notes_folder(folder)


def errors(files: dict[str, str | bytes]) -> list[Finding]:
    return [f for f in check(files) if f.error]


def notices(files: dict[str, str | bytes]) -> list[Finding]:
    return [f for f in check(files) if not f.error]


class FixtureTest(unittest.TestCase):
    def test_the_viewers_valid_examples_have_no_findings(self):
        self.assertEqual(check_notes_folder(FIXTURES / "valid" / "notes"), [])

    def test_the_viewers_notes_errors_are_found_with_code_file_and_line(self):
        cases = sorted((FIXTURES / "invalid").iterdir())
        self.assertTrue(cases)
        for case in cases:
            with self.subTest(case.name):
                expected = json.loads((case / "expected.json").read_text())
                found = check_notes_folder(case / "notes")
                self.assertEqual([(f.code, f.file, f.line) for f in found], [(expected["code"], expected["file"], expected["line"])])
                self.assertTrue(found[0].error)

    def test_missing_folder_has_no_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(check_notes_folder(Path(tmp) / "notes"), [])

    def test_a_finding_prints_as_file_line_code_and_text(self):
        finding = errors({"NOTE-001.md": NOTE + "Foo: x\n"})[0]
        self.assertEqual(str(finding), f"notes/NOTE-001.md:5: unknown_field: {finding.message}")


class NoteHeadTest(unittest.TestCase):
    def one(self, name: str, text: str) -> tuple[str, str, int]:
        found = errors({name: text})
        self.assertEqual(len(found), 1, found)
        return found[0].code, found[0].file, found[0].line

    def test_a_note_with_every_header_line_is_valid(self):
        text = (
            NOTE + "Topic: TOPIC-001\nReview: 2026-11-07T08:00:00Z\nMode: all\nCreated: 2026-10-01T09:30:00.5Z\n"
            "Updated: 2026-10-12T08:00:00Z\nArchived: true\nDeleted: 2026-10-13T08:00:00Z\n"
            "Triggers:\n- event P:STORY-003 Completed [fired 2026-10-12T08:00:00Z] [already_met]\n- topic_due\n"
            "Links:\n- reference P:STORY-001\n- reference topic:TOPIC-002\n- origin note:NOTE-002\n\nBody\n"
        )
        self.assertEqual(check({"NOTE-001.md": text, "topics.md": TOPIC + "\n"}), [])

    def test_a_new_note_without_uid_is_valid(self):
        self.assertEqual(check({"new-idee.md": NEW + "Topic: new:Ideen\n\nText\n", "topics.md": "- NEW | Ideen\n"}), [])

    def test_unknown_header_line(self):
        self.assertEqual(self.one("NOTE-001.md", NOTE + "Foo: x\n"), ("unknown_field", "notes/NOTE-001.md", 5))

    def test_line_without_colon(self):
        self.assertEqual(self.one("NOTE-001.md", NOTE + "just text\n"), ("invalid_value", "notes/NOTE-001.md", 5))

    def test_header_line_twice(self):
        self.assertEqual(self.one("NOTE-001.md", NOTE + "Summary: again\n"), ("invalid_value", "notes/NOTE-001.md", 5))

    def test_list_line_without_section(self):
        self.assertEqual(self.one("NOTE-001.md", NOTE + "- event P:S-1 Completed\n"), ("invalid_value", "notes/NOTE-001.md", 5))

    def test_section_name_with_text(self):
        self.assertEqual(self.one("NOTE-001.md", NOTE + "Triggers: topic_due\n"), ("invalid_value", "notes/NOTE-001.md", 5))

    def test_the_head_ends_at_the_first_blank_line(self):
        self.assertEqual(errors({"NOTE-001.md": NOTE + "\nFoo: this is the long text\n"}), [])

    def test_missing_summary_status_and_uid(self):
        self.assertEqual(self.one("NOTE-001.md", "# NOTE-001\nUid: u\nStatus: waiting\n"), ("missing_field", "notes/NOTE-001.md", 1))
        self.assertEqual(self.one("NOTE-001.md", "# NOTE-001\nUid: u\nSummary: s\n"), ("missing_field", "notes/NOTE-001.md", 1))
        self.assertEqual(self.one("NOTE-001.md", "# NOTE-001\nSummary: s\nStatus: waiting\n"), ("missing_field", "notes/NOTE-001.md", 1))

    def test_a_new_note_has_no_uid(self):
        self.assertEqual(self.one("new-idee.md", "# NEW\nUid: u\nSummary: s\nStatus: waiting\n"), ("invalid_value", "notes/new-idee.md", 2))

    def test_status_due_is_derived_and_never_in_a_file(self):
        found = errors({"NOTE-001.md": NOTE.replace("waiting", "due")})
        self.assertEqual([(f.code, f.line) for f in found], [("invalid_value", 4)])
        self.assertIn("due", found[0].message)

    def test_unknown_status_mode_and_archived(self):
        self.assertEqual(self.one("NOTE-001.md", NOTE.replace("waiting", "open")), ("invalid_value", "notes/NOTE-001.md", 4))
        self.assertEqual(self.one("NOTE-001.md", NOTE + "Mode: some\n"), ("invalid_value", "notes/NOTE-001.md", 5))
        self.assertEqual(self.one("NOTE-001.md", NOTE + "Archived: yes\n"), ("invalid_value", "notes/NOTE-001.md", 5))

    def test_times_are_utc_with_z(self):
        for key in ("Review", "Created", "Updated", "Deleted"):
            for value in ("2026-11-07", "2026-11-07T08:00:00", "2026-11-07T08:00:00+02:00", "tomorrow"):
                with self.subTest(key=key, value=value):
                    self.assertEqual(self.one("NOTE-001.md", NOTE + f"{key}: {value}\n"), ("invalid_value", "notes/NOTE-001.md", 5))

    def test_empty_times_are_fine(self):
        self.assertEqual(errors({"NOTE-001.md": NOTE + "Review:\nCreated:\nDeleted:\n"}), [])

    def test_first_line_must_match_the_file_name(self):
        self.assertEqual(self.one("NOTE-001.md", NOTE.replace("NOTE-001", "NOTE-002", 1)), ("file_label_mismatch", "notes/NOTE-001.md", 1))
        self.assertEqual(self.one("new-idee.md", NOTE), ("file_label_mismatch", "notes/new-idee.md", 1))
        self.assertEqual(self.one("NOTE-001.md", "\n" + NOTE), ("file_label_mismatch", "notes/NOTE-001.md", 1))

    def test_placeholder_names_use_lowercase_letters_digits_and_hyphens(self):
        for name in ("new-Idee.md", "new--idee.md", "new-idee-.md", "new-ID.md"):
            with self.subTest(name):
                self.assertEqual(self.one(name, NEW), ("invalid_placeholder", f"notes/{name}", 1))

    def test_triggers(self):
        base = NOTE + "Triggers:\n"
        self.assertEqual(self.one("NOTE-001.md", base + "- time 2026-10-12T08:00:00Z\n"), ("unknown_trigger", "notes/NOTE-001.md", 6))
        self.assertEqual(self.one("NOTE-001.md", base + "- cron daily\n"), ("unknown_trigger", "notes/NOTE-001.md", 6))
        self.assertEqual(self.one("NOTE-001.md", base + "- event P:S-1 Done\n"), ("invalid_value", "notes/NOTE-001.md", 6))
        self.assertEqual(self.one("NOTE-001.md", base + "- event\n"), ("invalid_value", "notes/NOTE-001.md", 6))
        self.assertEqual(self.one("NOTE-001.md", base + "- event P:S-1 Completed [bogus]\n"), ("invalid_value", "notes/NOTE-001.md", 6))
        self.assertEqual(self.one("NOTE-001.md", base + "- event P:S-1 Completed [fired soon]\n"), ("invalid_value", "notes/NOTE-001.md", 6))
        self.assertEqual(self.one("NOTE-001.md", base + "- topic_due soon\n"), ("invalid_value", "notes/NOTE-001.md", 6))

    def test_links(self):
        base = NOTE + "Links:\n"
        self.assertEqual(self.one("NOTE-001.md", base + "- blocks P:S-1\n"), ("invalid_value", "notes/NOTE-001.md", 6))
        self.assertEqual(self.one("NOTE-001.md", base + "- reference\n"), ("invalid_value", "notes/NOTE-001.md", 6))
        self.assertEqual(errors({"NOTE-001.md": base + "- reference P:S-1\n- origin P:S-2\n"}), [])

    def test_crlf_files_are_read_like_lf_files(self):
        self.assertEqual(check({"NOTE-001.md": (NOTE + "Triggers:\n- topic_due\n\nText\n").replace("\n", "\r\n")}), [])


class TopicsTest(unittest.TestCase):
    def one(self, text: str) -> tuple[str, int]:
        found = errors({"topics.md": text})
        self.assertEqual(len(found), 1, found)
        self.assertEqual(found[0].file, "notes/topics.md")
        return found[0].code, found[0].line

    def test_valid_tree_with_escapes_and_new_topic(self):
        text = (
            "- TOPIC-001 | Sync | uid=u1 | due=2026-12-01T00:00:00Z | created=2026-09-01T09:00:00Z | archived= | deleted=\n"
            "  - TOPIC-002 | Format \\| Dateien \\\\ \\n | uid=u2 | due=\n"
            "    - TOPIC-003 | Deep | uid=u3\n"
            "- NEW | Ideen | due=\n"
        )
        self.assertEqual(check({"topics.md": text}), [])

    def test_blank_lines_are_skipped(self):
        self.assertEqual(check({"topics.md": "\n" + TOPIC + "\n\n"}), [])

    def test_line_that_is_no_topic_row(self):
        self.assertEqual(self.one(TOPIC + "\nsomething\n"), ("invalid_value", 2))
        self.assertEqual(self.one("- TOPIC-1x | N | uid=u\n"), ("invalid_value", 1))

    def test_indentation(self):
        self.assertEqual(self.one(TOPIC + "\n - TOPIC-002 | N | uid=u2\n"), ("invalid_value", 2))
        self.assertEqual(self.one(TOPIC + "\n    - TOPIC-002 | N | uid=u2\n"), ("invalid_value", 2))
        self.assertEqual(self.one("  " + TOPIC + "\n"), ("invalid_value", 1))

    def test_name_is_required(self):
        self.assertEqual(self.one("- TOPIC-001 |  | uid=u\n"), ("missing_field", 1))

    def test_unknown_specification(self):
        self.assertEqual(self.one("- TOPIC-001 | N | uid=u | color=red\n"), ("unknown_field", 1))
        self.assertEqual(self.one("- TOPIC-001 | N | uid=u | due\n"), ("unknown_field", 1))

    def test_a_topic_with_label_needs_a_uid(self):
        self.assertEqual(self.one("- TOPIC-001 | N | due=\n"), ("missing_field", 1))

    def test_times(self):
        self.assertEqual(self.one("- TOPIC-001 | N | uid=u | due=2026-12-01\n"), ("invalid_value", 1))
        self.assertEqual(self.one("- TOPIC-001 | N | uid=u | deleted=later\n"), ("invalid_value", 1))


class CrossFileTest(unittest.TestCase):
    def test_duplicate_uid_between_notes(self):
        files = {"NOTE-001.md": NOTE, "NOTE-002.md": NOTE.replace("NOTE-001", "NOTE-002")}
        found = errors(files)
        self.assertEqual([(f.code, f.file, f.line) for f in found], [("duplicate_uid", "notes/NOTE-002.md", 1)])

    def test_duplicate_uid_between_a_note_and_a_topic(self):
        found = errors({"NOTE-001.md": NOTE, "topics.md": "- TOPIC-001 | N | uid=u-1\n"})
        self.assertEqual([(f.code, f.file, f.line) for f in found], [("duplicate_uid", "notes/NOTE-001.md", 1)])

    def test_duplicate_topic_label(self):
        found = errors({"topics.md": TOPIC + "\n- TOPIC-001 | Other | uid=t-2\n"})
        self.assertEqual([(f.code, f.file, f.line) for f in found], [("duplicate_label", "notes/topics.md", 2)])

    def test_duplicate_placeholder_topic(self):
        found = errors({"topics.md": "- NEW | Ideen\n- NEW | Ideen\n"})
        self.assertEqual([(f.code, f.file, f.line) for f in found], [("invalid_placeholder", "notes/topics.md", 2)])

    def test_a_new_note_and_a_new_topic_may_share_a_name(self):
        self.assertEqual(check({"new-ideen.md": NEW, "topics.md": "- NEW | new-ideen\n"}), [])


class FolderTest(unittest.TestCase):
    def test_merge_markers(self):
        text = NOTE + "\n<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> branch\n"
        found = errors({"NOTE-001.md": text})
        self.assertEqual([(f.code, f.file, f.line) for f in found], [("merge_markers", "notes/NOTE-001.md", 6)])

    def test_a_single_marker_line_is_not_a_conflict(self):
        self.assertEqual(errors({"NOTE-001.md": NOTE + "\n<<<<<<< just text\n"}), [])

    def test_unreadable_file(self):
        found = errors({"NOTE-001.md": b"\xff\xfe broken"})
        self.assertEqual([(f.code, f.file, f.line) for f in found], [("unreadable", "notes/NOTE-001.md", 1)])

    def test_every_file_reports_its_first_error(self):
        files = {"NOTE-001.md": NOTE + "Foo: x\nBar: y\n", "NOTE-002.md": "# NOTE-002\n", "topics.md": "bad\n"}
        found = errors(files)
        self.assertEqual(sorted(f.file for f in found), ["notes/NOTE-001.md", "notes/NOTE-002.md", "notes/topics.md"])

    def test_errors_come_before_notices(self):
        found = check({"readme.md": "x\n", "NOTE-001.md": NOTE + "Foo: x\n"})
        self.assertEqual([f.error for f in found], [True, False])


class NoticeTest(unittest.TestCase):
    def test_unknown_file_name_is_a_notice(self):
        found = notices({"Note-003.md": NOTE, "new_idee.md": NEW, "readme.md": "x\n"})
        self.assertEqual(sorted(f.file for f in found), ["notes/Note-003.md", "notes/new_idee.md", "notes/readme.md"])
        self.assertTrue(all(f.line == 1 and f.code == "ignored_file" for f in found))

    def test_a_document_without_its_note_is_a_notice(self):
        found = notices({"NOTE-009_notes.md": "text\n", "NOTE-001.md": NOTE, "NOTE-001_spec_topic.md": "t\n"})
        self.assertEqual([(f.code, f.file) for f in found], [("document_without_note", "notes/NOTE-009_notes.md")])

    def test_counters_hidden_and_other_extensions_are_ignored(self):
        self.assertEqual(check({"counters.md": "NOTE: 3\n", ".hidden.md": "x\n", "image.png": b"\x89PNG"}), [])


if __name__ == "__main__":
    unittest.main()
