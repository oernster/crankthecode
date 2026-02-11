from __future__ import annotations

import os
import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from fastapi.testclient import TestClient

from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
from app.http.seo import build_meta_description, get_site_url, to_iso_date, to_iso_datetime
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


def test_category_page_sets_distinct_title_and_meta_description_for_leadership():
    os.environ["SITE_URL"] = "https://example.com"
    try:
        app = create_app()
        client = TestClient(app)

        resp = client.get("/posts?q=cat:Leadership")
        assert resp.status_code == 200

        html = resp.text
        assert "<title>Decision Architecture | Posts | Crank The Code</title>" in html
        assert (
            '<meta name="description" content="Browse posts in Decision Architecture on Crank The Code."'
            in html
        )

        # Canonical should preserve the category query.
        assert (
            '<link rel="canonical" href="https://example.com/posts?q=cat:Leadership"'
            in html
        )
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


def test_robots_txt_falls_back_when_static_file_missing(monkeypatch):
    """Cover the `robots.txt` fallback path when `static/robots.txt` can't be read."""

    os.environ["SITE_URL"] = "https://example.com"
    try:
        # Force `Path.read_text()` to raise so the router uses the fallback body.
        from pathlib import Path

        def _raise(*args, **kwargs):
            raise OSError("boom")

        monkeypatch.setattr(Path, "read_text", _raise)

        app = create_app()
        client = TestClient(app)

        resp = client.get("/robots.txt")
        assert resp.status_code == 200
        assert "User-agent:" in resp.text
        assert "Allow:" in resp.text
        assert "Sitemap: https://example.com/sitemap.xml" in resp.text
    finally:
        os.environ.pop("SITE_URL", None)


def test_robots_txt_appends_sitemap_when_no_sitemap_line(monkeypatch):
    """Cover the `not replaced` path: when no Sitemap line exists, we append one."""

    os.environ["SITE_URL"] = "https://example.com"
    try:
        from pathlib import Path

        monkeypatch.setattr(Path, "read_text", lambda *a, **k: "User-agent: *\nDisallow:\n")

        app = create_app()
        client = TestClient(app)

        resp = client.get("/robots.txt")
        assert resp.status_code == 200
        assert "Sitemap: https://example.com/sitemap.xml" in resp.text
    finally:
        os.environ.pop("SITE_URL", None)


def test_robots_txt_appends_sitemap_without_extra_blank_line(monkeypatch):
    """Cover the `not replaced` branch where the static file already ends with a blank line."""

    os.environ["SITE_URL"] = "https://example.com"
    try:
        from pathlib import Path

        # Note the trailing blank line: the last split line is empty, so we should
        # *not* add an extra blank line before appending the sitemap.
        monkeypatch.setattr(
            Path,
            "read_text",
            lambda *a, **k: "User-agent: *\nDisallow:\n\n",
        )

        app = create_app()
        client = TestClient(app)

        resp = client.get("/robots.txt")
        assert resp.status_code == 200
        assert "Sitemap: https://example.com/sitemap.xml" in resp.text
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


def test_to_iso_datetime_parses_supported_formats_and_returns_none_for_invalid():
    assert to_iso_datetime("2026-01-20 10:10") == "2026-01-20T10:10:00"
    assert to_iso_datetime("2026-01-20") == "2026-01-20T12:00:00"
    assert to_iso_datetime("") is None
    assert to_iso_datetime("not-a-date") is None


def test_all_posts_have_required_seo_meta_and_valid_jsonld():
    """Regression net: ensure every `/posts/{slug}` page is SEO-complete.

    This intentionally does *not* enforce canonical query stripping (by request).
    """

    os.environ["SITE_URL"] = "https://example.com"
    try:
        app = create_app()
        client = TestClient(app)

        repo = FilesystemPostsRepository(posts_dir=Path("posts"))
        slugs = sorted([p.slug for p in repo.list_posts()])
        assert slugs, "Expected at least one post in /posts"

        for slug in slugs:
            resp = client.get(f"/posts/{slug}")
            assert resp.status_code == 200, slug
            html = resp.text

            # Canonical must exist and be stable.
            assert html.count('rel="canonical"') == 1, slug
            assert f'https://example.com/posts/{slug}' in html, slug

            # Description must exist and be non-empty.
            m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"\s*/?>', html)
            assert m, slug
            desc = m.group(1).strip()
            assert desc, slug
            assert len(desc) <= 160, slug

            # OpenGraph/Twitter essentials.
            assert 'property="og:title"' in html, slug
            assert 'property="og:description"' in html, slug
            assert 'property="og:image"' in html, slug
            assert 'name="twitter:card"' in html, slug

            # JSON-LD must be present and parseable.
            blocks = re.findall(
                r'<script\s+type="application/ld\+json">(.*?)</script>',
                html,
                flags=re.S,
            )
            assert blocks, slug
            parsed = []
            for raw in blocks:
                parsed.append(json.loads(raw))

            # Post pages must include BlogPosting.
            assert any(obj.get("@type") == "BlogPosting" for obj in parsed if isinstance(obj, dict)), slug
    finally:
        os.environ.pop("SITE_URL", None)


