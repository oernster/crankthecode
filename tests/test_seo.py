from __future__ import annotations

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from fastapi.testclient import TestClient

from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
from app.http.seo import build_meta_description
from app.main import create_app


def test_post_page_includes_meta_description_canonical_and_jsonld():
    os.environ["SITE_URL"] = "https://example.com"
    try:
        repo = FilesystemPostsRepository(posts_dir=Path("posts"))
        md = repo.get_post("trainer")
        assert md is not None

        expected = build_meta_description(md.blurb, fallback=md.one_liner, default="")
        assert expected

        app = create_app()
        client = TestClient(app)

        resp = client.get("/posts/trainer")
        assert resp.status_code == 200

        html = resp.text
        assert f'<link rel="canonical" href="https://example.com/posts/trainer"' in html
        assert f'<meta name="description" content="{expected}"' in html

        # JSON-LD should be present and identify the post.
        assert "application/ld+json" in html
        assert '"@type":"BlogPosting"' in html
        assert '"name":"Oliver Ernster"' in html
        assert '"mainEntityOfPage":"https://example.com/posts/trainer"' in html
    finally:
        os.environ.pop("SITE_URL", None)


def test_sitemap_lists_main_pages_and_posts():
    os.environ["SITE_URL"] = "https://example.com"
    try:
        app = create_app()
        client = TestClient(app)

        resp = client.get("/sitemap.xml")
        assert resp.status_code == 200
        assert "xml" in resp.headers.get("content-type", "").lower()

        root = ET.fromstring(resp.text)

        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [elem.text for elem in root.findall("sm:url/sm:loc", ns) if elem.text]

        assert "https://example.com/" in locs
        assert "https://example.com/posts" in locs
        assert "https://example.com/about" in locs
        assert "https://example.com/posts/trainer" in locs
    finally:
        os.environ.pop("SITE_URL", None)


def test_robots_txt_includes_sitemap_location():
    os.environ["SITE_URL"] = "https://example.com"
    try:
        app = create_app()
        client = TestClient(app)

        resp = client.get("/robots.txt")
        assert resp.status_code == 200
        assert "Sitemap: https://example.com/sitemap.xml" in resp.text
        assert re.search(r"(?im)^User-agent:\s*\*$", resp.text)
    finally:
        os.environ.pop("SITE_URL", None)

