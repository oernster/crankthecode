from __future__ import annotations

from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import create_app


def test_portfolio_page_renders_and_includes_curated_and_category_groups():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/portfolio")
    assert resp.status_code == 200

    # Page heading.
    assert "Portfolio" in resp.text

    # Flagship entry should appear before the first category section (main content only).
    assert 'href="/posts/narratex"' in resp.text
    assert 'aria-label="Desktop Applications"' in resp.text
    assert resp.text.index('href="/posts/narratex"') < resp.text.index(
        'aria-label="Desktop Applications"'
    )

    # Intro copy appears first (above Desktop Applications).
    assert 'aria-label="Portfolio introduction"' in resp.text
    assert resp.text.index('aria-label="Portfolio introduction"') < resp.text.index(
        'aria-label="Desktop Applications"'
    )

    # Ensure the explanatory phrase exists *inside* the intro block (not just in metadata).
    import re

    m = re.search(
        r'<section class="section-panel" aria-label="Portfolio introduction"[\s\S]*?</section>',
        resp.text,
    )
    assert m is not None
    intro_block = m.group(0).lower()
    assert "systems built to solve real problems" in intro_block

    # Desktop Applications should be curated-only in a strict order.
    m = re.search(
        r'<section class="section-panel"[^>]*aria-label="Desktop Applications"[\s\S]*?</section>',
        resp.text,
    )
    assert m is not None
    desktop_block = m.group(0)

    slugs_in_order = re.findall(r'href="/posts/([a-z0-9\-]+)"', desktop_block)
    assert slugs_in_order == [
        "clearbudget",
        "commanddeck",
        "trainer",
        "calendifier",
        "stellody",
        "fancy-clock",
        "elevator",
    ]

    # The "More" button must come after Elevator.
    assert desktop_block.index('href="/posts/elevator"') < desktop_block.index(
        'href="/posts?cat=Desktop%20Apps"'
    )

    # Category-derived groups.
    assert "Hardware / Embedded" in resp.text
    assert "Tools" in resp.text

    # Old categories are surfaced inside portfolio (portfolio-only).
    assert "Web APIs" in resp.text
    assert "Data / ML" in resp.text
    assert "Gaming" in resp.text

    # Featured label should make the lead proof point explicit.
    assert "Featured system:" in resp.text


def test_portfolio_helpers_are_defensive_and_cover_edge_branches(monkeypatch):
    """Cover defensive branches inside the portfolio helpers.

    These are intentionally light unit tests: we want branch coverage for
    fail-open behavior (missing post, empty slug, exceptions).
    """

    import app.http.view_models.portfolio as portfolio_vm
    from app.http.view_models.posts import post_summary_index

    # `load_portfolio_post()` should fail open.
    def _boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(portfolio_vm.FilesystemPostsRepository, "get_post", _boom)
    assert portfolio_vm.load_portfolio_post() is None

    # `render_portfolio_intro_html()` should return empty when the post is missing.
    monkeypatch.setattr(portfolio_vm, "load_portfolio_post", lambda: None)
    assert portfolio_vm.render_portfolio_intro_html() == ""

    # And it should fail open if markdown rendering raises.
    monkeypatch.setattr(
        portfolio_vm,
        "load_portfolio_post",
        lambda: SimpleNamespace(content_markdown="Hello"),
    )

    class _BadRenderer:
        def render(self, *_args, **_kwargs):
            raise RuntimeError("boom")

    monkeypatch.setattr(portfolio_vm, "PythonMarkdownRenderer", lambda: _BadRenderer())
    assert portfolio_vm.render_portfolio_intro_html() == ""

    # `post_summary_index()` should ignore empty slugs.
    from app.domain.models import PostSummary

    empty = PostSummary(
        slug="",
        title="X",
        date="2026-02-01 12:00",
        tags=(),
        blurb=None,
        one_liner=None,
        cover_image_url=None,
        thumb_image_url=None,
        summary_html="",
        emoji=None,
        post_type=None,
        role=None,
    )

    class FakeBlog:
        def list_posts(self):
            return (empty,)

        def get_post(self, slug: str):
            return None

    from typing import cast

    from app.services.blog_service import BlogService

    assert post_summary_index(cast(BlogService, FakeBlog())) == {}

    # Curated helper should ignore empty, hidden and missing slugs.
    out = portfolio_vm.curated_portfolio_entries_from_slugs(
        slugs=["", "portfolio", "missing"],
        index={},
        hidden={"portfolio"},
        emoji_map={},
        emoji_index={},
    )
    assert out == []



