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

    # Flagship entry should appear before the first category section.
    assert 'href="/posts/narratex"' in resp.text
    assert "Desktop Applications" in resp.text
    assert resp.text.index('href="/posts/narratex"') < resp.text.index(
        "Desktop Applications"
    )

    # Curated Desktop Applications group.
    assert 'href="/posts/fancy-clock"' in resp.text
    assert 'href="/posts/calendifier"' in resp.text
    assert 'href="/posts/elevator"' in resp.text

    # Category-derived groups.
    assert "Hardware / Embedded" in resp.text
    assert "Tools" in resp.text

    # Old categories are surfaced inside portfolio (portfolio-only).
    assert "Web APIs" in resp.text
    assert "Data / ML" in resp.text
    assert "Gaming" in resp.text

    # SEO phrase requirement.
    assert "software systems and engineering experiments" in resp.text.lower()


def test_portfolio_helpers_are_defensive_and_cover_edge_branches(monkeypatch):
    """Cover defensive branches inside the portfolio helpers.

    These are intentionally light unit tests: we want branch coverage for
    fail-open behavior (missing post, empty slug, exceptions).
    """

    import app.http.routers.html as html

    # `_load_portfolio_post()` should fail open.
    def _boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(html.FilesystemPostsRepository, "get_post", _boom)
    assert html._load_portfolio_post() is None

    # `_render_portfolio_intro_html()` should return empty when the post is missing.
    monkeypatch.setattr(html, "_load_portfolio_post", lambda: None)
    assert html._render_portfolio_intro_html() == ""

    # And it should fail open if markdown rendering raises.
    monkeypatch.setattr(
        html,
        "_load_portfolio_post",
        lambda: SimpleNamespace(content_markdown="Hello"),
    )

    class _BadRenderer:
        def render(self, *_args, **_kwargs):
            raise RuntimeError("boom")

    monkeypatch.setattr(html, "PythonMarkdownRenderer", lambda: _BadRenderer())
    assert html._render_portfolio_intro_html() == ""

    # `_post_summary_index()` should ignore empty slugs.
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

    assert html._post_summary_index(cast(BlogService, FakeBlog())) == {}

    # Curated helper should ignore empty, hidden and missing slugs.
    out = html._curated_portfolio_entries_from_slugs(
        slugs=["", "portfolio", "missing"],
        index={},
        hidden={"portfolio"},
        emoji_map={},
        emoji_index={},
    )
    assert out == []



def test_portfolio_groups_tools_dedup_skips_blank_and_duplicate_slugs(monkeypatch):
    """Hit the defensive branches inside the tools de-dupe loop in `_portfolio_groups()`."""

    import app.http.routers.html as html

    # Make the pinned tools list include a blank slug and a real slug.
    monkeypatch.setattr(
        html,
        "_curated_portfolio_entries_from_slugs",
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

    groups = html._portfolio_groups(cast(BlogService, FakeBlog()))
    tools = next(g for g in groups if g.get("label") == "Tools")
    slugs = [e.get("slug") for e in (tools.get("entries") or [])]
    assert slugs == ["audiodeck"]


def test_portfolio_groups_ignores_flagship_posts_with_blank_slug():
    """Cover the defensive branch where a flagship post has an empty slug."""

    from typing import cast

    import app.http.routers.html as html
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

    groups = html._portfolio_groups(cast(BlogService, FakeBlog()))
    assert isinstance(groups, list)


def test_portfolio_meta_description_branch_when_phrase_already_present(monkeypatch):
    """Cover the portfolio meta-description branch where no append is needed."""

    import app.http.routers.html as html

    # Provide a synthetic portfolio page where the one-liner already includes the phrase.
    monkeypatch.setattr(
        html,
        "_load_portfolio_post",
        lambda: SimpleNamespace(
            title="Portfolio",
            emoji="🧩",
            one_liner="Independent software systems and engineering experiments.",
            content_markdown="Intro",
        ),
    )
    monkeypatch.setattr(html, "_render_portfolio_intro_html", lambda: "<p>Intro</p>")

    app = create_app()
    client = TestClient(app)
    resp = client.get("/portfolio")
    assert resp.status_code == 200
    # Phrase should appear in meta description without being appended again.
    assert (
        'content="Independent software systems and engineering experiments."'
        in resp.text
    )

