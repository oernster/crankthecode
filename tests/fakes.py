from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from app.domain.models import MarkdownPost
from app.ports.posts_repository import PostsRepository


@dataclass(frozen=True, slots=True)
class InMemoryPostsRepository(PostsRepository):
    posts: Sequence[MarkdownPost]

    def list_posts(self) -> Sequence[MarkdownPost]:
        return tuple(self.posts)

    def get_post(self, slug: str) -> MarkdownPost | None:
        for p in self.posts:
            if p.slug == slug:
                return p
        return None
