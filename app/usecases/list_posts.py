from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from app.domain.models import PostSummary
from app.ports.markdown_renderer import MarkdownRenderer
from app.ports.posts_repository import PostsRepository


def _extract_summary_markdown(markdown_text: str) -> str:
    """Extract a summary as the first paragraph.

    Mirrors the original behavior: split on a blank line and use the first chunk.
    """

    parts = markdown_text.split("\n\n", 1)
    return parts[0].strip()


@dataclass(frozen=True, slots=True)
class ListPostsUseCase:
    repo: PostsRepository
    renderer: MarkdownRenderer

    def execute(self) -> Sequence[PostSummary]:
        posts = []
        for post in self.repo.list_posts():
            summary_md = _extract_summary_markdown(post.content_markdown)
            summary_html = self.renderer.render(summary_md)
            posts.append(
                PostSummary(
                    slug=post.slug,
                    title=post.title,
                    date=post.date,
                    tags=post.tags,
                    summary_html=summary_html,
                )
            )

        # Keep original semantics: string-sort date descending (YYYY-MM-DD expected)
        return tuple(sorted(posts, key=lambda p: p.date, reverse=True))
