from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from app.domain.models import PostDetail, PostSummary
from app.usecases.get_post import GetPostUseCase
from app.usecases.list_posts import ListPostsUseCase


@dataclass(frozen=True, slots=True)
class BlogService:
    """Application service façade (Service Layer pattern)."""

    list_posts_uc: ListPostsUseCase
    get_post_uc: GetPostUseCase

    def list_posts(self) -> Sequence[PostSummary]:
        return self.list_posts_uc.execute()

    def get_post(self, slug: str) -> PostDetail | None:
        return self.get_post_uc.execute(slug)
