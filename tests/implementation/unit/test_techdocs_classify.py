import tempfile
import unittest
from pathlib import Path

import helpers  # noqa: F401  (adds plugin/scripts to sys.path)
from projects import load_projects
from techdocs import classify


class ClassifyTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()

    def tearDown(self):
        self._tmp.cleanup()

    def project(self, extra=""):
        config = self.root / ".claude-harness" / "config.toml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(
            'version = 1\n[docs]\nroot = "docs"\n[modules]\ntechdocs = true\ndevelopment = true\n' + extra
        )
        return load_projects(self.root).get("root")

    def kind(self, project, rel):
        return classify(project, str(self.root / rel))

    def test_interface_index_counts_as_docs(self):
        self.assertEqual(self.kind(self.project(), "docs/development/interfaces.md"), "docs")

    def test_interface_docs_count_as_docs(self):
        project = self.project()
        self.assertEqual(self.kind(project, "docs/development/interfaces/core/api.md"), "docs")

    def test_architecture_rules_do_not_count(self):
        project = self.project()
        self.assertIsNone(self.kind(project, "docs/development/architecture.md"))
        self.assertIsNone(self.kind(project, "docs/development/architecture/plugins.md"))

    def test_architecture_part_off_interfaces_do_not_count(self):
        project = self.project("[development]\narchitecture = false\n")
        self.assertIsNone(self.kind(project, "docs/development/interfaces.md"))
        self.assertIsNone(self.kind(project, "docs/development/interfaces/a.md"))

    def test_development_module_off_interfaces_do_not_count(self):
        config = self.root / ".claude-harness" / "config.toml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text('version = 1\n[docs]\nroot = "docs"\n[modules]\ntechdocs = true\n')
        project = load_projects(self.root).get("root")
        self.assertIsNone(self.kind(project, "docs/development/interfaces.md"))

    def test_custom_development_path(self):
        project = self.project('[development]\npath = "dev"\n')
        self.assertEqual(self.kind(project, "docs/dev/interfaces/a.md"), "docs")
        self.assertIsNone(self.kind(project, "docs/development/interfaces/a.md"))

    def test_existing_classes_unchanged(self):
        project = self.project()
        self.assertEqual(self.kind(project, "README.md"), "docs")
        self.assertEqual(self.kind(project, "docs/techdocs/x.md"), "docs")
        self.assertEqual(self.kind(project, "src/app.py"), "project")
        self.assertIsNone(self.kind(project, "tests/test_a.py"))


if __name__ == "__main__":
    unittest.main()
