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

        blocks: list[str] = ["# Essay Index {.unnumbered}\n\n"]

        for section in sections:
            blocks.append(f"**{section.name}**\n\n")
            for post in section.posts:
                line = f"- **{post.title}**"
                if post.description:
                    line += f" - {post.description}"
                blocks.append(line + "\n")
            blocks.append("\n")

        return "".join(blocks)

    def _render_intro_about_me(self) -> str:
        if not self.paths.about_file.exists():
            return ""

        raw = self.paths.about_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(raw)
        body = normalize_content(fm.body, remove_heading_text="About me")
        return "".join(
            [
                "# Introduction\n\n",
                "## About me\n\n",
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

        # The prologue file is expected to define its own title/heading.
        return body + "\n\n"

    def render_book_markdown(self, *, sections: list[BookSection]) -> str:
        blocks: list[str] = []
        blocks.append(self.render_front_matter())
        blocks.append(self._render_prologue())
        blocks.append(self.render_essay_index(sections))
        blocks.append(self._render_intro_about_me())

        for section in sections:
            blocks.append(f"# {section.name}\n\n")
            for post in section.posts:
                body = normalize_content(post.body)
                blocks.append(f"## {post.title}\n\n")
                blocks.append(body + "\n\n")

        return "".join(blocks)
