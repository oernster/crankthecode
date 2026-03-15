from __future__ import annotations


def test_posts_view_switch_preserves_cat_and_layer_params():
    """`view=` is the primary filter; switching view must preserve secondary filters."""

    from fastapi.testclient import TestClient

    from app.main import create_app

    class FakeBlog:
        def list_posts(self):
            return ()

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/posts?view=writing&cat=Leadership&layer=structural-design")
    assert resp.status_code == 200

    # View-switch links should keep cat+layer.
    assert (
        'href="/posts?view=writing&amp;cat=Leadership&amp;layer=structural-design"'
        in resp.text
    )
    assert (
        'href="/posts?view=projects&amp;cat=Leadership&amp;layer=structural-design"'
        in resp.text
    )
    assert (
        'href="/posts?view=archive&amp;cat=Leadership&amp;layer=structural-design"'
        in resp.text
    )


def test_posts_legacy_exclude_blog_mapping_is_supported():
    """Legacy `exclude_blog` maps into the new `view` model when `view` absent."""

    from fastapi.testclient import TestClient

    from app.main import create_app
    from app.domain.models import PostSummary

    posts = (
        PostSummary(
            slug="essay",
            title="Essay",
            date="2026-02-01 12:00",
            tags=("cat:Leadership",),
            blurb=None,
            one_liner=None,
            cover_image_url=None,
            thumb_image_url=None,
            summary_html="",
            emoji=None,
        ),
        PostSummary(
            slug="tooling",
            title="Tooling",
            date="2026-02-02 12:00",
            tags=("cat:Tools",),
            blurb=None,
            one_liner=None,
            cover_image_url=None,
            thumb_image_url=None,
            summary_html="",
            emoji=None,
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

    # exclude_blog=1 historically meant "projects only".
    resp = client.get("/posts?exclude_blog=1")
    assert resp.status_code == 200
    assert 'href="/posts/tooling"' in resp.text
    assert 'href="/posts/essay"' not in resp.text

    # exclude_blog=0 historically meant "include blog" (closest is Archive).
    resp2 = client.get("/posts?exclude_blog=0")
    assert resp2.status_code == 200
    assert 'href="/posts/tooling"' in resp2.text
    assert 'href="/posts/essay"' in resp2.text


def test_posts_href_helpers_have_basic_coverage():
    """Pin coverage for tiny URL helpers in the HTML router."""

    from app.http.routers.html import (
        _posts_base_href,
        _posts_href,
        _posts_view_from_legacy_exclude_blog,
    )

    assert _posts_href(query="cat:Tools", exclude_blog=None) == "/posts?q=cat%3ATools"
    assert _posts_base_href(view=None) == "/posts"
    assert _posts_view_from_legacy_exclude_blog("maybe") is None

