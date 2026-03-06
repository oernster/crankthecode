from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.domain.tags import primary_layer_slug_from_tags

from book.book_builder.frontmatter import parse_frontmatter
from book.book_builder.markdown_normalizer import normalize_whitespace
from book.book_builder.models import SourcePost


@dataclass(frozen=True, slots=True)
class FilesystemBookPostsRepository:
    posts_dir: Path

    def list_posts(self) -> list[SourcePost]:
        posts: list[SourcePost] = []

        for path in sorted(self.posts_dir.glob("*.md")):
            if path.name.startswith("_"):
                continue

            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            tags = fm.meta.get("tags", [])
            tags_list = [str(t) for t in tags] if isinstance(tags, list) else []

            layer_slug = primary_layer_slug_from_tags(tags_list)
            if not layer_slug:
                continue

            title = normalize_whitespace(str(fm.meta.get("title", path.stem)))
            description = normalize_whitespace(str(fm.meta.get("description", "")))

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
