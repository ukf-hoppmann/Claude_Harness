import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import REPO_ROOT
from backlog import validate_backlog

FIXTURE = REPO_ROOT / "tests" / "fixtures" / "mindmap-files" / "valid"


class MindmapFolderTest(unittest.TestCase):
    def test_a_backlog_folder_with_mindmap_passes_without_a_message(self):
        report = validate_backlog(FIXTURE)
        self.assertEqual(report.errors, [])
        self.assertEqual(report.notices, [])
        self.assertEqual([i.identifier for i in report.items], ["STORY-001"])

    def test_the_content_of_mindmap_files_is_not_checked_here(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "todo"
            shutil.copytree(FIXTURE, folder)
            (folder / "mindmap" / "NODE-001.md").write_text("garbage\n")
            (folder / "mindmap" / "unknown.md").write_text("garbage\n")
            (folder / "mindmap" / "maps" / "x.md").write_text("garbage\n")
            report = validate_backlog(folder)
        self.assertEqual((report.errors, report.notices), ([], []))


if __name__ == "__main__":
    unittest.main()
