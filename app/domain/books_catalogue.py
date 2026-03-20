from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BookCatalogueEntry:
    title: str
    subtitle: str
    cover_asset: str
    amazon_uk_url: str
    hover_text: str

    @property
    def alt_text(self) -> str:
        subtitle = (self.subtitle or "").strip()
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
        subtitle="How Technical Organisations Fail and Recover",
        cover_asset="images/_cover_da.png",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0GT4JNMGK",
        hover_text="How technical organisations fail and recover",
    ),
    BookCatalogueEntry(
        title="Decision Architecture Patterns",
        subtitle="Recurring Structural Patterns in Technical Organisations",
        cover_asset="images/_cover_da_patterns.png",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0GT4CZ327",
        hover_text="Structural patterns that recur across technical organisations",
    ),
    BookCatalogueEntry(
        title="Relativistic Decision Architecture",
        subtitle="The Geometry of Decision Systems",
        cover_asset="images/_cover_relativistic_da_architecture.png",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0GT7D4P8G",
        hover_text="The geometry of decision systems",
    ),
)

