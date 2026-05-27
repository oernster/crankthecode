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

    # Desktop Applications should be date-desc sorted (no pinning/curation).
    m = re.search(
        r'<section class="section-panel"[^>]*aria-label="Desktop Applications"[\s\S]*?</section>',
        resp.text,
    )
    assert m is not None
    desktop_block = m.group(0)

    # Presence checks (avoid relying on the full universe of posts).
    assert 'href="/posts/locus"' in desktop_block
    assert 'href="/posts/clearbudget"' in desktop_block
    assert 'href="/posts/narratex"' in desktop_block

    # Ordering check (newest first).
    # Based on current post dates:
    # - Locus: 2026-05-27
    # - Clear Budget: 2026-05-22
    # - NarrateX: 2026-04-05
    assert desktop_block.index('href="/posts/locus"') < desktop_block.index(
        'href="/posts/clearbudget"'
    )
    assert desktop_block.index('href="/posts/clearbudget"') < desktop_block.index(
        'href="/posts/narratex"'
    )

    # Note: there is no per-section "More" link on /portfolio.

    # Category-derived groups.
    assert "Hardware / Embedded" in resp.text
    assert "Operational Tools" in resp.text

    # Old categories are surfaced inside portfolio (portfolio-only).
    assert "Web APIs" in resp.text
    assert "Data / ML" in resp.text
    assert "Gaming" in resp.text

    # Portfolio group order should match the curated layout.
    # NOTE: match only the section aria-labels (not the "items" or "More" aria-labels).
    ordered_labels = [
        "Desktop Applications",
        "Operational Tools",
        "Data / ML",
        "Gaming",
        "Hardware / Embedded",
        "Web APIs",
    ]
    indices = [resp.text.index(f'aria-label="{lbl}"') for lbl in ordered_labels]
    assert indices == sorted(indices)

    # Sidebar (menu) order should match the on-page section title order.
    # NOTE: scope to the portfolio sidebar group, and match the section querystring.
    sidebar_portfolio_labels = [
        "desktop-applications",
        "operational-tools",
        "data-ml",
        "gaming",
        "hardware-embedded",
        "web-apis",
    ]
    sidebar_indices = [
        resp.text.index(f'href="/portfolio?section={slug}"')
        for slug in sidebar_portfolio_labels
    ]
    assert sidebar_indices == sorted(sidebar_indices)

    # No featured/pinning block on portfolio.
    assert "Featured system:" not in resp.text


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

    nonempty = PostSummary(
        slug="ok",
        title="Ok",
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
            return (empty, nonempty)

        def get_post(self, slug: str):
            return None

    from typing import cast

    from app.services.blog_service import BlogService

    idx = post_summary_index(cast(BlogService, FakeBlog()))
    assert set(idx.keys()) == {"ok"}



def test_portfolio_groups_excludes_non_project_posts_by_tags():
    import app.http.view_models.portfolio as portfolio_vm

    from app.domain.models import PostSummary
    from app.services.blog_service import BlogService
    from typing import cast

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
    blog_post = PostSummary(
        slug="blog-post",
        title="Blog",
        date="2026-02-01 12:00",
        tags=("cat:Blog",),
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
            return (tools_post, blog_post)

        def get_post(self, slug: str):
            return None

    groups = portfolio_vm.portfolio_groups(cast(BlogService, FakeBlog()))
    tools = next(g for g in groups if g.get("label") == "Operational Tools")
    slugs = [e.get("slug") for e in (tools.get("entries") or [])]
    assert slugs == ["audiodeck"]


def test_portfolio_groups_ignores_posts_with_blank_slug():
    """Cover the defensive branch where a post has an empty slug."""

    from typing import cast

    import app.http.view_models.portfolio as portfolio_vm
    from app.domain.models import PostSummary
    from app.services.blog_service import BlogService

    empty_post = PostSummary(
        slug="",
        title="X",
        date="2026-02-01 12:00",
        tags=("cat:Tools",),
        blurb=None,
        one_liner=None,
        cover_image_url=None,
        thumb_image_url=None,
        summary_html="",
        emoji=None,
        post_type="project",
        role=None,
    )

    class FakeBlog:
        def list_posts(self):
            return (empty_post,)

        def get_post(self, slug: str):
            return None

    groups = portfolio_vm.portfolio_groups(cast(BlogService, FakeBlog()))
    assert isinstance(groups, list)
    all_slugs = [
        e.get("slug")
        for g in groups
        for e in (g.get("entries") or [])
        if isinstance(g, dict)
    ]
    assert all_slugs == []


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

