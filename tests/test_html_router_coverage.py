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

