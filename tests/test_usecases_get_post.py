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
                content_markdown="# Title",
            ),
        )
    )
    uc = GetPostUseCase(repo=repo, renderer=PythonMarkdownRenderer())
    result = uc.execute("hello")

    assert result is not None
    assert "<h1>" in result.content_html
