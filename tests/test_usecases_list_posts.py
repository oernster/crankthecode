from __future__ import annotations

from app.adapters.markdown_python_renderer import PythonMarkdownRenderer
from app.domain.models import MarkdownPost
from app.usecases.list_posts import ListPostsUseCase
from tests.fakes import InMemoryPostsRepository


def test_list_posts_sorts_by_date_desc_and_renders_summary():
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="old",
                title="Old",
                date="2020-01-01 12:00",
                tags=("t",),
                image=None,
                content_markdown="First para\n\nSecond para",
            ),
            MarkdownPost(
                slug="new",
                title="New",
                date="2021-01-01 12:00",
                tags=(),
                image=None,
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
                image="/static/images/cover.jpg",
                content_markdown="Intro\n\n![Banner](/static/images/cover.jpg)\n\nMore",
            ),
        )
    )
    uc = ListPostsUseCase(repo=repo, renderer=PythonMarkdownRenderer())

    result = uc.execute()
    assert len(result) == 1
    assert result[0].cover_image_url == "/static/images/cover.jpg"
    # Summary should not include the cover image markdown.
    assert "/static/images/cover.jpg" not in result[0].summary_html
