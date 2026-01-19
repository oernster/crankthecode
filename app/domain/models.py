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
    content_markdown: str


@dataclass(frozen=True, slots=True)
class PostSummary:
    """A lightweight projection suitable for index pages."""

    slug: str
    title: str
    date: str
    tags: Sequence[str]
    summary_html: str


@dataclass(frozen=True, slots=True)
class PostDetail:
    """A full post ready for rendering."""

    slug: str
    title: str
    date: str
    tags: Sequence[str]
    content_html: str
