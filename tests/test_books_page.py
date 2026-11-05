"""The books page and the catalogue entries behind it."""

from __future__ import annotations

import re

from fastapi.testclient import TestClient

from app.domain.books_catalogue import (
    EVERGENCE,
    BookCatalogueEntry,
    BookFormat,
    CompilationEdition,
    StandaloneBook,
    book_alt_text,
)
from app.main import create_app

_EDITIONS_MARKER = "books-grid--editions"


def _split_series_and_editions(html: str) -> tuple[str, str]:
    """Return the series grid and the editions row, as separate HTML slices."""

    start = html.index('aria-label="Published books"')
    split = html.index(_EDITIONS_MARKER, start)
    end = html.index("books-footer-note", split)
    return html[start:split], html[split:end]


def _books_html() -> str:
    resp = TestClient(create_app()).get("/books")
    assert resp.status_code == 200
    return resp.text


def test_books_page_renders_and_links_to_amazon_uk():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/books")
    assert resp.status_code == 200

    assert "Books" in resp.text

    # Read time is post-only; non-post pages should not render the pill.
    assert 'class="read-time-bar"' not in resp.text

    # Covers (served from /static as web-sized WebP copies). Support both
    # unfingerprinted and fingerprinted asset paths.
    for stem in (
        "_cover_da",
        "_cover_da_patterns",
        "_cover_relativistic_da_architecture",
        "_cover-da-move-space",
        "hardback_cover",
        "_cover_evergence",
    ):
        assert re.search(
            rf"/static/images/{re.escape(stem)}(?:\.[0-9a-f]{{8,}})?\.webp",
            resp.text,
        ), stem

    # Canonical Amazon UK links (no link switching).
    assert "https://www.amazon.co.uk/dp/B0GT4JNMGK" in resp.text
    assert "https://www.amazon.co.uk/dp/B0GT4CZ327" in resp.text
    assert "https://www.amazon.co.uk/dp/B0H8HTM8H3" in resp.text
    assert "https://www.amazon.co.uk/dp/B0GTDX7186" in resp.text

    # Complete series hardback compilation: labelled in its own row, not a 5th
    # peer card in the primary series grid.
    assert "Complete Series Edition" in resp.text
    assert "https://www.amazon.co.uk/dp/B0H8HVZKY1" in resp.text
    assert (
        "All four volumes combined into a single hardback reference edition"
        in resp.text
    )

    # Guardrail: the series grid holds exactly the 4 volumes; the compiled
    # edition and Evergence sit in the editions row after it.
    series, editions = _split_series_and_editions(resp.text)
    assert series.count('class="book-tile"') == 4, series
    assert editions.count('class="book-tile"') == 2, editions
    assert "Evergence" not in series
    assert "B0H8HVZKY1" not in series

    # Hover/subtitle text should be present (consistent behaviour across cards).
    assert "A Positional Model of Organisational Change" in resp.text

    # Subtitles must be visible (not hover-only) and must match hover text.
    assert re.search(
        r'class="book-title">\s*Decision Architecture\s*</div>',
        resp.text,
    ), resp.text
    assert re.search(
        r'class="book-subtitle">\s*How technical organisations fail and'
        r" recover\s*</div>",
        resp.text,
    ), resp.text

    assert re.search(
        r'class="book-title">\s*Decision Architecture: The Move Space\s*</div>',
        resp.text,
    ), resp.text
    assert re.search(
        r'class="book-subtitle">\s*A Positional Model of Organisational'
        r" Change\s*</div>",
        resp.text,
    ), resp.text

    # Source-of-truth guard: old title-case subtitle should not appear anymore.
    assert "How Technical Organisations Fail and Recover" not in resp.text


def test_book_catalogue_entry_alt_text_omits_empty_subtitle():
    entry = BookCatalogueEntry(
        title="T",
        cover_asset="images/x.png",
        amazon_uk_url="https://example.invalid",
        hover_text="",
    )
    assert entry.alt_text == "T"


def test_evergence_renders_in_the_editions_row():
    _, editions = _split_series_and_editions(_books_html())

    assert re.search(r'class="book-title">\s*Evergence\s*</div>', editions)
    assert re.search(
        r'class="book-subtitle">\s*A Framework for Human-AI Co-Evolution\s*</div>',
        editions,
    )


