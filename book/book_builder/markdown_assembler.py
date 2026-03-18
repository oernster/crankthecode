from __future__ import annotations

from dataclasses import dataclass

from book.book_builder.frontmatter import parse_frontmatter
from book.book_builder.markdown_normalizer import normalize_content
from book.book_builder.models import BookSection
from book.book_builder.paths import BookPaths


@dataclass(frozen=True, slots=True)
class MarkdownAssembler:
    paths: BookPaths

    def render_front_matter(self) -> str:
        return """

---

> Organisations fail slowly, then suddenly.
>
> Not because engineers lack skill,
> but because decisions lose structure.

---

"""

    def render_essay_index(self, sections: list[BookSection]) -> str:
        """Render a front-matter index."""

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

        # IMPORTANT: avoid a level-1 heading here for the same reason as intro
        # and section grouping: H1 becomes an EPUB "part" and can produce a
        # heading-only XHTML file in KDP's print converter.
        blocks: list[str] = ["## Essay Index {.unnumbered}\n\n"]
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

        # IMPORTANT:
        # We intentionally avoid emitting a level-1 heading here.
        # With `--top-level-division=part`, Pandoc writes each H1 as its own EPUB
        # "part" document. If an H1 only contains H2 children (and we split at
        # level 2), that part becomes a heading-only XHTML file, which KDP's
        # print converter can render as blank pages.
        return "".join(
            [
                "## Introduction\n\n",
                body + "\n\n",
            ]
        )

    def _render_prologue(self) -> str:
        """Render the book prologue from `book/prologue.md`.

        If the file is absent, omit the prologue (keeps the builder tolerant).
        """

        if not self.paths.prologue_file.exists():
            return ""

        raw = self.paths.prologue_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(raw)
        body = fm.body.strip()
        if not body:
            return ""

        return body + "\n\n"

    def render_book_markdown(self, *, sections: list[BookSection]) -> str:
        blocks: list[str] = []

        blocks.append(self.render_front_matter())

        prologue = self._render_prologue()
        if prologue.strip():
            blocks.append(prologue)

        essay_index = self.render_essay_index(sections)
        if essay_index.strip():
            blocks.append(essay_index)

        intro = self._render_intro_about_me()
        if intro.strip():
            blocks.append(intro)

        chapter_number = 1

        for section in sections:
            section_blocks: list[str] = []

            for post in section.posts:
                body = normalize_content(post.body).strip()
                if not body:
                    # Skip empty/near-empty chapters entirely.
                    continue

                # Explicit chapter heading for EPUB navigation and NarrateX detection
                section_blocks.append(
                    f"## Chapter {chapter_number}: {post.title}\n\n"
                )
                section_blocks.append(body + "\n\n")
                chapter_number += 1

            if section_blocks:
                # Do NOT emit a level-1 section heading here (see note above).
                # We keep section grouping in the front-matter index instead.
                blocks.extend(section_blocks)

        return "".join(blocks)
