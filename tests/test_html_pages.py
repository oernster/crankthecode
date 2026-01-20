from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def test_homepage_renders():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/")

    assert resp.status_code == 200
    assert "Featured Projects" in resp.text


def test_posts_index_renders_and_supports_query_filter():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/posts")
    assert resp.status_code == 200
    assert "All posts" in resp.text

    filtered = client.get("/posts", params={"q": "python"})
    assert filtered.status_code == 200
    assert "All posts" in filtered.text


def test_about_page_renders():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/about")

    assert resp.status_code == 200


def test_help_page_renders_and_is_noindex_and_masks_email():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/help")

    assert resp.status_code == 200
    assert "You Clicked Help" in resp.text
    assert '<meta name="robots" content="noindex"' in resp.text
    assert "[enable JavaScript]" in resp.text
    # Ensure we don't include a literal mailto in the static HTML.
    assert "mailto:" not in resp.text


def test_unknown_post_returns_404_html():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/posts/definitely-not-a-real-post")

    assert resp.status_code == 404
    assert "Post Not Found" in resp.text

