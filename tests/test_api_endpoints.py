from __future__ import annotations

from fastapi.testclient import TestClient

from app.http.deps import get_blog_service
from app.main import create_app
from tests.test_support import make_fake_blog_service


def test_api_list_posts_returns_summaries():
    app = create_app()
    app.dependency_overrides[get_blog_service] = make_fake_blog_service
    client = TestClient(app)

    resp = client.get("/api/posts")

    assert resp.status_code == 200
    payload = resp.json()
    assert isinstance(payload, list)
    assert payload[0]["slug"] == "hello"
    assert payload[0]["summary_html"].startswith("<p>")


def test_api_get_post_returns_detail_and_404_for_unknown():
    app = create_app()
    app.dependency_overrides[get_blog_service] = make_fake_blog_service
    client = TestClient(app)

    ok = client.get("/api/posts/hello")
    assert ok.status_code == 200
    assert ok.json()["content_html"].startswith("<h1>")

    missing = client.get("/api/posts/does-not-exist")
    assert missing.status_code == 404
    assert missing.json()["detail"] == "Post not found"


def test_api_get_post_meta_builds_og_fields_and_404_for_unknown():
    app = create_app()
    app.dependency_overrides[get_blog_service] = make_fake_blog_service
    client = TestClient(app)

    ok = client.get("/api/posts/hello/meta")
    assert ok.status_code == 200
    meta = ok.json()
    assert meta["og_title"].startswith("Hello")
    assert meta["og_description"]
    assert meta["og_image"].startswith("http")
    assert meta["og_url"].endswith("/posts/hello")

    missing = client.get("/api/posts/does-not-exist/meta")
    assert missing.status_code == 404
    assert missing.json()["detail"] == "Post not found"

