import tempfile
import unittest
from pathlib import Path, PurePosixPath

import helpers  # noqa: F401  (adds plugin/scripts to sys.path)
from harness_config import ConfigError, load_config, parse_config


class ParseConfigTest(unittest.TestCase):
    def test_valid_config(self):
        config = parse_config({
            "version": 1,
            "docs": {"root": "documentation", "language": "de"},
            "modules": {"todo": True, "daily": True},
            "todo": {"path": "planning"},
            "daily": {"path": "log"},
        })
        self.assertTrue(config.enabled("todo"))
        self.assertTrue(config.enabled("daily"))
        self.assertEqual(config.language, "de")
        self.assertEqual(config.docs_root, PurePosixPath("documentation"))
        self.assertEqual(config.todo_path, PurePosixPath("documentation/planning"))
        self.assertEqual(config.daily_path, PurePosixPath("documentation/log"))

    def test_defaults(self):
        config = parse_config({"version": 1})
        self.assertFalse(config.enabled("todo"))
        self.assertFalse(config.enabled("daily"))
        self.assertEqual(config.language, "en")
        self.assertEqual(config.todo_path, PurePosixPath("docs/todo"))
        self.assertEqual(config.daily_path, PurePosixPath("docs/daily"))
        self.assertFalse(config.enabled("techdocs"))
        self.assertEqual(config.techdocs_path, PurePosixPath("docs/techdocs"))
        self.assertEqual(config.techdocs, ("architecture", "interfaces", "configuration"))

    def test_techdocs_documents(self):
        config = parse_config({"version": 1, "techdocs": {"path": "tech", "documents": ["operations"]}})
        self.assertEqual(config.techdocs_path, PurePosixPath("docs/tech"))
        self.assertEqual(config.techdocs, ("operations",))
        self.assertEqual(parse_config({"version": 1, "techdocs": {"documents": []}}).techdocs, ())

    def test_development_suite(self):
        off = parse_config({"version": 1})
        self.assertFalse(off.part_enabled("architecture"))
        self.assertEqual(off.development_path, PurePosixPath("docs/development"))
        on = parse_config({"version": 1, "modules": {"development": True}})
        self.assertTrue(on.part_enabled("architecture"))
        opted_out = parse_config({
            "version": 1,
            "modules": {"development": True},
            "development": {"path": "rules", "architecture": False},
        })
        self.assertFalse(opted_out.part_enabled("architecture"))
        self.assertEqual(opted_out.development_path, PurePosixPath("docs/rules"))

    def test_harness_repo(self):
        self.assertEqual(parse_config({"version": 1}).harness_repos, ())
        config = parse_config({"version": 1, "harness": {"repo": ["/abs/harness", "~/code/harness"]}})
        self.assertEqual(config.harness_repos, ("/abs/harness", "~/code/harness"))
        self.assertEqual(parse_config({"version": 1, "harness": {"repo": []}}).harness_repos, ())

    def test_rejects_invalid_values(self):
        cases = [
            {"version": 2},
            {"version": 1, "extra": 1},
            {"version": 1, "modules": {"unknown": True}},
            {"version": 1, "modules": {"todo": "yes"}},
            {"version": 1, "todo": {"path": "/abs"}},
            {"version": 1, "todo": {"path": "../outside"}},
            {"version": 1, "todo": {"path": "docs", "other": 1}},
            {"version": 1, "docs": {"root": "/abs"}},
            {"version": 1, "docs": {"language": "deu"}},
            {"version": 1, "docs": {"language": "DE"}},
            {"version": 1, "docs": {"other": 1}},
            {"version": 1, "docs": "docs"},
            {"version": 1, "daily": {"path": "../x"}},
            {"version": 1, "techdocs": {"documents": ["unknown"]}},
            {"version": 1, "techdocs": {"documents": ["interfaces", "interfaces"]}},
            {"version": 1, "techdocs": {"documents": "interfaces"}},
            {"version": 1, "techdocs": {"path": "/abs"}},
            {"version": 1, "development": {"architecture": "yes"}},
            {"version": 1, "development": {"unknown": True}},
            {"version": 1, "development": {"path": "../x"}},
            {"version": 1, "harness": {"repo": "/abs/harness"}},
            {"version": 1, "harness": {"repo": ["relative/harness"]}},
            {"version": 1, "harness": {"repo": [""]}},
            {"version": 1, "harness": {"repo": [1]}},
            {"version": 1, "harness": {"other": 1}},
            {"version": 1, "harness": "x"},
        ]
        for data in cases:
            with self.subTest(data=data), self.assertRaises(ConfigError):
                parse_config(data)


class LoadConfigTest(unittest.TestCase):
    def test_missing_config_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(load_config(Path(tmp)))

    def test_invalid_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".claude-harness" / "config.toml"
            path.parent.mkdir()
            path.write_text("version = ")
            with self.assertRaises(ConfigError):
                load_config(Path(tmp))

    def test_template_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".claude-harness" / "config.toml"
            path.parent.mkdir()
            path.write_text((helpers.REPO_ROOT / "plugin/templates/config.toml").read_text())
            self.assertTrue(load_config(Path(tmp)).enabled("todo"))


if __name__ == "__main__":
    unittest.main()
