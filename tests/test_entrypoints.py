from __future__ import annotations

import runpy
import sys
import types

from fastapi.testclient import TestClient

from app.main import create_app


def test_favicon_route_serves_file_response():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/favicon.ico")

    assert resp.status_code == 200
    # A non-empty icon file should be served.
    assert len(resp.content) > 0


def test_root_main_module_can_run_as_script_without_starting_server(monkeypatch):
    # Exercise the `if __name__ == '__main__'` block in [`main.py`](main.py:1)
    # without actually starting a Uvicorn server.
    fake_uvicorn = types.ModuleType("uvicorn")
    fake_uvicorn.run = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, "uvicorn", fake_uvicorn)

    runpy.run_module("main", run_name="__main__")

