from __future__ import annotations

import os

from fastapi.testclient import TestClient

from app.main import create_app


def test_mmsp_endpoint_responds():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/.well-known/mmsp.json")

    assert resp.status_code == 200
    assert "application/mmsp+json" in resp.headers.get("content-type", "").lower()


def test_mmsp_manifest_required_fields():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/.well-known/mmsp.json")
    body = resp.json()

    assert body["mmsp"] == "1.0"
    assert body["title"] == "Crank The Code"
    assert body["feed_url"].endswith("/.well-known/mmsp.json")
    assert body["id"] == body["feed_url"]
    assert isinstance(body["items"], list)
    assert body["language"] == "en"
    assert len(body["authors"]) >= 1
    assert body["authors"][0]["name"] == "Oliver Ernster"


def test_mmsp_manifest_absolute_feed_url():
    os.environ["SITE_URL"] = "https://www.crankthecode.com/"
    try:
        app = create_app()
        client = TestClient(app)

        resp = client.get("/.well-known/mmsp.json")
        body = resp.json()

        assert body["feed_url"] == "https://www.crankthecode.com/.well-known/mmsp.json"
        assert body["id"] == "https://www.crankthecode.com/.well-known/mmsp.json"
    finally:
        os.environ.pop("SITE_URL", None)


def test_mmsp_items_have_required_fields():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/.well-known/mmsp.json")
    items = resp.json()["items"]

    assert len(items) > 0
    for item in items:
        assert "id" in item
        assert item["type"] == "article"
        assert "title" in item
        assert "url" in item
        assert "published" in item
        assert item["url"].startswith("http")
        assert "T" in item["published"]
        assert "+" in item["published"] or item["published"].endswith("Z")


def test_mmsp_items_have_absolute_urls():
    os.environ["SITE_URL"] = "https://www.crankthecode.com/"
    try:
        app = create_app()
        client = TestClient(app)

        resp = client.get("/.well-known/mmsp.json")
        items = resp.json()["items"]

        for item in items:
            assert item["url"].startswith("https://www.crankthecode.com/posts/")
    finally:
        os.environ.pop("SITE_URL", None)


def test_mmsp_excludes_hidden_and_special_posts():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/.well-known/mmsp.json")
    items = resp.json()["items"]

    slugs = [item["url"].rstrip("/").split("/")[-1] for item in items]
    assert "about-me" not in slugs
    assert "start-here" not in slugs
    assert "portfolio" not in slugs


def test_mmsp_max_twenty_items():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/.well-known/mmsp.json")
    items = resp.json()["items"]

    assert len(items) <= 20


def test_mmsp_poll_guidance_present():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/.well-known/mmsp.json")
    body = resp.json()

    poll = body.get("poll", {})
    assert poll.get("min", 0) >= 300
