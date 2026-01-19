from __future__ import annotations

from typing import Protocol, Sequence

from app.domain.models import MarkdownPost


class PostsRepository(Protocol):
    """Repository port for retrieving posts."""

    def list_posts(self) -> Sequence[MarkdownPost]:
        """Return all posts available in storage."""

    def get_post(self, slug: str) -> MarkdownPost | None:
        """Return a single post by slug, or None if it does not exist."""
