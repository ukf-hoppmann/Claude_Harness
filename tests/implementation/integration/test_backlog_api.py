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

ITEMS = f"{API}/backlog/items"


class BacklogApiTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name).resolve() / "project"
        self.todo = self.project / "docs" / "todo"
        self.todo.mkdir(parents=True)
        (self.todo / "TODO.md").write_text("x\n")
        self.viewer = FakeViewer()
        self.write_config(self.viewer.url)
        self.viewer.add_project("p1", "project", self.todo)
        self.viewer.routes[("GET", f"{API}/workspace/trash")] = (200, [])

    def tearDown(self):
        self.viewer.close()
        self._tmp.cleanup()

    def write_config(self, url, root=None, todo="true", extra=""):
        config = (root or self.project) / ".claude-harness" / "config.toml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(f'version = 1\n[modules]\ntodo = {todo}\n[todo]\napi_url = "{url}"\n{extra}')

    def write_subproject(self):
        self.write_config(self.viewer.url, extra='[projects]\nVariantFilter = "Plugins/VariantFilter"\n')
        sub = self.project / "Plugins" / "VariantFilter"
        self.write_config(self.viewer.url, root=sub)
        (sub / "docs" / "todo").mkdir(parents=True)
        (sub / "docs" / "todo" / "TODO.md").write_text("x\n")
        return sub / "docs" / "todo"

    def run_api(self, *args, stdin="", cwd=None):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "backlog_api.py"), *args],
            input=stdin, capture_output=True, text=True, timeout=30, cwd=cwd or self.project, env=env,
        )

    def last(self, method):
        return self.viewer.calls(method)[-1]

    def writes(self):
        return [r for r in self.viewer.requests if r["method"] != "GET"]

    def test_health(self):
        self.viewer.routes[("GET", f"{API}/core/health")] = (200, {"status": "ok"})
        result = self.run_api("health")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"status": "ok"', result.stdout)

    def test_unreachable_server_has_own_exit_code(self):
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        self.write_config(f"http://127.0.0.1:{port}{API}")
        result = self.run_api("health")
        self.assertEqual(result.returncode, 3)
        self.assertIn("not reachable", result.stderr)

    def test_index_uses_the_project_of_the_configured_backlog(self):
        text = "ID | Type | Status | Area | Title | Parent\nEPIC-001 | Epic | Open | Kern | Ä | -"
        self.viewer.routes[("GET", f"{API}/backlog/index")] = (200, {"text": text, "count": 1})
        result = self.run_api("index")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), text.splitlines())
        self.assertEqual(self.last("GET")["query"], {"projects": ["p1"]})
        self.assertEqual(self.writes(), [])

    def test_index_leaves_out_trashed_items_or_marks_them(self):
        text = ("ID | Type | Status | Area | Title | Parent\n"
                "STORY-001 | Story | Open | Kern | A | -\nTASK-001 | Task | Open | Kern | B | STORY-001")
        self.viewer.routes[("GET", f"{API}/backlog/index")] = (200, {"text": text, "count": 2})
        self.viewer.routes[("GET", f"{API}/workspace/trash")] = (200, [
            {"label": "TASK-001", "kind": "task"}, {"label": "STORY-001", "kind": "note"},
        ])
        lines = self.run_api("index").stdout.splitlines()
        self.assertEqual(lines, text.splitlines()[:2])
        lines = self.run_api("index", "--with-trash").stdout.splitlines()
        self.assertEqual(lines[2], "TASK-001 | Task | Open | Kern | B | STORY-001 (Papierkorb)")

    def test_show_marks_deleted_children_and_hints_at_unclosed_ones(self):
        item = {"label": "STORY-001", "children": [
            {"label": "TASK-001", "status": "Open", "deleted": True},
            {"label": "TASK-002", "status": "Completed", "deleted": False},
        ]}
        self.viewer.routes[("GET", f"{ITEMS}/STORY-001")] = (200, item)
        result = self.run_api("show", "STORY-001")
        children = json.loads(result.stdout)["children"]
        self.assertIn("Papierkorb", children[0]["note"])
        self.assertNotIn("note", children[1])
        self.assertIn("TASK-001 liegt im Papierkorb", result.stderr)

    def test_unregistered_backlog_has_own_exit_code_and_registers_nothing(self):
        self.viewer.projects.clear()
        self.viewer.add_project("other", "Other", self.project / "elsewhere")
        result = self.run_api("index")
        self.assertEqual(result.returncode, 4)
        self.assertIn("not registered", result.stderr)
        self.assertIn("register", result.stderr)
        self.assertEqual(self.writes(), [])

    def test_register_creates_the_project_with_a_mirror(self):
        self.viewer.projects.clear()
        result = self.run_api("register")
        self.assertEqual(result.returncode, 0, result.stderr)
        # The root project is named after the folder of its main checkout.
        self.assertEqual(self.last("POST")["body"], {
            "name": "project", "mirror_folder": str(self.todo), "mirror_enabled": True, "auto_sync": True,
        })
        self.assertIn("project", result.stdout)

    def test_register_refuses_an_already_registered_backlog(self):
        result = self.run_api("register")
        self.assertEqual(result.returncode, 2)
        self.assertIn("already registered as 'project'", result.stderr)
        self.assertEqual(self.writes(), [])

    def test_register_names_a_subproject_by_its_project_name(self):
        sub_todo = self.write_subproject()
        result = self.run_api("--project", "VariantFilter", "register")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last("POST")["body"]["name"], "VariantFilter")
        self.assertEqual(self.last("POST")["body"]["mirror_folder"], str(sub_todo))

    def test_subproject_backlog_by_project_name(self):
        sub_todo = self.write_subproject()
        self.viewer.add_project("p2", "VariantFilter", sub_todo)
        self.viewer.routes[("GET", f"{API}/backlog/index")] = (200, {"text": "ID", "count": 0})
        result = self.run_api("--project", "VariantFilter", "index")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last("GET")["query"], {"projects": ["p2"]})

    def test_sources_lists_the_names_the_viewer_knows(self):
        self.viewer.add_project("misc", "Allgemein")
        result = self.run_api("sources")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["Project | Folder", f"project | {self.todo}", "Allgemein | -"])
        self.assertEqual(self.writes(), [])

    def test_source_option_addresses_a_project_by_its_exact_name(self):
        self.viewer.add_project("misc", "Allgemein")
        self.viewer.routes[("GET", f"{API}/backlog/index")] = (200, {"text": "ID", "count": 0})
        result = self.run_api("--source", "Allgemein", "index")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last("GET")["query"], {"projects": ["misc"]})
        self.assertEqual(self.writes(), [])

    def test_unknown_source_names_the_known_ones_and_registers_nothing(self):
        self.viewer.add_project("misc", "Allgemein")
        result = self.run_api("--source", "allgemein", "index")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown source 'allgemein' (known: project, Allgemein)", result.stderr)
        self.assertEqual([r["path"] for r in self.viewer.requests], [PROJECTS])

    def test_source_and_project_exclude_each_other(self):
        self.write_subproject()
        result = self.run_api("--source", "Misc", "--project", "VariantFilter", "index")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--source", result.stderr)
        self.assertEqual(self.viewer.requests, [])

    def test_source_still_needs_the_todo_module_of_the_session_project(self):
        self.write_config(self.viewer.url, todo="false")
        result = self.run_api("--source", "Misc", "index")
        self.assertEqual(result.returncode, 2)
        self.assertIn("module todo is off", result.stderr)

    def test_unknown_project(self):
        self.write_subproject()
        result = self.run_api("--project", "Nope", "index")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown project 'Nope' (known: root, VariantFilter)", result.stderr)
        self.assertEqual(self.viewer.requests, [])

    def test_todo_module_off(self):
        self.write_config(self.viewer.url, todo="false")
        result = self.run_api("index")
        self.assertEqual(result.returncode, 2)
        self.assertIn("module todo is off", result.stderr)
        self.assertEqual(self.viewer.requests, [])

    def test_missing_todo_file_is_fine(self):
        (self.todo / "TODO.md").unlink()
        self.viewer.routes[("GET", f"{API}/backlog/index")] = (200, {"text": "ID", "count": 0})
        result = self.run_api("index")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_without_config(self):
        (self.project / ".claude-harness" / "config.toml").unlink()
        result = self.run_api("index")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no .claude-harness/config.toml", result.stderr)

    def test_show(self):
        self.viewer.routes[("GET", f"{ITEMS}/STORY-001")] = (200, {"label": "STORY-001", "version": 3})
        result = self.run_api("show", "STORY-001")
        self.assertEqual(json.loads(result.stdout), {"label": "STORY-001", "version": 3})
        self.assertEqual(self.last("GET")["query"], {"project": ["p1"]})

    def test_create_sends_project_type_and_fields_with_labels_resolved(self):
        self.viewer.add_label("p1", "EPIC-001", "u-epic")
        self.viewer.add_label("p1", "STORY-007", "u-dep")
        self.viewer.routes[("POST", ITEMS)] = (201, {"label": "STORY-002", "version": 1})
        payload = {"type": "Story", "title": "Neu „x“", "area": "A", "goal": "G", "completion_criteria": "C",
                   "parent": "EPIC-001", "required_for_parent": "Yes", "dependencies": ["STORY-007"]}
        result = self.run_api("create", stdin=json.dumps(payload, ensure_ascii=False))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last("POST")["body"], {"project": "p1", "type": "Story", "fields": {
            "title": "Neu „x“", "area": "A", "goal": "G", "completion_criteria": "C",
            "parent": "u-epic", "required_for_parent": True, "dependencies": ["u-dep"],
        }})

    def test_create_with_an_unknown_parent_label_writes_nothing(self):
        payload = {"type": "Story", "title": "T", "area": "A", "goal": "G", "completion_criteria": "C",
                   "parent": "EPIC-404"}
        result = self.run_api("create", stdin=json.dumps(payload))
        self.assertEqual(result.returncode, 1)
        self.assertIn("EPIC-404", result.stderr)
        self.assertEqual(self.writes(), [])

    def test_update_sends_integer_version_and_reports_conflict(self):
        self.viewer.routes[("PUT", f"{ITEMS}/STORY-001")] = (
            409, {"code": "version_conflict", "message": "Item changed.", "details": {"expected": 3}},
        )
        result = self.run_api("update", "STORY-001", "3", stdin='{"fields": {"status": "In progress"}}')
        self.assertEqual(result.returncode, 1)
        self.assertIn("HTTP 409 version_conflict: Item changed.", result.stderr)
        self.assertIn("read the item again", result.stderr)
        self.assertEqual(self.last("PUT")["body"], {"project": "p1", "version": 3,
                                                    "fields": {"status": "In progress"}})

    def test_update_resolves_labels_and_passes_resolution(self):
        self.viewer.add_label("p1", "EPIC-002", "u-epic2")
        self.viewer.routes[("PUT", f"{ITEMS}/STORY-001")] = (200, {"label": "STORY-001"})
        stdin = '{"fields": {"parent": "EPIC-002", "required_for_parent": "No", "dependencies": []}, "resolution": "R"}'
        result = self.run_api("update", "STORY-001", "3", stdin=stdin)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last("PUT")["body"], {"project": "p1", "version": 3, "resolution": "R", "fields": {
            "parent": "u-epic2", "required_for_parent": False, "dependencies": []}})

    def test_version_must_be_a_number(self):
        result = self.run_api("update", "STORY-001", "v1", stdin='{"fields": {}}')
        self.assertEqual(result.returncode, 2)
        self.assertIn("version", result.stderr)
        self.assertEqual(self.viewer.requests, [])

    def test_invalid_json_input(self):
        result = self.run_api("update", "STORY-001", "1", stdin="{kaputt")
        self.assertEqual(result.returncode, 2)
        self.assertIn("JSON", result.stderr)
        self.assertEqual(self.writes(), [])

    def test_note(self):
        self.viewer.routes[("POST", f"{ITEMS}/STORY-001/notes")] = (200, {"name": "n", "version": 2})
        entry = {"topic": "T", "decided": ["x"]}
        self.run_api("note", "STORY-001", stdin=json.dumps(entry))
        self.assertEqual(self.last("POST")["body"], {**entry, "project": "p1"})

    def show_route(self, identifier, item_type, *children):
        body = {"label": identifier, "type": item_type, "children": [
            {"label": label, "status": status, "deleted": deleted} for label, status, deleted in children]}
        self.viewer.routes[("GET", f"{ITEMS}/{identifier}")] = (200, body)
        self.viewer.routes[("POST", f"{ITEMS}/{identifier}/notes")] = (200, {"name": "n", "version": 2})
        self.viewer.routes[("PUT", f"{ITEMS}/{identifier}/documents/{identifier}_notes.md")] = (
            200, {"name": f"{identifier}_notes.md", "version": 3})

    def test_note_on_a_story_with_a_child_in_progress_gives_a_hint(self):
        self.show_route("STORY-001", "Story", ("TASK-002", "Open", False), ("TASK-003", "In progress", False))
        result = self.run_api("note", "STORY-001", stdin='{"topic": "T"}')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("TASK-003 is in progress", result.stderr)
        self.assertEqual(len(self.viewer.calls("POST")), 1)

    def test_put_doc_of_story_notes_gives_the_hint_but_a_spec_does_not(self):
        self.show_route("STORY-001", "Story", ("TASK-003", "In progress", False))
        self.viewer.routes[("PUT", f"{ITEMS}/STORY-001/documents/STORY-001_spec.md")] = (
            200, {"name": "STORY-001_spec.md", "version": 1})
        notes = self.run_api("put-doc", "STORY-001", "STORY-001_notes.md", "2", stdin="x")
        self.assertIn("TASK-003 is in progress", notes.stderr)
        spec = self.run_api("put-doc", "STORY-001", "STORY-001_spec.md", "1", stdin="x")
        self.assertEqual(spec.stderr, "")

    def test_note_gives_no_hint_without_a_child_in_progress(self):
        self.show_route("STORY-001", "Story", ("TASK-002", "Open", False), ("TASK-004", "In progress", True))
        self.assertEqual(self.run_api("note", "STORY-001", stdin='{"topic": "T"}').stderr, "")

    def test_note_on_a_task_gives_no_hint(self):
        self.show_route("TASK-002", "Task")
        self.assertEqual(self.run_api("note", "TASK-002", stdin='{"topic": "T"}').stderr, "")

    def test_note_is_still_written_when_the_lookup_fails(self):
        self.viewer.routes[("POST", f"{ITEMS}/STORY-001/notes")] = (200, {"name": "n", "version": 2})
        result = self.run_api("note", "STORY-001", stdin='{"topic": "T"}')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")

    STATE = f"{ITEMS}/STORY-001/notes/state"

    def test_state_prints_the_head_without_the_log(self):
        answer = {"name": "STORY-001_notes.md", "content": "- Goal/Status: g\n", "state": "current", "version": 4}
        self.viewer.routes[("GET", self.STATE)] = (200, answer)
        result = self.run_api("state", "STORY-001")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), answer)
        self.assertEqual(self.last("GET")["query"], {"project": ["p1"]})

    def test_entries_asks_for_the_last_ones(self):
        entries = [{"position": 3, "day": "2026-10-21", "topic": "T", "text": "## 2026-10-21 — T\n"}]
        self.viewer.routes[("GET", f"{ITEMS}/STORY-001/notes/entries")] = (200, entries)
        result = self.run_api("entries", "STORY-001", "--last", "2")
        self.assertEqual(json.loads(result.stdout), entries)
        self.assertEqual(self.last("GET")["query"], {"project": ["p1"], "last": ["2"]})

    def test_put_state_sends_the_text_and_shows_hints(self):
        hint = {"code": "notes_state_long", "message": "More than 15 points under - Decided:"}
        self.viewer.routes[("PUT", self.STATE)] = (200, {"state": "current", "version": 5, "hints": [hint]})
        result = self.run_api("put-state", "STORY-001", "4", stdin="- Goal/Status: g\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last("PUT")["body"], {"project": "p1", "content": "- Goal/Status: g\n", "version": 4})
        self.assertIn("hint: More than 15 points under - Decided:", result.stderr)
        self.assertEqual(json.loads(result.stdout)["version"], 5)

    def test_confirm_state_sends_only_the_version(self):
        self.viewer.routes[("POST", f"{self.STATE}/confirm")] = (200, {"state": "current", "version": 5, "hints": []})
        result = self.run_api("confirm-state", "STORY-001", "4")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last("POST")["body"], {"project": "p1", "version": 4})
        self.assertEqual(result.stderr, "")

    def test_state_versions_are_checked_before_any_request(self):
        for command in ("put-state", "confirm-state"):
            result = self.run_api(command, "STORY-001", "v1", stdin="x")
            self.assertEqual(result.returncode, 2)
        self.assertEqual(self.viewer.requests, [])

    def test_note_passes_a_new_head_and_shows_hints(self):
        hint = {"code": "notes_state_stale", "message": "The head is stale."}
        self.viewer.routes[("POST", f"{ITEMS}/STORY-001/notes")] = (200, {"name": "n", "hints": [hint]})
        entry = {"topic": "T", "decided": ["x"], "state": "- Goal/Status: g\n", "state_version": 4}
        result = self.run_api("note", "STORY-001", stdin=json.dumps(entry))
        self.assertEqual(self.last("POST")["body"], {**entry, "project": "p1"})
        self.assertIn("hint: The head is stale.", result.stderr)

    def test_put_doc_of_notes_shows_hints_of_the_server(self):
        hint = {"code": "notes_history_rewritten", "message": "An earlier entry was changed."}
        path = f"{ITEMS}/STORY-001/documents/STORY-001_notes.md"
        self.viewer.routes[("PUT", path)] = (200, {"name": "STORY-001_notes.md", "version": 3, "hints": [hint]})
        result = self.run_api("put-doc", "STORY-001", "STORY-001_notes.md", "2", stdin="x")
        self.assertIn("hint: An earlier entry was changed.", result.stderr)

    def test_viewer_without_head_support_gets_a_clear_message(self):
        result = self.run_api("state", "STORY-001")
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not support the notes head", result.stderr)

    def run_in_session(self, *args, stdin=""):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_CODE_SESSION_ID="s1",
                   CLAUDE_PLUGIN_DATA=str(Path(self._tmp.name) / "data"))
        return subprocess.run([sys.executable, str(SCRIPTS / "backlog_api.py"), *args], input=stdin,
                              capture_output=True, text=True, timeout=30, cwd=self.project, env=env)

    def test_session_remembers_changed_notes_and_active_items(self):
        from state import read_items
        self.viewer.routes[("POST", f"{ITEMS}/STORY-001/notes")] = (200, {"name": "n"})
        self.viewer.routes[("PUT", f"{ITEMS}/TASK-002")] = (200, {"label": "TASK-002"})
        self.viewer.routes[("GET", f"{ITEMS}/TASK-003/documents/TASK-003_spec.md")] = (
            200, {"name": "TASK-003_spec.md", "content": "x", "version": 1})
        self.viewer.routes[("GET", f"{ITEMS}/TASK-003/documents/TASK-003_notes.md")] = (
            200, {"name": "TASK-003_notes.md", "content": "x", "version": 1})
        self.run_in_session("note", "STORY-001", stdin='{"topic": "T"}')
        self.run_in_session("update", "TASK-002", "1", stdin='{"fields": {"status": "In progress"}}')
        self.run_in_session("update", "TASK-004", "1", stdin='{"fields": {"status": "Open"}}')
        self.run_in_session("doc", "TASK-003", "TASK-003_spec.md")
        self.run_in_session("doc", "TASK-003", "TASK-003_notes.md")
        data = Path(self._tmp.name) / "data"
        old = os.environ.get("CLAUDE_PLUGIN_DATA")
        os.environ["CLAUDE_PLUGIN_DATA"] = str(data)
        try:
            self.assertEqual(read_items("s1", "notes"), {("root", "STORY-001")})
            self.assertEqual(read_items("s1", "active"), {("root", "TASK-002"), ("root", "TASK-003")})
        finally:
            if old is None:
                del os.environ["CLAUDE_PLUGIN_DATA"]
            else:
                os.environ["CLAUDE_PLUGIN_DATA"] = old

    def test_nothing_is_remembered_without_a_session(self):
        self.viewer.routes[("POST", f"{ITEMS}/STORY-001/notes")] = (200, {"name": "n"})
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CODE_SESSION_ID"}
        env.update(CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(Path(self._tmp.name) / "data"))
        result = subprocess.run([sys.executable, str(SCRIPTS / "backlog_api.py"), "note", "STORY-001"],
                                input='{"topic": "T"}', capture_output=True, text=True, timeout=30,
                                cwd=self.project, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((Path(self._tmp.name) / "data").exists())

    def test_doc_prints_version_and_content(self):
        self.viewer.routes[("GET", f"{ITEMS}/STORY-001/documents/STORY-001_notes.md")] = (
            200, {"name": "STORY-001_notes.md", "kind": "notes", "content": "# Notizen\n\nText\n", "version": 7},
        )
        result = self.run_api("doc", "STORY-001", "STORY-001_notes.md")
        self.assertEqual(result.stdout, "version: 7\n\n# Notizen\n\nText\n")
        self.assertEqual(self.last("GET")["query"], {"project": ["p1"]})

    def test_put_doc_sends_raw_content(self):
        path = f"{ITEMS}/STORY-001/documents/STORY-001_spec.md"
        self.viewer.routes[("PUT", path)] = (200, {"name": "STORY-001_spec.md", "version": 1})
        self.run_api("put-doc", "STORY-001", "STORY-001_spec.md", "new", stdin="# Spec\n\n„Text“\n")
        self.assertEqual(self.viewer.calls("PUT")[0]["body"],
                         {"project": "p1", "content": "# Spec\n\n„Text“\n", "version": None})
        self.run_api("put-doc", "STORY-001", "STORY-001_spec.md", "1", "--summary", "Kurz.", stdin="x")
        self.assertEqual(self.viewer.calls("PUT")[1]["body"],
                         {"project": "p1", "content": "x", "version": 1, "summary": "Kurz."})

    def test_delete_goes_to_the_trash_by_uid(self):
        self.viewer.add_label("p1", "EPIC-001", "u-epic")
        self.viewer.routes[("DELETE", f"{API}/workspace/elements/u-epic")] = (200, {"deleted": ["u-epic"]})
        result = self.run_api("delete", "EPIC-001", "3", "--cascade")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last("DELETE")["query"], {"version": ["3"], "cascade": ["true"]})

    def test_restore_from_the_trash_by_uid(self):
        self.viewer.add_label("p1", "EPIC-001", "u-epic", deleted=True)
        self.viewer.routes[("POST", f"{API}/workspace/trash/restore")] = (200, {"restored": ["u-epic"]})
        result = self.run_api("restore", "EPIC-001")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last("POST")["body"], {"uids": ["u-epic"]})

    def test_trash_lists_only_backlog_items_of_the_project(self):
        self.viewer.routes[("GET", f"{API}/workspace/trash")] = (200, [
            {"label": "STORY-003", "kind": "story"}, {"label": "NOTE-001", "kind": "note"},
        ])
        result = self.run_api("trash")
        self.assertEqual(json.loads(result.stdout), [{"label": "STORY-003", "kind": "story"}])
        self.assertEqual(self.last("GET")["query"], {"projects": ["p1"]})

    def test_retype_posts_version_and_type(self):
        self.viewer.routes[("POST", f"{ITEMS}/TASK-004/retype")] = (200, {"new_label": "STORY-009"})
        result = self.run_api("retype", "TASK-004", "2", "Story")
        self.assertEqual(self.last("POST")["body"], {"project": "p1", "version": 2, "type": "Story"})
        self.assertIn("STORY-009", result.stdout)

    def test_move_resolves_the_parent_and_moves_to_the_top_with_a_dash(self):
        self.viewer.add_label("p1", "EPIC-002", "u-epic2")
        self.viewer.routes[("POST", f"{ITEMS}/STORY-001/move")] = (200, {"label": "STORY-001"})
        self.run_api("move", "STORY-001", "4", "EPIC-002", "--position", "0")
        self.assertEqual(self.last("POST")["body"], {"project": "p1", "version": 4, "parent": "u-epic2",
                                                     "position": 0})
        self.run_api("move", "STORY-001", "5", "-")
        self.assertEqual(self.last("POST")["body"], {"project": "p1", "version": 5, "parent": None})

    def test_reopen_reopens_the_item_and_its_closed_ancestors(self):
        self.viewer.routes[("POST", f"{ITEMS}/STORY-001/reopen")] = (200, {"reopened": ["EPIC-001", "STORY-001"]})
        result = self.run_api("reopen", "STORY-001")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.last("POST")["body"], {"project": "p1"})

    def test_areas(self):
        self.viewer.routes[("GET", f"{API}/backlog/areas")] = (200, {"areas": ["A", "B"]})
        result = self.run_api("areas")
        self.assertEqual(result.stdout.splitlines(), ["A", "B"])

    def test_no_purge_command(self):
        result = self.run_api("purge", "EPIC-001", "1")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.writes(), [])

    def test_worktree_uses_the_project_of_the_main_checkout(self):
        def git(*args, cwd=self.project):
            subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)

        git("init", "-q", "-b", "main")
        git("add", "-A")
        git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init")
        worktree = self.project / ".claude" / "worktrees" / "w1"
        git("worktree", "add", "-q", "-b", "w1", str(worktree))
        self.viewer.routes[("GET", f"{API}/backlog/index")] = (200, {"text": "ID", "count": 0})
        result = self.run_api("index", cwd=worktree)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.writes(), [])
        self.assertEqual(self.last("GET")["query"], {"projects": ["p1"]})


if __name__ == "__main__":
    unittest.main()
