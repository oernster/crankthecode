"""Authored book data rendered on `/books`: one home for every book card.

Three kinds of entry, kept apart on purpose: the series volumes, the compiled
hardback of the series and books that stand outside the series. They share one
module so they can share one alt-text rule; the domain imports nothing but the
standard library, including other domain modules.
"""

from __future__ import annotations

from dataclasses import dataclass


def book_alt_text(title: str, detail: str) -> str:
    """Accessible cover text: the title, then the detail line when there is one.

    One home for the rule every book card on `/books` follows, so the series
    volumes, the compiled edition and the standalone books cannot drift apart.
    """

    detail = (detail or "").strip()
    if detail:
        return f"{title} - {detail}"
    return title


@dataclass(frozen=True, slots=True)
class BookCatalogueEntry:
    title: str
    cover_asset: str
    amazon_uk_url: str
    hover_text: str

    @property
    def subtitle(self) -> str:
        """Human subtitle shown on `/books`.

        Single source of truth is `hover_text` so visible subtitle, hover tooltip
        and accessible text stay consistent without duplicating authored strings.
        """

        return (self.hover_text or "").strip()

    @property
    def alt_text(self) -> str:
        return book_alt_text(self.title, self.subtitle)


@dataclass(frozen=True, slots=True)
class CompilationEdition:
    """A derived/compiled artefact, labelled apart from the series volumes."""

    title: str
    cover_asset: str
    amazon_uk_url: str
    support_line: str

    @property
    def alt_text(self) -> str:
        return book_alt_text(self.title, self.support_line)


@dataclass(frozen=True, slots=True)
class BookFormat:
    """One way to get a book.

    `url` is None while a format is announced but not yet published: the page
    then shows the label as forthcoming text, never as a link that goes nowhere.
    Publishing the format is a one-line change, filling in the URL.
    """

    label: str
    url: str | None = None

    @property
    def is_available(self) -> bool:
        return bool(self.url)


@dataclass(frozen=True, slots=True)
class StandaloneBook:
    """A book outside the Decision Architecture series, labelled as such."""

    title: str
    subtitle: str
    summary: str
    cover_asset: str
    cover_url: str
    formats: tuple[BookFormat, ...]

    @property
    def alt_text(self) -> str:
        return book_alt_text(self.title, self.subtitle)


# Notes for every entry below:
# - `cover_asset` is an `asset_url()` path (relative to `static/`). Each points
#   at the web-sized WebP copy; the PNG beside it is the master it came from.
# - Canonical Amazon UK links are used directly (no redirects, no tracking).

# The series volumes, in reading order.
BOOKS_CATALOGUE: tuple[BookCatalogueEntry, ...] = (
    BookCatalogueEntry(
        title="Decision Architecture",
        cover_asset="images/_cover_da.webp",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0GT4JNMGK",
        hover_text="How technical organisations fail and recover",
    ),
    BookCatalogueEntry(
        title="Decision Architecture Patterns",
        cover_asset="images/_cover_da_patterns.webp",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0GT4CZ327",
        hover_text="Structural patterns that recur across technical organisations",
    ),
    BookCatalogueEntry(
        title="Decision Architecture: The Move Space",
        cover_asset="images/_cover-da-move-space.webp",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0GTDX7186",
        hover_text="A Positional Model of Organisational Change",
    ),
    BookCatalogueEntry(
        title="Relativistic Decision Architecture",
        cover_asset="images/_cover_relativistic_da_architecture.webp",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0H8HTM8H3",
        hover_text="The geometry of decision systems",
    ),
)

# Separate from `BOOKS_CATALOGUE` on purpose: this is a compiled reference
# edition, not another peer volume in the series.
COMPLETE_SERIES_EDITION = CompilationEdition(
    title="Decision Architecture Series",
    cover_asset="images/hardback_cover.webp",
    amazon_uk_url="https://www.amazon.co.uk/dp/B0H8HVZKY1",
    support_line="All four volumes combined into a single hardback reference edition",
)

# A separate thesis from the series: it is rendered beside the compiled
# edition, under its own label, so it never reads as a fifth series volume.
EVERGENCE = StandaloneBook(
    title="Evergence",
    subtitle="A Framework for Human-AI Co-Evolution",
    summary="A provisional research framework, separate from the series above.",
    cover_asset="images/_cover_evergence.webp",
    cover_url="https://ernster.dev/Evergence/",
    formats=(
        BookFormat(
            label="Read the living framework",
            url="https://ernster.dev/Evergence/",
        ),
        # Hardback in publication: set `url` to its Amazon UK link when live.
        BookFormat(label="Hardback"),
    ),
)
