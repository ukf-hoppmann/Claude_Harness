import json
import os
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS
from helpers.fake_viewer import API, FakeViewer

P = f"{API}/projects/project"


class NotesApiTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name).resolve() / "project"
        self.todo = self.project / "docs" / "todo"
        self.todo.mkdir(parents=True)
        self.viewer = FakeViewer()
        self.write_config(self.viewer.url)
        self.viewer.sources.append({"id": "src1", "project": "project", "path": str(self.todo)})

    def tearDown(self):
        self.viewer.close()
        self._tmp.cleanup()

    def write_config(self, url, notes="true"):
        config = self.project / ".claude-harness" / "config.toml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(f'version = 1\n[modules]\nnotes = {notes}\n[todo]\napi_url = "{url}"\n')

    def run_api(self, *args, stdin=""):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "notes_api.py"), *args],
            input=stdin, capture_output=True, text=True, timeout=30, cwd=self.project, env=env,
        )

    def route(self, method, path, body=None, status=200):
        self.viewer.routes[(method, path)] = (status, {} if body is None else body)

    def last(self):
        return self.viewer.requests[-1]

    def test_health(self):
        self.route("GET", f"{API}/health", {"status": "ok", "api": "2"})
        result = self.run_api("health")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"status": "ok"', result.stdout)

    def test_module_off_is_a_usage_error(self):
        self.write_config(self.viewer.url, notes="false")
        result = self.run_api("index")
        self.assertEqual(result.returncode, 2)
        self.assertIn("module notes is off", result.stderr)
        self.assertEqual(self.viewer.requests, [])

    def test_unreachable_server_has_own_exit_code(self):
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        self.write_config(f"http://127.0.0.1:{port}{API}")
        result = self.run_api("health")
        self.assertEqual(result.returncode, 3)
        self.assertIn("not reachable", result.stderr)

    def test_no_command_and_unknown_command_show_usage(self):
        self.assertEqual(self.run_api().returncode, 2)
        result = self.run_api("purge", "NOTE-001")
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage: notes_api.py", result.stderr)
        self.assertEqual(self.viewer.requests, [])

    def test_index_lists_topics_and_notes_of_the_project(self):
        self.route("GET", f"{API}/notes/index", {
            "topics": [{"project": "project", "label": "TOPIC-001", "name": "Sprint", "parent": None,
                        "path": ["Sprint"], "due_at": "2026-10-14T08:00:00Z", "due": False, "note_count": 2}],
            "notes": [{"project": "project", "label": "NOTE-001", "summary": "Check the DB size", "status": "due",
                       "reason": "review_expired", "review_at": "2026-10-01T08:00:00Z", "topic": "TOPIC-001",
                       "archived": False}],
        })
        result = self.run_api("index")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), [
            "Topics: Label | Path | Due at | Due | Notes",
            "TOPIC-001 | Sprint | 2026-10-14T08:00:00Z | no | 2",
            "Notes: Label | Status | Reason | Review at | Topic | Summary",
            "NOTE-001 | due | review_expired | 2026-10-01T08:00:00Z | TOPIC-001 | Check the DB size",
        ])
        self.assertEqual(self.last()["query"], {"project": ["project"]})

    def test_index_filters_and_all_projects(self):
        self.route("GET", f"{API}/notes/index", {"topics": [], "notes": [
            {"project": "other", "label": "NOTE-004", "summary": "S", "status": "waiting", "reason": None,
             "review_at": None, "topic": None, "archived": False}]})
        result = self.run_api("index", "--topic", "TOPIC-001", "--status", "snoozed", "--due", "--archived",
                              "--linked-item", "STORY-002")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["query"], {
            "project": ["project"], "topic": ["TOPIC-001"], "status": ["snoozed"], "due": ["true"],
            "archived": ["true"], "linked_item": ["STORY-002"],
        })
        result = self.run_api("index", "--all-projects")
        self.assertEqual(self.last()["query"], {})
        # Notes of other projects name their project.
        self.assertIn("other NOTE-004 | waiting | - | - | - | S", result.stdout)

    def test_due_prints_the_due_list(self):
        self.route("GET", f"{API}/notes/due", [{"project": "project", "label": "NOTE-001", "summary": "S"}])
        result = self.run_api("due")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [{"project": "project", "label": "NOTE-001", "summary": "S"}])

    def test_show_and_create_and_update(self):
        self.route("GET", f"{P}/notes/NOTE-001", {"label": "NOTE-001", "version": "v1"})
        self.assertIn('"version": "v1"', self.run_api("show", "NOTE-001").stdout)
        self.route("POST", f"{P}/notes", {"label": "NOTE-002", "version": "v1"}, status=201)
        result = self.run_api("create", stdin='{"summary": "Ä", "topic": "TOPIC-001"}')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["body"], {"summary": "Ä", "topic": "TOPIC-001"})
        self.route("PATCH", f"{P}/notes/NOTE-002", {"label": "NOTE-002", "version": "v2"})
        self.run_api("update", "NOTE-002", "v1", stdin='{"body": null}')
        self.assertEqual(self.last()["body"], {"version": "v1", "body": None})

    def test_status_changes_carry_the_version(self):
        for action in ("keep", "finish", "snooze", "move"):
            self.route("POST", f"{P}/notes/NOTE-001/{action}", {"label": "NOTE-001"})
        self.run_api("keep", "NOTE-001", "v1")
        self.assertEqual(self.last()["body"], {"version": "v1"})
        self.run_api("finish", "NOTE-001", "v1", "dropped")
        self.assertEqual(self.last()["body"], {"version": "v1", "status": "dropped"})
        result = self.run_api("finish", "NOTE-001", "v1", "promoted")
        self.assertEqual(result.returncode, 2)
        self.run_api("snooze", "NOTE-001", "v1", stdin='{"review_at": "2026-11-01T08:00:00+01:00"}')
        self.assertEqual(self.last()["body"], {"version": "v1", "review_at": "2026-11-01T08:00:00+01:00"})
        self.run_api("snooze", "NOTE-001", "v1")
        self.assertEqual(self.last()["body"], {"version": "v1"})
        self.run_api("move", "NOTE-001", "v1", "other", "--topic", "TOPIC-003")
        self.assertEqual(self.last()["body"], {"version": "v1", "project": "other", "topic": "TOPIC-003"})

    def test_delete_and_restore_need_no_version(self):
        self.route("DELETE", f"{P}/notes/NOTE-001", {"label": "NOTE-001"})
        self.route("POST", f"{P}/notes/NOTE-001/restore", {"label": "NOTE-001"})
        self.assertEqual(self.run_api("delete", "NOTE-001").returncode, 0)
        self.assertEqual(self.last()["method"], "DELETE")
        self.assertEqual(self.run_api("restore", "NOTE-001").returncode, 0)
        self.assertEqual(self.last()["body"], None)

    def test_triggers_links_and_reverse_lookups(self):
        self.route("POST", f"{P}/notes/NOTE-001/triggers", {"label": "NOTE-001"}, status=201)
        self.run_api("trigger-add", "NOTE-001", stdin='{"kind": "time", "at": "2026-10-14T09:00:00+02:00"}')
        self.assertEqual(self.last()["body"], {"kind": "time", "at": "2026-10-14T09:00:00+02:00"})
        self.route("DELETE", f"{P}/notes/NOTE-001/triggers/7", {"label": "NOTE-001"})
        self.run_api("trigger-remove", "NOTE-001", "7")
        self.assertEqual((self.last()["method"], self.last()["path"]), ("DELETE", f"{P}/notes/NOTE-001/triggers/7"))
        self.route("POST", f"{P}/notes/NOTE-001/links", {"id": 3}, status=201)
        self.run_api("link-add", "NOTE-001", stdin='{"kind": "item", "target": "STORY-002", "role": "reference"}')
        self.assertEqual(self.last()["body"], {"kind": "item", "target": "STORY-002", "role": "reference"})
        self.route("DELETE", f"{P}/notes/NOTE-001/links/3", [])
        self.run_api("link-remove", "NOTE-001", "3")
        self.assertEqual(self.last()["path"], f"{P}/notes/NOTE-001/links/3")
        for command, arg, path in (
            ("links", "NOTE-001", f"{P}/notes/NOTE-001/links"),
            ("backlinks", "NOTE-001", f"{P}/notes/NOTE-001/backlinks"),
            ("notes-of-item", "STORY-002", f"{P}/items/STORY-002/notes"),
            ("notes-of-topic", "TOPIC-001", f"{P}/topics/TOPIC-001/notes"),
        ):
            self.route("GET", path, [])
            self.assertEqual(self.run_api(command, arg).returncode, 0, command)
            self.assertEqual(self.last()["path"], path)

    def test_documents_of_a_note(self):
        self.route("GET", f"{P}/notes/NOTE-001/documents/NOTE-001_notes.md",
                   {"name": "NOTE-001_notes.md", "kind": "notes", "content": "Text ä\n", "version": "d1"})
        result = self.run_api("doc", "NOTE-001", "NOTE-001_notes.md")
        self.assertEqual(result.stdout, "version: d1\n\nText ä\n")
        self.route("PUT", f"{P}/notes/NOTE-001/documents/NOTE-001_spec.md",
                   {"name": "NOTE-001_spec.md", "version": "d2"})
        result = self.run_api("put-doc", "NOTE-001", "NOTE-001_spec.md", "new", stdin="# Spec\n")
        self.assertEqual(self.last()["body"], {"content": "# Spec\n", "version": None})
        self.assertIn("saved, version d2", result.stdout)
        self.route("POST", f"{P}/notes/NOTE-001/notes", {"name": "NOTE-001_notes.md"})
        self.run_api("note-entry", "NOTE-001", stdin='{"topic": "T", "decided": ["x"]}')
        self.assertEqual(self.last()["body"], {"topic": "T", "decided": ["x"]})

    def test_topics(self):
        self.route("GET", f"{P}/topics", [])
        self.run_api("topics", "--deleted")
        self.assertEqual(self.last()["query"], {"include_deleted": ["true"]})
        self.route("POST", f"{P}/topics", {"label": "TOPIC-001"}, status=201)
        self.run_api("topic-create", stdin='{"name": "Sprint", "due_at": "2026-10-14T08:00:00+02:00"}')
        self.assertEqual(self.last()["body"], {"name": "Sprint", "due_at": "2026-10-14T08:00:00+02:00"})
        self.route("PATCH", f"{P}/topics/TOPIC-001", {"label": "TOPIC-001"})
        self.run_api("topic-update", "TOPIC-001", stdin='{"due_at": null}')
        self.assertEqual(self.last()["body"], {"due_at": None})
        self.route("POST", f"{P}/topics/TOPIC-001/move", {"label": "TOPIC-001"})
        self.run_api("topic-move", "TOPIC-001", stdin='{"parent": null}')
        self.assertEqual(self.last()["body"], {"parent": None})
        self.route("DELETE", f"{P}/topics/TOPIC-001", {"topics": [], "notes": []})
        self.run_api("topic-delete", "TOPIC-001", "--cascade")
        self.assertEqual(self.last()["query"], {"cascade": ["true"]})
        self.route("POST", f"{P}/topics/TOPIC-001/restore", {"topics": [], "notes": []})
        self.assertEqual(self.run_api("topic-restore", "TOPIC-001").returncode, 0)
        self.route("GET", f"{P}/trash", {"topics": [], "notes": []})
        self.assertEqual(self.run_api("trash").returncode, 0)

    def test_notices_and_decisions(self):
        self.route("GET", f"{API}/notices", [])
        self.run_api("notices", "NOTE-001", "--side", "note", "--open")
        self.assertEqual(self.last()["query"],
                         {"project": ["project"], "label": ["NOTE-001"], "side": ["note"], "open": ["true"]})
        self.route("POST", f"{API}/notices/12/decision", {"notice": {}, "note": {}})
        self.run_api("decide", "12", stdin='{"decision": "keep", "version": "v1"}')
        self.assertEqual(self.last()["body"], {"decision": "keep", "version": "v1"})

    def test_promote_and_demote(self):
        self.route("POST", f"{API}/notes/project/NOTE-001/promote", {"note": {}, "item": {"id": "TASK-005"}})
        body = '{"version": "v1", "item_type": "Task", "area": "A", "goal": "G", "completion_criteria": "C"}'
        result = self.run_api("promote", "NOTE-001", stdin=body)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["body"]["item_type"], "Task")
        self.route("POST", f"{API}/items/src1/STORY-001/demote", {"item": {}, "note": {"label": "NOTE-009"}})
        result = self.run_api("demote", "STORY-001", stdin='{"version": "i1", "topic": "TOPIC-001"}')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["body"], {"version": "i1", "topic": "TOPIC-001"})

    def test_settings_can_only_be_read(self):
        self.route("GET", f"{API}/notes/settings", {"max_topic_depth": 3, "review_days": 30})
        result = self.run_api("settings")
        self.assertEqual(json.loads(result.stdout), {"max_topic_depth": 3, "review_days": 30})
        sent = len(self.viewer.requests)
        self.assertEqual(self.run_api("settings", "--set", "review_days=5").returncode, 2)
        self.assertEqual(len(self.viewer.requests), sent)
        self.assertEqual({r["method"] for r in self.viewer.requests}, {"GET"})

    def test_server_errors_are_reported_with_code_and_conflict_hint(self):
        self.route("POST", f"{P}/notes/NOTE-001/keep",
                   {"code": "version_conflict", "message": "changed", "details": {}}, status=409)
        result = self.run_api("keep", "NOTE-001", "old")
        self.assertEqual(result.returncode, 1)
        self.assertIn("HTTP 409 version_conflict", result.stderr)
        self.assertIn("never retry blindly", result.stderr)

    def test_bad_stdin_is_a_usage_error(self):
        result = self.run_api("create", stdin="[1]")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.viewer.calls("POST"), [])

    def add_misc_source(self):
        self.viewer.sources.append({"id": "misc1", "project": "Misc", "path": "", "backend": "database",
                                    "sync_path": None, "markdown_path": None, "mirror": "none"})

    def test_sources_lists_the_names_the_viewer_knows(self):
        self.add_misc_source()
        result = self.run_api("sources")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["Project | Folder", f"project | {self.todo}", "Misc | -"])

    def test_source_option_addresses_the_notes_of_another_project(self):
        self.add_misc_source()
        self.route("GET", f"{API}/projects/Misc/topics", [])
        result = self.run_api("--source", "Misc", "topics")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["path"], f"{API}/projects/Misc/topics")
        self.assertEqual(self.viewer.calls("POST"), [])

    def test_unknown_source_names_the_known_ones(self):
        self.add_misc_source()
        result = self.run_api("--source", "misc", "topics")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown source 'misc' (known: project, Misc)", result.stderr)

    def test_source_and_project_exclude_each_other(self):
        result = self.run_api("--source", "Misc", "--project", "x", "topics")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--source", result.stderr)
        self.assertEqual(self.viewer.requests, [])

    def test_missing_source_is_registered(self):
        self.viewer.sources.clear()
        # The fake viewer names a source registered without a project "p".
        self.route("GET", f"{API}/projects/p/topics", [])
        result = self.run_api("topics")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.viewer.calls("POST")[0]["body"], {"path": str(self.todo)})
        self.assertEqual(self.last()["path"], f"{API}/projects/p/topics")


if __name__ == "__main__":
    unittest.main()
