from __future__ import annotations

import os
import xml.etree.ElementTree as ET

from fastapi.testclient import TestClient

from app.main import create_app


def test_retired_topic_surfaces_redirect_to_essays():
    app = create_app()
    client = TestClient(app, base_url="http://localhost")

    for path in (
        "/topics",
        "/topics/architecture",
        "/topics/cto-operating-model",
        "/topics/decision-systems",
        "/topics/organisational-structure",
        "/topics/structural-design",
        "/decision-architecture",
    ):
        resp = client.get(path, follow_redirects=False)
        assert resp.status_code == 301, path
        assert resp.headers.get("location") == "/essays", path


def test_about_author_alias_redirects_to_about():
    app = create_app()
    # Use localhost to bypass canonical-host middleware so we test the route handler.
    client = TestClient(app, base_url="http://localhost")

    resp = client.get("/about/oliver-ernster", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers.get("location") == "/about"


def test_start_here_post_includes_orientation_links_to_topics_and_about():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/posts/start-here")
    assert resp.status_code == 200
    # Orientation / Explore navigation moved to /explore; Start Here should
    # remain clean.
    assert 'href="/topics"' not in resp.text
    assert 'aria-label="Orientation"' not in resp.text
    assert 'aria-label="Explore themes"' not in resp.text


def test_sitemap_includes_essays_and_build_log_but_no_retired_pages():
    os.environ["SITE_URL"] = "https://example.com"
    try:
        app = create_app()
        client = TestClient(app)

        resp = client.get("/sitemap.xml")
        assert resp.status_code == 200

        root = ET.fromstring(resp.text)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [elem.text for elem in root.findall("sm:url/sm:loc", ns) if elem.text]

        assert "https://example.com/essays" in locs
        assert "https://example.com/build-log" in locs
        assert "https://example.com/patterns" in locs
        # Alias route should be discoverable but canonical remains /about.
        assert "https://example.com/about/oliver-ernster" in locs

        # The retired taxonomy no longer appears.
        assert "https://example.com/topics" not in locs
        assert "https://example.com/decision-architecture" not in locs
        assert not any("/topics/" in loc for loc in locs)
    finally:
        os.environ.pop("SITE_URL", None)