def test_books_page_never_links_the_free_framework():
    # The page sells the book; pointing at the free framework undercuts it.
    html = _books_html()

    assert "ernster.dev/Evergence" not in html
    assert "living framework" not in html.lower()


def _evergence_section(editions: str) -> str:
    return editions[editions.index('aria-label="Evergence"') :]


_EVERGENCE_HARDBACK_URL = "https://www.amazon.co.uk/dp/B0HQFRWWGN"


def _evergence_with(*formats: BookFormat) -> StandaloneBook:
    return StandaloneBook(
        title=EVERGENCE.title,
        subtitle=EVERGENCE.subtitle,
        summary=EVERGENCE.summary,
        cover_asset=EVERGENCE.cover_asset,
        formats=formats,
    )


def test_unpublished_format_renders_as_text_never_a_link(monkeypatch):
    # The rule outlives any one book: a format announced before it publishes.
    pending = _evergence_with(BookFormat(label="Hardback"))
    monkeypatch.setattr("app.http.routers.books.EVERGENCE", pending)

    _, editions = _split_series_and_editions(_books_html())
    evergence = _evergence_section(editions)

    pending = re.search(
        r'<span class="book-format book-format--pending">'
        r"\s*Hardback: coming soon\s*</span>",
        evergence,
    )
    assert pending, evergence
    # Nothing to buy yet, so nothing in the tile is a link: not the cover,
    # not a placeholder anchor standing in for the missing hardback.
    assert not re.search(r"<a[\s>]", evergence), evergence
    assert "book-cover-link--static" in evergence


def test_entry_guidance_offers_evergence_after_the_series():
    html = _books_html()
    start = html.index('aria-label="Entry points"')
    guidance = html[start : html.index("books-series-label", start)]

    beyond = guidance.index("books-entry-guidance__item--beyond")
    # Evergence comes after every series entry, set apart from the progression.
    assert guidance.index("Complete Series Edition") < beyond
    assert re.search(
        rf'href="{re.escape(_EVERGENCE_HARDBACK_URL)}"[^>]*>\s*Evergence\s*</a>',
        guidance[beyond:],
    ), guidance


def test_evergence_cover_links_the_hardback_with_no_format_pill():
    _, editions = _split_series_and_editions(_books_html())
    evergence = _evergence_section(editions)

    # The cover is the one link to the published hardback, as on every other
    # book card; a published format adds no pill of its own.
    assert evergence.count(f'href="{_EVERGENCE_HARDBACK_URL}"') == 1, evergence
    assert re.search(
        rf'<a\s+class="book-cover-link"\s+href="{re.escape(_EVERGENCE_HARDBACK_URL)}"',
        evergence,
    ), evergence
    assert "book-formats" not in evergence
    assert "book-cover-link--static" not in evergence
    assert "coming soon" not in evergence


def test_purchase_url_is_the_first_published_format():
    pending = BookFormat(label="Hardback")
    paperback = BookFormat(label="Paperback", url="https://example.invalid/pb")
    hardback = BookFormat(label="Hardback", url="https://example.invalid/hb")

    def book(*formats: BookFormat) -> StandaloneBook:
        return StandaloneBook(
            title="T", subtitle="", summary="", cover_asset="x", formats=formats
        )

    assert book(pending).purchase_url is None
    assert book().purchase_url is None
    assert book(pending, paperback, hardback).purchase_url == paperback.url

    assert book(pending, paperback).pending_formats == (pending,)
    assert book(paperback, hardback).pending_formats == ()


def test_book_format_is_available_only_with_a_url():
    assert BookFormat(label="Hardback").is_available is False
    assert BookFormat(label="Hardback", url="").is_available is False
    assert BookFormat(label="Hardback", url="https://example.invalid").is_available


def test_standalone_book_alt_text_joins_title_and_subtitle():
    assert EVERGENCE.alt_text == ("Evergence - A Framework for Human-AI Co-Evolution")


def test_book_alt_text_strips_detail_and_omits_it_when_blank():
    assert book_alt_text("T", "  detail  ") == "T - detail"
    assert book_alt_text("T", "   ") == "T"


def test_compilation_edition_alt_text_omits_empty_support_line():
    edition = CompilationEdition(
        title="Decision Architecture Series",
        cover_asset="images/hardback_cover.webp",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0H8HVZKY1",
        support_line="",
    )
    assert edition.alt_text == "Decision Architecture Series"
