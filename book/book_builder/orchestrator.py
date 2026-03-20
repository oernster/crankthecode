from __future__ import annotations

from dataclasses import dataclass

from book.book_builder.markdown_assembler import MarkdownAssembler
from book.book_builder.pandoc_epub import PandocEpubBuilder
from book.book_builder.paths import BookPaths
from book.book_builder.repository import FilesystemBookPostsRepository
from book.book_builder.sectioning import SectionOrganizer


@dataclass(frozen=True, slots=True)
class BuildOrchestrator:
    """High-level use case: build the Decision Architecture epub."""

    paths: BookPaths
    section_priority: dict[str, int]
    required_category: str | None = None

    def build(self) -> None:
        # Ensure the output directory exists.
        self.paths.output_file.parent.mkdir(parents=True, exist_ok=True)

        posts_repo = FilesystemBookPostsRepository(
            posts_dir=self.paths.posts_dir,
            required_category=self.required_category,
        )
        organizer = SectionOrganizer(section_priority=self.section_priority)
        assembler = MarkdownAssembler(paths=self.paths)
        epub_builder = PandocEpubBuilder(
            metadata_file=self.paths.metadata_file,
            combined_markdown_file=self.paths.temp_combined,
            css_file=self.paths.css_file,
            cover_file=self.paths.cover_file,
            output_file=self.paths.output_file,
        )

        posts = posts_repo.list_posts()
        sections = organizer.organize(posts)
        combined = assembler.render_book_markdown(sections=sections)
        self.paths.temp_combined.write_text(combined, encoding="utf-8")

        try:
            epub_builder.build()
        finally:
            if self.paths.temp_combined.exists():
                # NOTE: Temporary debugging aid. Keep the combined markdown so we
                # can inspect for headings-only / empty sections that cause blank
                # pages in KDP preview.
                # self.paths.temp_combined.unlink()
                pass

        print("Book created successfully")
        print(self.paths.output_file)
