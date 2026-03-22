from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BookCatalogueEntry:
    title: str
    cover_asset: str
    amazon_uk_url: str
    hover_text: str

    @property
    def subtitle(self) -> str:
        """Human subtitle shown on `/books`.

        Single source of truth is `hover_text` so visible subtitle, hover tooltip,
        and accessible text stay consistent without duplicating authored strings.
        """

        return (self.hover_text or "").strip()

    @property
    def alt_text(self) -> str:
        subtitle = self.subtitle
        if subtitle:
            return f"{self.title} — {subtitle}"
        return self.title


# Single source of truth for authored books rendered on `/books`.
#
# Notes:
# - `cover_asset` is an `asset_url()` path (relative to `static/`).
# - Canonical Amazon UK links are used directly (no redirects, no tracking).
BOOKS_CATALOGUE: tuple[BookCatalogueEntry, ...] = (
    BookCatalogueEntry(
        title="Decision Architecture",
        cover_asset="images/_cover_da.png",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0GT4JNMGK",
        hover_text="How technical organisations fail and recover",
    ),
    BookCatalogueEntry(
        title="Decision Architecture Patterns",
        cover_asset="images/_cover_da_patterns.png",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0GT4CZ327",
        hover_text="Structural patterns that recur across technical organisations",
    ),
    BookCatalogueEntry(
        title="Decision Architecture: The Move Space",
        cover_asset="images/_cover-da-move-space.png",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0GTDX7186",
        hover_text="A Positional Model of Organisational Change",
    ),
    BookCatalogueEntry(
        title="Relativistic Decision Architecture",
        cover_asset="images/_cover_relativistic_da_architecture.png",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0GT7D4P8G",
        hover_text="The geometry of decision systems",
    ),
)

