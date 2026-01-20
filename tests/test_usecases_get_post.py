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
            ),
        )
    )
    uc = GetPostUseCase(repo=repo, renderer=PythonMarkdownRenderer())
    result = uc.execute("hello")

    assert result is not None
    assert result.cover_image_url == "/static/images/cover.png"
    # Should not render the duplicated cover image inside the content.
    assert "/static/images/cover.png" not in result.content_html


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
            ),
        )
    )
    uc = GetPostUseCase(repo=repo, renderer=PythonMarkdownRenderer())
    result = uc.execute("hello")

    assert result is not None
    assert result.cover_image_url == "/static/images/cover.png"
    assert "/static/images/cover.png" not in result.content_html
