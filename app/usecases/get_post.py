from __future__ import annotations

from dataclasses import dataclass

from app.domain.models import PostDetail
from app.ports.markdown_renderer import MarkdownRenderer
from app.ports.posts_repository import PostsRepository


@dataclass(frozen=True, slots=True)
class GetPostUseCase:
    repo: PostsRepository
    renderer: MarkdownRenderer

    def execute(self, slug: str) -> PostDetail | None:
        post = self.repo.get_post(slug)
        if post is None:
            return None

        html_content = self.renderer.render(post.content_markdown)
        return PostDetail(
            slug=post.slug,
            title=post.title,
            date=post.date,
            tags=post.tags,
            content_html=html_content,
        )
