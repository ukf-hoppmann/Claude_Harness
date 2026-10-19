import json
import os
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS
from helpers.fake_viewer import API, PROJECTS, FakeViewer

N = f"{API}/notes"


class NotesApiTest(unittest.TestCase):
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

    def write_config(self, url, todo="true", backend="api"):
        config = self.project / ".claude-harness" / "config.toml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(
            f'version = 1\n[modules]\ntodo = {todo}\n[todo]\nbackend = "{backend}"\napi_url = "{url}"\n'
        )

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

    def writes(self):
        return [r for r in self.viewer.requests if r["method"] != "GET"]

    def test_health(self):
        self.route("GET", f"{API}/core/health", {"status": "ok"})
        result = self.run_api("health")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"status": "ok"', result.stdout)

    def test_todo_off_is_a_usage_error(self):
        self.write_config(self.viewer.url, todo="false")
        result = self.run_api("index")
        self.assertEqual(result.returncode, 2)
        self.assertIn("module todo is off", result.stderr)
        self.assertEqual(self.viewer.requests, [])

    def test_files_backend_has_no_notes(self):
        self.write_config(self.viewer.url, backend="files")
        result = self.run_api("index")
        self.assertEqual(result.returncode, 2)
        self.assertIn("notes need todo.backend", result.stderr)
        self.assertEqual(self.viewer.requests, [])

    def test_unreachable_server_has_own_exit_code(self):
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        self.write_config(f"http://127.0.0.1:{port}{API}")
        result = self.run_api("health")
        self.assertEqual(result.returncode, 3)
        self.assertIn("not reachable", result.stderr)

    def test_unregistered_project_has_own_exit_code(self):
        self.viewer.projects.clear()
        result = self.run_api("index")
        self.assertEqual(result.returncode, 4)
        self.assertIn("not registered", result.stderr)
        self.assertEqual(self.writes(), [])

    def test_no_command_and_unknown_command_show_usage(self):
        self.assertEqual(self.run_api().returncode, 2)
        result = self.run_api("purge", "NOTE-001")
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage: notes_api.py", result.stderr)
        self.assertEqual(self.viewer.requests, [])

    def test_index_prints_the_compact_tables_of_the_project(self):
        self.route("GET", f"{N}/index/lines", {
            "topics": "Label | Name | Due at | Due | Notes\nTOPIC-001 | Sprint | - | no | 2",
            "notes": "Label | Status | Reason | Review at | Topic | Summary\nNOTE-001 | due | review_expired | x | - | S",
            "topic_count": 1, "note_count": 1,
        })
        result = self.run_api("index")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), [
            "Topics: Label | Name | Due at | Due | Notes", "TOPIC-001 | Sprint | - | no | 2",
            "Notes: Label | Status | Reason | Review at | Topic | Summary",
            "NOTE-001 | due | review_expired | x | - | S",
        ])
        self.assertEqual(self.last()["query"], {"projects": ["p1"]})

    def test_index_filters_and_all_projects(self):
        self.route("GET", f"{N}/index/lines", {"topics": "Label", "notes": "Label"})
        self.run_api("index", "--status", "snoozed", "--due", "--archived", "--query", "DB")
        self.assertEqual(self.last()["query"], {
            "projects": ["p1"], "statuses": ["snoozed,due,done,dropped,promoted"], "query": ["DB"],
        })
        self.run_api("index", "--all-projects")
        self.assertEqual(self.last()["query"], {})

    def test_due_lists_all_projects(self):
        self.route("GET", f"{N}/due", {"count": 1, "notes": [{"label": "NOTE-001"}]})
        result = self.run_api("due")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"count": 1, "notes": [{"label": "NOTE-001"}]})
        self.assertEqual(self.last()["query"], {})

    def test_show_create_and_update(self):
        self.route("GET", f"{N}/notes/NOTE-001", {"label": "NOTE-001", "version": 1})
        self.assertIn('"version": 1', self.run_api("show", "NOTE-001").stdout)
        self.assertEqual(self.last()["query"], {"project": ["p1"]})
        self.route("POST", f"{N}/notes", {"label": "NOTE-002", "version": 1}, status=201)
        result = self.run_api("create", stdin='{"summary": "Ä", "topic": "TOPIC-001"}')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["body"], {"project": "p1", "fields": {"summary": "Ä", "topic": "TOPIC-001"}})
        self.route("PUT", f"{N}/notes/NOTE-002", {"label": "NOTE-002", "version": 2})
        self.run_api("update", "NOTE-002", "1", stdin='{"body": null}')
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 1, "fields": {"body": None}})

    def test_status_changes_carry_the_version(self):
        for action in ("keep", "finish", "snooze", "move"):
            self.route("POST", f"{N}/notes/NOTE-001/{action}", {"label": "NOTE-001"})
        self.viewer.add_project("p2", "other")
        self.run_api("keep", "NOTE-001", "1")
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 1})
        self.run_api("finish", "NOTE-001", "1", "dropped")
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 1, "status": "dropped"})
        self.assertEqual(self.run_api("finish", "NOTE-001", "1", "promoted").returncode, 2)
        self.run_api("snooze", "NOTE-001", "1", stdin='{"review_at": "2026-11-01T08:00:00+01:00"}')
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 1, "review_at": "2026-11-01T08:00:00+01:00"})
        self.run_api("snooze", "NOTE-001", "1")
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 1})
        result = self.run_api("move", "NOTE-001", "1", "other", "--topic", "TOPIC-003")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["body"],
                         {"project": "p1", "version": 1, "target_project": "p2", "topic": "TOPIC-003"})

    def test_version_must_be_a_number(self):
        result = self.run_api("keep", "NOTE-001", "v1")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.viewer.requests, [])

    def test_delete_goes_to_the_trash_by_uid(self):
        self.viewer.add_label("p1", "NOTE-001", "u-note")
        self.route("DELETE", f"{API}/workspace/elements/u-note", {"deleted": ["u-note"]})
        result = self.run_api("delete", "NOTE-001", "2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["query"], {"version": ["2"]})

    def test_restore_from_the_trash_or_from_the_archive(self):
        self.viewer.add_label("p1", "NOTE-001", "u-note", deleted=True)
        self.route("POST", f"{API}/workspace/trash/restore", {"restored": ["u-note"]})
        self.assertEqual(self.run_api("restore", "NOTE-001", "2").returncode, 0)
        self.assertEqual(self.last()["body"], {"uids": ["u-note"]})
        self.viewer.add_label("p1", "NOTE-002", "u-note2")
        self.route("POST", f"{N}/notes/NOTE-002/restore", {"label": "NOTE-002"})
        self.assertEqual(self.run_api("restore", "NOTE-002", "3").returncode, 0)
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 3})

    def test_triggers(self):
        self.route("POST", f"{N}/notes/NOTE-001/triggers", {"label": "NOTE-001"}, status=201)
        self.run_api("trigger-add", "NOTE-001", stdin='{"kind": "event", "target": "STORY-002", "status": "Completed"}')
        self.assertEqual(self.last()["body"],
                         {"project": "p1", "kind": "event", "target": "STORY-002", "status": "Completed"})
        # The old names still work: topic_due and target_status.
        self.run_api("trigger-add", "NOTE-001", stdin='{"kind": "topic_due"}')
        self.assertEqual(self.last()["body"], {"project": "p1", "kind": "topic_date"})
        self.run_api("trigger-add", "NOTE-001", stdin='{"kind": "event", "target": "STORY-002", "target_status": "Rejected"}')
        self.assertEqual(self.last()["body"]["status"], "Rejected")
        written = len(self.writes())
        result = self.run_api("trigger-add", "NOTE-001", stdin='{"kind": "time", "at": "2026-10-14T09:00:00+02:00"}')
        self.assertEqual(result.returncode, 2)
        self.assertIn("alarms_api.py", result.stderr)
        self.assertEqual(len(self.writes()), written)
        self.route("DELETE", f"{N}/triggers/t7", {"label": "NOTE-001"})
        self.assertEqual(self.run_api("trigger-remove", "t7").returncode, 0)

    def test_event_trigger_on_another_project_resolves_the_item(self):
        self.viewer.add_project("p2", "other")
        self.viewer.add_label("p2", "STORY-009", "u-foreign")
        self.route("POST", f"{N}/notes/NOTE-001/triggers", {"label": "NOTE-001"}, status=201)
        self.run_api("trigger-add", "NOTE-001",
                     stdin='{"kind": "event", "target": "STORY-009", "target_project": "other", "status": "Completed"}')
        self.assertEqual(self.last()["body"],
                         {"project": "p1", "kind": "event", "target": "u-foreign", "status": "Completed"})

    def test_links_by_label_become_workspace_links(self):
        self.viewer.add_label("p1", "NOTE-001", "u-note")
        self.viewer.add_label("p1", "STORY-002", "u-story")
        self.route("POST", f"{API}/workspace/links", {"uid": "l3"}, status=201)
        self.run_api("link-add", "NOTE-001", stdin='{"target": "STORY-002"}')
        self.assertEqual(self.last()["body"], {"from_uid": "u-note", "to_uid": "u-story", "role": "reference"})
        self.viewer.add_project("p2", "other")
        self.viewer.add_label("p2", "NOTE-004", "u-other")
        self.run_api("link-add", "NOTE-001", stdin='{"target": "NOTE-004", "target_project": "other", "role": "origin"}')
        self.assertEqual(self.last()["body"], {"from_uid": "u-note", "to_uid": "u-other", "role": "origin"})
        self.route("DELETE", f"{API}/workspace/links/l3", {})
        self.assertEqual(self.run_api("link-remove", "l3").returncode, 0)

    def test_links_backlinks_and_notes_of_an_item(self):
        self.viewer.add_label("p1", "NOTE-001", "u-note")
        self.viewer.add_label("p1", "STORY-002", "u-story")
        self.route("GET", f"{API}/workspace/elements/u-note/links",
                   {"outgoing": [{"label": "STORY-002"}], "incoming": [{"label": "NOTE-007"}]})
        self.assertEqual(json.loads(self.run_api("links", "NOTE-001").stdout), [{"label": "STORY-002"}])
        self.assertEqual(json.loads(self.run_api("backlinks", "NOTE-001").stdout), [{"label": "NOTE-007"}])
        self.route("GET", f"{API}/workspace/elements/u-story/links",
                   {"outgoing": [], "incoming": [{"label": "NOTE-001", "kind": "note"},
                                                 {"label": "STORY-001", "kind": "story"}]})
        result = self.run_api("notes-of-item", "STORY-002")
        self.assertEqual(json.loads(result.stdout), [{"label": "NOTE-001", "kind": "note"}])

    def test_documents_of_a_note(self):
        self.route("GET", f"{N}/notes/NOTE-001/documents/NOTE-001_notes.md",
                   {"name": "NOTE-001_notes.md", "kind": "notes", "content": "Text ä\n", "version": 4})
        self.assertEqual(self.run_api("doc", "NOTE-001", "NOTE-001_notes.md").stdout, "version: 4\n\nText ä\n")
        self.route("PUT", f"{N}/notes/NOTE-001/documents/NOTE-001_spec.md", {"name": "NOTE-001_spec.md", "version": 1})
        result = self.run_api("put-doc", "NOTE-001", "NOTE-001_spec.md", "new", stdin="# Spec\n")
        self.assertEqual(self.last()["body"], {"project": "p1", "content": "# Spec\n", "version": None})
        self.assertIn("saved, version 1", result.stdout)
        self.route("POST", f"{N}/notes/NOTE-001/entries", {"name": "NOTE-001_notes.md"})
        self.run_api("note-entry", "NOTE-001", stdin='{"topic": "T", "decided": ["x"]}')
        self.assertEqual(self.last()["body"], {"project": "p1", "topic": "T", "decided": ["x"]})
        self.route("GET", f"{N}/notes/NOTE-001/documents", [])
        self.assertEqual(self.run_api("docs", "NOTE-001").returncode, 0)

    def test_topics(self):
        self.route("GET", f"{N}/index", {"topics": [{"label": "TOPIC-001"}], "notes": []})
        self.assertEqual(json.loads(self.run_api("topics").stdout), [{"label": "TOPIC-001"}])
        self.route("GET", f"{N}/topics/TOPIC-001/content", {"topics": [], "notes": []})
        self.assertEqual(self.run_api("topic", "TOPIC-001").returncode, 0)
        self.route("POST", f"{N}/topics", {"label": "TOPIC-001"}, status=201)
        self.run_api("topic-create", stdin='{"name": "Sprint", "due_at": "2026-10-14T08:00:00+02:00"}')
        self.assertEqual(self.last()["body"], {"project": "p1", "name": "Sprint", "due_at": "2026-10-14T08:00:00+02:00"})
        self.route("PUT", f"{N}/topics/TOPIC-001", {"label": "TOPIC-001"})
        self.run_api("topic-update", "TOPIC-001", "2", stdin='{"due_at": null}')
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 2, "fields": {"due_at": None}})
        self.route("POST", f"{N}/topics/TOPIC-001/move", {"label": "TOPIC-001"})
        self.run_api("topic-move", "TOPIC-001", "3", stdin='{"parent": null}')
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 3, "parent": None})
        for action in ("archive", "delete"):
            self.route("POST", f"{N}/topics/TOPIC-001/{action}", {})
            self.run_api(f"topic-{action}", "TOPIC-001", "4", stdin='{"active_notes": "move", "move_to": null}')
            self.assertEqual(self.last()["body"], {"project": "p1", "version": 4, "active_notes": "move", "move_to": None})
        self.route("POST", f"{N}/topics/TOPIC-001/reactivate", {})
        self.run_api("topic-reactivate", "TOPIC-001", "5")
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 5})
        self.viewer.add_label("p1", "TOPIC-001", "u-topic", deleted=True)
        self.route("POST", f"{API}/workspace/trash/restore", {})
        self.run_api("topic-restore", "TOPIC-001")
        self.assertEqual(self.last()["body"], {"uids": ["u-topic"]})

    def test_trash_lists_notes_and_topics_of_the_project(self):
        self.route("GET", f"{API}/workspace/trash", [{"label": "NOTE-002", "kind": "note"},
                                                     {"label": "TOPIC-001", "kind": "topic"},
                                                     {"label": "STORY-001", "kind": "story"}])
        result = self.run_api("trash")
        self.assertEqual([e["label"] for e in json.loads(result.stdout)], ["NOTE-002", "TOPIC-001"])
        self.assertEqual(self.last()["query"], {"projects": ["p1"]})

    def test_notices_and_decisions(self):
        self.route("GET", f"{N}/notes/NOTE-001", {"label": "NOTE-001", "notices": [{"uid": "n1"}]})
        self.assertEqual(json.loads(self.run_api("notices", "NOTE-001").stdout), [{"uid": "n1"}])
        self.route("GET", f"{N}/items/STORY-001/notices", [{"uid": "n2"}])
        result = self.run_api("notices", "STORY-001", "--side", "item")
        self.assertEqual(json.loads(result.stdout), [{"uid": "n2"}])
        self.assertEqual(self.last()["query"], {"project": ["p1"]})
        self.route("POST", f"{N}/notices/n1/decide", {"notice": {}})
        self.run_api("decide", "n1", stdin='{"decision": "keep", "version": 1}')
        self.assertEqual(self.last()["body"], {"decision": "keep", "version": 1})

    def test_promote_resolves_item_labels_and_demote(self):
        self.viewer.add_label("p1", "EPIC-001", "u-epic")
        self.route("POST", f"{N}/notes/NOTE-001/promote", {"item": {"label": "TASK-005"}})
        body = ('{"version": 2, "type": "Task", "fields": {"area": "A", "goal": "G", "completion_criteria": "C", '
                '"parent": "EPIC-001", "required_for_parent": "Yes"}}')
        result = self.run_api("promote", "NOTE-001", stdin=body)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 2, "type": "Task", "fields": {
            "area": "A", "goal": "G", "completion_criteria": "C", "parent": "u-epic", "required_for_parent": True}})
        self.route("POST", f"{N}/items/STORY-001/demote", {"note": {"label": "NOTE-009"}})
        result = self.run_api("demote", "STORY-001", stdin='{"version": 3, "topic": "TOPIC-001"}')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["body"], {"project": "p1", "version": 3, "topic": "TOPIC-001"})

    def test_settings_can_only_be_read(self):
        self.route("GET", f"{N}/settings", {"max_topic_depth": 3, "review_days": 30})
        self.assertEqual(json.loads(self.run_api("settings").stdout), {"max_topic_depth": 3, "review_days": 30})
        sent = len(self.viewer.requests)
        self.assertEqual(self.run_api("settings", "--set", "review_days=5").returncode, 2)
        self.assertEqual(len(self.viewer.requests), sent)
        self.assertEqual({r["method"] for r in self.viewer.requests}, {"GET"})

    def test_server_errors_are_reported_with_code_and_conflict_hint(self):
        self.route("POST", f"{N}/notes/NOTE-001/keep",
                   {"code": "version_conflict", "message": "changed", "details": {}}, status=409)
        result = self.run_api("keep", "NOTE-001", "1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("HTTP 409 version_conflict", result.stderr)
        self.assertIn("never retry blindly", result.stderr)

    def test_bad_stdin_is_a_usage_error(self):
        result = self.run_api("create", stdin="[1]")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.writes(), [])

    def test_sources_lists_the_names_the_viewer_knows(self):
        self.viewer.add_project("misc", "Allgemein")
        result = self.run_api("sources")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["Project | Folder", f"project | {self.todo}", "Allgemein | -"])

    def test_source_option_addresses_the_notes_of_another_project(self):
        self.viewer.add_project("misc", "Allgemein")
        self.route("GET", f"{N}/index", {"topics": [], "notes": []})
        result = self.run_api("--source", "Allgemein", "topics")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last()["query"], {"projects": ["misc"]})
        self.assertEqual(self.writes(), [])

    def test_unknown_source_names_the_known_ones(self):
        self.viewer.add_project("misc", "Allgemein")
        result = self.run_api("--source", "allgemein", "topics")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown source 'allgemein' (known: project, Allgemein)", result.stderr)
        self.assertEqual([r["path"] for r in self.viewer.requests], [PROJECTS])

    def test_source_and_project_exclude_each_other(self):
        result = self.run_api("--source", "Misc", "--project", "x", "topics")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--source", result.stderr)
        self.assertEqual(self.viewer.requests, [])


if __name__ == "__main__":
    unittest.main()
