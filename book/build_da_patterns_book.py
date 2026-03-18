"""Build the Decision Architecture Patterns book (EPUB).

This deliberately mirrors the simpler Decision Architecture book builder
approach so the EPUB structure stays consistent across both books.

Patterns-specific behaviour retained:
- filters only decision-architecture-patterns posts
- remaps layer slugs to book-facing section labels
- uses patterns-specific metadata / cover / prologue / output paths
- keeps the thesis post first
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


def _find_repo_root_for_script(*, start: Path) -> Path:
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate
    raise RuntimeError(f"Unable to locate repo root from: {start}")


_REPO_ROOT = _find_repo_root_for_script(start=Path(__file__))
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


from book.book_builder.frontmatter import parse_frontmatter  # noqa: E402
from book.book_builder.markdown_normalizer import normalize_content  # noqa: E402
from book.book_builder.models import BookSection, SourcePost  # noqa: E402
from book.book_builder.pandoc_epub import PandocEpubBuilder  # noqa: E402
from book.book_builder.paths import BookPaths, find_repo_root  # noqa: E402


REQUIRED_CATEGORY = "cat:decision-architecture-patterns"

SECTION_PRIORITY = {
    "decision-primitives": 1,
    "decision-interfaces": 2,
    "authority-models": 3,
    "system-dynamics": 4,
    "pattern-catalogue": 5,
}

LAYER_LABELS = {
    "decision-primitives": "Decision Objects",
    "decision-interfaces": "Decision Interfaces",
    "authority-models": "Authority Patterns",
    "system-dynamics": "Behaviour Patterns",
    "pattern-catalogue": "System Patterns",
}

VALID_LAYERS = set(LAYER_LABELS.keys())

THESIS_DISTILLED_STEM = "OODAThesisDistilled"


@dataclass(frozen=True, slots=True)
class PatternsBookPaths:
    repo_root: Path
    posts_dir: Path
    book_dir: Path
    about_file: Path
    prologue_file: Path
    output_file: Path
    temp_combined: Path
    css_file: Path
    metadata_file: Path
    cover_file: Path

    @classmethod
    def from_repo_root(cls, repo_root: Path) -> "PatternsBookPaths":
        base = BookPaths.from_repo_root(repo_root)
        return cls(
            repo_root=base.repo_root,
            posts_dir=base.posts_dir,
            book_dir=base.book_dir,
            about_file=base.about_file,
            prologue_file=base.book_dir / "prologue_patterns.md",
            output_file=repo_root / "docs" / "decision-architecture-patterns.epub",
            temp_combined=base.book_dir / "_combined_da_patterns_book.md",
            css_file=base.css_file,
            metadata_file=base.book_dir / "_metadata_patterns.yaml",
            cover_file=base.book_dir / "_cover_da_patterns.png",
        )


@dataclass(frozen=True, slots=True)
class PatternsRepository:
    posts_dir: Path

    def _extract_layer(self, tags: list[str]) -> str | None:
        for tag in tags:
            if not isinstance(tag, str):
                continue
            if tag.startswith("layer:"):
                slug = tag.split(":", 1)[1].strip()
                if slug in VALID_LAYERS:
                    return slug
        return None

    def list_posts(self) -> list[SourcePost]:
        posts: list[SourcePost] = []

        for path in sorted(self.posts_dir.glob("*.md")):
            if path.name.startswith("_"):
                continue

            raw = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(raw)

            tags = [str(t) for t in fm.meta.get("tags", [])]
            if REQUIRED_CATEGORY not in tags:
                continue

            layer = self._extract_layer(tags)
            if not layer:
                continue

            posts.append(
                SourcePost(
                    path=path,
                    title=str(fm.meta.get("title", path.stem)),
                    description=str(fm.meta.get("one_liner", "")),
                    body=fm.body,
                    layer_slug=layer,
                )
            )

        return posts


@dataclass(frozen=True, slots=True)
class SectionOrganizer:
    def organize(self, posts: list[SourcePost]) -> list[BookSection]:
        sections: dict[str, BookSection] = {}

        for post in posts:
            slug = post.layer_slug

            if slug not in sections:
                sections[slug] = BookSection(
                    layer_slug=slug,
                    name=LAYER_LABELS[slug],
                    priority=SECTION_PRIORITY[slug],
                )

            sections[slug].posts.append(post)

        for section in sections.values():
            section.posts.sort(key=lambda p: p.path.name)

        return sorted(sections.values(), key=lambda s: s.priority)


@dataclass(frozen=True, slots=True)
class PatternsMarkdownAssembler:
    paths: PatternsBookPaths

    def render_front_matter(self) -> str:
        return """
---

> Technical organisations rarely fail in unique ways.
>
> They repeat structural mistakes until authority, responsibility
> and decision flow drift apart.

---

