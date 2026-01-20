from __future__ import annotations

from app.adapters.markdown_python_renderer import PythonMarkdownRenderer
from app.domain.models import MarkdownPost
from app.usecases.list_posts import (
    ListPostsUseCase,
    _extract_cover_image_and_strip,
    _strip_image_paragraph,
)
from tests.fakes import InMemoryPostsRepository


def test_list_posts_sorts_by_date_desc_and_renders_summary():
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="old",
                title="Old",
                date="2020-01-01 12:00",
                tags=("t",),
                blurb=None,
                one_liner=None,
                image=None,
                thumb_image=None,
                extra_images=(),
                content_markdown="First para\n\nSecond para",
            ),
            MarkdownPost(
                slug="new",
                title="New",
                date="2021-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image=None,
                thumb_image=None,
                extra_images=(),
                content_markdown="Hello\n\nMore",
            ),
        )
    )
    uc = ListPostsUseCase(repo=repo, renderer=PythonMarkdownRenderer())

    result = uc.execute()

    assert [p.slug for p in result] == ["new", "old"]
    assert "<p>" in result[0].summary_html
    assert "Hello" in result[0].summary_html


def test_list_posts_prefers_frontmatter_image_as_cover_and_strips_matching_image_paragraph():
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="one",
                title="One",
                date="2021-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image="/static/images/cover.jpg",
                thumb_image=None,
                extra_images=(),
                content_markdown="Intro\n\n![Banner](/static/images/cover.jpg)\n\nMore",
            ),
        )
    )
    uc = ListPostsUseCase(repo=repo, renderer=PythonMarkdownRenderer())

    result = uc.execute()
    assert len(result) == 1
    assert result[0].cover_image_url == "/static/images/cover.jpg"
    assert result[0].thumb_image_url == "/static/images/cover.jpg"
    # Summary should not include the cover image markdown.
    assert "/static/images/cover.jpg" not in result[0].summary_html


def test_list_posts_prefers_thumb_image_when_provided():
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="one",
                title="One",
                date="2021-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image="/static/images/cover.jpg",
                thumb_image="/static/images/thumb.png",
                extra_images=(),
                content_markdown="Intro\n\nMore",
            ),
        )
    )
    uc = ListPostsUseCase(repo=repo, renderer=PythonMarkdownRenderer())

    result = uc.execute()

    assert result[0].cover_image_url == "/static/images/cover.jpg"
    assert result[0].thumb_image_url == "/static/images/thumb.png"


def test_cover_helpers_handle_empty_markdown_gracefully():
    cover, remaining = _extract_cover_image_and_strip("")
    assert cover is None
    assert remaining == ""

    # Stripping an image from empty content should be a no-op.
    assert _strip_image_paragraph("", "/static/images/x.png") == ""
