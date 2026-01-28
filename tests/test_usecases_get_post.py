from __future__ import annotations

from app.adapters.markdown_python_renderer import PythonMarkdownRenderer
from app.domain.models import MarkdownPost
from app.usecases.get_post import GetPostUseCase
from tests.fakes import InMemoryPostsRepository


def test_get_post_returns_none_when_missing():
    repo = InMemoryPostsRepository(posts=())
    uc = GetPostUseCase(repo=repo, renderer=PythonMarkdownRenderer())
    assert uc.execute("missing") is None


def test_get_post_renders_html_when_found():
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="hello",
                title="Hello",
                date="2020-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image=None,
                thumb_image=None,
                extra_images=(),
                content_markdown="# Title",
                emoji=None,
            ),
        )
    )
    uc = GetPostUseCase(repo=repo, renderer=PythonMarkdownRenderer())
    result = uc.execute("hello")

    assert result is not None
    assert "<h1>" in result.content_html


def test_get_post_uses_frontmatter_image_as_cover_and_strips_matching_image_paragraph():
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="hello",
                title="Hello",
                date="2020-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image="/static/images/cover.png",
                thumb_image=None,
                extra_images=(),
                content_markdown="Intro\n\n![Banner](/static/images/cover.png)\n\nMore text",
                emoji=None,
            ),
        )
    )
    uc = GetPostUseCase(repo=repo, renderer=PythonMarkdownRenderer())
    result = uc.execute("hello")

    assert result is not None
    assert result.cover_image_url == "/static/images/cover.png"
    # Should not render the duplicated cover image inside the content.
    assert "/static/images/cover.png" not in result.content_html


def test_get_post_does_not_strip_cover_image_when_it_only_appears_in_body():
    """Regression test: don't remove images from legitimate sections (e.g. screenshots)."""

    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="hello",
                title="Hello",
                date="2020-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image="/static/images/cover.png",
                thumb_image=None,
                extra_images=(),
                content_markdown="Intro\n\n## Screenshots\n\n![Main](/static/images/cover.png)\n\nMore text",
                emoji=None,
            ),
        )
    )
    uc = GetPostUseCase(repo=repo, renderer=PythonMarkdownRenderer())
    result = uc.execute("hello")

    assert result is not None
    # Still uses frontmatter cover...
    assert result.cover_image_url == "/static/images/cover.png"
    # ...but does not strip the image from the body when it's not near the start.
    assert "/static/images/cover.png" in result.content_html


def test_get_post_extracts_first_standalone_image_as_cover_when_no_frontmatter_image():
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="hello",
                title="Hello",
                date="2020-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image=None,
                thumb_image=None,
                extra_images=(),
                content_markdown="![Cover](/static/images/cover.png)\n\nHello",
                emoji=None,
            ),
        )
    )
    uc = GetPostUseCase(repo=repo, renderer=PythonMarkdownRenderer())
    result = uc.execute("hello")

    assert result is not None
    assert result.cover_image_url == "/static/images/cover.png"
    assert "/static/images/cover.png" not in result.content_html


def test_get_post_axisdb_injects_install_terminal_when_has_problem_solution_impact_section():
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="axisdb",
                title="AxisDB",
                date="2020-01-01 12:00",
                tags=(),
                blurb="Project blurb",
                one_liner=None,
                image=None,
                thumb_image=None,
                extra_images=(),
                content_markdown=(
                    "## Problem → Solution → Impact\n\n"
                    "Some body.\n\n"
                    "More body.\n"
                ),
                emoji=None,
            ),
        )
    )
    uc = GetPostUseCase(repo=repo, renderer=PythonMarkdownRenderer())
    result = uc.execute("axisdb")

    assert result is not None
    assert "fake-terminal--axisdb-install" in result.content_html


def test_get_post_inserts_author_screenshots_section_when_has_problem_solution_impact_but_no_primary_images():
    # Covers the branch where we have a PSI section, but no cover/extra images;
    # still includes the author-provided screenshots body.
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="hello",
                title="Hello",
                date="2020-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image=None,
                thumb_image=None,
                extra_images=(),
                content_markdown=(
                    "## Problem → Solution → Impact\n\n"
                    "PSI body\n\n"
                    "## Screenshots\n\n"
                    "![Shot](/static/images/s.png)\n"
                ),
                emoji=None,
            ),
        )
    )
    uc = GetPostUseCase(repo=repo, renderer=PythonMarkdownRenderer())
    result = uc.execute("hello")

    assert result is not None
    assert "<h2>" in result.content_html
    assert "/static/images/s.png" in result.content_html
