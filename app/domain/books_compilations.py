from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CompilationEdition:
    """A derived/compiled artefact rendered separately from the primary series grid."""

    title: str
    cover_asset: str
    amazon_uk_url: str
    support_line: str

    @property
    def alt_text(self) -> str:
        support = (self.support_line or "").strip()
        if support:
            return f"{self.title} — {support}"
        return self.title


# Separate from `BOOKS_CATALOGUE` on purpose: this is a compiled reference
# edition, not another peer volume in the series.
COMPLETE_SERIES_EDITION = CompilationEdition(
    title="Decision Architecture Series",
    cover_asset="images/hardback_cover.png",
    amazon_uk_url="https://www.amazon.co.uk/dp/B0GTMVV8T5",
    support_line="All four volumes combined into a single hardback reference edition",
)

