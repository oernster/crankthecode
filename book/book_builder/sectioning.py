from __future__ import annotations

from dataclasses import dataclass

from app.domain.tags import humanize_layer_slug

from book.book_builder.models import BookSection, SourcePost


@dataclass(frozen=True, slots=True)
class SectionOrganizer:
    """Group posts into sections ordered by priority then name."""

    section_priority: dict[str, int]

    def organize(self, posts: list[SourcePost]) -> list[BookSection]:
        sections_by_slug: dict[str, BookSection] = {}

        for post in posts:
            slug = post.layer_slug
            section = sections_by_slug.get(slug)
            if section is None:
                section = BookSection(
                    layer_slug=slug,
                    name=humanize_layer_slug(slug),
                    priority=self.section_priority.get(slug, 999),
                )
                sections_by_slug[slug] = section

            section.posts.append(post)

        for section in sections_by_slug.values():
            section.posts.sort(key=lambda p: p.path.name)

        return sorted(
            sections_by_slug.values(),
            key=lambda s: (s.priority, s.name),
        )
