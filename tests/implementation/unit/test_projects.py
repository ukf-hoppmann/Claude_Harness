import tempfile
import unittest
from pathlib import Path, PurePosixPath

import helpers  # noqa: F401  (adds plugin/scripts to sys.path)
from harness_config import ConfigError
from projects import load_projects


def write_config(folder: Path, text: str) -> None:
    path = folder / ".claude-harness" / "config.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("version = 1\n" + text)


REGISTRY = '[projects]\nA = "Plugins/A"\nB = "Plugins/B"\n'


class LoadProjectsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()

    def tearDown(self):
        self._tmp.cleanup()

    def test_without_root_config(self):
        self.assertIsNone(load_projects(self.root))

    def test_invalid_root_config_raises(self):
        write_config(self.root, "[projects]\nroot = 'x'\n")
        with self.assertRaises(ConfigError):
            load_projects(self.root)

    def test_without_registry_only_root(self):
        write_config(self.root, "[modules]\ntodo = true\n")
        projects = load_projects(self.root)
        self.assertFalse(projects.has_subprojects())
        self.assertEqual([p.name for p in projects.projects], ["root"])
        root = projects.get("root")
        self.assertEqual(root.path, PurePosixPath("."))
        self.assertEqual(root.root, self.root)
        self.assertIs(projects.for_file(str(self.root / "src" / "x.py")), root)
        self.assertEqual(projects.errors, ())

    def test_assigns_files_to_their_project(self):
        write_config(self.root, REGISTRY)
        write_config(self.root / "Plugins" / "A", '[docs]\nlanguage = "en"\n')
        write_config(self.root / "Plugins" / "B", '[docs]\nlanguage = "de"\n')
        projects = load_projects(self.root)
        self.assertTrue(projects.has_subprojects())
        self.assertEqual([p.name for p in projects.projects], ["root", "A", "B"])
        a = projects.get("A")
        self.assertEqual(a.path, PurePosixPath("Plugins/A"))
        self.assertEqual(a.root, self.root / "Plugins" / "A")
        self.assertEqual(a.config.language, "en")
        self.assertIs(projects.for_file(str(self.root / "Plugins/A/src/x.py")), a)
        self.assertIs(projects.for_file("Plugins/B/README.md"), projects.get("B"))
        self.assertIs(projects.for_file(str(self.root / "core/api.py")), projects.get("root"))
        self.assertIs(projects.for_file(str(self.root / "Plugins/Ax/y.py")), projects.get("root"))
        self.assertIsNone(projects.for_file("/elsewhere/file.py"))
        self.assertEqual(a.relative(str(self.root / "Plugins/A/src/x.py")), PurePosixPath("src/x.py"))
        self.assertIsNone(a.relative(str(self.root / "core/api.py")))

    def test_broken_subproject_is_reported_and_skipped(self):
        write_config(self.root, REGISTRY + 'C = "Plugins/C"\n')
        write_config(self.root / "Plugins" / "A", "")
        write_config(self.root / "Plugins" / "B", "version = 1\n")  # duplicate key: invalid TOML
        # Plugins/C has no config at all.
        projects = load_projects(self.root)
        self.assertEqual([p.name for p in projects.projects], ["root", "A"])
        self.assertEqual([name for name, _ in projects.errors], ["B", "C"])
        self.assertIn(".claude-harness/config.toml", dict(projects.errors)["C"])
        self.assertIsNone(projects.for_file(str(self.root / "Plugins/B/x.py")))
        self.assertIsNone(projects.for_file(str(self.root / "Plugins/C/x.py")))
        self.assertIs(projects.for_file(str(self.root / "Plugins/A/x.py")), projects.get("A"))
        self.assertEqual(
            projects.registry,
            (("A", PurePosixPath("Plugins/A")), ("B", PurePosixPath("Plugins/B")), ("C", PurePosixPath("Plugins/C"))),
        )

    def test_subproject_must_not_register_projects(self):
        write_config(self.root, REGISTRY)
        write_config(self.root / "Plugins" / "A", '[projects]\nX = "x"\n')
        write_config(self.root / "Plugins" / "B", "")
        projects = load_projects(self.root)
        self.assertEqual([p.name for p in projects.projects], ["root", "B"])
        self.assertIn("only allowed in the root project", dict(projects.errors)["A"])


if __name__ == "__main__":
    unittest.main()
