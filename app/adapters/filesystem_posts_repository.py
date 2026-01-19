from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import frontmatter

from app.domain.models import MarkdownPost
from app.ports.posts_repository import PostsRepository


@dataclass(frozen=True, slots=True)
class FilesystemPostsRepository(PostsRepository):
    """Reads posts from a directory containing `*.md` files."""

    posts_dir: Path

    def list_posts(self) -> Sequence[MarkdownPost]:
        posts: list[MarkdownPost] = []
        for post_file in self.posts_dir.glob("*.md"):
            posts.append(self._load_file(post_file))
        return tuple(posts)

    def get_post(self, slug: str) -> MarkdownPost | None:
        post_path = self.posts_dir / f"{slug}.md"
        if not post_path.exists():
            return None
        return self._load_file(post_path)

    @staticmethod
    def _load_file(path: Path) -> MarkdownPost:
        post = frontmatter.load(path)
        slug = path.stem

        title = post.get("title", slug)
        # Preserve current default behavior.
        date = post.get("date", "1900-01-01")
        tags = post.get("tags", [])
        if tags is None:
            tags = []

        return MarkdownPost(
            slug=slug,
            title=str(title),
            date=str(date),
            tags=tuple(str(t) for t in tags),
            content_markdown=post.content,
        )
