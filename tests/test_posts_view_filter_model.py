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
            post_type=None,
            role=None,
        ),
        PostSummary(
            slug="tooling",
            title="Tooling",
            date="2026-02-02 12:00",
            # "Tools & Libraries" is the current project category; the old bare
            # "Tools" label was retired when the projects taxonomy was recut.
            tags=("cat:Tools & Libraries",),
            blurb=None,
            one_liner=None,
            cover_image_url=None,
            thumb_image_url=None,
            summary_html="",
            emoji=None,
            post_type=None,
            role=None,
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

    # exclude_blog=1 historically meant "projects only"; the projects view is
    # gone, so it now lands on Writing, which lists everything non-blog.
    resp = client.get("/posts?exclude_blog=1")
    assert resp.status_code == 200
    assert 'href="/posts/tooling"' in resp.text
    # The Leadership essay keeps its dedicated Decision Architecture hub, so the
    # Writing listing does not repeat it.
    assert 'href="/posts/essay"' not in resp.text

    # exclude_blog=0 historically meant "include blog" (closest is Archive).
    resp2 = client.get("/posts?exclude_blog=0")
    assert resp2.status_code == 200
    assert 'href="/posts/tooling"' in resp2.text
    assert 'href="/posts/essay"' in resp2.text


def test_retired_project_write_up_slugs_redirect_to_the_portfolio_hub():
    """The project essays moved to ernster.dev; old slugs must not 404."""

    from fastapi.testclient import TestClient

    from app.main import create_app

    app = create_app()
    client = TestClient(app, base_url="http://localhost")

    resp = client.get("/posts/fulcrum", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers["location"] == "https://ernster.dev/fulcrum/"

    resp_case = client.get("/posts/PigeonPost", follow_redirects=False)
    assert resp_case.status_code == 301
    assert resp_case.headers["location"] == "https://pigeonpost.ink"


def test_writing_view_excludes_hub_categories_but_explicit_cat_still_lists():
    """The Writing listing must not duplicate the DA and Patterns hubs.

    Their groups disappear from /posts?view=writing (each post remains
    reachable via its /topics or /patterns hub) while a deliberate
    ?cat=Leadership filter still lists the posts.
    """

    from fastapi.testclient import TestClient

    from app.main import create_app

    app = create_app()
    client = TestClient(app)

    # The old Writing view is retired: it 301s to the Selected Essays page.
    resp = client.get("/posts?view=writing", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers.get("location") == "/essays"

    # And its Blog variant lands on the Build Log.
    resp = client.get("/posts?view=writing&cat=Blog", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers.get("location") == "/build-log"

    resp_cat = client.get("/posts?cat=Leadership")
    assert resp_cat.status_code == 200
    assert 'href="/posts/lead2"' in resp_cat.text


def test_posts_href_helpers_have_basic_coverage():
    """Pin coverage for tiny URL helpers in the HTML router."""

    from app.http.view_models.sidebar import (
        posts_base_href as _posts_base_href,
        posts_href as _posts_href,
        posts_view_from_legacy_exclude_blog as _posts_view_from_legacy_exclude_blog,
    )

    assert _posts_href(query="cat:Tools", exclude_blog=None) == "/posts?q=cat%3ATools"
    assert _posts_base_href(view=None) == "/posts"
    assert _posts_view_from_legacy_exclude_blog("maybe") is None
