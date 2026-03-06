from __future__ import annotations

import json
import os
import re
import xml.etree.ElementTree as ET

from fastapi.testclient import TestClient

from app.main import create_app


def test_topics_index_renders_and_includes_decision_systems_link():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/topics")
    assert resp.status_code == 200
    assert "Topics" in resp.text
    # One stable hub slug that exists in the corpus.
    assert 'href="/topics/decision-systems"' in resp.text


def test_topic_hub_page_lists_posts_and_emits_jsonld_and_canonical():
    os.environ["SITE_URL"] = "https://example.com"
    try:
        app = create_app()
        client = TestClient(app)

        resp = client.get("/topics/decision-systems")
        assert resp.status_code == 200

        html = resp.text
        assert '<link rel="canonical" href="https://example.com/topics/decision-systems"' in html
        assert "application/ld+json" in html

        # Ensure at least one known decision-systems leadership post is listed.
        assert 'href="/posts/lead1"' in html

        # JSON-LD should be parseable.
        blocks = re.findall(
            r'<script\s+type="application/ld\+json">(.*?)</script>',
            html,
            flags=re.S,
        )
        assert blocks
        for raw in blocks:
            json.loads(raw)
    finally:
        os.environ.pop("SITE_URL", None)


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
    assert 'href="/topics"' in resp.text
    assert 'href="/about"' in resp.text


def test_sitemap_includes_topics_and_topic_hub_pages():
    os.environ["SITE_URL"] = "https://example.com"
    try:
        app = create_app()
        client = TestClient(app)

        resp = client.get("/sitemap.xml")
        assert resp.status_code == 200

        root = ET.fromstring(resp.text)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [elem.text for elem in root.findall("sm:url/sm:loc", ns) if elem.text]

        assert "https://example.com/topics" in locs
        assert "https://example.com/topics/decision-systems" in locs
        # Alias route should be discoverable but canonical remains /about.
        assert "https://example.com/about/oliver-ernster" in locs
    finally:
        os.environ.pop("SITE_URL", None)

