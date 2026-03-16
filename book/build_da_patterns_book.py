"""Build the Decision Architecture Patterns book (EPUB).

Enhancements:

1. GoF-style PART structure
2. Pattern summaries at the start of each Part
3. Intent / Description / Consequences headers
4. No modification required to post content
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


from book.book_builder.models import BookSection, SourcePost  # noqa
from book.book_builder.pandoc_epub import PandocEpubBuilder  # noqa
from book.book_builder.paths import BookPaths, find_repo_root  # noqa


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

_ROMAN = ["I", "II", "III", "IV", "V"]


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass(frozen=True, slots=True)
class Frontmatter:
    meta: dict[str, Any]
    body: str


def parse_frontmatter(markdown: str) -> Frontmatter:
    match = _FRONTMATTER_RE.match(markdown or "")
    if not match:
        return Frontmatter(meta={}, body=markdown or "")

    meta = yaml.safe_load(match.group(1)) or {}

    return Frontmatter(meta=dict(meta), body=(markdown or "")[match.end():])


@dataclass(frozen=True, slots=True)
class PatternsRepository:
    posts_dir: Path

    def _extract_layer(self, tags: list[str]) -> str | None:
        for tag in tags:
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

            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)

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

        for s in sections.values():
            s.posts.sort(key=lambda p: p.path.name)

        return sorted(sections.values(), key=lambda s: s.priority)


def render_pattern(post: SourcePost) -> str:

    intent = post.description.strip()

    md = []

    md.append(f"# {post.title}")
    md.append("")

    if intent:
        md.append("## Intent")
        md.append("")
        md.append(intent)
        md.append("")

    md.append("## Description")
    md.append("")
    md.append(post.body.strip())
    md.append("")

    md.append("## Consequences")
    md.append("")
    md.append(
        "This pattern alters how decision objects move through the organisation. "
        "Applying it may change authority distribution, escalation behaviour and "
        "decision latency across the system."
    )
    md.append("")

    return "\n".join(md)


def render_part_summary(section: BookSection) -> str:

    md = []

    md.append("## Patterns in this Part")
    md.append("")

    for post in section.posts:
        md.append(f"- **{post.title}** – {post.description}")

    md.append("")

    return "\n".join(md)


def build_markdown(sections: list[BookSection]) -> str:

    md: list[str] = []

    for i, section in enumerate(sections):

        part = _ROMAN[i] if i < len(_ROMAN) else str(i + 1)

        md.append("")
        md.append(f"# Part {part}")
        md.append("")
        md.append(f"## {section.name}")
        md.append("")

        md.append(render_part_summary(section))

        for post in section.posts:
            md.append(render_pattern(post))

    return "\n".join(md)


def main():

    repo_root = find_repo_root(start=Path(__file__).resolve())

    base = BookPaths.from_repo_root(repo_root)

    paths = BookPaths(
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

    repo = PatternsRepository(paths.posts_dir)
    organizer = SectionOrganizer()

    posts = repo.list_posts()
    sections = organizer.organize(posts)

    combined = build_markdown(sections)

    paths.temp_combined.write_text(combined, encoding="utf-8")

    epub = PandocEpubBuilder(
        metadata_file=paths.metadata_file,
        combined_markdown_file=paths.temp_combined,
        css_file=paths.css_file,
        cover_file=paths.cover_file,
        output_file=paths.output_file,
    )

    epub.build()

    paths.temp_combined.unlink(missing_ok=True)

    print("Decision Architecture Patterns book created")
    print(paths.output_file)


if __name__ == "__main__":
    main()