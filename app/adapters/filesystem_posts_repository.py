from __future__ import annotations

from dataclasses import dataclass
from datetime import date as Date
from datetime import datetime, time
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
        published_at_raw = post.get("date", "1900-01-01")
        tags = post.get("tags", [])
        image = post.get("image")
        if tags is None:
            tags = []

        published_at = FilesystemPostsRepository._normalize_published_at(
            published_at_raw
        )

        return MarkdownPost(
            slug=slug,
            title=str(title),
            date=published_at,
            tags=tuple(str(t) for t in tags),
            image=str(image) if image else None,
            content_markdown=post.content,
        )

    @staticmethod
    def _normalize_published_at(value: object) -> str:
        """Normalize `date` frontmatter into a sortable `YYYY-MM-DD HH:MM` string.

        Supports:
        - `YYYY-MM-DD` strings (assumed midday)
        - ISO datetime strings (with `T` or space separator)
        - `datetime.date` and `datetime.datetime` values
        """

        # python-frontmatter may parse YAML dates into `date`/`datetime`.
        if isinstance(value, datetime):
            dt = value
        elif isinstance(value, Date):
            dt = datetime.combine(value, time(12, 0))
        elif isinstance(value, str):
            raw = value.strip()
            raw = raw.removesuffix("Z")
            # Date-only: assume midday.
            try:
                if len(raw) == 10 and raw[4] == "-" and raw[7] == "-":
                    d = Date.fromisoformat(raw)
                    dt = datetime.combine(d, time(12, 0))
                else:
                    dt = datetime.fromisoformat(raw.replace(" ", "T"))
            except ValueError:
                # Fall back to a string coercion; better to show *something*.
                return str(value)
        else:
            dt = datetime(1900, 1, 1, 12, 0)

        return dt.strftime("%Y-%m-%d %H:%M")
