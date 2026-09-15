import json
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from threading import Thread

import pytest

from app import Handler


@pytest.fixture(scope="module")
def server_address():
    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield server.server_address
        finally:
            server.shutdown()
            thread.join(timeout=5)


@pytest.mark.parametrize(
    ("path", "status", "payload"),
    [
        ("/", 200, {"message": "Hello, world!"}),
        ("/health", 200, {"status": "ok"}),
        ("/health?check=ready", 200, {"status": "ok"}),
        ("/missing", 404, {"error": "Not found"}),
    ],
)
def test_get(server_address, path, status, payload):
    connection = HTTPConnection(*server_address, timeout=5)
    try:
        connection.request("GET", path)
        response = connection.getresponse()
        body = response.read()
        assert response.status == status
        assert response.getheader("Content-Type") == "application/json; charset=utf-8"
        assert int(response.getheader("Content-Length")) == len(body)
        assert json.loads(body) == payload
    finally:
        connection.close()
