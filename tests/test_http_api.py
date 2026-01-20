from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def test_api_posts_endpoint_responds():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/api/posts")

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_api_get_post_returns_404_for_missing_slug():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/api/posts/definitely-not-a-real-post")

    assert resp.status_code == 404
    assert resp.json().get("detail") == "Post not found"


def test_api_get_post_returns_content_for_known_slug():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/api/posts/trainer")

    assert resp.status_code == 200
    body = resp.json()
    assert body["slug"] == "trainer"
    assert body["title"]
    assert isinstance(body.get("tags"), list)
    assert "content_html" in body
