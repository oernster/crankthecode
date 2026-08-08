"""What the posts index hides, narrows and tolerates."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.domain.models import PostSummary
from app.main import create_app


def _mk_summary(
    *,
    slug: str,
    title: str,
    date: str,
    tags: tuple[str, ...] = (),
    cover: str | None = None,
    thumb: str | None = None,
) -> PostSummary:
    return PostSummary(
        slug=slug,
        title=title,
        date=date,
        tags=tags,
        blurb=None,
        one_liner=None,
        cover_image_url=cover,
        thumb_image_url=thumb,
        emoji=None,
        summary_html="",
        post_type=None,
        role=None,
    )


def test_posts_index_excludes_about_me_from_all_lists(monkeypatch):
    posts = (
        _mk_summary(
            slug="about-me",
            title="About Me",
            date="2026-01-18 07:35",
            tags=("about",),
        ),
        _mk_summary(
            slug="axisdb",
            title="AxisDB",
            date="2026-01-19 10:00",
            tags=("db",),
        ),
        _mk_summary(
            slug="demoapp",
            title="DemoApp",
            date="2026-01-19 13:45",
            tags=("desktop",),
        ),
    )

    class FakeBlog:
        def list_posts(self):
            return posts

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/posts?view=archive")
    assert resp.status_code == 200
    assert "About Me" not in resp.text


def test_posts_index_excludes_axisdb_from_tools_category_view(monkeypatch):
    posts = (
        _mk_summary(
            slug="axisdb",
            title="AxisDB",
            date="2026-01-19 10:00",
            # AxisDB is not tagged as a Tools category post.
            tags=("db",),
        ),
        _mk_summary(
            slug="demoapp",
            title="DemoApp",
            date="2026-01-19 13:45",
            tags=("desktop", "cat:Tools"),
        ),
    )

    class FakeBlog:
        def list_posts(self):
            return posts

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/posts?q=cat:Tools")
    assert resp.status_code == 200
    assert "AxisDB" not in resp.text
    assert "DemoApp" in resp.text


def test_posts_index_category_title_empty_is_tolerated(monkeypatch):
    """Covers the `cat_text == ''` branch when computing category SEO titles."""

    posts = (
        _mk_summary(
            slug="lead1",
            title="Leadership One",
            date="2026-02-07 10:10",
            tags=("cat:Leadership",),
        ),
    )

    class FakeBlog:
        def list_posts(self):
            return posts

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service
    import app.http.routers.posts as posts_router

    # Force `cat_display` to become empty after `.strip()` so the code exercises
    # the `if cat_text:` false branch.
    monkeypatch.setattr(posts_router, "category_label_for_query", lambda *a, **k: " ")

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/posts?q=cat:Leadership")
    assert resp.status_code == 200


def test_excluded_slugs_blog_query_empty_set_branch_covered():
    """Covers the `_excluded_slugs_for_query()` branch where the CSV is empty."""

    class FakeBlog:
        def list_posts(self):
            return ()

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/posts?q=cat:Blog&exclude_blog=0")
    assert resp.status_code == 200


def test_is_blog_post_by_cat_covers_branches():
    from app.http.view_models.sidebar import is_blog_post_by_cat

    assert is_blog_post_by_cat([]) is False
    assert is_blog_post_by_cat(["x"]) is False
    assert is_blog_post_by_cat(["cat:Blog"]) is True
    assert is_blog_post_by_cat(["cat:blog"]) is True
    assert is_blog_post_by_cat(["CAT:BLOG"]) is True
