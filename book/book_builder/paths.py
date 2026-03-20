from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def find_repo_root(*, start: Path) -> Path:
    """Find the repository root by walking up to a `pyproject.toml` marker."""

    current = start.resolve()
    for parent in (current, *current.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    return current


@dataclass(frozen=True, slots=True)
class BookPaths:
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
    def from_repo_root(cls, repo_root: Path) -> "BookPaths":
        book_dir = repo_root / "book"
        private_epubs_dir = book_dir / "private_epubs"
        return cls(
            repo_root=repo_root,
            posts_dir=repo_root / "posts",
            book_dir=book_dir,
            about_file=book_dir / "about-me-book.md",
            prologue_file=book_dir / "prologue.md",
            # Non-public artifact: keep in repo but do not serve from `/docs`.
            output_file=private_epubs_dir / "Decision-Architecture.epub",
            temp_combined=book_dir / "_combined_book.md",
            css_file=book_dir / "_book_style.css",
            metadata_file=book_dir / "_metadata.yaml",
            cover_file=book_dir / "_cover.png",
        )
