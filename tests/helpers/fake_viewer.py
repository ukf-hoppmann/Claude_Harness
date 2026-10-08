import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

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
            source = {"id": "new1", "project": body.get("project") or "p", "path": body["path"]}
            self.sources.append(source)
            return 200, source
        return self.routes.get((method, path), (404, {"code": "not_found", "message": "no route"}))

    def calls(self, method):
        return [r for r in self.requests if r["method"] == method]

    def close(self):
        self.server.shutdown()
        self.server.server_close()
