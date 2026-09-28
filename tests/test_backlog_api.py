import json
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from helpers import SCRIPTS

API = "/api/v2"


class FakeViewer:
    """A tiny stand-in for the ToDo-Viewer API that records requests and answers from a route table."""

    def __init__(self):
        self.requests: list[dict] = []
        self.sources: list[dict] = []
        # (method, path) -> (status, body); path without query string.
        self.routes: dict[tuple[str, str], tuple[int, object]] = {}
        viewer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def _handle(self):
                url = urlsplit(self.path)
                length = int(self.headers.get("Content-Length") or 0)
                body = json.loads(self.rfile.read(length)) if length else None
                viewer.requests.append(
                    {"method": self.command, "path": url.path, "query": parse_qs(url.query), "body": body}
                )
                status, answer = viewer.answer(self.command, url.path, body)
                data = json.dumps(answer).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            do_GET = do_POST = do_PATCH = do_PUT = do_DELETE = _handle

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}{API}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def answer(self, method, path, body):
        if (method, path) == ("GET", f"{API}/sources"):
            return 200, self.sources
        if (method, path) == ("POST", f"{API}/sources"):
            source = {"id": "new1", "project": "p", "path": body["path"]}
            self.sources.append(source)
            return 200, source
        return self.routes.get((method, path), (404, {"code": "not_found", "message": "no route"}))

    def calls(self, method):
        return [r for r in self.requests if r["method"] == method]

    def close(self):
        self.server.shutdown()
        self.server.server_close()


