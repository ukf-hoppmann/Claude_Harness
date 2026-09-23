import tempfile
import unittest
from pathlib import Path, PurePosixPath

import helpers  # noqa: F401  (adds plugin/scripts to sys.path)
from harness_config import ConfigError, load_config, parse_config


class ParseConfigTest(unittest.TestCase):
    def test_valid_config(self):
        config = parse_config({"version": 1, "modules": {"todo": True}, "todo": {"path": "planning"}})
        self.assertTrue(config.enabled("todo"))
        self.assertEqual(config.todo_path, PurePosixPath("planning"))

    def test_defaults(self):
        config = parse_config({"version": 1})
        self.assertFalse(config.enabled("todo"))
        self.assertEqual(config.todo_path, PurePosixPath("docs/todo"))

    def test_rejects_invalid_values(self):
        cases = [
            {"version": 2},
            {"version": 1, "extra": 1},
            {"version": 1, "modules": {"unknown": True}},
            {"version": 1, "modules": {"todo": "yes"}},
            {"version": 1, "todo": {"path": "/abs"}},
            {"version": 1, "todo": {"path": "../outside"}},
            {"version": 1, "todo": {"path": "docs", "other": 1}},
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