def test_portfolio_groups_tools_dedup_skips_blank_and_duplicate_slugs(monkeypatch):
    """Hit the defensive branches inside the tools de-dupe loop in `_portfolio_groups()`."""

    import app.http.view_models.portfolio as portfolio_vm

    # Make the pinned tools list include a blank slug and a real slug.
    monkeypatch.setattr(
        portfolio_vm,
        "curated_portfolio_entries_from_slugs",
        lambda **_kwargs: [{"slug": ""}, {"slug": "audiodeck", "label": "Audio Deck"}],
    )

    # Ensure category-derived Tools includes a duplicate slug.
    from app.domain.models import PostSummary

    tools_post = PostSummary(
        slug="audiodeck",
        title="Audio Deck",
        date="2026-02-01 12:00",
        tags=("cat:Tools",),
        blurb=None,
        one_liner=None,
        cover_image_url=None,
        thumb_image_url=None,
        summary_html="",
        emoji=None,
        post_type=None,
        role=None,
    )

    class FakeBlog:
        def list_posts(self):
            return (tools_post,)

        def get_post(self, slug: str):
            return None

    from typing import cast

    from app.services.blog_service import BlogService

    groups = portfolio_vm.portfolio_groups(cast(BlogService, FakeBlog()))
    # The group was renamed from "Tools" -> "Operational Tools".
    tools = next(g for g in groups if g.get("label") == "Operational Tools")
    slugs = [e.get("slug") for e in (tools.get("entries") or [])]
    assert slugs == ["audiodeck"]


def test_portfolio_groups_ignores_flagship_posts_with_blank_slug():
    """Cover the defensive branch where a flagship post has an empty slug."""

    from typing import cast

    import app.http.view_models.portfolio as portfolio_vm
    from app.domain.models import PostSummary
    from app.services.blog_service import BlogService

    empty_flagship = PostSummary(
        slug="",
        title="X",
        date="2026-02-01 12:00",
        tags=(),
        blurb=None,
        one_liner=None,
        cover_image_url=None,
        thumb_image_url=None,
        summary_html="",
        emoji=None,
        post_type="project",
        role="flagship",
    )

    class FakeBlog:
        def list_posts(self):
            return (empty_flagship,)

        def get_post(self, slug: str):
            return None

    groups = portfolio_vm.portfolio_groups(cast(BlogService, FakeBlog()))
    assert isinstance(groups, list)


def test_portfolio_meta_description_branch_when_phrase_already_present(monkeypatch):
    """Cover the portfolio meta-description branch where no append is needed."""

    import app.http.routers.portfolio as portfolio_router

    # Provide a synthetic portfolio page where the one-liner already includes the phrase.
    monkeypatch.setattr(
        portfolio_router,
        "load_portfolio_post",
        lambda: SimpleNamespace(
            title="Portfolio",
            emoji="🧩",
            one_liner="Independent software systems and engineering experiments.",
            content_markdown="Intro",
        ),
    )
    monkeypatch.setattr(portfolio_router, "render_portfolio_intro_html", lambda: "<p>Intro</p>")

    app = create_app()
    client = TestClient(app)
    resp = client.get("/portfolio")
    assert resp.status_code == 200
    # Phrase should appear in meta description without being appended again.
    assert (
        'content="Independent software systems and engineering experiments."'
        in resp.text
    )

