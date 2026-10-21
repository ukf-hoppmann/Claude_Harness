import json
import unittest

from helpers import REPO_ROOT
import notes_head
from notes_head import CURRENT, MISSING, STALE, NotesHeadError

VECTORS = REPO_ROOT / "tests" / "fixtures" / "notes-state" / "checksum.json"

LOG = "## 2026-10-01 — First\n\n### Discussed\n\n- a\n\n## 2026-10-02 — Second\n\n### Decided\n\n- b\n"
HEAD = "## State\n\n- Goal/Status: g\n- Next step: n\n- Open: nothing\n- Decided:\n  - b (2026-10-02)\n- References: none\n"


def notes(head: str = HEAD, stamp: str | None = None, log: str = LOG) -> str:
    text = "# TASK-001 — Title\n\n" + head
    if stamp is not None:
        text += f"\n{stamp}\n"
    return text + "\n" + log


class ChecksumTest(unittest.TestCase):
    def test_shared_vectors(self):
        for vector in json.loads(VECTORS.read_text())["vectors"]:
            with self.subTest(vector["name"]):
                self.assertEqual(notes_head.canonical(vector["protocol"]), vector["canonical"])
                self.assertEqual(notes_head.checksum(vector["protocol"]), vector["checksum"])

    def test_example_in_format_md(self):
        text = (REPO_ROOT / "plugin" / "skills" / "todo" / "format.md").read_text()
        example = text.split("```markdown\n# STORY-012", 1)[1].split("```", 1)[0]
        self.assertEqual(notes_head.state_of("# STORY-012" + example), CURRENT)


class StateTest(unittest.TestCase):
    def test_without_head_is_missing(self):
        self.assertEqual(notes_head.state_of("# TASK-001 — Title\n\n" + LOG), MISSING)

    def test_without_stamp_is_stale(self):
        self.assertEqual(notes_head.state_of(notes()), STALE)

    def test_confirmed_is_current(self):
        self.assertEqual(notes_head.state_of(notes_head.confirmed(notes())), CURRENT)

    def test_new_entry_makes_it_stale(self):
        text = notes_head.confirmed(notes()) + "\n## 2026-10-03 — Third\n\n### Open\n\n- c\n"
        self.assertEqual(notes_head.state_of(text), STALE)

    def test_whitespace_at_line_end_does_not_matter(self):
        text = notes_head.confirmed(notes())
        self.assertEqual(notes_head.state_of(text.replace("- a\n", "- a  \n")), CURRENT)

    def test_split(self):
        parts = notes_head.split(notes_head.confirmed(notes()))
        self.assertEqual(parts.title, "# TASK-001 — Title")
        self.assertIn("- Goal/Status: g", parts.state)
        self.assertNotIn("State confirmed", parts.state)
        self.assertEqual(parts.stamp, ("2026-10-02", "Second", notes_head.checksum(LOG)))
        self.assertEqual(parts.entries, LOG)

    def test_last_entry(self):
        self.assertEqual(notes_head.last_entry(notes()), ("2026-10-02", "Second"))
        self.assertIsNone(notes_head.last_entry("# T\n"))


class ConfirmTest(unittest.TestCase):
    def test_writes_the_stamp_line(self):
        text = notes_head.confirmed(notes())
        stamp = f"State confirmed after entry 2026-10-02 — Second ({notes_head.checksum(LOG)})"
        self.assertEqual(text, notes(stamp=stamp))

    def test_replaces_an_old_stamp_and_nothing_else(self):
        old = notes(stamp="State confirmed after entry 2026-10-01 — First (000000000000)")
        new = notes_head.confirmed(old)
        self.assertEqual(new, notes(stamp=f"State confirmed after entry 2026-10-02 — Second ({notes_head.checksum(LOG)})"))
        self.assertEqual(notes_head.confirmed(new), new)

    def test_keeps_crlf(self):
        text = notes_head.confirmed(notes().replace("\n", "\r\n"))
        self.assertNotIn("\n", text.replace("\r\n", ""))
        self.assertEqual(notes_head.state_of(text), CURRENT)

    def test_without_head(self):
        with self.assertRaises(NotesHeadError):
            notes_head.confirmed("# TASK-001 — Title\n\n" + LOG)

    def test_without_entries(self):
        with self.assertRaises(NotesHeadError):
            notes_head.confirmed(notes(log=""))


class HintsTest(unittest.TestCase):
    def test_decided_count(self):
        head = "## State\n\n- Goal/Status: g\n- Decided:\n  - a\n  - b\n    - detail\n- References: r\n"
        # Nested bullets count too, like in the ToDo-Viewer.
        self.assertEqual(notes_head.decided_count(notes(head=head)), 3)
        self.assertEqual(notes_head.decided_count("# T\n\n" + LOG), 0)

    def test_history_rewritten(self):
        old = notes()
        appended = old + "\n## 2026-10-03 — Third\n\n### Open\n\n- c\n"
        self.assertFalse(notes_head.history_rewritten(old, appended))
        self.assertFalse(notes_head.history_rewritten(old, notes_head.confirmed(old)))
        self.assertTrue(notes_head.history_rewritten(old, old.replace("- a", "- changed")))
        self.assertTrue(notes_head.history_rewritten(old, notes(log=LOG.split("## 2026-10-02")[0])))


if __name__ == "__main__":
    unittest.main()
