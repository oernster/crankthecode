from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True, slots=True)
class MarkdownPost:
    """A post as stored in markdown with frontmatter metadata."""

    slug: str
    title: str
    date: str
    tags: Sequence[str]
    blurb: str | None
    one_liner: str | None
    image: str | None
    # Optional thumbnail image used for homepage/buttons. If omitted, `image` is used.
    thumb_image: str | None
    extra_images: Sequence[str]
    content_markdown: str


@dataclass(frozen=True, slots=True)
class PostSummary:
    """A lightweight projection suitable for index pages."""

    slug: str
    title: str
    date: str
    tags: Sequence[str]
    blurb: str | None
    one_liner: str | None
    cover_image_url: str | None
    thumb_image_url: str | None
    summary_html: str


@dataclass(frozen=True, slots=True)
class PostDetail:
    """A full post ready for rendering."""

    slug: str
    title: str
    date: str
    tags: Sequence[str]
    blurb: str | None
    one_liner: str | None
    cover_image_url: str | None
    extra_image_urls: Sequence[str]
    content_html: str