class BacklogApiTest(unittest.TestCase):
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

    def write_config(self, url):
        config = self.project / ".claude-harness" / "config.toml"
        config.parent.mkdir(exist_ok=True)
        config.write_text(f'version = 1\n[modules]\ntodo = true\n[todo]\napi_url = "{url}"\n')

    def run_api(self, *args, stdin="", folder=None):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "backlog_api.py"), str(folder or self.todo), *args],
            input=stdin, capture_output=True, text=True, timeout=30,
        )

    def test_health(self):
        self.viewer.routes[("GET", f"{API}/health")] = (200, {"status": "ok", "api": "2"})
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

    def test_index_uses_the_source_of_the_backlog_folder(self):
        self.viewer.routes[("GET", f"{API}/index")] = (200, {"items": [
            {"source_id": "src1", "id": "EPIC-001", "type": "Epic", "status": "Open", "title": "Ä", "parent": None},
            {"source_id": "src1", "id": "STORY-001", "type": "Story", "status": "Open", "title": "B",
             "parent": "EPIC-001"},
        ]})
        result = self.run_api("index")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), [
            "ID | Type | Status | Title | Parent",
            "EPIC-001 | Epic | Open | Ä | -",
            "STORY-001 | Story | Open | B | EPIC-001",
        ])
        self.assertEqual(self.viewer.calls("GET")[-1]["query"], {"source_id": ["src1"]})
        self.assertEqual(self.viewer.calls("POST"), [])

    def test_missing_source_is_registered(self):
        self.viewer.sources.clear()
        self.viewer.routes[("GET", f"{API}/index")] = (200, {"items": []})
        result = self.run_api("index")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.viewer.calls("POST")[0]["body"], {"path": str(self.todo)})
        self.assertIn("registered", result.stderr)
        self.assertEqual(self.viewer.calls("GET")[-1]["query"], {"source_id": ["new1"]})

    def test_show(self):
        self.viewer.routes[("GET", f"{API}/items/src1/STORY-001")] = (200, {"id": "STORY-001", "version": "v1"})
        result = self.run_api("show", "STORY-001")
        self.assertEqual(json.loads(result.stdout), {"id": "STORY-001", "version": "v1"})

    def test_create_adds_source_id(self):
        self.viewer.routes[("POST", f"{API}/items")] = (201, {"id": "STORY-002", "version": "v1"})
        payload = {"type": "Story", "title": "Neu „x“", "area": "A", "goal": "G", "completion_criteria": "C"}
        result = self.run_api("create", stdin=json.dumps(payload, ensure_ascii=False))
        self.assertEqual(result.returncode, 0, result.stderr)
        body = [r for r in self.viewer.calls("POST") if r["path"] == f"{API}/items"][0]["body"]
        self.assertEqual(body, {**payload, "source_id": "src1"})

    def test_update_sends_version_and_reports_conflict(self):
        self.viewer.routes[("PATCH", f"{API}/items/src1/STORY-001")] = (
            409, {"code": "version_conflict", "message": "Item changed.", "details": {"id": "STORY-001"}},
        )
        result = self.run_api("update", "STORY-001", "v1", stdin='{"fields": {"status": "In progress"}}')
        self.assertEqual(result.returncode, 1)
        self.assertIn("HTTP 409 version_conflict: Item changed.", result.stderr)
        self.assertIn("read the item again", result.stderr)
        self.assertEqual(
            self.viewer.calls("PATCH")[0]["body"], {"version": "v1", "fields": {"status": "In progress"}}
        )

    def test_invalid_json_input(self):
        result = self.run_api("update", "STORY-001", "v1", stdin="{kaputt")
        self.assertEqual(result.returncode, 2)
        self.assertIn("JSON", result.stderr)
        self.assertEqual(self.viewer.calls("PATCH"), [])

    def test_note(self):
        self.viewer.routes[("POST", f"{API}/items/src1/STORY-001/notes")] = (200, {"name": "n", "version": "v2"})
        entry = {"topic": "T", "decided": ["x"]}
        self.run_api("note", "STORY-001", stdin=json.dumps(entry))
        self.assertEqual(self.viewer.calls("POST")[-1]["body"], entry)

    def test_doc_prints_version_and_content(self):
        self.viewer.routes[("GET", f"{API}/items/src1/STORY-001/documents/STORY-001_notes.md")] = (
            200, {"name": "STORY-001_notes.md", "kind": "notes", "content": "# Notizen\n\nText\n", "version": "v7"},
        )
        result = self.run_api("doc", "STORY-001", "STORY-001_notes.md")
        self.assertEqual(result.stdout, "version: v7\n\n# Notizen\n\nText\n")

    def test_put_doc_sends_raw_content(self):
        path = f"{API}/items/src1/STORY-001/documents/STORY-001_spec.md"
        self.viewer.routes[("PUT", path)] = (200, {"name": "STORY-001_spec.md", "version": "v1"})
        self.run_api("put-doc", "STORY-001", "STORY-001_spec.md", "new", stdin="# Spec\n\n„Text“\n")
        self.assertEqual(self.viewer.calls("PUT")[0]["body"], {"content": "# Spec\n\n„Text“\n", "version": None})
        self.run_api("put-doc", "STORY-001", "STORY-001_spec.md", "v1", "--summary", "Kurz.", stdin="x")
        self.assertEqual(self.viewer.calls("PUT")[1]["body"], {"content": "x", "version": "v1", "summary": "Kurz."})

    def test_delete_and_restore(self):
        self.viewer.routes[("DELETE", f"{API}/items/src1/EPIC-001")] = (200, [])
        self.viewer.routes[("POST", f"{API}/trash/src1/EPIC-001/restore")] = (200, [])
        self.run_api("delete", "EPIC-001", "v3", "--cascade")
        self.assertEqual(self.viewer.calls("DELETE")[0]["query"], {"version": ["v3"], "cascade": ["true"]})
        self.run_api("restore", "EPIC-001", "v4")
        self.assertEqual(self.viewer.calls("POST")[-1]["body"], {"version": "v4"})

    def test_no_purge_command(self):
        result = self.run_api("purge", "EPIC-001", "v1")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.viewer.calls("DELETE"), [])

    def test_worktree_folder_uses_the_main_checkout_source(self):
        def git(*args, cwd=self.project):
            subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)

        git("init", "-q", "-b", "main")
        (self.todo / "TODO.md").write_text("x\n")
        git("add", "-A")
        git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init")
        worktree = self.project / ".claude" / "worktrees" / "w1"
        git("worktree", "add", "-q", "-b", "w1", str(worktree))
        self.viewer.routes[("GET", f"{API}/index")] = (200, {"items": []})
        result = self.run_api("index", folder=worktree / "docs" / "todo")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.viewer.calls("POST"), [])
        self.assertEqual(self.viewer.calls("GET")[-1]["query"], {"source_id": ["src1"]})


if __name__ == "__main__":
    unittest.main()
