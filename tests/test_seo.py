from __future__ import annotations

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from fastapi.testclient import TestClient

from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
from app.http.seo import build_meta_description, get_site_url, to_iso_date
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


def test_get_site_url_uses_default_when_no_env_and_no_request():
    os.environ.pop("SITE_URL", None)
    assert get_site_url(None).startswith("https://")


def test_build_meta_description_empty_returns_empty_string():
    assert build_meta_description(None, fallback=None, default="") == ""


def test_build_meta_description_truncates_with_ellipsis():
    long = "x" * 500
    desc = build_meta_description(long, default="")
    assert desc.endswith("…")
    assert len(desc) <= 160


def test_to_iso_date_parses_supported_formats_and_returns_none_for_invalid():
    assert to_iso_date("2026-01-20 10:10") == "2026-01-20"
    assert to_iso_date("2026-01-20") == "2026-01-20"
    assert to_iso_date("") is None
    assert to_iso_date("not-a-date") is None