"""

    def render_pattern_index(self, sections: list[BookSection]) -> str:
        # Only include posts that will actually render as chapters.
        eligible: list[tuple[BookSection, list[str]]] = []
        for section in sections:
            lines: list[str] = []
            for post in section.posts:
                if not normalize_content(post.body).strip():
                    continue
                line = f"- **{post.title}**"
                if post.description:
                    line += f" - {post.description}"
                lines.append(line)
            if lines:
                eligible.append((section, lines))

        if not eligible:
            return ""

        # IMPORTANT: avoid a level-1 heading here.
        # With `--top-level-division=part`, Pandoc writes each H1 as its own EPUB
        # "part" document; KDP's print converter can render heading-only parts as
        # blank pages.
        blocks: list[str] = ["## Pattern Index {.unnumbered}\n\n"]
        for section, lines in eligible:
            blocks.append(f"**{section.name}**\n\n")
            blocks.extend([line + "\n" for line in lines])
            blocks.append("\n")

        return "".join(blocks)

    def _render_intro_about_me(self) -> str:
        if not self.paths.about_file.exists():
            return ""

        raw = self.paths.about_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(raw)
        body = normalize_content(fm.body, remove_heading_text="About me").strip()
        if not body:
            # Avoid emitting headings-only sections (Pandoc still paginates them).
            return ""

        return "".join(
            [
                # IMPORTANT:
                # We intentionally avoid emitting a level-1 heading here.
                # With `--top-level-division=part`, Pandoc writes each H1 as its
                # own EPUB "part" document. If an H1 only contains H2 children
                # (and we split at level 2), that part becomes a heading-only
                # XHTML file, which KDP's print converter can render as blank
                # pages.
                "## Introduction\n\n",
                body + "\n\n",
            ]
        )

    def _render_prologue(self) -> str:
        if not self.paths.prologue_file.exists():
            return ""

        raw = self.paths.prologue_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(raw)
        body = fm.body.strip()

        if not body:
            return ""

        return body + "\n\n"

    def render_book_markdown(
        self,
        *,
        sections: list[BookSection],
        thesis_post: SourcePost | None,
    ) -> str:
        blocks: list[str] = []

        blocks.append(self.render_front_matter())

        prologue = self._render_prologue()
        if prologue.strip():
            blocks.append(prologue)

        pattern_index = self.render_pattern_index(sections)
        if pattern_index.strip():
            blocks.append(pattern_index)

        intro = self._render_intro_about_me()
        if intro.strip():
            blocks.append(intro)

        chapter_number = 1

        if thesis_post is not None:
            thesis_body = normalize_content(thesis_post.body).strip()
            if thesis_body:
                # IMPORTANT:
                # Do not add a standalone H2/H1 wrapper like "Thesis Distilled".
                # With `--split-level=2`, an H2 becomes its own XHTML file.
                # A heading-only XHTML becomes blank pages in KDP print preview.
                blocks.append(
                    f"## Chapter {chapter_number}: {thesis_post.title}\n\n"
                )
                blocks.append(thesis_body + "\n\n")
                chapter_number += 1

        for section in sections:
            section_blocks: list[str] = []

            for post in section.posts:
                body = normalize_content(post.body).strip()
                if not body:
                    continue
                section_blocks.append(
                    f"## Chapter {chapter_number}: {post.title}\n\n"
                )
                section_blocks.append(body + "\n\n")
                chapter_number += 1

            if section_blocks:
                # Do NOT emit a level-1 section heading here (see note above).
                blocks.extend(section_blocks)

        return "".join(blocks)


def main() -> None:
    repo_root = find_repo_root(start=Path(__file__).resolve())
    paths = PatternsBookPaths.from_repo_root(repo_root)

    paths.output_file.parent.mkdir(parents=True, exist_ok=True)

    repo = PatternsRepository(posts_dir=paths.posts_dir)
    organizer = SectionOrganizer()
    assembler = PatternsMarkdownAssembler(paths=paths)
    epub_builder = PandocEpubBuilder(
        metadata_file=paths.metadata_file,
        combined_markdown_file=paths.temp_combined,
        css_file=paths.css_file,
        cover_file=paths.cover_file,
        output_file=paths.output_file,
    )

    posts = repo.list_posts()

    thesis_post: SourcePost | None = None
    remaining_posts: list[SourcePost] = []

    for post in posts:
        if post.path.stem == THESIS_DISTILLED_STEM:
            thesis_post = post
            continue
        remaining_posts.append(post)

    sections = organizer.organize(remaining_posts)
    combined = assembler.render_book_markdown(
        sections=sections,
        thesis_post=thesis_post,
    )

    paths.temp_combined.write_text(combined, encoding="utf-8")

    try:
        epub_builder.build()
    finally:
        if paths.temp_combined.exists():
            # NOTE: Temporary debugging aid. Keep the combined markdown so we can
            # inspect for headings-only / empty sections that cause blank pages.
            # paths.temp_combined.unlink()
            pass

    print("Decision Architecture Patterns book created")
    print(paths.output_file)


if __name__ == "__main__":
    main()
