from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from app.domain.tags import primary_layer_slug_from_tags

from book.book_builder.frontmatter import parse_frontmatter
from book.book_builder.markdown_normalizer import normalize_whitespace
from book.book_builder.models import SourcePost


@dataclass(frozen=True, slots=True)
class FilesystemBookPostsRepository:
    """Load markdown posts from the filesystem for book generation.

    Optionally filters posts by a required category tag.

    - If `required_category` is like `cat:leadership`, only posts containing that
      tag are included.
    - If `required_category` is like `!cat:decision-architecture-patterns`, posts
      containing the tag are excluded.
    """

    posts_dir: Path
    required_category: str | None = None

    def _has_required_category(self, tags: Iterable[str]) -> bool:
        """Check whether the post includes the required category."""
        if not self.required_category:
            return True

        required = self.required_category.strip()
        if required.startswith("!"):
            excluded = required[1:].strip()
            return excluded not in tags

        return required in tags

    def list_posts(self) -> list[SourcePost]:
        posts: list[SourcePost] = []

        for path in sorted(self.posts_dir.glob("*.md")):
            if path.name.startswith("_"):
                continue

            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)

            tags = fm.meta.get("tags", [])
            tags_list = [str(t) for t in tags] if isinstance(tags, list) else []

            # --- Category filter (new) ---
            if not self._has_required_category(tags_list):
                continue

            # Determine layer slug
            layer_slug = primary_layer_slug_from_tags(tags_list)
            if not layer_slug:
                continue

            title = normalize_whitespace(str(fm.meta.get("title", path.stem)))
            description = normalize_whitespace(
                str(
                    fm.meta.get(
                        "description",
                        fm.meta.get("one_liner", ""),
                    )
                )
            )

            posts.append(
                SourcePost(
                    path=path,
                    title=title,
                    description=description,
                    body=fm.body,
                    layer_slug=layer_slug,
                )
            )

        return posts
