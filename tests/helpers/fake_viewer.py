import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit

API = "/api"
PROJECTS = f"{API}/workspace/projects"


class FakeViewer:
    """A tiny stand-in for the ToDo-Viewer API that records requests and answers from a route table.

    Projects (`GET`/`POST /workspace/projects`) and label lookups (`GET /workspace/projects/<uid>/labels/<label>`)
    are answered from `projects` and `labels`; everything else from `routes`.
    """

    def __init__(self):
        self.requests: list[dict] = []
        self.sources: list[dict] = []
        self.projects: list[dict] = []
        # (project uid, label) -> element as resolve_label answers it.
        self.labels: dict[tuple[str, str], dict] = {}
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
                path = unquote(url.path)
                viewer.requests.append(
                    {"method": self.command, "path": path, "query": parse_qs(url.query), "body": body}
                )
                status, answer = viewer.answer(self.command, path, body)
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

    def add_project(self, uid, name, folder=None):
        project = {"uid": uid, "name": name, "mirror_folder": None if folder is None else str(folder),
                   "mirror_enabled": folder is not None, "version": 1}
        self.projects.append(project)
        return project

    def add_label(self, project_uid, label, uid, deleted=False):
        self.labels[(project_uid, label)] = {"uid": uid, "kind": label.split("-")[0].lower(), "label": label,
                                             "version": 1, "deleted": deleted}

    def answer(self, method, path, body):
        if (method, path) == ("GET", f"{API}/sources"):
            return 200, self.sources
        if (method, path) == ("POST", f"{API}/sources"):
            source = {"id": "new1", "project": body.get("project") or "p", "path": body["path"]}
            self.sources.append(source)
            return 200, source
        if (method, path) == ("GET", PROJECTS):
            return 200, self.projects
        if (method, path) == ("POST", PROJECTS):
            return 201, self.add_project("new-uid", body["name"], body.get("mirror_folder"))
        parts = path.removeprefix(PROJECTS + "/").split("/")
        if method == "GET" and path.startswith(PROJECTS + "/") and len(parts) == 3 and parts[1] == "labels":
            element = self.labels.get((parts[0], parts[2]))
            if element is None:
                return 404, {"code": "not_found", "message": f"Label {parts[2]} gibt es nicht", "details": {}}
            return 200, element
        return self.routes.get((method, path), (404, {"code": "not_found", "message": "no route"}))

    def calls(self, method):
        return [r for r in self.requests if r["method"] == method]

    def close(self):
        self.server.shutdown()
        self.server.server_close()
