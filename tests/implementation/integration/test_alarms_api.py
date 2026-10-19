import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS
from helpers.fake_viewer import API, FakeViewer

A = f"{API}/alarms/alarms"


class AlarmsApiTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name).resolve() / "project"
        self.todo = self.project / "docs" / "todo"
        self.todo.mkdir(parents=True)
        self.viewer = FakeViewer()
        self.write_config(self.viewer.url)
        self.viewer.add_project("p1", "project", self.todo)

    def tearDown(self):
        self.viewer.close()
        self._tmp.cleanup()

    def write_config(self, url, backend="api"):
        config = self.project / ".claude-harness" / "config.toml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(f'version = 1\n[modules]\ntodo = true\n[todo]\nbackend = "{backend}"\napi_url = "{url}"\n')

    def run_api(self, *args, stdin=""):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "alarms_api.py"), *args],
            input=stdin, capture_output=True, text=True, timeout=30, cwd=self.project, env=env,
        )

    def route(self, method, path, body=None, status=200):
        self.viewer.routes[(method, path)] = (status, {} if body is None else body)

    def last(self):
        return self.viewer.requests[-1]

    def test_files_backend_has_no_alarms(self):
        self.write_config(self.viewer.url, backend="files")
        result = self.run_api("list")
        self.assertEqual(result.returncode, 2)
        self.assertIn("todo.backend", result.stderr)
        self.assertEqual(self.viewer.requests, [])

    def test_list_of_the_project_or_all_projects(self):
        self.route("GET", A, [{"label": "ALARM-001"}])
        result = self.run_api("list")
        self.assertEqual(json.loads(result.stdout), [{"label": "ALARM-001"}])
        self.assertEqual(self.last()["query"], {"projects": ["p1"]})
        self.run_api("list", "--due", "--all-projects")
        self.assertEqual(self.last()["query"], {"due_only": ["true"]})

    def test_show(self):
        self.route("GET", f"{A}/ALARM-001", {"label": "ALARM-001", "version": 2})
        self.assertIn('"version": 2', self.run_api("show", "ALARM-001").stdout)
        self.assertEqual(self.last()["query"], {"project": ["p1"]})

    def test_create_passes_own_labels_and_resolves_other_projects(self):
        self.viewer.add_project("p2", "other")
        self.viewer.add_label("p2", "STORY-009", "u-foreign")
        self.route("POST", A, {"label": "ALARM-002"}, status=201)
        stdin = '{"at": "2026-10-20T09:00:00+02:00", "targets": ["NOTE-001", "other:STORY-009"]}'
        result = self.run_api("create", stdin=stdin)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["body"], {"project": "p1", "fields": {
            "at": "2026-10-20T09:00:00+02:00", "targets": ["NOTE-001", "u-foreign"]}})
        self.run_api("create", stdin='{"at": "2026-10-20T09:00:00+02:00", "text": "Zahnarzt"}')
        self.assertEqual(self.last()["body"],
                         {"project": "p1", "fields": {"at": "2026-10-20T09:00:00+02:00", "text": "Zahnarzt"}})

    def test_update_snooze_finish_reopen_carry_the_version(self):
        self.route("PUT", f"{A}/ALARM-001", {})
        self.run_api("update", "ALARM-001", "2", stdin='{"targets": []}')
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 2, "fields": {"targets": []}})
        for action in ("snooze", "finish", "reopen"):
            self.route("POST", f"{A}/ALARM-001/{action}", {})
        self.run_api("snooze", "ALARM-001", "3")
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 3})
        self.run_api("snooze", "ALARM-001", "3", "--until", "2026-10-20T10:00:00+02:00")
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 3, "until": "2026-10-20T10:00:00+02:00"})
        self.run_api("finish", "ALARM-001", "4")
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 4})
        self.run_api("reopen", "ALARM-001", "5")
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 5})

    def test_version_must_be_a_number(self):
        self.assertEqual(self.run_api("finish", "ALARM-001", "x").returncode, 2)
        self.assertEqual(self.viewer.requests, [])

    def test_delete_and_restore_through_the_trash(self):
        self.viewer.add_label("p1", "ALARM-001", "u-alarm")
        self.route("DELETE", f"{API}/workspace/elements/u-alarm", {})
        self.run_api("delete", "ALARM-001", "2")
        self.assertEqual(self.last()["query"], {"version": ["2"]})
        self.route("POST", f"{API}/workspace/trash/restore", {})
        self.run_api("restore", "ALARM-001")
        self.assertEqual(self.last()["body"], {"uids": ["u-alarm"]})

    def test_unknown_command_shows_usage(self):
        result = self.run_api("purge")
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage: alarms_api.py", result.stderr)


if __name__ == "__main__":
    unittest.main()
