from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SourcePost:
    """A markdown post that will be included in the book."""

    path: Path
    title: str
    description: str
    body: str
    layer_slug: str


@dataclass(slots=True)
class BookSection:
    """A collection of posts grouped under a decision-architecture layer."""

    layer_slug: str
    name: str
    priority: int
    posts: list[SourcePost] = field(default_factory=list)
