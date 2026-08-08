"""How GetPostUseCase assembles the Screenshots section."""

from __future__ import annotations

from app.assets.manifest import AssetManifest
from app.domain.models import MarkdownPost


def test_get_post_helper_functions_cover_empty_and_fallback_paths():
    from app.usecases.get_post import _extract_markdown_sections

    assert _extract_markdown_sections("", title="Screenshots") == ("", [])


def test_get_post_injects_screenshots_dedupes_and_keeps_embedded():
    from app.usecases.get_post import GetPostUseCase

    class IdentityRenderer:
        def render(self, markdown_text: str) -> str:
            return markdown_text

    class FakeRepo:
        def __init__(self, post: MarkdownPost):
            self._post = post

        def list_posts(self):
            return (self._post,)

        def get_post(self, slug: str):
            return self._post if slug == self._post.slug else None

    md_with_psi = (
        "## Problem -> Solution -> Impact\n\n" "Some content\n\n" "## Next\n\n" "More\n"
    )
    post = MarkdownPost(
        slug="demo",
        title="Demo",
        date="2026-01-01 12:00",
        tags=("x",),
        blurb=None,
        one_liner="a project",  # makes it a project-like post
        image="/static/images/a.png",
        thumb_image=None,
        emoji=None,
        social_image=None,
        # Includes an empty-string URL to hit the `if not url: continue` branch,
        # plus a duplicate to hit the de-dupe branch.
        extra_images=(
            "",
            "/static/images/a.png",
            "/static/images/b.png",
            "/static/images/b.png",
        ),
        content_markdown=md_with_psi,
        post_type=None,
        role=None,
    )

    uc = GetPostUseCase(
        repo=FakeRepo(post),
        renderer=IdentityRenderer(),
        assets=AssetManifest(mapping={}),
    )
    detail = uc.execute("demo")
    assert detail is not None
    assert "## Screenshots" in detail.content_html
    # Only one occurrence of each URL.
    assert detail.content_html.count("/static/images/a.png") == 1
    assert detail.content_html.count("/static/images/b.png") == 1

    # No PSI section but author provided Screenshots section: it should be retained.
    md_with_screens = (
        "# Title\n\nIntro\n\n## Screenshots\n\n![x](/static/images/x.png)\n"
    )
    post2 = MarkdownPost(
        slug="demo2",
        title="Demo2",
        date="2026-01-01 12:00",
        tags=("x",),
        blurb=None,
        one_liner=None,
        # Provide an explicit cover image so `GetPostUseCase` does *not* treat the
        # embedded screenshot image as the cover (the cover-strip is restricted to
        # the first 2 paragraphs).
        image="/static/images/cover.png",
        thumb_image=None,
        emoji=None,
        social_image=None,
        extra_images=(),
        content_markdown=md_with_screens,
        post_type=None,
        role=None,
    )
    uc2 = GetPostUseCase(
        repo=FakeRepo(post2),
        renderer=IdentityRenderer(),
        assets=AssetManifest(mapping={}),
    )
    detail2 = uc2.execute("demo2")
    assert detail2 is not None
    assert "## Screenshots" in detail2.content_html
    assert "/static/images/x.png" in detail2.content_html


def test_get_post_usecase_has_psi_but_no_screenshots_no_changes():
    """Covers the `has_psi` path.

    There are zero screenshot URLs and no embedded screenshots.
    """

    from app.usecases.get_post import GetPostUseCase

    class IdentityRenderer:
        def render(self, markdown_text: str) -> str:
            return markdown_text

    class FakeRepo:
        def __init__(self, post: MarkdownPost):
            self._post = post

        def list_posts(self):
            return (self._post,)

        def get_post(self, slug: str):
            return self._post if slug == self._post.slug else None

    md_with_psi_no_images = (
        "## Problem -> Solution -> Impact\n\n"
        "Text only.\n\n"
        "## Next\n\n"
        "Still text.\n"
    )

    post = MarkdownPost(
        slug="psi-no-images",
        title="PSI No Images",
        date="2026-01-01 12:00",
        tags=("x",),
        blurb=None,
        one_liner=None,
        image=None,
        thumb_image=None,
        emoji=None,
        social_image=None,
        extra_images=(),
        content_markdown=md_with_psi_no_images,
        post_type=None,
        role=None,
    )

    uc = GetPostUseCase(
        repo=FakeRepo(post),
        renderer=IdentityRenderer(),
        assets=AssetManifest(mapping={}),
    )
    detail = uc.execute("psi-no-images")
    assert detail is not None
    # No screenshot content injected.
    assert "## Screenshots" not in detail.content_html
    assert detail.content_html.strip().startswith("## Problem")


def test_get_post_includes_author_screenshots_section_when_has_psi(monkeypatch):
    """Covers the branch that re-attaches author-provided Screenshots under PSI."""

    from app.usecases.get_post import GetPostUseCase

    md = (
        "---\n"
        "title: 'Demo'\n"
        "date: '2026-02-01'\n"
        "tags: ['x']\n"
        "---\n\n"
        "# Demo\n\n"
        "## Problem -> Solution -> Impact\n\n"
        "Some content.\n\n"
        "## Screenshots\n\n"
        "![shot](/static/images/me.jpg)\n\n"
        "More screenshots text.\n\n"
        "## Next\n\n"
        "Tail.\n"
    )

    post = MarkdownPost(
        slug="demo",
        title="Demo",
        date="2026-02-01 12:00",
        tags=("x",),
        blurb=None,
        one_liner=None,
        image=None,
        thumb_image=None,
        extra_images=(),
        content_markdown=md,
        emoji=None,
        social_image=None,
        post_type=None,
    )

    class FakeRepo:
        def list_posts(self):
            return ()

        def get_post(self, slug: str):
            assert slug == "demo"
            return post

    class IdentityRenderer:
        def render(self, markdown_text: str) -> str:
            # For coverage tests we can treat markdown as the final output.
            return markdown_text

    uc = GetPostUseCase(
        repo=FakeRepo(), renderer=IdentityRenderer(), assets=AssetManifest(mapping={})
    )
    detail = uc.execute("demo")
    assert detail is not None

    # The section should still exist after processing.
    assert "## Screenshots" in detail.content_html
    assert "More screenshots text." in detail.content_html


def test_get_post_appends_screenshots_when_body_markdown_empty_covers_else_branch():
    """Cover the branch where the post body is empty but screenshots exist.

    This hits the `else: markdown_wo_cover = screenshots_md + "\n"` path.
    """

    from app.usecases.get_post import GetPostUseCase

    class IdentityRenderer:
        def render(self, markdown_text: str) -> str:
            return markdown_text

    class FakeRepo:
        def get_post(self, slug: str):
            assert slug == "demo"
            return MarkdownPost(
                slug="demo",
                title="Demo",
                date="2026-02-01 12:00",
                tags=("x",),
                blurb=None,
                one_liner=None,
                image=None,
                thumb_image=None,
                extra_images=("/static/images/one.png",),
                content_markdown="",  # empty body
                emoji=None,
                social_image=None,
                post_type=None,
                role=None,
            )

        def list_posts(self):
            return ()

    uc = GetPostUseCase(
        repo=FakeRepo(), renderer=IdentityRenderer(), assets=AssetManifest(mapping={})
    )
    detail = uc.execute("demo")
    assert detail is not None
    assert detail.content_html.startswith("## Screenshots")
    assert "/static/images/one.png" in detail.content_html
