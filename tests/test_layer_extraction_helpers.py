from __future__ import annotations

from app.http.routers.html import _extract_category_queries_from_tags
from app.http.routers.html import _extract_layer_slugs_from_tags
from app.http.routers.html import _category_label_for_query


def test_extract_layer_slugs_normalizes_and_ignores_invalid_entries():
    tags = [
        "",
        "   ",
        "python",
        "layer:",
        "layer:   ",
        "layer:Decision__Systems!!",
        "layer:decision-systems",
    ]

    slugs = _extract_layer_slugs_from_tags(tags)
    assert "decision-systems" in slugs


def test_humanize_layer_slug_preserves_cto_acronym():
    from app.http.routers.html import _humanize_layer_slug

    assert _humanize_layer_slug("cto-operating-model") == "CTO Operating Model"
    assert _humanize_layer_slug("") == ""


def test_extract_category_queries_ignores_empty_cat_label():
    tags = [
        "cat:",
        "cat:   ",
        "cat:Tools",
    ]
    out = _extract_category_queries_from_tags(tags)
    assert "cat:Tools" in out
    assert not any(x.strip().lower() == "cat:" for x in out)


def test_category_label_for_query_returns_none_when_category_not_found():
    """Coverage for the non-match branch when using the dynamic sidebar model."""

    class FakeBlog:
        def list_posts(self):
            return ()

        def get_post(self, slug: str):
            return None

    from typing import cast
    from app.services.blog_service import BlogService

    assert (
        _category_label_for_query(
            "cat:Tools", blog=cast(BlogService, FakeBlog()), exclude_blog=True
        )
        is None
    )


def test_category_label_for_query_finds_label_when_category_exists():
    """Coverage for the matching branch in `_category_label_for_query()`."""

    from typing import cast

    from app.domain.models import PostSummary
    from app.services.blog_service import BlogService

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
    )

    class FakeBlog:
        def list_posts(self):
            return posts

        def get_post(self, slug: str):
            return None

    label = _category_label_for_query(
        "cat:Tools", blog=cast(BlogService, FakeBlog()), exclude_blog=True
    )
    assert isinstance(label, str)
    assert "Tools" in label


def test_posts_index_seo_branch_handles_empty_category_text_gracefully():
    """Coverage for the `cat_label` SEO branch where `cat_text` ends up empty."""

    from fastapi.testclient import TestClient

    from app.domain.models import PostSummary
    from app.main import create_app
    from app.http.deps import get_blog_service

    posts = (
        PostSummary(
            slug="a",
            title="A",
            date="2026-02-01 12:00",
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

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    # Force `cat_label` truthy but with whitespace so cat_text becomes empty
    # after the emoji/title split.
    resp = client.get("/posts", params={"cat": "   "})
    assert resp.status_code == 200

