from __future__ import annotations


from pathlib import Path

from book.book_builder.markdown_assembler import MarkdownAssembler
from book.book_builder.models import BookSection, SourcePost
from book.book_builder.paths import BookPaths
from book.book_builder.repository import FilesystemBookPostsRepository


def _post(*, stem: str, title: str, body: str) -> SourcePost:
    # Path is only used for stable sort in the builder.
    return SourcePost(
        path=Path(f"{stem}.md"),
        title=title,
        description="",
        body=body,
        layer_slug="architecture",
    )


def test_decision_architecture_builder_skips_empty_chapters_and_sections():
    paths = BookPaths(
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

    sections = [
        BookSection(
            layer_slug="architecture",
            name="Architecture",
            priority=1,
            posts=[
                _post(stem="empty", title="Empty", body="\n\n"),
                _post(stem="real", title="Real", body="# Real\n\nSome content."),
            ],
        ),
        BookSection(
            layer_slug="decision-systems",
            name="Decision Systems",
            priority=2,
            posts=[
                _post(stem="empty2", title="Empty 2", body="\n"),
            ],
        ),
    ]

    out = MarkdownAssembler(paths=paths).render_book_markdown(sections=sections)

    # Empty chapters should not produce chapter headings.
    assert "Chapter 1: Empty" not in out
    assert "Chapter" in out

    # The section that contains only empty posts should not be emitted.
    assert "# Decision Systems" not in out


def test_decision_architecture_builder_omits_headings_only_intro_when_about_me_is_empty(tmp_path: Path):
    about_file = tmp_path / "about.md"
    about_file.write_text("---\ntitle: About me\n---\n\n\n", encoding="utf-8")

    paths = BookPaths(
        repo_root=Path("."),
        posts_dir=Path("posts"),
        book_dir=Path("book"),
        about_file=about_file,
        prologue_file=Path("book") / "__missing__prologue.md",
        output_file=Path("docs") / "__missing__.epub",
        temp_combined=Path("book") / "__missing__combined.md",
        css_file=Path("book") / "__missing__.css",
        metadata_file=Path("book") / "__missing__.yaml",
        cover_file=Path("book") / "__missing__.png",
    )

    out = MarkdownAssembler(paths=paths).render_book_markdown(
        sections=[
            BookSection(
                layer_slug="architecture",
                name="Architecture",
                priority=1,
                posts=[_post(stem="real", title="Real", body="Some content")],
            )
        ]
    )

    assert "# Introduction" not in out


def test_decision_architecture_builder_does_not_emit_level1_sections_or_level1_intro():
    paths = BookPaths(
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

    out = MarkdownAssembler(paths=paths).render_book_markdown(
        sections=[
            BookSection(
                layer_slug="architecture",
                name="Architecture",
                priority=1,
                posts=[_post(stem="real", title="Real", body="Some content")],
            )
        ]
    )

    assert "\n# Architecture\n" not in out
    assert "\n# Introduction\n" not in out


def test_filesystem_book_posts_repository_supports_excluding_category(tmp_path: Path):
    (tmp_path / "a.md").write_text(
        "---\n"
        "title: A\n"
        "tags: [cat:decision-architecture-patterns, layer:decision-primitives]\n"
        "---\n"
        "Body\n",
        encoding="utf-8",
    )
    (tmp_path / "b.md").write_text(
        "---\n"
        "title: B\n"
        "tags: [cat:leadership, layer:architecture]\n"
        "---\n"
        "Body\n",
        encoding="utf-8",
    )

    repo = FilesystemBookPostsRepository(
        posts_dir=tmp_path,
        required_category="!cat:decision-architecture-patterns",
    )
    posts = repo.list_posts()
    titles = [p.title for p in posts]
    assert titles == ["B"]

