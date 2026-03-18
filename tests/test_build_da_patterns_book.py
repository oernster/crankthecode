from __future__ import annotations


from pathlib import Path

from book.build_da_patterns_book import THESIS_DISTILLED_STEM, PatternsBookPaths, PatternsMarkdownAssembler
from book.book_builder.models import BookSection, SourcePost


def _post(*, stem: str, title: str, one_liner: str = "", body: str = "Body") -> SourcePost:
    # Path is only used for stable sort in the builder.
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

    # Provide non-existent files so the optional prologue/about branches are skipped.
    paths = PatternsBookPaths(
        repo_root=Path("."),
        posts_dir=Path("posts"),
        book_dir=Path("book"),
        about_file=Path("book") / "__missing__about.md",
        prologue_file=Path("book") / "__missing__prologue.md",
        output_file=Path("docs") / "__missing__.epub",
        temp_combined=Path("book") / "__missing__combined.md",
        css_file=Path("book") / "__missing__.css",
        metadata_file=Path("book") / "__missing__.yaml",
        cover_file=Path("book") / "__missing__.png",
    )
    out = PatternsMarkdownAssembler(paths=paths).render_book_markdown(
        sections=[section],
        thesis_post=thesis,
    )

    assert "## Chapter 1: Decision Architecture - Thesis Distilled" in out
    assert "## Chapter 2: Decision factory" in out
    assert "## Chapter 3: Decision cache" in out


def test_patterns_builder_skips_empty_thesis_and_empty_sections():
    empty_thesis = _post(
        stem=THESIS_DISTILLED_STEM,
        title="Decision Architecture - Thesis Distilled",
        body="\n\n",
    )

    empty_section = BookSection(
        layer_slug="decision-primitives",
        name="Decision Objects",
        priority=1,
        posts=[_post(stem="empty", title="Empty", body="\n")],
    )
    real_section = BookSection(
        layer_slug="decision-primitives",
        name="Real Section",
        priority=2,
        posts=[_post(stem="real", title="Real", body="Some content")],
    )

    paths = PatternsBookPaths(
        repo_root=Path("."),
        posts_dir=Path("posts"),
        book_dir=Path("book"),
        about_file=Path("book") / "__missing__about.md",
        prologue_file=Path("book") / "__missing__prologue.md",
        output_file=Path("docs") / "__missing__.epub",
        temp_combined=Path("book") / "__missing__combined.md",
        css_file=Path("book") / "__missing__.css",
        metadata_file=Path("book") / "__missing__.yaml",
        cover_file=Path("book") / "__missing__.png",
    )

    out = PatternsMarkdownAssembler(paths=paths).render_book_markdown(
        sections=[empty_section, real_section],
        thesis_post=empty_thesis,
    )

    assert "# Thesis Distilled" not in out
    assert "# Decision Objects" not in out
    assert "# Real Section" in out


def test_patterns_builder_does_not_emit_level1_thesis_heading():
    thesis = _post(
        stem=THESIS_DISTILLED_STEM,
        title="Decision Architecture - Thesis Distilled",
        body="Some content",
    )
    section = BookSection(
        layer_slug="decision-primitives",
        name="Decision Objects",
        priority=1,
        posts=[_post(stem="real", title="Real", body="Some content")],
    )

    paths = PatternsBookPaths(
        repo_root=Path("."),
        posts_dir=Path("posts"),
        book_dir=Path("book"),
        about_file=Path("book") / "__missing__about.md",
        prologue_file=Path("book") / "__missing__prologue.md",
        output_file=Path("docs") / "__missing__.epub",
        temp_combined=Path("book") / "__missing__combined.md",
        css_file=Path("book") / "__missing__.css",
        metadata_file=Path("book") / "__missing__.yaml",
        cover_file=Path("book") / "__missing__.png",
    )

    out = PatternsMarkdownAssembler(paths=paths).render_book_markdown(
        sections=[section],
        thesis_post=thesis,
    )

    assert "\n# Thesis Distilled\n" not in out


def test_patterns_builder_does_not_emit_heading_only_thesis_wrapper():
    thesis = _post(
        stem=THESIS_DISTILLED_STEM,
        title="Decision Architecture - Thesis Distilled",
        body="Some content",
    )
    section = BookSection(
        layer_slug="decision-primitives",
        name="Decision Objects",
        priority=1,
        posts=[_post(stem="real", title="Real", body="Some content")],
    )

    paths = PatternsBookPaths(
        repo_root=Path("."),
        posts_dir=Path("posts"),
        book_dir=Path("book"),
        about_file=Path("book") / "__missing__about.md",
        prologue_file=Path("book") / "__missing__prologue.md",
        output_file=Path("docs") / "__missing__.epub",
        temp_combined=Path("book") / "__missing__combined.md",
        css_file=Path("book") / "__missing__.css",
        metadata_file=Path("book") / "__missing__.yaml",
        cover_file=Path("book") / "__missing__.png",
    )

    out = PatternsMarkdownAssembler(paths=paths).render_book_markdown(
        sections=[section],
        thesis_post=thesis,
    )

    assert "\n## Thesis Distilled\n" not in out

