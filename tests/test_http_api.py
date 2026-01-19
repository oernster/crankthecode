from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def test_api_posts_endpoint_responds():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/api/posts")

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
