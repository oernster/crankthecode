"""Build the Decision Architecture Patterns book (EPUB).

This builder is intentionally self-contained so it does NOT depend on the
shared repository/tag resolution logic used by the original Decision
Architecture book pipeline.

Why:
- The shared repository can still pick up older layer/tag conventions.
- This book must include ONLY posts tagged with:
    cat:decision-architecture-patterns
- It must also only recognise the approved new layer slugs:
    decision-primitives
    decision-interfaces
    authority-models
    system-dynamics
    pattern-catalogue

This keeps Pandoc / chapter behaviour aligned with the working original
builder while preventing DA posts from bleeding into the Patterns book.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


def _find_repo_root_for_script(*, start: Path) -> Path:
    """Find the repository root when this script is executed as a file."""
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate
    raise RuntimeError(f"Unable to locate repo root from: {start}")


_REPO_ROOT = _find_repo_root_for_script(start=Path(__file__))
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


from book.book_builder.markdown_assembler import MarkdownAssembler  # noqa: E402
from book.book_builder.models import BookSection, SourcePost  # noqa: E402
from book.book_builder.pandoc_epub import PandocEpubBuilder  # noqa: E402
from book.book_builder.paths import BookPaths, find_repo_root  # noqa: E402


# ---------------------------------------------------------------------------
# Canonical Decision Architecture Patterns taxonomy
# ---------------------------------------------------------------------------

REQUIRED_CATEGORY = "cat:decision-architecture-patterns"

SECTION_PRIORITY: dict[str, int] = {
    "decision-primitives": 1,
    "decision-interfaces": 2,
    "authority-models": 3,
    "system-dynamics": 4,
    "pattern-catalogue": 5,
}

LAYER_LABELS: dict[str, str] = {
    "decision-primitives": "Decision Primitives",
    "decision-interfaces": "Decision Interfaces",
    "authority-models": "Authority Models",
    "system-dynamics": "System Dynamics",
    "pattern-catalogue": "Pattern Catalogue",
}

VALID_LAYERS = set(LAYER_LABELS.keys())


# ---------------------------------------------------------------------------
# Minimal frontmatter parsing
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass(frozen=True, slots=True)
class Frontmatter:
    meta: dict[str, Any]
    body: str


def parse_frontmatter(markdown: str) -> Frontmatter:
    match = _FRONTMATTER_RE.match(markdown or "")
    if not match:
        return Frontmatter(meta={}, body=markdown or "")

    meta = yaml.safe_load(match.group(1))
    if meta is None or not isinstance(meta, dict):
        meta = {}

    return Frontmatter(meta=dict(meta), body=(markdown or "")[match.end() :])


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\u00a0", " ")).strip()


# ---------------------------------------------------------------------------
# Patterns-only repository
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PatternsBookRepository:
    posts_dir: Path

    def _extract_patterns_layer_slug(self, tags: list[str]) -> str | None:
        """Return only approved new layer slugs.

        This intentionally avoids any old generic tag parsing helpers so the
        old taxonomy cannot leak into this build.
        """
        for tag in tags:
            if not tag.startswith("layer:"):
                continue
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

            raw_tags = fm.meta.get("tags", [])
            tags = [str(t).strip() for t in raw_tags] if isinstance(raw_tags, list) else []

            # Hard filter to the new category only.
            if REQUIRED_CATEGORY not in tags:
                continue

            # Hard filter to the new canonical layer taxonomy only.
            layer_slug = self._extract_patterns_layer_slug(tags)
            if not layer_slug:
                continue

            title = normalize_whitespace(str(fm.meta.get("title", path.stem)))
            description = normalize_whitespace(
                str(fm.meta.get("description", fm.meta.get("one_liner", "")))
            )

            posts.append(
                SourcePost(
                    path=path,
                    title=title,
                    description=description,
                    body=fm.body,
                    layer_slug=layer_slug,
                )
            )

        return posts


# ---------------------------------------------------------------------------
# Patterns-only section organiser
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PatternsSectionOrganizer:
    section_priority: dict[str, int]

    def organize(self, posts: list[SourcePost]) -> list[BookSection]:
        sections_by_slug: dict[str, BookSection] = {}

        for post in posts:
            slug = post.layer_slug
            section = sections_by_slug.get(slug)
            if section is None:
                section = BookSection(
                    layer_slug=slug,
                    name=LAYER_LABELS[slug],
                    priority=self.section_priority[slug],
                )
                sections_by_slug[slug] = section

            section.posts.append(post)

        # Preserve deterministic ordering. Your posts already use dated filenames,
        # so sorting by path name mirrors the existing book behaviour.
        for section in sections_by_slug.values():
            section.posts.sort(key=lambda p: p.path.name)

        return sorted(
            sections_by_slug.values(),
            key=lambda s: (s.priority, s.name),
        )


# ---------------------------------------------------------------------------
# Build entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    repo_root = find_repo_root(start=Path(__file__).resolve())

    base_paths = BookPaths.from_repo_root(repo_root)

    paths = BookPaths(
        repo_root=base_paths.repo_root,
        posts_dir=base_paths.posts_dir,
        book_dir=base_paths.book_dir,
        about_file=base_paths.about_file,
        prologue_file=base_paths.book_dir / "prologue_patterns.md",
        output_file=repo_root / "docs" / "decision-architecture-patterns.epub",
        temp_combined=base_paths.book_dir / "_combined_da_patterns_book.md",
        css_file=base_paths.css_file,
        metadata_file=base_paths.book_dir / "_metadata_patterns.yaml",
        cover_file=base_paths.book_dir / "_cover_da_patterns.png",
    )

    # Ensure output directory exists.
    paths.output_file.parent.mkdir(parents=True, exist_ok=True)

    posts_repo = PatternsBookRepository(posts_dir=paths.posts_dir)
    organizer = PatternsSectionOrganizer(section_priority=SECTION_PRIORITY)
    assembler = MarkdownAssembler(paths=paths)
    epub_builder = PandocEpubBuilder(
        metadata_file=paths.metadata_file,
        combined_markdown_file=paths.temp_combined,
        css_file=paths.css_file,
        cover_file=paths.cover_file,
        output_file=paths.output_file,
    )

    posts = posts_repo.list_posts()
    sections = organizer.organize(posts)

    combined = assembler.render_book_markdown(sections=sections)
    paths.temp_combined.write_text(combined, encoding="utf-8")

    try:
        epub_builder.build()
    finally:
        if paths.temp_combined.exists():
            paths.temp_combined.unlink()

    print("Decision Architecture Patterns book created successfully")
    print(paths.output_file)


if __name__ == "__main__":
    main()