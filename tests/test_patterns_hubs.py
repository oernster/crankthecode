from __future__ import annotations

from fastapi.testclient import TestClient

from app.domain.models import PostSummary
from app.main import create_app


def _mk_summary(*, slug: str, title: str, date: str, tags: tuple[str, ...]) -> PostSummary:
    return PostSummary(
        slug=slug,
        title=title,
        date=date,
        tags=tags,
        blurb=None,
        one_liner=None,
        cover_image_url=None,
        thumb_image_url=None,
        summary_html="",
        emoji=None,
        post_type=None,
        role=None,
    )


def test_patterns_index_renders_layer_pills_and_groups_and_orders_posts_newest_first():
    posts = (
        _mk_summary(
            slug="p1",
            title="Old Primitive",
            date="2026-02-01 10:00",
            tags=(
                "cat:decision-architecture-patterns",
                "layer:decision-primitives",
            ),
        ),
        _mk_summary(
            slug="p2",
            title="New Primitive",
            date="2026-02-02 10:00",
            tags=(
                "cat:decision-architecture-patterns",
                "layer:decision-primitives",
            ),
        ),
        _mk_summary(
            slug="p3",
            title="Interfaces",
            date="2026-02-03 10:00",
            tags=(
                "cat:decision-architecture-patterns",
                "layer:decision-interfaces",
            ),
        ),
        _mk_summary(
            slug="p4",
            title="Unlayered Patterns",
            date="2026-02-04 10:00",
            tags=("cat:decision-architecture-patterns",),
        ),
        _mk_summary(
            slug="p5",
            title="Weird Layer Patterns",
            date="2026-02-05 10:00",
            tags=(
                "cat:decision-architecture-patterns",
                "layer:weird_layer!!",
            ),
        ),
        _mk_summary(
            slug="not-pattern",
            title="Not Patterns",
            date="2026-02-04 10:00",
            tags=("cat:Tools",),
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

    resp = client.get("/patterns")
    assert resp.status_code == 200

    html = resp.text
    assert "Decision Architecture Patterns" in html
    assert 'href="/patterns/decision-primitives"' in html
    assert 'href="/patterns/decision-interfaces"' in html
    assert 'href="/patterns/authority-models"' in html
    assert 'href="/patterns/system-dynamics"' in html
    assert 'href="/patterns/pattern-catalogue"' in html

    # Only patterns posts should show up.
    assert "Not Patterns" not in html

    # Group ordering: preferred layers first, unknown layers next, General last.
    idx_primitives = html.index("Decision Primitives")
    idx_weird = html.index("Weird Layer")
    idx_general = html.index("General")
    assert idx_primitives < idx_weird < idx_general

    # Ordering within a layer must be newest-first.
    idx_new = html.index("New Primitive")
    idx_old = html.index("Old Primitive")
    assert idx_new < idx_old


def test_patterns_layer_page_lists_posts_newest_first_and_humanizes_unknown_layers():
    posts = (
        _mk_summary(
            slug="a",
            title="Older",
            date="2026-02-01 10:00",
            tags=(
                "cat:decision-architecture-patterns",
                "layer:decision-primitives",
            ),
        ),
        _mk_summary(
            slug="b",
            title="Newer",
            date="2026-02-02 10:00",
            tags=(
                "cat:decision-architecture-patterns",
                "layer:decision-primitives",
            ),
        ),
        _mk_summary(
            slug="c",
            title="Strange Layer",
            date="2026-02-03 10:00",
            tags=(
                "cat:decision-architecture-patterns",
                "layer:weird_layer!!",
            ),
        ),
        _mk_summary(
            slug="not-pattern",
            title="Not Patterns",
            date="2026-02-04 10:00",
            tags=(
                "cat:Tools",
                "layer:decision-primitives",
            ),
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

    resp = client.get("/patterns/decision-primitives")
    assert resp.status_code == 200
    html = resp.text
    assert "Decision Primitives" in html
    assert 'href="/patterns"' in html

    # Non-pattern posts must not leak into layer views.
    assert "Not Patterns" not in html

    idx_new = html.index("Newer")
    idx_old = html.index("Older")
    assert idx_new < idx_old

    # Unknown layers should still render (fallback label via humanize).
    resp = client.get("/patterns/weird_layer!!")
    assert resp.status_code == 200
    assert "Weird Layer" in resp.text


def test_patterns_layer_page_supports_general_alias_for_unlayered_posts():
    posts = (
        _mk_summary(
            slug="x",
            title="Unlayered",
            date="2026-02-01 10:00",
            tags=("cat:decision-architecture-patterns",),
        ),
        _mk_summary(
            slug="y",
            title="Layered",
            date="2026-02-02 10:00",
            tags=(
                "cat:decision-architecture-patterns",
                "layer:decision-primitives",
            ),
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

    resp = client.get("/patterns/general")
    assert resp.status_code == 200
    assert "General" in resp.text
    assert "Unlayered" in resp.text
    assert "Layered" not in resp.text


def test_category_posts_grouped_by_layer_tolerates_empty_cat_tag():
    """Coverage for the defensive empty-`cat_tag` path."""

    class FakeBlog:
        def list_posts(self):
            return ()

        def get_post(self, slug: str):
            return None

    from app.http.routers.html import _category_posts_grouped_by_layer

    assert (
        _category_posts_grouped_by_layer(
            FakeBlog(),
            cat_tag="",
            layer_label_overrides=None,
            preferred_layer_order=None,
        )
        == []
    )

