from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def test_canonical_redirect_middleware_allows_localhost_without_redirect():
    """Local dev should not be forced onto https://www.crankthecode.com."""

    app = create_app()
    client = TestClient(app, base_url="http://localhost")

    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 200


def test_canonical_redirect_middleware_redirects_http_apex_to_https_www():
    app = create_app()
    client = TestClient(app, base_url="http://crankthecode.com")

    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers["location"] == "https://www.crankthecode.com/"


def test_canonical_redirect_middleware_preserves_path_and_query_on_redirect():
    app = create_app()
    client = TestClient(app, base_url="http://www.crankthecode.com")

    resp = client.get("/posts?q=python", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers["location"] == "https://www.crankthecode.com/posts?q=python"

