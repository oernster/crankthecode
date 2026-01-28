from __future__ import annotations

from dataclasses import dataclass
from datetime import date as Date
from datetime import datetime, time
from pathlib import Path
from typing import Iterable, Sequence

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
    def _normalize_tags(value: object) -> list[str]:
        """Normalize frontmatter `tags` into a list of strings.

        Supports:
        - YAML list/tuple/set
        - single string ("blog" or "blog, python")
        - None/null

        This prevents edge-cases where callers iterate a string and end up with
        per-character "tags".
        """

        if value is None:
            return []

        if isinstance(value, str):
            raw = value.strip()
            if not raw:
                return []
            # Allow a simple comma-separated string.
            parts = [p.strip() for p in raw.split(",")]
            return [p for p in parts if p]

        if isinstance(value, (list, tuple, set)):
            out: list[str] = []
            for item in value:
                if item is None:
                    continue
                s = str(item).strip()
                if s:
                    out.append(s)
            return out

        # Fallback: coerce to a single tag string.
        s = str(value).strip()
        return [s] if s else []

    @staticmethod
    def _load_file(path: Path) -> MarkdownPost:
        # Explicitly decode markdown files as UTF-8.
        #
        # Rationale: relying on implicit/default encodings can produce mojibake
        # (e.g. "Whatâ€™s" instead of "What’s") when UTF-8 bytes are decoded as
        # cp1252/latin-1. This showed up in RSS/HTML output for smart quotes and
        # emoji. Reading text ourselves ensures consistent Unicode handling.
        try:
            raw_text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Tolerate UTF-8 BOM if present.
            raw_text = path.read_text(encoding="utf-8-sig")

        post = frontmatter.loads(raw_text)
        slug = path.stem

        title = post.get("title", slug)
        published_at_raw = post.get("date", "1900-01-01")
        tags_raw = post.get("tags", [])
        blurb = post.get("blurb")
        one_liner = post.get("one_liner")
        image = post.get("image")
        thumb_image = post.get("thumb_image")
        social_image = post.get("social_image")
        emoji = post.get("emoji")
        extra_images_raw = post.get("extra_images", [])

        tags = FilesystemPostsRepository._normalize_tags(tags_raw)

        # Safety net: blog posts should always be discoverable in `/posts?q=blog`.
        # The posts index uses client-side filtering against `title + tags`.
        if slug.lower().startswith("blog"):
            tags_lower = {t.strip().lower() for t in tags}
            if "blog" not in tags_lower:
                tags = ["blog", *tags]

        if extra_images_raw is None:
            extra_images_raw = []

        if blurb is not None:
            blurb = str(blurb).strip()
            if not blurb:
                blurb = None

        if one_liner is not None:
            one_liner = str(one_liner).strip()
            if not one_liner:
                one_liner = None

        published_at = FilesystemPostsRepository._normalize_published_at(
            published_at_raw
        )

        return MarkdownPost(
            slug=slug,
            title=str(title),
            date=published_at,
            tags=tuple(tags),
            blurb=blurb,
            one_liner=one_liner,
            image=str(image) if image else None,
            thumb_image=str(thumb_image) if thumb_image else None,
            emoji=str(emoji).strip() if emoji else None,
            social_image=str(social_image) if social_image else None,
            extra_images=tuple(str(u) for u in extra_images_raw),
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
