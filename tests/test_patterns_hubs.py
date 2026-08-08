from __future__ import annotations

from fastapi.testclient import TestClient

from app.domain.models import PostSummary
from app.main import create_app


def _mk_summary(
    *,
    slug: str,
    title: str,
    date: str,
    tags: tuple[str, ...],
    emoji: str | None = None,
) -> PostSummary:
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
        emoji=emoji,
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
    idx_primitives = html.index("Decision Objects")
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
            emoji="🪐",
        ),
        _mk_summary(
            slug="b",
            title="Newer",
            date="2026-02-02 10:00",
            tags=(
                "cat:decision-architecture-patterns",
                "layer:decision-primitives",
            ),
            emoji="🧱",
        ),
        _mk_summary(
            slug="c",
            title="Strange Layer",
            date="2026-02-03 10:00",
            tags=(
                "cat:decision-architecture-patterns",
                "layer:weird_layer!!",
            ),
            emoji="🧿",
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
    assert "Decision Objects" in html
    assert 'href="/patterns"' in html
    assert 'href="/patterns"' in html

    # Non-pattern posts must not leak into layer views.
    assert "Not Patterns" not in html

    idx_new = html.index("Newer")
    idx_old = html.index("Older")
    assert idx_new < idx_old

    # Individual posts should render as links.
    assert 'class="btn-link"' in html
    assert "Newer" in html
    assert "Older" in html

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
            emoji="🧷",
        ),
        _mk_summary(
            slug="y",
            title="Layered",
            date="2026-02-02 10:00",
            tags=(
                "cat:decision-architecture-patterns",
                "layer:decision-primitives",
            ),
            emoji="🧨",
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

    from typing import cast

    from app.http.view_models.leadership import category_posts_grouped_by_layer
    from app.services.blog_service import BlogService

    assert (
        category_posts_grouped_by_layer(
            cast(BlogService, FakeBlog()),
            cat_tag="",
            layer_label_overrides=None,
            preferred_layer_order=None,
        )
        == []
    )


def test_patterns_gateway_shows_header_copy_and_featured_start_here_row():
    """Acceptance: new header copy, exactly the 8 featured cards in order,
    all 42 OODA posts listed beneath and none removed or redirected."""

    from app.domain.taxonomy import PATTERNS_FEATURED_SLUGS

    app = create_app()
    client = TestClient(app, base_url="http://localhost")

    resp = client.get("/patterns")
    assert resp.status_code == 200
    html = resp.text

    # Header copy links the essays and the books.
    assert "A pattern language for decision systems" in html
    assert 'href="/essays"' in html
    assert "This is the catalogue in card form" in html
    assert 'href="/books"' in html

    # Start here row: exactly the featured slugs, in list order.
    assert 'aria-label="Start here patterns"' in html
    start = html.index('aria-label="Start here patterns"')
    end = html.index('aria-label="Patterns groups"')
    row = html[start:end]
    assert row.count("posts-featured-pill__title") == len(PATTERNS_FEATURED_SLUGS) == 8
    positions = [row.index(f'href="/posts/{s}"') for s in PATTERNS_FEATURED_SLUGS]
    assert positions == sorted(positions)

    # All 42 pattern posts are listed beneath and each still serves 200.
    groups = html[end:]
    ooda = [f"OODA{i}" for i in range(1, 43)]
    for slug in ooda:
        assert f'href="/posts/{slug}"' in groups, slug
    for slug in (ooda[0], ooda[-1]):
        post = client.get(f"/posts/{slug}", follow_redirects=False)
        assert post.status_code == 200, slug

    # Five layer sections present.
    for label in (
        "Authority Patterns",
        "Behaviour Patterns",
        "Decision Interfaces",
        "Decision Objects",
        "System Patterns",
    ):
        assert label in groups, label


def test_patterns_ordering_has_no_timestamp_ties():
    """OODA32/OODA33 and OODA10/OODA22 once shared timestamps; ordering must
    never depend on a tie."""

    from app.http.deps import get_blog_service

    posts = get_blog_service().list_posts()
    dates = [str(p.date) for p in posts if str(p.slug or "").upper().startswith("OODA")]
    assert len(dates) == 42
    assert len(set(dates)) == len(dates), "duplicate OODA timestamps"
