from __future__ import annotations

from fastapi.testclient import TestClient

from app.domain.models import PostSummary
from app.main import create_app


def test_posts_index_supports_cat_and_layer_params_and_filters_with_and_semantics():
    """`layer:` is a subcategory within `cat:`; filtering requires BOTH tags."""

    posts = (
        PostSummary(
            slug="a",
            title="A",
            date="2026-02-01 12:00",
            tags=("cat:Leadership", "layer:decision-systems"),
            blurb=None,
            one_liner=None,
            cover_image_url=None,
            thumb_image_url=None,
            summary_html="",
            emoji=None,
        ),
        PostSummary(
            slug="b",
            title="B",
            date="2026-02-02 12:00",
            tags=("cat:Leadership", "layer:organisational-structure"),
            blurb=None,
            one_liner=None,
            cover_image_url=None,
            thumb_image_url=None,
            summary_html="",
            emoji=None,
        ),
        PostSummary(
            slug="c",
            title="C",
            date="2026-02-03 12:00",
            tags=("cat:Tools", "layer:decision-systems"),
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

    resp = client.get("/posts", params={"cat": "Leadership", "layer": "decision-systems"})
    assert resp.status_code == 200
    assert 'href="/posts/a"' in resp.text
    assert 'href="/posts/b"' not in resp.text
    assert 'href="/posts/c"' not in resp.text


def test_sidebar_renders_nested_layers_under_category_and_humanizes_labels():
    posts = (
        PostSummary(
            slug="a",
            title="A",
            date="2026-02-01 12:00",
            tags=("cat:Leadership", "layer:decision-systems"),
            blurb=None,
            one_liner=None,
            cover_image_url=None,
            thumb_image_url=None,
            summary_html="",
            emoji=None,
        ),
        PostSummary(
            slug="b",
            title="B",
            date="2026-02-01 12:00",
            tags=("cat:Blog",),
            blurb=None,
            one_liner=None,
            cover_image_url=None,
            thumb_image_url=None,
            summary_html="",
            emoji=None,
        ),
        PostSummary(
            slug="c",
            title="C",
            date="2026-02-01 12:00",
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

    resp = client.get("/posts")
    assert resp.status_code == 200

    # Decision Architecture (cat:Leadership) should be pinned to the top of the
    # category list.
    leadership_pos = resp.text.find("cat=Leadership")
    blog_pos = resp.text.find("cat=Blog")
    tools_pos = resp.text.find("cat=Tools")
    assert leadership_pos != -1
    assert blog_pos != -1
    assert tools_pos != -1
    assert leadership_pos < blog_pos < tools_pos

    # The fixed "All" link should appear below categories.
    assert resp.text.find("cat=Tools") < resp.text.find('aria-label="All"')

    # Category link.
    assert "cat=Leadership" in resp.text

    # Layer link under that category, humanized.
    assert "layer=decision-systems" in resp.text
    assert "Decision Systems" in resp.text


def test_layer_slug_normalization_collapses_spaces_underscores_and_punctuation():
    """Coverage for the layer slug normalizer (non-trivial input)."""

    posts = (
        PostSummary(
            slug="a",
            title="A",
            date="2026-02-01 12:00",
            tags=("cat:Leadership", "layer:  Decision__Systems!!  "),
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

    resp = client.get("/posts")
    assert resp.status_code == 200

    # Normalized layer slug should appear in the sidebar link href.
    assert "layer=decision-systems" in resp.text


def test_legacy_q_cat_deeplink_still_filters_posts():
    posts = (
        PostSummary(
            slug="a",
            title="A",
            date="2026-02-01 12:00",
            tags=("cat:Tools",),
            blurb=None,
            one_liner=None,
            cover_image_url=None,
            thumb_image_url=None,
            summary_html="",
            emoji=None,
        ),
        PostSummary(
            slug="b",
            title="B",
            date="2026-02-02 12:00",
            tags=("cat:Leadership",),
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

    resp = client.get("/posts", params={"q": "cat:Tools"})
    assert resp.status_code == 200
    assert 'href="/posts/a"' in resp.text
    assert 'href="/posts/b"' not in resp.text

