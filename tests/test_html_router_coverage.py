from __future__ import annotations

from fastapi.testclient import TestClient

from app.http.routers import html as html_module
from app.main import create_app


def test_category_label_for_query_returns_label_and_none():
    assert (
        html_module._category_label_for_query("api|apis|fastapi|django|rest|web")
        == "🌐 Web APIs"
    )
    assert html_module._category_label_for_query("") is None
    assert html_module._category_label_for_query("not-a-real-category") is None


def test_load_about_html_fail_open_for_missing_post_and_exception(monkeypatch):
    class FakeRepoMissing:
        def __init__(self, *args, **kwargs):
            pass

        def get_post(self, slug: str):
            return None

    monkeypatch.setattr(html_module, "FilesystemPostsRepository", FakeRepoMissing)
    assert html_module._load_about_html() == ""

    class FakeRepoExplodes:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("boom")

    monkeypatch.setattr(html_module, "FilesystemPostsRepository", FakeRepoExplodes)
    assert html_module._load_about_html() == ""


def test_read_post_renders_non_project_post_without_date_or_cover_image():
    # This covers the branches where:
    # - is_project is False (no one_liner/blurb)
    # - published_iso is None (invalid date)
    # - no jsonld image (no cover)
    class FakeBlog:
        def list_posts(self):
            return []

        def get_post(self, slug: str):
            if slug != "hello":
                return None
            return type(
                "Detail",
                (),
                {
                    "slug": "hello",
                    "title": "Hello",
                    "date": "not-a-date",
                    "tags": (),
                    "blurb": None,
                    "one_liner": None,
                    "cover_image_url": None,
                    "social_image_url": None,
                    "extra_image_urls": (),
                    "content_html": "<h1>Hello</h1>",
                },
            )

    app = create_app()
    from app.http.deps import get_blog_service

    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/posts/hello")
    assert resp.status_code == 200
    assert "<h1>Hello</h1>" in resp.text


def test_extract_category_queries_from_tags_skips_empty_and_cat_colon_only():
    from app.http.routers.html import _extract_category_queries_from_tags

    # Covers:
    # - empty/whitespace tags
    # - `cat:` with no label
    # - normalization (whitespace collapse + Title Case)
    out = _extract_category_queries_from_tags(
        [
            "",
            "   ",
            "cat:",
            "CAT:   ",
            "cat:  tools  ",
            "tools",
        ]
    )
    assert out == {"cat:Tools"}


def test_sidebar_label_with_emoji_maps_known_labels_and_passes_through_unknowns():
    from app.http.routers.html import _sidebar_label_with_emoji

    assert _sidebar_label_with_emoji("Tools") == "🧰 Tools"
    assert _sidebar_label_with_emoji("Hardware") == "🔧 Hardware"
    assert _sidebar_label_with_emoji("Governance") == "🏛️ Governance"
    assert _sidebar_label_with_emoji("Leadership") == "♟️ Decision Architecture"
    assert _sidebar_label_with_emoji("Web Apis") == "🌐 Web APIs"
    assert _sidebar_label_with_emoji("Unmapped") == "Unmapped"
    assert _sidebar_label_with_emoji("") == ""


def test_legacy_leadership_blog_posts_redirect_to_leadership_slugs():
    app = create_app()
    client = TestClient(app, base_url="http://localhost")

    # Legacy redirects have been removed; ensure blog18 is served normally.
    resp = client.get("/posts/blog18", follow_redirects=False)
    assert resp.status_code == 200
    assert "When consensus becomes the goal" in resp.text


def test_dev_site_clears_cache_header_on_localhost_responses():
    """Cover dev-only Clear-Site-Data header.

    This is only emitted for 127.0.0.1/localhost to prevent sticky cached
    redirects during local iteration.
    """

    app = create_app()
    client = TestClient(app, base_url="http://127.0.0.1:8003")

    resp = client.get("/posts")
    assert resp.status_code == 200
    assert resp.headers.get("Clear-Site-Data") == '"cache"'

    resp = client.get("/posts/blog18")
    assert resp.status_code == 200
    assert resp.headers.get("Clear-Site-Data") == '"cache"'

