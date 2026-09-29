import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import helpers  # noqa: F401  (adds plugin/scripts to sys.path)
import harness_repo
from harness_config import parse_config


def make_repo(path: Path, name: str = "claude-harness") -> Path:
    manifest = path / "plugin/.claude-plugin/plugin.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps({"name": name}))
    return path


class ConfiguredRepoTest(unittest.TestCase):
    def test_first_valid_path_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            other = make_repo(base / "other", name="other-plugin")
            first = make_repo(base / "first")
            second = make_repo(base / "second")
            config = parse_config({"version": 1, "harness": {"repo": [
                str(base / "missing"), str(other), str(base), str(first), str(second),
            ]}})
            self.assertEqual(harness_repo.configured_repo(config), first)

    def test_expands_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(Path(tmp) / "harness")
            with mock.patch.dict(os.environ, {"HOME": tmp}):
                config = parse_config({"version": 1, "harness": {"repo": ["~/harness"]}})
                self.assertEqual(harness_repo.configured_repo(config), repo)

    def test_none_without_valid_path(self):
        self.assertIsNone(harness_repo.configured_repo(parse_config({"version": 1})))


class SuggestedRepoTest(unittest.TestCase):
    def write(self, base: Path, data) -> Path:
        path = base / "known_marketplaces.json"
        path.write_text(data if isinstance(data, str) else json.dumps(data))
        return path

    def test_directory_marketplace_is_suggested(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = make_repo(base / "harness")
            clone = make_repo(base / "clone")
            marketplaces = self.write(base, {
                "remote": {"source": {"source": "github", "path": str(clone)}},
                "unrelated": {"source": {"source": "directory", "path": str(base / "missing")}},
                "dev": {"source": {"source": "directory", "path": str(repo)}},
            })
            self.assertEqual(harness_repo.suggested_repo(marketplaces), repo)

    def test_no_suggestion(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            clone = make_repo(base / "clone")
            self.assertIsNone(harness_repo.suggested_repo(base / "missing.json"))
            self.assertIsNone(harness_repo.suggested_repo(self.write(base, "{broken")))
            self.assertIsNone(harness_repo.suggested_repo(self.write(base, [1, 2])))
            github = {"remote": {"source": {"source": "github", "path": str(clone)}}}
            self.assertIsNone(harness_repo.suggested_repo(self.write(base, github)))


class MainTest(unittest.TestCase):
    def run_main(self, root: Path, argv: list[str]) -> tuple[int, str]:
        out = io.StringIO()
        with mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(root)}), redirect_stdout(out):
            code = harness_repo.main(argv)
        return code, out.getvalue()

    def test_prints_configured_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = make_repo(root / "harness")
            config = root / ".claude-harness/config.toml"
            config.parent.mkdir()
            config.write_text(f'version = 1\n[harness]\nrepo = ["{repo}"]\n')
            self.assertEqual(self.run_main(root, []), (0, f"{repo}\n"))

    def test_silent_without_or_with_invalid_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(self.run_main(root, []), (0, ""))
            config = root / ".claude-harness/config.toml"
            config.parent.mkdir()
            config.write_text("version = 2\n")
            self.assertEqual(self.run_main(root, []), (0, ""))

    def test_wrong_usage(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch("sys.stderr", io.StringIO()):
            self.assertEqual(self.run_main(Path(tmp), ["--other"])[0], 2)


if __name__ == "__main__":
    unittest.main()
