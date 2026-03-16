from __future__ import annotations


from book.build_da_patterns_book import (
    THESIS_DISTILLED_STEM,
    build_markdown,
)
from book.book_builder.models import BookSection, SourcePost


def _post(*, stem: str, title: str, one_liner: str = "", body: str = "Body") -> SourcePost:
    # Path is only used for stable sort in the builder.
    from pathlib import Path

    return SourcePost(
        path=Path(f"{stem}.md"),
        title=title,
        description=one_liner,
        body=body,
        layer_slug="decision-primitives",
    )


def test_build_markdown_renders_thesis_distilled_as_chapter_1_and_prefixes_chapters():
    thesis = _post(
        stem=THESIS_DISTILLED_STEM,
        title="Decision Architecture - Thesis Distilled",
        body="# Decision architecture as a pattern language\n\nSome text.",
    )

    # Single fake section with two pattern posts.
    section = BookSection(
        layer_slug="decision-primitives",
        name="Decision Objects",
        priority=1,
        posts=[
            _post(stem="OODA1", title="Decision factory", one_liner="Create decisions"),
            _post(stem="OODA2", title="Decision cache", one_liner="Cache decisions"),
        ],
    )

    out = build_markdown(sections=[section], thesis_post=thesis)

    assert "## Chapter 1: Decision Architecture - Thesis Distilled" in out
    assert "## Chapter 2: Decision factory" in out
    assert "## Chapter 3: Decision cache" in out

