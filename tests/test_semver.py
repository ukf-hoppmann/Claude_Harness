import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS
from projects import load_projects
from semver import allowed_next, parse_version, status


class VersionTest(unittest.TestCase):
    def test_parse_version(self):
        self.assertEqual(parse_version("1.2.3"), (1, 2, 3))
        self.assertEqual(parse_version(" 0.10.0\n"), (0, 10, 0))
        for text in ("1.2", "01.2.3", "1.2.3-beta", "1.2.3+build", "v1.2.3", "1.2.3\n4.5.6", ""):
            with self.subTest(text=text):
                self.assertIsNone(parse_version(text))

    def test_allowed_next(self):
        self.assertEqual(allowed_next((1, 4, 2)), [(1, 4, 2), (1, 4, 3), (1, 5, 0), (2, 0, 0)])


class SemverRepoTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name).resolve()
        self.project = base / "project"
        self.data = base / "data"
        self.project.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.write_config()
        self.write("docs/VERSION", "0.1.0\n")
        self.commit("src/app.py", "initial")

    def tearDown(self):
        self._tmp.cleanup()

    def git(self, *args, cwd=None):
        subprocess.run(["git", "-C", str(cwd or self.project), *args], check=True, capture_output=True)

    def write_config(self, semver="", root=None, extra=""):
        config = (root or self.project) / ".claude-harness" / "config.toml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(f"version = 1\n{extra}[modules]\nsemver = true\n[semver]\n{semver}")

    def write(self, path, text, root=None):
        target = (root or self.project) / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self, path, message):
        target = self.project / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(target.read_text() + "x\n" if target.exists() else "x\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def status(self, name="root"):
        projects = load_projects(self.project)
        return status(projects, projects.get(name))

    def run_script(self, script, *args, payload=None):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script), *args],
            input=json.dumps(payload or {}),
            capture_output=True,
            text=True,
            env=env,
        )


class StatusTest(SemverRepoTest):
    def test_without_tag_no_step_check(self):
        self.write("docs/VERSION", "3.0.0\n")
        result = self.status()
        self.assertEqual(result.version, (3, 0, 0))
        self.assertIsNone(result.last_tag)
        self.assertEqual(result.findings, [])
        self.assertIsNone(result.unreleased)

    def test_missing_and_invalid_version_file(self):
        (self.project / "docs/VERSION").unlink()
        self.assertIn("does not exist", self.status().findings[0])
        self.write("docs/VERSION", "1.0\n")
        self.assertIn("MAJOR.MINOR.PATCH", self.status().findings[0])

    def test_step_check_against_last_tag(self):
        self.git("tag", "v0.1.0")
        for text, ok in (("0.1.0", True), ("0.1.1", True), ("0.2.0", True), ("1.0.0", True),
                         ("0.1.2", False), ("0.3.0", False), ("0.2.1", False), ("0.0.9", False)):
            with self.subTest(version=text):
                self.write("docs/VERSION", text + "\n")
                findings = self.status().findings
                self.assertEqual(findings == [], ok, findings)

    def test_highest_tag_by_version_and_foreign_tags_ignored(self):
        self.git("tag", "v0.9.0")
        self.git("tag", "v0.10.0")
        self.git("tag", "vnext")
        self.git("tag", "Other-v5.0.0")
        self.git("tag", "v1.0.0-beta")
        self.write("docs/VERSION", "0.10.0\n")
        result = self.status()
        self.assertEqual(result.last_tag, "v0.10.0")
        self.assertEqual(result.findings, [])

    def test_sync_files(self):
        self.write_config('sync = ["package.json", "Cargo.toml"]\n')
        self.write("package.json", '{"name": "x", "version": "0.1.0"}\n')
        findings = self.status().findings
        self.assertEqual(len(findings), 1)
        self.assertIn("Cargo.toml does not exist", findings[0])
        self.write("Cargo.toml", '[package]\nversion = "0.0.9"\n')
        findings = self.status().findings
        self.assertEqual(len(findings), 1)
        self.assertIn("Cargo.toml does not contain 0.1.0", findings[0])
        self.write("Cargo.toml", '[package]\nversion = "0.1.0"\n')
        self.assertEqual(self.status().findings, [])

    def test_unreleased_commits_under_paths(self):
        self.write_config('paths = ["src"]\n')
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "config")
        self.git("tag", "v0.1.0")
        self.commit("src/app.py", "feature")
        self.commit("tests/test_app.py", "tests only")
        result = self.status()
        self.assertEqual([c.subject for c in result.unreleased], ["feature"])

    def test_subprojects_have_own_tags_and_root_excludes_them(self):
        self.write_config(extra='[projects]\nA = "Plugins/A"\n')
        sub = self.project / "Plugins/A"
        self.write_config(root=sub)
        self.write("docs/VERSION", "2.0.1\n", root=sub)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "add A")
        self.git("tag", "v0.1.0")
        self.git("tag", "A-v2.0.0")
        self.commit("Plugins/A/lib.py", "change A")
        root, a = self.status(), self.status("A")
        self.assertEqual(root.last_tag, "v0.1.0")
        self.assertEqual(root.unreleased, [])
        self.assertEqual(a.last_tag, "A-v2.0.0")
        self.assertEqual(a.tag_prefix, "A-v")
        self.assertEqual([c.subject for c in a.unreleased], ["change A"])
        self.assertEqual(a.findings, [])


class StatusCliTest(SemverRepoTest):
    def test_status_output(self):
        self.git("tag", "v0.1.0")
        self.commit("src/app.py", "feature")
        result = self.run_script("semver.py", "status")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Version file: docs/VERSION (0.1.0)", result.stdout)
        self.assertIn("Last release: v0.1.0", result.stdout)
        self.assertIn("0.1.1 (patch)", result.stdout)
        self.assertIn("feature", result.stdout)

    def test_module_off(self):
        (self.project / ".claude-harness/config.toml").write_text("version = 1\n")
        result = self.run_script("semver.py", "status")
        self.assertEqual(result.returncode, 1)
        self.assertIn("not enabled", result.stderr)


if __name__ == "__main__":
    unittest.main()
